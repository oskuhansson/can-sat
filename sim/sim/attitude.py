"""Burkens orientering och vad den kostar på länken.

Monopolen i burken har ett mönster som beror på vinkeln mellan **antennaxeln**
och riktningen till markstationen:

    G(θ) = G_max + 10·log₁₀(sin²θ)

Nollan sitter alltså både mot zenit (θ = 0) och mot nadir (θ = 180°). Det gör
orienteringen till en förlustkälla som är lätt att glömma: vid apogeum står
markstationen nästan rakt under burken, alltså θ ≈ 170-180°, och då är antennen
i sin egen nollnivå.

Förlusten är som störst just när avståndet är som kortast och marginalen som
bäst — och den försvinner när burken kommer ned och stationen ligger nära
horisonten (θ ≈ 90°, sin²θ = 1). Det är därför den måste räknas, inte antas.
"""

from __future__ import annotations

import math

from .config import AttitudeConfig


def unit_from_az_el(az_deg: float, el_deg: float) -> tuple[float, float, float]:
    """Enhetsvektor för en az/el-riktning.

    Azimuten mäts **medurs från norr** (+y), som `geometry.az_el_range` gör, så
    horisontalkomponenten är (sin az, cos az) — inte (cos az, sin az). Att blanda
    de två konventionerna roterar hela riktningen 90 grader, vilket är lätt att
    inte upptäcka eftersom pekfelet då bara ser "lite konstigt" ut.
    """
    ce = math.cos(math.radians(el_deg))
    return (
        ce * math.sin(math.radians(az_deg)),
        ce * math.cos(math.radians(az_deg)),
        math.sin(math.radians(el_deg)),
    )


def axis_vector(t_s: float, cfg: AttitudeConfig) -> tuple[float, float, float]:
    """Antennaxelns riktning vid tiden t.

    Axeln lutar `tilt_amplitude_deg` från vertikalen och sveper runt med
    `tilt_rate_hz` — en kon, vilket är den enklaste deterministiska modellen av
    pendling/precession under en fallskärm. Vid amplitud 0 pekar axeln rakt upp.
    """
    a = math.radians(cfg.tilt_amplitude_deg)
    if a <= 0.0:
        return (0.0, 0.0, 1.0)
    phi = 2.0 * math.pi * cfg.tilt_rate_hz * t_s + math.radians(cfg.phase_deg)
    return (math.sin(a) * math.cos(phi), math.sin(a) * math.sin(phi), math.cos(a))


def _dot(a, b) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _normalize(v):
    n = math.sqrt(_dot(v, v))
    if n < 1e-12:
        return (0.0, 0.0, 1.0)
    return (v[0] / n, v[1] / n, v[2] / n)


def pattern_loss_db(
    axis: tuple[float, float, float],
    to_station: tuple[float, float, float],
    floor_db: float,
) -> float:
    """Monopolens mönsterförlust i riktningen till markstationen.

    `to_station` är enhetsvektorn **från burken** mot stationen. θ är vinkeln
    mellan antennaxeln och den vektorn. Klipps vid `floor_db` — vid exakt
    nadir blir sin²θ = 0 och logaritmen går mot −∞, vilket inte är en antenn.
    """
    cos_t = max(-1.0, min(1.0, _dot(axis, to_station)))
    sin2 = max(1e-12, 1.0 - cos_t * cos_t)
    return max(floor_db, 10.0 * math.log10(sin2))


def ground_polarization_vector(
    az_deg: float, el_deg: float, mode: str
) -> tuple[float, float, float]:
    """Markantennens polarisationsvektor, vinkelrät mot dess bomriktning.

    En yagi polariserar längs elementen. `"vertical"` betyder att elementen står
    vertikalt, alltså att E är den del av "upp" som är vinkelrät mot bommen.

    Riktningen räknas **analytiskt** ur az/el i stället för att projicera
    vektorn numeriskt. Projektionen kollapsar när bommen pekar rakt upp
    (|perp| = cos e → 0) och då blir riktningen godtycklig. Den analytiska formen
    är en enhetsvektor för alla elevationer och går mot horisonten längs azimuten
    när e → 90°, vilket är den naturliga fortsättningen.

    Azimuten mäts medurs från norr, så horisontaldelen är (sin a, cos a).
    """
    e = math.radians(el_deg)
    a = math.radians(az_deg)
    if mode == "vertical":
        return (-math.sin(e) * math.sin(a), -math.sin(e) * math.cos(a), math.cos(e))
    # Horisontell polarisation: vinkelrät mot bommens horisontalprojektion.
    return (math.cos(a), -math.sin(a), 0.0)


def transverse_component(
    axis: tuple[float, float, float], direction: tuple[float, float, float]
) -> tuple[float, float, float] | None:
    """Den del av `axis` som är vinkelrät mot `direction`.

    Det är den riktning en monopol **strålar** i. En dipol längs ẑ har
    fjärrfältet riktat längs θ̂, inte längs ẑ — E måste vara vinkelrät mot
    utbredningsriktningen. Returnerar None när axeln är parallell med
    utbredningen (exakt nolla), där polarisationen inte är definierad.
    """
    proj = _dot(axis, direction)
    perp = (
        axis[0] - direction[0] * proj,
        axis[1] - direction[1] * proj,
        axis[2] - direction[2] * proj,
    )
    n = math.sqrt(_dot(perp, perp))
    if n < 1e-6:
        return None
    return (perp[0] / n, perp[1] / n, perp[2] / n)


def polarization_loss_db(
    axis: tuple[float, float, float],
    to_station: tuple[float, float, float],
    az_aim_deg: float,
    el_aim_deg: float,
    cfg: AttitudeConfig,
) -> float:
    """Polarisationsmässig missanpassning mellan burk och markantenn.

    Burkens E-vektor är **tvärkomponenten av axeln**, inte axeln själv: ett
    fjärrfält måste stå vinkelrätt mot utbredningsriktningen (θ̂ för en monopol).

    Det är lätt att ta fel här och sätta E = axeln. Då blir en vertikal monopol
    "korspolariserad" mot en antenn som pekar rakt upp, och man får ~15 dB extra
    förlust vid apogeum — men det är **samma** geometriska nolla som
    `sin²θ`-mönstret redan räknar. Att räkna den två gånger gör attitydförlusten
    dubbelt så stor som den är.

    Rotation kring den egna axeln ändrar ingenting: mönstret är
    rotationssymmetriskt och E-vektorn roterar med, så `spin_rate_hz` är en no-op
    för den här antennen.
    """
    can_pol = transverse_component(axis, to_station)
    if can_pol is None:
        # Exakt i nollan: mönstret har redan klippt förlusten, polarisationen
        # saknar mening. Att returnera ett straff här vore att räkna dubbelt.
        return 0.0
    ground_pol = ground_polarization_vector(az_aim_deg, el_aim_deg, cfg.ground_polarization)
    c = abs(_dot(can_pol, ground_pol))
    if c < 1e-6:
        return max(cfg.floor_db, -60.0)
    return max(cfg.floor_db, 20.0 * math.log10(c))
