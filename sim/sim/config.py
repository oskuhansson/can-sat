"""Konfiguration: dataklasser som speglar JSON-scenariofilerna.

Allt som skiljer två system åt — band, antenn, gimbal, bana — ska rymmas i en
scenariofil. Ingen modul här nedanför får innehålla CanSat-specifika tal.

Okända fält avvisas medvetet: en stavning som tyst ignoreras är den vanligaste
orsaken till att en simulering "inte stämmer" utan att någon märker varför.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Hjälpmedel
# ---------------------------------------------------------------------------


class ConfigError(ValueError):
    """Fel i en scenariofil — fel sorts fält, saknat värde eller dålig enhet."""


def _check_keys(cls: type, data: dict) -> None:
    known = {f.name for f in fields(cls)}
    extra = set(data) - known
    if extra:
        raise ConfigError(
            f"{cls.__name__}: okända fält {sorted(extra)}. Kända: {sorted(known)}"
        )


def _require(data: dict, key: str, where: str) -> Any:
    if key not in data:
        raise ConfigError(f"{where}: saknar obligatoriskt fält '{key}'")
    return data[key]


def _tuple_of_floats(value: Any, length: int, where: str) -> tuple[float, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ConfigError(f"{where}: väntade en lista med {length} tal, fick {value!r}")
    return tuple(float(v) for v in value)


# ---------------------------------------------------------------------------
# Delar
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TrajectoryConfig:
    """Sändarens bana. Rak nedfart med vinddrift — se geometry.descent_track."""

    start_position_m: tuple[float, float, float]
    descent_rate_mps: float
    wind_mps: tuple[float, float] = (0.0, 0.0)
    stop_altitude_m: float = 0.0
    max_duration_s: float = 600.0

    @classmethod
    def from_dict(cls, data: dict) -> "TrajectoryConfig":
        _check_keys(cls, data)
        rate = float(_require(data, "descent_rate_mps", "trajectory"))
        if rate <= 0:
            raise ConfigError("trajectory.descent_rate_mps måste vara positiv")
        return cls(
            start_position_m=_tuple_of_floats(
                _require(data, "start_position_m", "trajectory"), 3, "trajectory.start_position_m"
            ),
            descent_rate_mps=rate,
            wind_mps=_tuple_of_floats(data.get("wind_mps", (0.0, 0.0)), 2, "trajectory.wind_mps"),
            stop_altitude_m=float(data.get("stop_altitude_m", 0.0)),
            max_duration_s=float(data.get("max_duration_s", 600.0)),
        )


@dataclass(frozen=True)
class StationConfig:
    """Markstationens placering. Antennhöjden räknas in i elevationen."""

    position_m: tuple[float, float, float] = (0.0, 0.0, 0.0)
    antenna_height_m: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> "StationConfig":
        _check_keys(cls, data)
        return cls(
            position_m=_tuple_of_floats(data.get("position_m", (0.0, 0.0, 0.0)), 3, "station.position_m"),
            antenna_height_m=float(data.get("antenna_height_m", 0.0)),
        )


@dataclass(frozen=True)
class Stage:
    """Ett steg i mottagarkedjan, för Friis-kaskaden."""

    name: str
    gain_db: float
    noise_figure_db: float

    @classmethod
    def from_dict(cls, data: dict) -> "Stage":
        _check_keys(cls, data)
        return cls(
            name=str(_require(data, "name", "radio.rx_stages[]")),
            gain_db=float(_require(data, "gain_db", "radio.rx_stages[]")),
            noise_figure_db=float(_require(data, "noise_figure_db", "radio.rx_stages[]")),
        )


@dataclass(frozen=True)
class RadioConfig:
    """Radiofronten. `eirp_dbm` kan anges direkt eller räknas fram ur effekt + antennvinst.

    `duty_cycle_limit` är en andel (0,01 = 1 %) och gäller per timme enligt
    ETSI EN 300 220-2, som mäter över en timme — inte per flygning. Utelämnas
    den kontrolleras ingen gräns.
    """

    frequency_mhz: float
    eirp_dbm: float
    rx_stages: tuple[Stage, ...]
    receiver_noise_figure_db: float
    modulation: str
    tx_power_dbm: float | None = None
    tx_antenna_gain_dbi: float | None = None
    duty_cycle_limit: float | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "RadioConfig":
        _check_keys(cls, data)
        freq = float(_require(data, "frequency_mhz", "radio"))
        if freq <= 0:
            raise ConfigError("radio.frequency_mhz måste vara positiv")

        stages = tuple(Stage.from_dict(s) for s in data.get("rx_stages", []))

        eirp = data.get("eirp_dbm")
        if eirp is None:
            power = data.get("tx_power_dbm")
            gain = data.get("tx_antenna_gain_dbi", 0.0)
            if power is None:
                raise ConfigError("radio: ange antingen 'eirp_dbm' eller 'tx_power_dbm'")
            eirp = float(power) + float(gain)
        else:
            eirp = float(eirp)

        limit = data.get("duty_cycle_limit")
        return cls(
            frequency_mhz=freq,
            eirp_dbm=eirp,
            rx_stages=stages,
            receiver_noise_figure_db=float(
                _require(data, "receiver_noise_figure_db", "radio")
            ),
            modulation=str(_require(data, "modulation", "radio")),
            tx_power_dbm=None if data.get("tx_power_dbm") is None else float(data["tx_power_dbm"]),
            tx_antenna_gain_dbi=None
            if data.get("tx_antenna_gain_dbi") is None
            else float(data["tx_antenna_gain_dbi"]),
            duty_cycle_limit=None if limit is None else float(limit),
        )


@dataclass(frozen=True)
class AntennaConfig:
    """Markantennens mönster. `model` väljer implementation i antenna.py."""

    model: str
    peak_gain_dbi: float
    beamwidth_3db_deg: float | None = None
    exponent: float | None = None
    sidelobe_db: float | None = None
    backlobe_db: float | None = None
    pattern_file: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "AntennaConfig":
        _check_keys(cls, data)
        model = str(_require(data, "model", "antenna"))
        bw = data.get("beamwidth_3db_deg")
        if model in ("gaussian", "cosn") and bw is None and data.get("exponent") is None:
            raise ConfigError(f"antenna: modellen '{model}' kräver 'beamwidth_3db_deg'")
        return cls(
            model=model,
            peak_gain_dbi=float(_require(data, "peak_gain_dbi", "antenna")),
            beamwidth_3db_deg=None if bw is None else float(bw),
            exponent=None if data.get("exponent") is None else float(data["exponent"]),
            sidelobe_db=None if data.get("sidelobe_db") is None else float(data["sidelobe_db"]),
            backlobe_db=None if data.get("backlobe_db") is None else float(data["backlobe_db"]),
            pattern_file=data.get("pattern_file"),
        )


@dataclass(frozen=True)
class VegetationConfig:
    """ITU-R P.833-10, ekv. 1: A = A_m * (1 - exp(-d*gamma/A_m))."""

    gamma_db_per_m: float = 0.0
    a_max_db: float = 0.0
    foliage_depth_m: float = 0.0
    foliage_top_m: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> "VegetationConfig":
        _check_keys(cls, data)
        return cls(
            gamma_db_per_m=float(data.get("gamma_db_per_m", 0.0)),
            a_max_db=float(data.get("a_max_db", 0.0)),
            foliage_depth_m=float(data.get("foliage_depth_m", 0.0)),
            foliage_top_m=float(data.get("foliage_top_m", 0.0)),
        )


@dataclass(frozen=True)
class ShadowingConfig:
    """Lognormalskuggning som AR(1), så att nivån glider i stället för att fladdra."""

    sigma_db: float = 0.0
    correlation: float = 0.95

    @classmethod
    def from_dict(cls, data: dict) -> "ShadowingConfig":
        _check_keys(cls, data)
        rho = float(data.get("correlation", 0.95))
        if not 0.0 <= rho < 1.0:
            raise ConfigError("propagation.shadowing.correlation måste ligga i [0, 1)")
        return cls(sigma_db=float(data.get("sigma_db", 0.0)), correlation=rho)


@dataclass(frozen=True)
class MultipathConfig:
    """Tvåvägsmodell (markreflexion). Default av — se propagation.py."""

    model: str = "none"
    reflection: float = 0.5

    @classmethod
    def from_dict(cls, data: dict) -> "MultipathConfig":
        _check_keys(cls, data)
        model = str(data.get("model", "none"))
        if model not in ("none", "two_ray"):
            raise ConfigError(f"propagation.multipath.model: okänd '{model}' (none|two_ray)")
        return cls(model=model, reflection=float(data.get("reflection", 0.5)))


@dataclass(frozen=True)
class PropagationConfig:
    vegetation: VegetationConfig = VegetationConfig()
    shadowing: ShadowingConfig = ShadowingConfig()
    multipath: MultipathConfig = MultipathConfig()

    @classmethod
    def from_dict(cls, data: dict) -> "PropagationConfig":
        _check_keys(cls, data)
        return cls(
            vegetation=VegetationConfig.from_dict(data.get("vegetation", {})),
            shadowing=ShadowingConfig.from_dict(data.get("shadowing", {})),
            multipath=MultipathConfig.from_dict(data.get("multipath", {})),
        )


@dataclass(frozen=True)
class GimbalConfig:
    """Mekaniken. Ordningen i gimbal.py: svepgräns -> glapp -> kvantisering."""

    az_slew_deg_per_s: float = 30.0
    el_slew_deg_per_s: float = 30.0
    resolution_deg: float = 0.0
    backlash_deg: float = 0.0
    min_elevation_deg: float = 0.0
    max_elevation_deg: float = 90.0

    @classmethod
    def from_dict(cls, data: dict) -> "GimbalConfig":
        _check_keys(cls, data)
        lo = float(data.get("min_elevation_deg", 0.0))
        hi = float(data.get("max_elevation_deg", 90.0))
        if hi <= lo:
            raise ConfigError("gimbal: max_elevation_deg måste vara större än min_elevation_deg")
        return cls(
            az_slew_deg_per_s=float(data.get("az_slew_deg_per_s", 30.0)),
            el_slew_deg_per_s=float(data.get("el_slew_deg_per_s", 30.0)),
            resolution_deg=float(data.get("resolution_deg", 0.0)),
            backlash_deg=float(data.get("backlash_deg", 0.0)),
            min_elevation_deg=lo,
            max_elevation_deg=hi,
        )


@dataclass(frozen=True)
class TrackerConfig:
    """Pekstrategin. `gps_available=False` tvingar fram en svepande acquisition."""

    gps_available: bool = True
    gps_horizontal_sigma_m: float = 5.0
    gps_vertical_sigma_m: float = 8.0
    gps_dropout_after_s: float | None = None
    lock_delay_s: float = 2.0
    park_az_deg: float = 0.0
    park_el_deg: float = 45.0
    scan_dwell_s: float = 0.4
    rssi_fine_sigma_deg: float | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "TrackerConfig":
        _check_keys(cls, data)
        dropout = data.get("gps_dropout_after_s")
        return cls(
            gps_available=bool(data.get("gps_available", True)),
            gps_horizontal_sigma_m=float(data.get("gps_horizontal_sigma_m", 5.0)),
            gps_vertical_sigma_m=float(data.get("gps_vertical_sigma_m", 8.0)),
            gps_dropout_after_s=None if dropout is None else float(dropout),
            lock_delay_s=float(data.get("lock_delay_s", 2.0)),
            park_az_deg=float(data.get("park_az_deg", 0.0)),
            park_el_deg=float(data.get("park_el_deg", 45.0)),
            scan_dwell_s=float(data.get("scan_dwell_s", 0.4)),
            rssi_fine_sigma_deg=None
            if data.get("rssi_fine_sigma_deg") is None
            else float(data["rssi_fine_sigma_deg"]),
        )


@dataclass(frozen=True)
class PacketConfig:
    """Paketkadens. `payload_bytes` styr lufttiden via modulation.airtime_s."""

    interval_s: float = 0.5
    payload_bytes: int = 20
    airtime_override_s: float | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "PacketConfig":
        _check_keys(cls, data)
        override = data.get("airtime_override_s")
        return cls(
            interval_s=float(data.get("interval_s", 0.5)),
            payload_bytes=int(data.get("payload_bytes", 20)),
            airtime_override_s=None if override is None else float(override),
        )


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    time_step_s: float
    trajectory: TrajectoryConfig
    station: StationConfig
    radio: RadioConfig
    antenna: AntennaConfig
    propagation: PropagationConfig
    gimbal: GimbalConfig
    tracker: TrackerConfig
    packet: PacketConfig
    seed: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "Scenario":
        _check_keys(cls, data)
        return cls(
            name=str(_require(data, "name", "scenario")),
            description=str(data.get("description", "")),
            time_step_s=float(data.get("time_step_s", 0.1)),
            trajectory=TrajectoryConfig.from_dict(_require(data, "trajectory", "scenario")),
            station=StationConfig.from_dict(data.get("station", {})),
            radio=RadioConfig.from_dict(_require(data, "radio", "scenario")),
            antenna=AntennaConfig.from_dict(_require(data, "antenna", "scenario")),
            propagation=PropagationConfig.from_dict(data.get("propagation", {})),
            gimbal=GimbalConfig.from_dict(data.get("gimbal", {})),
            tracker=TrackerConfig.from_dict(data.get("tracker", {})),
            packet=PacketConfig.from_dict(data.get("packet", {})),
            seed=int(data.get("seed", 0)),
        )


def load_scenario(path: str | Path) -> Scenario:
    """Läs en scenariofil. Sökvägen kan vara relativ till anroparens katalog."""
    path = Path(path)
    if not path.is_file():
        raise ConfigError(f"hittar ingen scenariofil: {path}")
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: scenariofilen måste innehålla ett JSON-objekt")
    return Scenario.from_dict(data)
