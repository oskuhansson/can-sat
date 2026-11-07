"""Motorn: kör ett scenario och ger en tidsserie.

Varje tidssteg gör samma sak i samma ordning, och ordningen är en del av
modellen:

    sann position  ->  vad trackern tror  ->  vart gimbalen pekar  ->  pekfel
                   ->  antennvinst  ->  vägförlust  ->  mottagen effekt
                   ->  marginal  ->  paketförlust

Att trackern får veta om signalen hördes i **föregående** steg är medvetet: en
RSSI-följare kan inte veta något om ett paket den ännu inte fått.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from . import linkbudget, modulation, propagation
from .antenna import AntennaPattern, make_pattern
from .config import Scenario
from .geometry import (
    az_el_range,
    descent_track,
    pointing_error_deg,
    station_antenna_position,
    time_steps,
)
from .gimbal import Gimbal
from .tracker import Tracker

# Under den här marginalen antas RSSI-följaren tappa toppen. Det är inte en
# fysikalisk gräns utan en modell av att toppjakt kräver att signalen hörs.
RSSI_MIN_MARGIN_DB = 3.0


@dataclass
class Step:
    """Ett tidssteg. Kolumnerna blir CSV:ns rubriker."""

    t_s: float
    az_true_deg: float
    el_true_deg: float
    range_m: float
    az_cmd_deg: float
    el_cmd_deg: float
    az_gimbal_deg: float
    el_gimbal_deg: float
    pointing_error_deg: float
    rx_gain_dbi: float
    fspl_db: float
    vegetation_db: float
    multipath_db: float
    shadowing_db: float
    path_loss_db: float
    rx_power_dbm: float
    sensitivity_dbm: float
    margin_db: float
    per: float
    phase: str
    gps_used: bool
    packet_slot: bool
    packet_lost: bool


@dataclass
class SimulationResult:
    scenario_name: str
    seed: int
    steps: list[Step]
    summary: dict[str, float | str]
    constants: dict[str, float | int | str | None] = field(default_factory=dict)

    def rows(self) -> list[dict]:
        """Tidsserien som lista av dictar, redo för CSV eller DataFrame."""
        return [s.__dict__.copy() for s in self.steps]


def _percentile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round(q * (len(ordered) - 1)))))
    return ordered[idx]


def run(scenario: Scenario, seed: int | None = None, pattern: AntennaPattern | None = None) -> SimulationResult:
    """Kör ett scenario. Samma seed ger samma resultat, varje gång."""
    used_seed = scenario.seed if seed is None else int(seed)
    rng = np.random.default_rng(used_seed)

    pattern = pattern or make_pattern(scenario.antenna)
    station = station_antenna_position(scenario.station)

    chain = linkbudget.analyse_chain(scenario.radio)
    sf, bandwidth_khz = modulation.parse_mode(scenario.radio.modulation)
    sensitivity_chip = modulation.sensitivity_dbm(
        sf, bandwidth_khz, scenario.radio.frequency_mhz
    )
    sensitivity = linkbudget.effective_sensitivity_dbm(sensitivity_chip, chain)

    airtime = scenario.packet.airtime_override_s
    if airtime is None:
        airtime = modulation.airtime_s(sf, bandwidth_khz, scenario.packet.payload_bytes)

    shadowing = propagation.ShadowingProcess(scenario.propagation.shadowing, rng)
    tracker = Tracker(
        scenario.tracker,
        pattern.beamwidth_3db_deg,
        station,
        rng,
        airtime_s=airtime,
        max_scan_deg=scenario.antenna.max_scan_deg,
    )
    gimbal = Gimbal(
        scenario.gimbal, scenario.tracker.park_az_deg, scenario.tracker.park_el_deg
    )
    electronic = scenario.tracker.scan_mode == "electronic"

    timestamps = time_steps(scenario.trajectory, scenario.time_step_s)
    steps: list[Step] = []

    signal_ok = True
    next_packet_t = timestamps[0]
    previous_t = timestamps[0]
    # Var antennen faktiskt står. Trackern får veta det, så att låsningen
    # jämförs med den riktning gimbalen hunnit fram till — inte med den
    # kommenderade. Skillnaden är hela poängen med en slevgräns.
    actual_az = scenario.tracker.park_az_deg
    actual_el = scenario.tracker.park_el_deg

    for t in timestamps:
        dt = max(0.0, t - previous_t)
        previous_t = t

        position = descent_track(scenario.trajectory, t)
        az_true, el_true, distance = az_el_range(station, position)

        # Vad trackern tror, och vart antennen faktiskt pekar.
        command = tracker.command(
            t, position, signal_ok, gimbal_az_deg=actual_az, gimbal_el_deg=actual_el
        )
        if electronic:
            # Fasstyrd array: strålen flyttas elektroniskt. Ingen svephastighet,
            # inget glapp, ingen mekanisk upplösning — men den egna
            # faskvantiseringen finns kvar i arrayfaktorn.
            az_gimbal, el_gimbal = command.az_deg, command.el_deg
        else:
            az_gimbal, el_gimbal = gimbal.step(dt, command.az_deg, command.el_deg)
        actual_az, actual_el = az_gimbal, el_gimbal

        error = pointing_error_deg(az_true, el_true, az_gimbal, el_gimbal)
        # Kommandoriktningen skickas separat: för hybriden är det dit den
        # elektroniska strålen styrs, medan `az_gimbal/el_gimbal` är arrayens
        # bredsida. Skickades bara den ena skulle arrayen peka perfekt på målet
        # redan under svepningen — ett orakel den inte har tillgång till.
        rx_gain = pattern.gain_towards(
            az_true,
            el_true,
            az_gimbal,
            el_gimbal,
            command.az_deg,
            command.el_deg,
        )

        # Vägen från sändare till mottagare.
        losses = propagation.total_path_loss_db(
            frequency_mhz=scenario.radio.frequency_mhz,
            distance_m=distance,
            elevation_deg=el_true,
            vegetation=scenario.propagation.vegetation,
            multipath=scenario.propagation.multipath,
            tx_height_m=max(0.0, position[2] - station[2]),
            rx_height_m=scenario.station.antenna_height_m,
        )
        shadow_db = shadowing.step()

        rx_power = linkbudget.received_power_dbm(
            scenario.radio.eirp_dbm, losses["path_loss_db"], rx_gain, shadow_db
        )
        margin = linkbudget.margin_db(rx_power, sensitivity)
        per = modulation.packet_error_rate(margin)

        # Pakethändelse?
        packet_slot = t >= next_packet_t - 1e-9
        packet_lost = False
        if packet_slot:
            packet_lost = bool(rng.random() < per)
            next_packet_t += scenario.packet.interval_s

        steps.append(
            Step(
                t_s=t,
                az_true_deg=az_true,
                el_true_deg=el_true,
                range_m=distance,
                az_cmd_deg=command.az_deg,
                el_cmd_deg=command.el_deg,
                az_gimbal_deg=az_gimbal,
                el_gimbal_deg=el_gimbal,
                pointing_error_deg=error,
                rx_gain_dbi=rx_gain,
                fspl_db=losses["fspl_db"],
                vegetation_db=losses["vegetation_db"],
                multipath_db=losses["multipath_db"],
                shadowing_db=shadow_db,
                path_loss_db=losses["path_loss_db"],
                rx_power_dbm=rx_power,
                sensitivity_dbm=sensitivity,
                margin_db=margin,
                per=per,
                phase=command.phase,
                gps_used=command.gps_used,
                packet_slot=packet_slot,
                packet_lost=packet_lost,
            )
        )

        # Nästa stegs tracker får veta om signalen hördes nu.
        signal_ok = margin > RSSI_MIN_MARGIN_DB

    summary = _summarise(
        scenario, steps, tracker, pattern, chain, sensitivity, sensitivity_chip, airtime
    )
    constants = {
        "sensitivity_dbm": sensitivity,
        "sensitivity_chip_dbm": sensitivity_chip,
        "noise_figure_db": chain.noise_figure_db,
        "airtime_s": airtime,
        "beamwidth_3db_deg": pattern.beamwidth_3db_deg,
        "lock_time_s": tracker.lock_time_s,
        "scan_time_s": tracker.scan_time_s,
        "frequency_mhz": scenario.radio.frequency_mhz,
        "eirp_dbm": scenario.radio.eirp_dbm,
        # Array- och svepuppgifter. None för alla scenarier som inte är arrayer,
        # så att inget befintligt scenario påverkas.
        "scan_mode": scenario.tracker.scan_mode,
        "scan_dwell_s": tracker.scan_dwell_s,
        "antenna_model": scenario.antenna.model,
        "array_nx": scenario.antenna.array_nx,
        "array_ny": scenario.antenna.array_ny,
        "phase_bits": scenario.antenna.phase_bits,
        "spacing_lambda": scenario.antenna.spacing_lambda,
        "element_gain_dbi": scenario.antenna.element_gain_dbi,
        "max_scan_deg": scenario.antenna.max_scan_deg,
    }
    return SimulationResult(scenario.name, used_seed, steps, summary, constants)


def _summarise(
    scenario: Scenario,
    steps: list[Step],
    tracker: Tracker,
    pattern: AntennaPattern,
    chain: linkbudget.ReceiverChain,
    sensitivity: float,
    sensitivity_chip: float,
    airtime: float,
) -> dict[str, float | str]:
    """Räkna ihop det som är värt att titta på."""
    if not steps:
        return {}

    # Låst = trackern har en riktning att följa. "acquire", "park" och "hold" är
    # alla tillstånd där antennen inte följer sändaren, så de räknas inte med.
    locked = [s for s in steps if s.phase in ("gps", "rssi")]
    errors = [s.pointing_error_deg for s in steps if not math.isnan(s.pointing_error_deg)]
    locked_errors = [
        s.pointing_error_deg for s in locked if not math.isnan(s.pointing_error_deg)
    ]
    margins = [s.margin_db for s in steps]

    packets = [s for s in steps if s.packet_slot]
    lost = [s for s in packets if s.packet_lost]
    loss_fraction = len(lost) / len(packets) if packets else 0.0

    # Längsta sammanhängande förlust — "datahålet".
    longest_run_s = 0.0
    run_length = 0
    for s in packets:
        if s.packet_lost:
            run_length += 1
            longest_run_s = max(longest_run_s, run_length * scenario.packet.interval_s)
        else:
            run_length = 0

    # Förlust i slutet av nedfarten, där vegetationen biter.
    tail_start = steps[-1].t_s * 0.75
    tail_packets = [s for s in packets if s.t_s >= tail_start]
    tail_lost = [s for s in tail_packets if s.packet_lost]
    tail_fraction = len(tail_lost) / len(tail_packets) if tail_packets else 0.0

    worst = min(steps, key=lambda s: s.margin_db)
    veg = [s.vegetation_db for s in steps]

    # Hybriden: hur ofta ligger målet utanför den elektroniska konen, så att
    # arrayen klämmer vid max_scan och gimbalen måste flytta? Och hur stor blir
    # scanförlusten av att elementet inte pekar rakt fram?
    max_scan = scenario.antenna.max_scan_deg
    elem_bw = scenario.antenna.element_beamwidth_3db_deg or 65.0
    if max_scan is not None:
        outside = [s for s in steps if s.pointing_error_deg > max_scan]
        outside_fraction = len(outside) / len(steps)
        outside_time_s = len(outside) * scenario.time_step_s
        scan_loss = [
            12.0 * (min(s.pointing_error_deg, max_scan) / elem_bw) ** 2 for s in steps
        ]
        scan_loss_mean_db = sum(scan_loss) / len(scan_loss)
        scan_loss_max_db = max(scan_loss)
    else:
        outside_fraction = float("nan")
        outside_time_s = float("nan")
        scan_loss_mean_db = float("nan")
        scan_loss_max_db = float("nan")

    # Duty cycle mäts över en timme, inte över flygningen. Under en flygning på
    # några minuter är det därför hela timbudgeten som är taket.
    total_airtime_s = len(packets) * airtime
    limit = scenario.radio.duty_cycle_limit
    budget_s = limit * 3600.0 if limit else None

    return {
        "duration_s": steps[-1].t_s,
        "packets_sent": len(packets),
        "packets_lost": len(lost),
        "loss_fraction": loss_fraction,
        "longest_loss_run_s": longest_run_s,
        "tail_loss_fraction": tail_fraction,
        "pointing_error_mean_deg": sum(errors) / len(errors) if errors else float("nan"),
        "pointing_error_p95_deg": _percentile(errors, 0.95),
        "pointing_error_max_deg": max(errors) if errors else float("nan"),
        "pointing_error_locked_mean_deg": (
            sum(locked_errors) / len(locked_errors) if locked_errors else float("nan")
        ),
        "pointing_error_locked_max_deg": max(locked_errors) if locked_errors else float("nan"),
        "margin_min_db": worst.margin_db,
        "margin_min_at_s": worst.t_s,
        "margin_mean_db": sum(margins) / len(margins),
        "margin_below_zero_fraction": sum(1 for m in margins if m < 0) / len(margins),
        "vegetation_max_db": max(veg),
        "rx_gain_loss_max_db": pattern.peak_gain_dbi - min(s.rx_gain_dbi for s in steps),
        "rx_gain_loss_mean_db": pattern.peak_gain_dbi
        - (sum(s.rx_gain_dbi for s in steps) / len(steps)),
        "lock_time_s": tracker.lock_time_s,
        "scan_time_s": tracker.scan_time_s,
        "sensitivity_dbm": sensitivity,
        "sensitivity_chip_dbm": sensitivity_chip,
        "noise_figure_db": chain.noise_figure_db,
        "sensitivity_improvement_db": chain.sensitivity_improvement_db,
        "airtime_s": airtime,
        "duty_cycle": modulation.duty_cycle_fraction(airtime, scenario.packet.interval_s),
        "airtime_total_s": total_airtime_s,
        "airtime_budget_s": budget_s if budget_s is not None else float("nan"),
        "duty_cycle_ok": (budget_s is None) or (total_airtime_s <= budget_s),
        "beamwidth_3db_deg": pattern.beamwidth_3db_deg,
        "tolerance_1db_deg": linkbudget.tolerance_angle_deg(pattern.beamwidth_3db_deg, 1.0),
        "phase_acquire_fraction": sum(1 for s in steps if s.phase == "acquire") / len(steps),
        "scan_mode": scenario.tracker.scan_mode,
        "scan_dwell_s": tracker.scan_dwell_s,
        "outside_scan_fraction": outside_fraction,
        "outside_scan_time_s": outside_time_s,
        "scan_loss_mean_db": scan_loss_mean_db,
        "scan_loss_max_db": scan_loss_max_db,
    }
