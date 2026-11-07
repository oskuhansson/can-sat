"""Geometri: position -> azimut, elevation och räckvidd.

Koordinatsystem (högerhänt, enheter i meter):

    x = öst, y = nord, z = upp

Azimut mäts **medurs från norr** (0-360 grader), vilket är vad en gimbal och en
kompass använder. Elevation mäts från horisontalplanet uppåt (0-90 grader).

Att hålla fast vid en konvention i hela paketet är inte pedanteri: blands azimut
räknad från öst med azimut räknad från norr får pekfelet att se slumpmässigt ut.
"""

from __future__ import annotations

import math

from .config import StationConfig, TrajectoryConfig

Vec3 = tuple[float, float, float]


def station_antenna_position(station: StationConfig) -> Vec3:
    """Markantennens fascentrum — stationens position plus masthöjd."""
    x, y, z = station.position_m
    return (x, y, z + station.antenna_height_m)


def az_el_range(origin: Vec3, target: Vec3) -> tuple[float, float, float]:
    """Riktning och avstånd från `origin` till `target`.

    Returnerar (azimut_grader, elevation_grader, räckvidd_meter).
    """
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    dz = target[2] - origin[2]

    horizontal = math.hypot(dx, dy)
    rng = math.hypot(horizontal, dz)

    # atan2(x, y) ger vinkeln från +y (nord) mot +x (öst) = medurs. Precis vad vi vill.
    az = math.degrees(math.atan2(dx, dy)) % 360.0
    el = math.degrees(math.atan2(dz, horizontal))
    return az, el, rng


def pointing_error_deg(az_a: float, el_a: float, az_b: float, el_b: float) -> float:
    """Vinkeln mellan två riktningar på himlen, i grader.

    Det här är det tal som antennmodellen matas med. Det är en vinkel på en sfär,
    inte en differens i azimut och elevation var för sig — vid hög elevation är en
    azimutskillnad på 10 grader nästan ingen skillnad alls.
    """
    a_az, a_el = math.radians(az_a), math.radians(el_a)
    b_az, b_el = math.radians(az_b), math.radians(el_b)

    cos_sep = math.sin(a_el) * math.sin(b_el) + math.cos(a_el) * math.cos(b_el) * math.cos(
        a_az - b_az
    )
    # Flyttalsfel kan ge 1+1e-16, som annars kastar ValueError i acos.
    cos_sep = max(-1.0, min(1.0, cos_sep))
    return math.degrees(math.acos(cos_sep))


def direction_cosines(az_deg: float, el_deg: float) -> tuple[float, float]:
    """Riktningscosinus (u, v) för en riktning på himlen.

    En plan array i horisontalplanet bryr sig inte om azimut och elevation var för
    sig, utan om var på enhetscirkeln riktningen ligger när den projiceras upp på
    antennplanet. Det är den projektionen (u, v) som arrayfaktorn räknas i.

    Med zenitvinkeln zeta = 90 - el gäller u = sin(zeta)*cos(az) och
    v = sin(zeta)*sin(az), alltså u = cos(el)*cos(az) och v = cos(el)*sin(az).
    Följden u^2 + v^2 = cos^2(el) <= 1 är den himmel som är synlig ovanför
    horisonten; horisonten själv ligger på enhetscirkeln.

    En riktning rakt upp (el = 90) ger (0, 0), vilket är arrayens bredsida.
    """
    el = math.radians(el_deg)
    az = math.radians(az_deg)
    cos_el = math.cos(el)
    return (cos_el * math.cos(az), cos_el * math.sin(az))


def elevation_at_range(altitude_m: float, range_m: float) -> float:
    """Elevationen till en punkt på given höjd och snedavstånd."""
    if range_m <= 0:
        return 90.0
    return math.degrees(math.asin(max(-1.0, min(1.0, altitude_m / range_m))))


def descent_track(trajectory: TrajectoryConfig, t_s: float) -> Vec3:
    """Position vid tiden t för en rak nedfart med vinddrift.

    Modellen är medvetet enkel: konstant sjunkhastighet och konstant vind. En
    fallskärmsnedfart har visserligen pendling, men pendlingen ändrar inte
    elevationen nämnvärt och skulle bara göra kurvorna svårare att läsa.
    """
    x0, y0, z0 = trajectory.start_position_m
    wx, wy = trajectory.wind_mps
    z = z0 - trajectory.descent_rate_mps * t_s
    return (x0 + wx * t_s, y0 + wy * t_s, z)


def track_duration_s(trajectory: TrajectoryConfig) -> float:
    """Hur länge nedfarten varar, till `stop_altitude_m`."""
    drop = trajectory.start_position_m[2] - trajectory.stop_altitude_m
    if drop <= 0:
        return 0.0
    return min(drop / trajectory.descent_rate_mps, trajectory.max_duration_s)


def time_steps(trajectory: TrajectoryConfig, time_step_s: float) -> list[float]:
    """Tidsstämplarna för hela banan, inklusive sluttiden."""
    duration = track_duration_s(trajectory)
    if duration <= 0:
        return [0.0]
    n = int(round(duration / time_step_s))
    return [min(i * time_step_s, duration) for i in range(n + 1)]


def foliage_path_length_m(
    elevation_deg: float,
    foliage_depth_m: float,
    foliage_top_m: float,
) -> float:
    """Hur lång sträcka radiosignalen går genom lövverk, i meter.

    Modellen: lövbältet ligger runt mottagaren, `foliage_depth_m` djupt och
    `foliage_top_m` högt. Strålen från sändaren kommer in på elevationen `el`.
    På horisontellt avstånd r från mottagaren är strålen på höjden r*tan(el).
    Den är alltså inne i lövverket så länge r*tan(el) < foliage_top_m, dvs upp
    till r = foliage_top_m / tan(el) — men aldrig längre än bältets djup.

    Vid elevation 0 (strålen går längs marken) är hela bältet i vägen. Vid hög
    elevation går strålen ovanför träden och förlusten blir noll. Det är precis
    den övergång som gör att länkar tappar data sent i en nedfart.
    """
    if foliage_depth_m <= 0 or foliage_top_m <= 0:
        return 0.0

    el = math.radians(max(0.0, min(89.9, elevation_deg)))
    tan_el = math.tan(el)
    if tan_el <= 1e-9:
        horizontal = foliage_depth_m
    else:
        horizontal = min(foliage_depth_m, foliage_top_m / tan_el)

    # Sned längd genom bältet, inte horisontell.
    return horizontal / max(0.05, math.cos(el))
