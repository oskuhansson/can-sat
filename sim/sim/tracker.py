"""Trackern: vad gimbalen ska sikta på.

Tre lägen, och övergångarna mellan dem är själva poängen med simuleringen:

* **acquire** — innan låsning sveper gimbalen himlen. Utan GPS finns ingen
  riktning att räkna på, så antennen måste leta. Pekfelet är då vinkeln mellan
  sveppositionen och sändaren, vilket nästan alltid är stort.
* **gps** — sändarens position finns i telemetrin. Trackern räknar om den till
  azimut/elevation med samma geometri som sanningen, men från en **brusig**
  position. Felet blir därför automatiskt stort på nära håll och litet på långt
  håll — precis som i verkligheten.
* **rssi** — ingen GPS. Trackern följer RSSI-toppen med en noggrannhet som är en
  bråkdel av strålbredden.

Två olika RSSI-noggrannheter används med flit. En **sökning** över hela himlen
kan bara skilja ut ungefär en tiondel av strålbredden. En **finjustering** kring
en topp man redan hittat — vilket är vad som sker när GPS:en gett riktningen —
löser mycket bättre, ungefär en femtiondel. Att använda sökningens noggrannhet
också för finjusteringen gör GPS-läget orimligt dåligt: 4,8° jitter på en 48°-lob
förvandlar ett pekfel på 0,3° till 2,1°.

Läget **hold** inträder när signalen försvinner: en RSSI-följare kan inte
toppjaga något den inte hör. Då hålls den senaste vinkeln, och felet växer i takt
med att sändaren rör sig.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .config import ConfigError, TrackerConfig
from .geometry import az_el_range, pointing_error_deg


# Rastret cachas per max_scan: att verifiera täckningen numeriskt kostar några
# hundra millisekunder och parametern tar bara ett fåtal värden.
_RASTER_CACHE: dict[float, list[tuple[float, float]]] = {}


def _ring_azimuths(elev_deg: float, alpha_deg: float) -> int:
    """Hur många azimuter som behövs på en ring för att täcka den.

    Härleds ur kravet att två närliggande riktningar på samma elevation högst
    får ligga `alpha` grader isär: cos(alpha) = sin²e + cos²e·cos(daz).
    """
    if elev_deg >= 90.0 - 1e-9:
        return 1
    ce = math.cos(math.radians(elev_deg))
    se = math.sin(math.radians(elev_deg))
    ca = math.cos(math.radians(alpha_deg))
    if ce < 1e-9:
        return 1
    arg = (ca - se * se) / (ce * ce)
    if arg >= 1.0 or arg <= -1.0:
        return 1
    daz = 2.0 * math.degrees(math.acos(arg))
    if daz <= 1e-6:
        return 1
    return max(1, int(math.ceil(360.0 / daz)))


def _raster_candidates(alpha_deg: float, shrink: float) -> list[tuple[float, float]]:
    step = alpha_deg * shrink
    elevations = []
    e = 90.0
    while e > 1e-9:
        elevations.append(e)
        e -= step
    if not elevations or elevations[-1] > 1e-9:
        elevations.append(0.0)
    out: list[tuple[float, float]] = []
    for e in elevations:
        n = _ring_azimuths(e, alpha_deg)
        for k in range(n):
            out.append((360.0 * k / n, e))
    return out


def raster_coverage(raster: list[tuple[float, float]], alpha_deg: float) -> float:
    """Andel av himlen (cos-el-viktad) som ligger inom `alpha` från rastret."""
    el = np.arange(0.0, 90.0001, 2.0)
    az = np.arange(0.0, 360.0, 2.0)
    az_grid, el_grid = np.meshgrid(np.radians(az), np.radians(el))
    points = np.stack(
        [
            np.cos(el_grid) * np.cos(az_grid),
            np.cos(el_grid) * np.sin(az_grid),
            np.sin(el_grid),
        ],
        axis=-1,
    ).reshape(-1, 3)
    weights = np.cos(el_grid).reshape(-1)
    covered = np.zeros(len(points), dtype=bool)
    cos_a = math.cos(math.radians(alpha_deg))
    for az_deg, el_deg in raster:
        a = math.radians(az_deg)
        e = math.radians(el_deg)
        v = np.array(
            [math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)]
        )
        covered |= (points @ v) >= cos_a - 1e-12
    return float(weights[covered].sum() / weights.sum())


def covering_raster(alpha_deg: float) -> list[tuple[float, float]]:
    """Gimbalriktningar som täcker himlen med en kon av halfvinkeln `alpha`.

    Den tidigare konstruktionen — `n_el = ceil(90/coverage)` rader jämnt
    utspridda mellan 0 och 90 grader — gav två rader (0 och 90) vid max_scan 30
    och lämnade 47 % av himlen otäckt. En sändare kunde då stå i en riktning som
    rastret aldrig besökte, hur länge svepet än pågick.

    Här byggs ringar med den azimuth-täthet som krävs, och täckningen verifieras
    numeriskt. Räcker den inte tätas ringarna. Rastret sorteras med zenit först:
    det är där en fallande sändare börjar, och det är så en operatör söker.
    """
    if alpha_deg <= 0:
        raise ConfigError("tracker: max_scan_deg måste vara positiv")
    if alpha_deg in _RASTER_CACHE:
        return _RASTER_CACHE[alpha_deg]
    best: list[tuple[float, float]] | None = None
    best_cov = -1.0
    for shrink in (1.0, 0.85, 0.7, 0.55, 0.4):
        candidate = _raster_candidates(alpha_deg, shrink)
        cov = raster_coverage(candidate, alpha_deg)
        if cov > best_cov:
            best, best_cov = candidate, cov
        if cov >= 0.995:
            break
    if best is None or best_cov < 0.95:  # pragma: no cover - skyddsnät
        raise ConfigError(
            f"tracker: kunde inte täcka himlen med max_scan {alpha_deg} grader "
            f"(bästa täckning {100 * best_cov:.1f} %)"
        )
    # Zenit först, sedan nedåt. Determinism: samma lista varje gång.
    best = sorted(best, key=lambda p: (-p[1], p[0]))
    _RASTER_CACHE[alpha_deg] = best
    return best


@dataclass
class TrackerOutput:
    az_deg: float
    el_deg: float
    phase: str
    gps_used: bool


class Tracker:
    def __init__(
        self,
        cfg: TrackerConfig,
        beamwidth_deg: float,
        station_position: tuple[float, float, float],
        rng: np.random.Generator,
        airtime_s: float = 0.0,
        max_scan_deg: float | None = None,
    ):
        self.cfg = cfg
        self.station = station_position
        self.rng = rng
        self.beamwidth = beamwidth_deg
        self.electronic = cfg.scan_mode == "electronic"
        self.hybrid = cfg.scan_mode == "hybrid"
        self.max_scan_deg = max_scan_deg

        # Sökning respektive finjustering har olika noggrannhet.
        search_sigma = (
            cfg.rssi_fine_sigma_deg
            if cfg.rssi_fine_sigma_deg is not None
            else max(0.3, beamwidth_deg / 10.0)
        )
        self.rssi_sigma_search = search_sigma
        self.rssi_sigma_fine = max(0.2, search_sigma / 5.0)

        # Tiden man måste stå still i varje strålposition.
        #
        # Mekaniskt: gimbalens dwell, som är en mekanisk tidskonstant.
        # Elektroniskt: strålen flyttas på mikrosekunder, men för att UPPTÄCKA
        # sändaren måste man lyssna minst ett helt paket i riktningen. Därför
        # max(switch_time, lufttid) — och därför är elektronisk svepning snabb
        # men inte momentan. Det är hela poängen att simulera.
        if self.hybrid:
            if max_scan_deg is None:
                raise ConfigError(
                    "tracker.scan_mode 'hybrid' kräver antenna.max_scan_deg"
                )
            # Gimbalen rastrar så att konen (2*max_scan bred) täcker himlen.
            # Rastret verifieras numeriskt — den tidigare varianten lämnade
            # 12-47 % av himlen otäckt, så en sändare kunde stå oåtkomlig.
            self._raster = covering_raster(float(max_scan_deg))
            self.n_az = 0
            self.n_el = 0
            # Inne i konen scannar arrayen elektroniskt. Antalet delpositioner
            # sätts av **arrayens** strålbredd, inte elementets: den
            # syntetiserade loben är smalare (44 grader mot elementets 65), och
            # elementets bredd gav 4 positioner i stället för 9 — fyra gånger
            # för kort sveptid.
            coverage = 2.0 * float(max_scan_deg)
            self.n_elec = max(1, math.ceil(coverage / beamwidth_deg)) ** 2
            self.scan_dwell_s = max(cfg.switch_time_s, airtime_s) * self.n_elec
            # Låsning när gimbalen är inom konen: då kan arrayen styra resten.
            self.lock_tolerance_deg = float(max_scan_deg)
        else:
            self._raster = None
            self.n_elec = 1
            self.scan_dwell_s = (
                max(cfg.switch_time_s, airtime_s) if self.electronic else cfg.scan_dwell_s
            )
            self.n_az = max(1, math.ceil(360.0 / beamwidth_deg))
            self.n_el = max(1, math.ceil(90.0 / beamwidth_deg))
            self.lock_tolerance_deg = beamwidth_deg / 2.0

        self.n_positions = (
            len(self._raster) if self._raster is not None else self.n_az * self.n_el
        )
        self.scan_time_s = self.n_positions * self.scan_dwell_s

        self.lock_time_s: float = math.nan
        self._lock_candidate_t: float | None = None
        self._rssi_offset = 0.0
        self._rssi_rho = 0.9
        self._held: tuple[float, float] | None = None

    # ------------------------------------------------------------------
    def _sweep_position(self, t_s: float) -> tuple[float, float]:
        """Var antennen står i svepet vid tiden t.

        Sekvensen är deterministisk — samma seed ska ge samma svep. Hybriden
        följer ett verifierat täckande raster; de mekaniska och elektroniska
        varianterna stegar azimuten varv runt och höjer sedan elevationen.
        """
        dwell = max(1e-6, self.scan_dwell_s)

        if self._raster is not None:
            step = int(t_s / dwell) % len(self._raster)
            return self._raster[step]

        total = self.n_az * self.n_el
        step = int(t_s / dwell) % total
        az = (step % self.n_az) * (360.0 / self.n_az)
        row = step // self.n_az
        el = 45.0 if self.n_el == 1 else 90.0 * row / (self.n_el - 1)
        return az, el

    def _drift(self, sigma: float) -> float:
        innovation = float(self.rng.normal(0.0, sigma))
        self._rssi_offset = (
            self._rssi_rho * self._rssi_offset
            + math.sqrt(1.0 - self._rssi_rho**2) * innovation
        )
        return self._rssi_offset

    def _gps_position(self, true_pos: tuple[float, float, float]) -> tuple[float, float, float]:
        sx = float(self.rng.normal(0.0, self.cfg.gps_horizontal_sigma_m))
        sy = float(self.rng.normal(0.0, self.cfg.gps_horizontal_sigma_m))
        sz = float(self.rng.normal(0.0, self.cfg.gps_vertical_sigma_m))
        return (true_pos[0] + sx, true_pos[1] + sy, true_pos[2] + sz)

    # ------------------------------------------------------------------
    def command(
        self,
        t_s: float,
        true_pos: tuple[float, float, float],
        signal_ok: bool = True,
        gimbal_az_deg: float | None = None,
        gimbal_el_deg: float | None = None,
    ) -> TrackerOutput:
        """Vilken azimut/elevation gimbalen ska styras mot vid tiden t.

        `gimbal_az_deg/gimbal_el_deg` är var antennen **står** just nu, inte var
        den är kommenderad. Låsningen måste jämföras med den faktiska
        riktningen: annars registreras en låsning vid en svepposition som
        gimbalen ännu inte hunnit fram till, och pekfelet ser mindre ut än det är.
        """
        cfg = self.cfg
        true_az, true_el, _ = az_el_range(self.station, true_pos)

        # 0. Digital array med flera mottagarkedjor lyssnar i alla riktningar
        #    samtidigt. Då finns riktningen från första stunden och det finns
        #    ingen acquisitionsfas alls — låsningstiden blir noll. Det är den
        #    undre gränsen, inte ett system i den här budgeten.
        if cfg.simultaneous_beams and math.isnan(self.lock_time_s):
            self.lock_time_s = t_s

        # 0b. Parkera och håll — vad en operatör faktiskt gör: gimbalen ställs i
        #     den förväntade uppskjutningsriktningen innan första paketet kommit,
        #     i stället för att svepa blint över himlen. Utan det här tvingas
        #     yagin svepa i onödan och framstår som sämre än den är.
        if cfg.park_and_hold and t_s < cfg.lock_delay_s:
            self._held = (cfg.park_az_deg, cfg.park_el_deg)
            return TrackerOutput(cfg.park_az_deg, cfg.park_el_deg, "park", False)

        # 1. Har vi GPS? Då är riktningen känd så fort första paketet kommit.
        gps_active = cfg.gps_available and (
            cfg.gps_dropout_after_s is None or t_s < cfg.gps_dropout_after_s
        )
        if gps_active and t_s >= cfg.lock_delay_s:
            if math.isnan(self.lock_time_s):
                self.lock_time_s = t_s
            noisy = self._gps_position(true_pos)
            az, el, _ = az_el_range(self.station, noisy)
            fine = self._drift(self.rssi_sigma_fine) * 0.5
            self._held = (az + fine, el + fine)
            return TrackerOutput(az + fine, el + fine, "gps", True)

        # 2. Utan GPS: svep tills strålen träffar. Låsningen sker när **den
        #    faktiska** riktningen ligger inom `lock_tolerance_deg` från
        #    sändaren. För hybriden är toleransen hela den elektroniska konen:
        #    räcker det att gimbalen är inom max_scan kan arrayen styra resten.
        #
        #    Att riktningen stämmer betyder dock inte att sändaren hittats. Man
        #    måste lyssna i varje strålposition minst ett paket — för hybriden
        #    alla `n_elec` delpositioner inne i konen. Därför dröjer låsningen en
        #    `scan_dwell_s` efter att konen först täckt målet. Utan den
        #    fördröjningen blev låsningstiden noll, vilket är en artefakt av
        #    tidssteget och inte ett fysikaliskt svar.
        if math.isnan(self.lock_time_s):
            az_sweep, el_sweep = self._sweep_position(t_s)
            ref_az = az_sweep if gimbal_az_deg is None else gimbal_az_deg
            ref_el = el_sweep if gimbal_el_deg is None else gimbal_el_deg
            error = pointing_error_deg(ref_az, ref_el, true_az, true_el)
            if error <= self.lock_tolerance_deg:
                if self._lock_candidate_t is None:
                    self._lock_candidate_t = t_s
                if t_s >= self._lock_candidate_t + self.scan_dwell_s - 1e-9:
                    self.lock_time_s = t_s
                else:
                    return TrackerOutput(az_sweep, el_sweep, "acquire", False)
            else:
                self._lock_candidate_t = None
                return TrackerOutput(az_sweep, el_sweep, "acquire", False)

        # 3. Låst utan GPS: följ RSSI-toppen, men bara om signalen hörs.
        if not signal_ok and self._held is not None:
            az, el = self._held
            return TrackerOutput(az, el, "hold", False)

        offset = self._drift(self.rssi_sigma_search)
        az = true_az + offset
        el = true_el + offset * 0.5
        self._held = (az, el)
        return TrackerOutput(az, el, "rssi", False)
