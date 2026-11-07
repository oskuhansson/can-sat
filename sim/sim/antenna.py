"""Antennmönster: förstärkning som funktion av vinkeln från bomriktningen.

Alla modeller tar **en** vinkel: hur många grader pekar antennen fel. Det är
avsiktligt. En gimbal har två axlar, men antennen bryr sig bara om vinkeln mellan
där den pekar och där sändaren är — och den vinkeln räknas ut i geometry.py.

Pekförlusten i projektet skrivs `L = 12(θ/θ3dB)²`, vilket är exakt `gaussian`-
modellen nedan. Att de två stämmer är inte en slump: 12 dB-faktorn är den
paraboliska approximation som brukar användas för huvudloben.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np

from .config import AntennaConfig, ConfigError

# Standardnivå för sidolober när inget annat anges, relativt toppen.
DEFAULT_SIDELOBE_DB = -20.0
DEFAULT_BACKLOBE_DB = -25.0


class AntennaPattern:
    """Ett mönster: mata in pekfel i grader, få förstärkning i dBi."""

    def __init__(self, cfg: AntennaConfig, gain_fn: Callable[[float], float], beamwidth_deg: float):
        self.cfg = cfg
        self.model = cfg.model
        self.peak_gain_dbi = cfg.peak_gain_dbi
        self.beamwidth_3db_deg = beamwidth_deg
        self._gain_fn = gain_fn

    def gain_dbi(self, off_angle_deg: float) -> float:
        return float(self._gain_fn(abs(off_angle_deg)))

    def __call__(self, off_angle_deg: float) -> float:
        return self.gain_dbi(off_angle_deg)


# ---------------------------------------------------------------------------
# Modeller
# ---------------------------------------------------------------------------

_MODELS: dict[str, Callable[[AntennaConfig], Callable[[float], float]]] = {}


def register_model(name: str):
    """Gör en ny mönstermodell tillgänglig via `"model": "<namn>"` i scenariofilen."""

    def decorator(fn: Callable[[AntennaConfig], Callable[[float], float]]):
        _MODELS[name] = fn
        return fn

    return decorator


def available_models() -> list[str]:
    return sorted(_MODELS)


@register_model("isotropic")
def _isotropic(cfg: AntennaConfig) -> Callable[[float], float]:
    """Ingen riktverkan alls — samma nivå åt alla håll.

    Används för att isolera resten av kedjan: om ett scenario med `isotropic`
    fortfarande tappar paket är det inte pekningen som är problemet.
    """
    return lambda _theta: cfg.peak_gain_dbi


@register_model("gaussian")
def _gaussian(cfg: AntennaConfig) -> Callable[[float], float]:
    """Parabolisk huvudlob: G(θ) = G_max - 12*(θ/θ3dB)².

    Gäller bara runt bomriktningen. Bortom `cutoff` faller modellen till en
    sidolobenivå, annars skulle den ge orimliga dämpningar (vid 180 grader blir
    uttrycket -12*(180/17.5)² = -1270 dB, vilket inte är en antenn).
    """
    bw = _require_beamwidth(cfg, "gaussian")
    floor_db = cfg.peak_gain_dbi + (
        cfg.backlobe_db if cfg.backlobe_db is not None else DEFAULT_BACKLOBE_DB
    )
    # Klipp vid ungefär första nollstället, där parabeln inte längre beskriver något.
    cutoff = cfg.exponent if cfg.exponent is not None else 1.5 * bw

    def gain(theta: float) -> float:
        if theta <= cutoff:
            return cfg.peak_gain_dbi - 12.0 * (theta / bw) ** 2
        return floor_db

    return gain


@register_model("cosn")
def _cosn(cfg: AntennaConfig) -> Callable[[float], float]:
    """G(θ) = G_max * cos^n(θ), noll utanför ±90 grader.

    En enkel modell för en horn- eller patchantenn. `exponent` är n; om den
    utelämnas räknas den fram ur strålbredden via cos^n(θ3dB/2) = 0.5.
    """
    bw = _require_beamwidth(cfg, "cosn")
    n = cfg.exponent
    if n is None:
        half = math.radians(bw / 2.0)
        n = math.log(0.5) / math.log(max(1e-6, math.cos(half)))
    floor_db = cfg.peak_gain_dbi + (
        cfg.backlobe_db if cfg.backlobe_db is not None else DEFAULT_BACKLOBE_DB
    )

    def gain(theta: float) -> float:
        if theta >= 89.9:
            return floor_db
        c = math.cos(math.radians(theta))
        return cfg.peak_gain_dbi + 10.0 * math.log10(max(1e-12, c**n))

    return gain


@register_model("yagi")
def _yagi(cfg: AntennaConfig) -> Callable[[float], float]:
    """Yagi-approximation: huvudlob, sidolober och baklob.

    Huvudloben är parabolisk intill bomriktningen, därefter ett platt fält av
    sidolober. Modellen är grov — den fångar att en yagi har tydliga sidolober,
    inte var de sitter. Vill du ha det riktiga mönstret: kör NEC och använd
    `"model": "file"`.
    """
    bw = _require_beamwidth(cfg, "yagi")
    side = cfg.peak_gain_dbi + (
        cfg.sidelobe_db if cfg.sidelobe_db is not None else DEFAULT_SIDELOBE_DB
    )
    back = cfg.peak_gain_dbi + (
        cfg.backlobe_db if cfg.backlobe_db is not None else DEFAULT_BACKLOBE_DB
    )
    first_null = 1.25 * bw

    def gain(theta: float) -> float:
        if theta < first_null:
            return max(side, cfg.peak_gain_dbi - 12.0 * (theta / bw) ** 2)
        if theta < 110.0:
            return side
        return back

    return gain


@register_model("file")
def _file(cfg: AntennaConfig) -> Callable[[float], float]:
    """Mönster inläst från textfil: två kolumner, `vinkel_grader förstärkning_dbi`.

    Filen ska ha stigande vinkel från 0 (bomriktning) till 180 (rakt bakåt).
    Värden mellan punkterna interpoleras linjärt; utanför intervallet används
    ändpunkterna.
    """
    if not cfg.pattern_file:
        raise ConfigError("antenna: modellen 'file' kräver 'pattern_file'")

    path = Path(cfg.pattern_file)
    if not path.is_file():
        raise ConfigError(f"antenna: hittar inte mönsterfilen {path}")

    table = np.loadtxt(path)
    if table.ndim != 2 or table.shape[1] < 2 or table.shape[0] < 2:
        raise ConfigError(f"{path}: väntade minst två rader med två kolumner")
    angles = table[:, 0]
    gains = table[:, 1]

    def gain(theta: float) -> float:
        return float(np.interp(theta, angles, gains))

    return gain


# ---------------------------------------------------------------------------
# Fabrik
# ---------------------------------------------------------------------------


def _require_beamwidth(cfg: AntennaConfig, model: str) -> float:
    if cfg.beamwidth_3db_deg is None:
        raise ConfigError(f"antenna: modellen '{model}' kräver 'beamwidth_3db_deg'")
    if cfg.beamwidth_3db_deg <= 0:
        raise ConfigError("antenna.beamwidth_3db_deg måste vara positiv")
    return cfg.beamwidth_3db_deg


def estimate_beamwidth_deg(gain_dbi: float) -> float:
    """Grov skattning av strålbredden ur förstärkningen.

    Rymdvinkeln är ungefär 4*pi/G, och för en någorlunda symmetrisk lob gäller
    Ω ≈ 1.27*θ². Används bara när scenariofilen saknar strålbredd — den riktiga
    siffran ska komma från antennens datablad eller en NEC-körning.
    """
    g = 10.0 ** (gain_dbi / 10.0)
    theta_rad = math.sqrt(4.0 * math.pi / (1.27 * max(g, 1.0)))
    return math.degrees(theta_rad)


def make_pattern(cfg: AntennaConfig) -> AntennaPattern:
    """Bygg ett mönster ur konfigurationen."""
    if cfg.model not in _MODELS:
        raise ConfigError(
            f"antenna.model: okänd '{cfg.model}'. Tillgängliga: {', '.join(available_models())}"
        )
    gain_fn = _MODELS[cfg.model](cfg)
    bw = cfg.beamwidth_3db_deg
    if bw is None:
        bw = estimate_beamwidth_deg(cfg.peak_gain_dbi)
    return AntennaPattern(cfg, gain_fn, bw)
