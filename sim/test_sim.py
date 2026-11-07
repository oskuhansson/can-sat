"""Självtester för simuleringen.

Körs med:

    python test_sim.py

Varje kontroll skriver PASS eller FAIL. Avslutar med exit-kod 1 om något fallerar,
så att den kan användas som grind i en pipeline.
"""

from __future__ import annotations

import sys
import time
from dataclasses import replace
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sim import geometry, gimbal, linkbudget, modulation, propagation  # noqa: E402
from sim.antenna import estimate_beamwidth_deg, make_pattern  # noqa: E402
from sim.config import ConfigError, load_scenario  # noqa: E402
from sim.engine import run  # noqa: E402
from sim.report import to_frame  # noqa: E402

SCENARIOS = HERE / "scenarios"
PASS = 0
FAIL = 0


def section(title: str) -> None:
    print()
    print(title)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        suffix = f"  [{detail}]" if detail else ""
        print(f"  FAIL  {name}{suffix}")


def close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def main() -> int:
    started = time.perf_counter()

    # ------------------------------------------------------------------
    section("1. Fysik — enstaka formler mot kända värden")
    fspl_868 = propagation.fspl_db(868.0, 1500.0)
    fspl_24 = propagation.fspl_db(2400.0, 1500.0)
    check(
        "FSPL 868 MHz @1,5 km = 94,7 dB",
        close(fspl_868, 94.7, 0.15),
        f"fick {fspl_868:.2f}",
    )
    check(
        "FSPL 2,4 GHz @1,5 km = 103,6 dB",
        close(fspl_24, 103.6, 0.15),
        f"fick {fspl_24:.2f}",
    )
    check(
        "2,4 GHz kostar 8,8 dB mer än 868",
        close(fspl_24 - fspl_868, 8.83, 0.05),
        f"fick {fspl_24 - fspl_868:.2f}",
    )

    # Pekförlust: 12*(theta/theta3dB)^2 ska ge exakt 1 dB vid toleransvinkeln.
    tol_868 = linkbudget.tolerance_angle_deg(48.4, 1.0)
    tol_24 = linkbudget.tolerance_angle_deg(17.5, 1.0)
    check(
        "Tolerans för 1 dB: 868 ±14,0 grader",
        close(tol_868, 13.97, 0.1),
        f"fick {tol_868:.2f}",
    )
    check(
        "Tolerans för 1 dB: 2,4 GHz ±5,1 grader",
        close(tol_24, 5.05, 0.1),
        f"fick {tol_24:.2f}",
    )
    check(
        "Pekförlust är 1 dB vid toleransvinkeln",
        close(linkbudget.pointing_loss_db(tol_868, 48.4), 1.0, 1e-6),
    )

    # Antennmodellen ska ge -3 dB vid halva strålbredden.
    sc_868 = load_scenario(SCENARIOS / "cansat_868.json")
    pattern = make_pattern(sc_868.antenna)
    at_half = pattern.gain_dbi(pattern.beamwidth_3db_deg / 2.0)
    check(
        "Gaussisk lob ger -3 dB vid theta3dB/2",
        close(at_half, sc_868.antenna.peak_gain_dbi - 3.0, 0.01),
        f"fick {at_half:.2f} dBi",
    )
    check(
        "Antennmodellen är monoton utåt",
        pattern.gain_dbi(5.0) > pattern.gain_dbi(15.0) > pattern.gain_dbi(40.0),
    )

    # Friis-kaskad: LNA + pad ska ge NF 1,17 dB, dvs 4,83 dB bättre än chippen.
    chain = linkbudget.analyse_chain(sc_868.radio)
    check(
        "Kaskadbrusfaktor 868 = 1,17 dB",
        close(chain.noise_figure_db, 1.17, 0.02),
        f"fick {chain.noise_figure_db:.3f}",
    )
    check(
        "Känslighet förbättras 4,83 dB av fronten",
        close(chain.sensitivity_improvement_db, 4.83, 0.05),
        f"fick {chain.sensitivity_improvement_db:.2f}",
    )
    sens = linkbudget.effective_sensitivity_dbm(-129.0, chain)
    check(
        "Känslighet SF9/125 kHz = -133,8 dBm",
        close(sens, -133.83, 0.05),
        f"fick {sens:.2f}",
    )

    # Lufttid: 20 byte vid SF9/125 kHz tar ~108 ms.
    # (Formeln multiplicerar med (CR+4)/4; med CR+4 blev det 185 ms, alltså 71 %
    # för långt, vilket gjorde varje duty cycle-slutsats fel.)
    airtime = modulation.airtime_s(9, 125.0, 20)
    check(
        "Lufttid SF9/125 kHz, 20 byte = 108 ms",
        close(airtime, 0.1085, 0.005),
        f"fick {airtime * 1000:.1f} ms",
    )
    airtime_24 = modulation.airtime_s(9, 812.0, 20)
    check(
        "2,4 GHz är minst 5x snabbare på samma payload",
        airtime / airtime_24 > 5.0,
        f"forhallande {airtime / airtime_24:.1f}",
    )
    check(
        "PER vid marginal 0 dB = 1 %",
        close(modulation.packet_error_rate(0.0), 0.01, 1e-9),
    )
    # PER klamps till ett golv pa 1e-6, sa jamforelsen maste ligga under det.
    per0 = modulation.packet_error_rate(0.0)
    per2 = modulation.packet_error_rate(2.0)
    per4 = modulation.packet_error_rate(4.0)
    check("PER faller med marginalen", per4 < per2 < per0)
    check(
        "PER ar 1 vid starkt negativ marginal",
        modulation.packet_error_rate(-20.0) == 1.0,
    )

    # Vegetation: mer lovverk vid lag elevation an vid hog.
    veg = sc_868.propagation.vegetation
    veg_low = propagation.vegetation_loss_db(veg, 2.0)
    veg_high = propagation.vegetation_loss_db(veg, 70.0)
    check(
        "Vegetation kostar mer vid lag elevation",
        veg_low > veg_high,
        f"lag {veg_low:.2f} dB, hog {veg_high:.2f} dB",
    )
    check(
        "Vegetationsforlusten ar rimlig for 868 (2-8 dB)",
        2.0 < veg_low < 8.0,
        f"fick {veg_low:.2f} dB",
    )

    # Geometri
    az, el, dist = geometry.az_el_range((0.0, 0.0, 2.0), (0.0, 200.0, 1100.0))
    check("Azimut rakt fram = 0 grader", close(az, 0.0, 0.01), f"fick {az:.2f}")
    check("Elevation mot hogt mal ~80 grader", close(el, 79.7, 0.2), f"fick {el:.2f}")
    check("Rackvidd ~1116 m", close(dist, 1116.0, 3.0), f"fick {dist:.1f}")
    check(
        "Pekfel ar noll for samma riktning",
        close(geometry.pointing_error_deg(31.0, 20.0, 31.0, 20.0), 0.0, 1e-9),
    )

    # Gimbal: glapp och upplosning
    g = gimbal.Gimbal(replace(sc_868.gimbal, backlash_deg=2.0, resolution_deg=0.0))
    before = g.az
    g.step(0.1, 1.0, 45.0)  # 1 grad, mindre an halva glappet
    check("Glapp: 1 grads kommandororelse flyttar inget", close(g.az, before, 1e-9))
    g.step(0.1, 10.0, 45.0)
    check("Glapp: storre rorelse tar upp spelet", g.az > before)

    g2 = gimbal.Gimbal(replace(sc_868.gimbal, backlash_deg=0.0, resolution_deg=0.5))
    g2.step(1.0, 10.3, 45.0)
    check(
        "Upplosning: vinkeln kvantiseras till 0,5 grader",
        close((g2.az / 0.5) % 1.0, 0.0, 1e-9) or close((g2.az / 0.5) % 1.0, 1.0, 1e-9),
        f"fick {g2.az}",
    )
    sl = gimbal.scan_duration_s(17.5, 0.4)
    sw = gimbal.scan_duration_s(48.4, 0.4)
    check(
        "Smal strale tar minst 5x langre att svepa himlen",
        sl > 5.0 * sw,
        f"17,5 grader {sl:.0f} s vs 48,4 grader {sw:.0f} s",
    )

    # ------------------------------------------------------------------
    section("2. Scenarier — alla tre kor och ger rimliga utfall")
    sc_24 = load_scenario(SCENARIOS / "cansat_24.json")
    sc_gen = load_scenario(SCENARIOS / "generic_example.json")

    res_868 = run(sc_868, seed=1)
    res_24 = run(sc_24, seed=1)
    res_gen = run(sc_gen, seed=1)

    for label, res in (("868", res_868), ("2,4", res_24), ("generisk", res_gen)):
        check(
            f"{label}: fick en tidsserie",
            len(res.steps) > 100,
            f"{len(res.steps)} steg",
        )
        check(
            f"{label}: skickade paket",
            res.summary["packets_sent"] > 10,
            f"{res.summary['packets_sent']:.0f}",
        )

    check(
        "868: positiv marginal hela flygningen",
        res_868.summary["margin_min_db"] > 10.0,
        f"min {res_868.summary['margin_min_db']:.1f} dB",
    )
    check(
        "868: tappar i praktiken inga paket",
        res_868.summary["loss_fraction"] < 0.02,
        f"{res_868.summary['loss_fraction'] * 100:.1f} %",
    )
    check(
        "868: pekfel under 2 grader efter lasning",
        res_868.summary["pointing_error_locked_mean_deg"] < 2.0,
        f"medel {res_868.summary['pointing_error_locked_mean_deg']:.2f} grader",
    )
    check(
        "GPS-pekning racker aven for 2,4 GHz tolerans (5,1 grader)",
        res_868.summary["pointing_error_locked_mean_deg"]
        < res_24.summary["tolerance_1db_deg"],
        f"pekfel {res_868.summary['pointing_error_locked_mean_deg']:.2f} vs "
        f"tolerans {res_24.summary['tolerance_1db_deg']:.2f} grader",
    )
    check(
        "2,4: smalare strale an 868",
        res_24.summary["beamwidth_3db_deg"] < res_868.summary["beamwidth_3db_deg"],
    )
    check(
        "2,4: mindre tolerans an 868 (1 dB)",
        res_24.summary["tolerance_1db_deg"] < res_868.summary["tolerance_1db_deg"],
        f"{res_24.summary['tolerance_1db_deg']:.1f} vs "
        f"{res_868.summary['tolerance_1db_deg']:.1f} grader",
    )
    check(
        "2,4: hogre brusfaktor an 868 (samma pad, lagre LNA-vinst)",
        res_24.summary["noise_figure_db"] > res_868.summary["noise_figure_db"],
        f"{res_24.summary['noise_figure_db']:.2f} vs {res_868.summary['noise_figure_db']:.2f} dB",
    )
    check(
        "2,4: vegetation kostar mer an 868",
        res_24.summary["vegetation_max_db"] > res_868.summary["vegetation_max_db"],
        f"{res_24.summary['vegetation_max_db']:.1f} vs "
        f"{res_868.summary['vegetation_max_db']:.1f} dB",
    )
    check(
        "generisk: annat band an CanSat (433 MHz)",
        res_gen.constants["frequency_mhz"] == 433.0,
    )
    check(
        "generisk: rundstraalande antenn ger noll pekforlust",
        close(res_gen.summary["rx_gain_loss_max_db"], 0.0, 0.001),
        f"fick {res_gen.summary['rx_gain_loss_max_db']:.3f} dB",
    )
    check(
        "generisk: ingen vegetation i konfigurationen",
        close(res_gen.summary["vegetation_max_db"], 0.0, 1e-9),
    )

    # ------------------------------------------------------------------
    section("3. Deterministisk — samma seed ger samma resultat")
    a = run(sc_868, seed=7)
    b = run(sc_868, seed=7)
    check(
        "Tva korningar med samma seed ar identiska",
        to_frame(a).equals(to_frame(b)),
    )
    c = run(sc_868, seed=8)
    check(
        "Olika seed ger olika tidsserie",
        not to_frame(a).equals(to_frame(c)),
    )

    # ------------------------------------------------------------------
    section("4. Acquisition utan GPS — den smala stralen straffar sig")
    seeds = list(range(101, 121))
    start = time.perf_counter()

    keys = (
        "loss_fraction",
        "rx_gain_loss_mean_db",
        "lock_time_s",
        "margin_min_db",
    )

    def stats(scenario) -> dict[str, float]:
        runs = [run(scenario, seed=s) for s in seeds]
        out: dict[str, float] = {}
        for key in keys:
            values = [r.summary[key] for r in runs]
            usable = [v for v in values if v == v]  # filtrera bort nan
            out[key] = sum(usable) / len(usable) if usable else float("nan")
        return out

    s_868_gps = stats(sc_868)
    s_868_nogps = stats(replace(sc_868, tracker=replace(sc_868.tracker, gps_available=False)))
    s_24_gps = stats(sc_24)
    s_24_nogps = stats(replace(sc_24, tracker=replace(sc_24.tracker, gps_available=False)))
    elapsed = time.perf_counter() - start

    check(
        "Med GPS klarar bada scenarierna sig (<5 % forlust)",
        s_868_gps["loss_fraction"] < 0.05 and s_24_gps["loss_fraction"] < 0.05,
        f"868 {s_868_gps['loss_fraction'] * 100:.1f} %, "
        f"2,4 {s_24_gps['loss_fraction'] * 100:.1f} %",
    )
    check(
        "Utan GPS far bada storre pekforlust",
        s_868_nogps["rx_gain_loss_mean_db"] > s_868_gps["rx_gain_loss_mean_db"]
        and s_24_nogps["rx_gain_loss_mean_db"] > s_24_gps["rx_gain_loss_mean_db"],
    )
    check(
        "2,4 far storre pekforlust an 868 utan GPS",
        s_24_nogps["rx_gain_loss_mean_db"] > s_868_nogps["rx_gain_loss_mean_db"],
        f"2,4 {s_24_nogps['rx_gain_loss_mean_db']:.1f} dB vs "
        f"868 {s_868_nogps['rx_gain_loss_mean_db']:.1f} dB",
    )
    check(
        "Smal strale hittar sandaren senare an bred",
        s_24_nogps["lock_time_s"] > s_868_nogps["lock_time_s"],
        f"2,4 {s_24_nogps['lock_time_s']:.1f} s vs 868 {s_868_nogps['lock_time_s']:.1f} s",
    )

    print()
    print("  Medel over 20 seed:")
    print("    scenario            forlust   pekforlust   lasning   samsta marginal")
    for label, st in (
        ("868, GPS", s_868_gps),
        ("868, ingen GPS", s_868_nogps),
        ("2,4, GPS", s_24_gps),
        ("2,4, ingen GPS", s_24_nogps),
    ):
        print(
            f"    {label:<18} {st['loss_fraction'] * 100:6.1f} %"
            f" {st['rx_gain_loss_mean_db']:9.1f} dB"
            f" {st['lock_time_s']:8.1f} s"
            f" {st['margin_min_db']:8.1f} dB"
        )
    print(f"    ({len(seeds) * 4} korningar pa {elapsed:.1f} s)")

    # ------------------------------------------------------------------
    section("5. Konfigurationsfel fangas")
    try:
        load_scenario(HERE / "scenarios" / "finns-inte.json")
        check("Saknad fil ger fel", False)
    except ConfigError:
        check("Saknad fil ger ConfigError", True)

    bad = SCENARIOS / "_tmp_bad.json"
    bad.write_text('{"name": "x", "typo_falt": 1}', encoding="utf-8")
    try:
        load_scenario(bad)
        check("Okant falt ger fel", False)
    except ConfigError as exc:
        check("Okant falt ger ConfigError", "typo_falt" in str(exc), str(exc))
    finally:
        bad.unlink(missing_ok=True)

    check(
        "Stralbredd kan skattas ur forstarkningen",
        10.0 < estimate_beamwidth_deg(15.0) < 60.0,
        f"fick {estimate_beamwidth_deg(15.0):.1f} grader",
    )

    # ------------------------------------------------------------------
    total = time.perf_counter() - started
    print()
    print(f"=== {PASS} PASS, {FAIL} FAIL  ({total:.1f} s) ===")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
