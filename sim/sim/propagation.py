"""Utbredning: fri rymd, vegetation, skuggning och markreflexion.

Varje funktion här tar in fysikaliska storheter och ger tillbaka **förlust i dB**
(positivt tal = dämpning), utom markreflexionen som kan ge vinst.
"""

from __future__ import annotations

import math

import numpy as np

from .config import MultipathConfig, ShadowingConfig, VegetationConfig
from .geometry import foliage_path_length_m

SPEED_OF_LIGHT = 299_792_458.0


def fspl_db(frequency_mhz: float, distance_m: float) -> float:
    """Fri rymd-förlust: 32,44 + 20log10(f_MHz) + 20log10(d_km).

    Konstanten 32,44 är 20log10(4*pi/c) med f i MHz och d i km. Under ~1 m
    tappar formeln sin mening (närfält), så avståndet klipps till 1 m.
    """
    if frequency_mhz <= 0:
        raise ValueError("frekvensen måste vara positiv")
    d_km = max(distance_m, 1.0) / 1000.0
    return 32.44 + 20.0 * math.log10(frequency_mhz) + 20.0 * math.log10(d_km)


def wavelength_m(frequency_mhz: float) -> float:
    return SPEED_OF_LIGHT / (frequency_mhz * 1e6)


def vegetation_loss_db(cfg: VegetationConfig, elevation_deg: float) -> float:
    """ITU-R P.833-10 ekv. 1: A = A_m * (1 - exp(-d*gamma/A_m)).

    `d` är sträckan genom lövverket (geometry.foliage_path_length_m), `gamma`
    dämpningen per meter och `A_m` den asymptotiska maxförlusten. Formeln mättar
    alltså: hur djupt in i skogen man än går blir förlusten aldrig värre än A_m.

    Typvärden ur rekommendationen: 868 MHz gamma=0,17 dB/m, A_m=26,5 dB;
    2,4 GHz gamma=0,34 dB/m, A_m=34,1 dB.
    """
    if cfg.a_max_db <= 0 or cfg.gamma_db_per_m <= 0:
        return 0.0
    depth = foliage_path_length_m(
        elevation_deg, cfg.foliage_depth_m, cfg.foliage_top_m
    )
    if depth <= 0:
        return 0.0
    return cfg.a_max_db * (1.0 - math.exp(-depth * cfg.gamma_db_per_m / cfg.a_max_db))


class ShadowingProcess:
    """Lognormalskuggning som en AR(1)-process.

    Att dra ett nytt slumptal varje tidssteg ger ett orealistiskt flimmer — i
    verkligheten ändras skuggningen när sändaren rör sig genom miljön, inte
    mellan två millisekunder. AR(1) gör att nivån glider:

        s[t] = rho*s[t-1] + sqrt(1-rho^2)*sigma*N(0,1)

    Stationär standardavvikelse blir sigma, och rho styr hur snabbt den driver.
    """

    def __init__(self, cfg: ShadowingConfig, rng: np.random.Generator):
        self.sigma_db = cfg.sigma_db
        self.rho = cfg.correlation
        self.rng = rng
        self.state = 0.0
        if self.sigma_db > 0:
            self.state = float(self.rng.normal(0.0, self.sigma_db))

    def step(self) -> float:
        """Nästa skuggningsvärde i dB. Positivt = dämpning."""
        if self.sigma_db <= 0:
            return 0.0
        innovation = float(self.rng.normal(0.0, self.sigma_db))
        self.state = self.rho * self.state + math.sqrt(1.0 - self.rho**2) * innovation
        return self.state


def multipath_gain_db(
    cfg: MultipathConfig,
    frequency_mhz: float,
    distance_m: float,
    tx_height_m: float,
    rx_height_m: float,
) -> float:
    """Tvåvägsmodell: direktvåg plus markreflexion, som funktion av fasskillnaden.

    Vågorna färdas olika långt. För d >> h_t, h_r är vägskillnaden

        Delta = 2*h_t*h_r/d

    och fasskillnaden phi = 2*pi*Delta/lambda. Den totala fältstyrkan relativt
    fri rymd är |1 + Gamma*exp(-j*phi)|, med Gamma = -reflection för en
    horisontalpolariserad våg som reflekteras i mark.

    Modellen ger upp till +6 dB (konstruktivt) och djupa nollställen
    (destruktivt). Den är avsiktligt **avstängd som default**: en riktig
    reflektion har spridning och frekvensberoende som en enkel tvåvägsmodell
    inte fångar, och nollställena flyttar sig snabbare än tidssteget.
    """
    if cfg.model == "none" or cfg.reflection <= 0:
        return 0.0

    lam = wavelength_m(frequency_mhz)
    if distance_m <= 0 or tx_height_m <= 0 or rx_height_m <= 0:
        return 0.0

    delta = 2.0 * tx_height_m * rx_height_m / distance_m
    phi = 2.0 * math.pi * delta / lam

    # Komplex fältamplitud: direktvåg (1) + reflekterad (-reflection * e^-j phi)
    real = 1.0 - cfg.reflection * math.cos(phi)
    imag = -cfg.reflection * math.sin(phi)
    magnitude = math.hypot(real, imag)

    return 20.0 * math.log10(max(1e-3, magnitude))


def total_path_loss_db(
    frequency_mhz: float,
    distance_m: float,
    elevation_deg: float,
    vegetation: VegetationConfig,
    multipath: MultipathConfig,
    tx_height_m: float,
    rx_height_m: float,
) -> dict[str, float]:
    """Summerar de förluster som beror på vägen. Skuggning läggs på separat."""
    fspl = fspl_db(frequency_mhz, distance_m)
    veg = vegetation_loss_db(vegetation, elevation_deg)
    mp = multipath_gain_db(
        multipath, frequency_mhz, distance_m, tx_height_m, rx_height_m
    )
    return {
        "fspl_db": fspl,
        "vegetation_db": veg,
        "multipath_db": -mp,  # redovisas som förlust; negativ = konstruktivt
        "path_loss_db": fspl + veg - mp,
    }
