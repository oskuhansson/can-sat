"""Självtester för simuleringen.

Körs med:

    python test_sim.py

Varje kontroll skriver PASS eller FAIL. Avslutar med exit-kod 1 om något fallerar,
så att den kan användas som grind i en pipeline.
"""

from __future__ import annotations

import math
import sys
import time
from dataclasses import replace
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sim import geometry, gimbal, linkbudget, modulation, propagation  # noqa: E402
from sim.antenna import (  # noqa: E402
    array_factor,
    array_peak_gain_dbi,
    estimate_beamwidth_deg,
    make_pattern,
)
from sim.config import ConfigError, load_scenario  # noqa: E402
from sim.engine import run  # noqa: E402
from sim.report import to_frame  # noqa: E402
from sim.tracker import covering_raster, raster_coverage  # noqa: E402

# Samma skael som i run.py: pipeas utskriften blir a/a/o mojibake pa Windows om
# vi inte tvingar UTF-8. En riktig konsol lamnas orord.
if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

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

    # Lufttid: 20 byte vid SF9/125 kHz tar 185,3 ms (AN1200.13).
    airtime = modulation.airtime_s(9, 125.0, 20)
    check(
        "Lufttid SF9/125 kHz, 20 byte = 185 ms",
        close(airtime, 0.1853, 0.005),
        f"fick {airtime * 1000:.1f} ms",
    )
    # Regression: header-termen var inverterad (IH = 1 betyder *implicit* header,
    # sa explicit header ska inte dra av 20). Felet syntes bara dar ceil()
    # passerade en grans — SF9 var oberord, SF7 och SF8 var 10 % for korta.
    # Referensvarden fran EpiSensors AN1200.13-kalkylator, 20 byte, CRC pa.
    for sf, ref_ms in ((7, 56.58), (8, 102.9), (12, 1318.9)):
        got = modulation.airtime_s(sf, 125.0, 20)
        check(
            f"Lufttid SF{sf}/125 kHz, 20 byte = {ref_ms:.1f} ms",
            close(got * 1000.0, ref_ms, 0.5),
            f"fick {got * 1000:.1f} ms",
        )
    check(
        "Lufttid ar monoton i SF",
        all(
            modulation.airtime_s(sf, 125.0, 20) < modulation.airtime_s(sf + 1, 125.0, 20)
            for sf in (7, 8, 9, 10, 11)
        ),
        "okar inte med SF",
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
    section("6. Plan fasstyrd array — fysik, svepning och bakatskompatibilitet")

    sc_arr = load_scenario(SCENARIOS / "cansat_24_array.json")
    pat_arr = make_pattern(sc_arr.antenna)

    # 6a. Toppforstarkning: koherent summering ger 10log10(N), inte 20log10(N).
    check(
        "array: 2x2 ger +6,02 dB over elementet",
        close(array_peak_gain_dbi(10.0, 2, 2) - 10.0, 6.02, 0.01),
        f"fick {array_peak_gain_dbi(10.0, 2, 2) - 10.0:.2f} dB",
    )
    check(
        "array: 4x4 ger +12,04 dB over elementet",
        close(array_peak_gain_dbi(10.0, 4, 4) - 10.0, 12.04, 0.01),
        f"fick {array_peak_gain_dbi(10.0, 4, 4) - 10.0:.2f} dB",
    )
    check(
        "array: 1x1 ar elementet sjalvt",
        close(array_peak_gain_dbi(10.0, 1, 1), 10.0, 1e-9),
    )

    # 6b. Arrayfaktorn ska vara exakt 1 i styrriktningen.
    check(
        "array: AF = 1 i styrriktningen",
        close(array_factor(2, 2, 0.5, 0.0, 0.0, 0.0, 0.0, 4), 1.0, 1e-9),
        f"fick {array_factor(2, 2, 0.5, 0.0, 0.0, 0.0, 0.0, 4):.6f}",
    )
    check(
        "array: AF ar ocksa 1 utan fasfoenkantisering",
        close(array_factor(2, 2, 0.5, 0.0, 0.0, 0.0, 0.0, None), 1.0, 1e-9),
    )

    # 6c. Moenstret ska ga via 2D-vagen, men bara arrayen.
    check("array: 2D-vagen ar aktiv", pat_arr.is_2d)
    check("yagi: 2D-vagen ar INTE aktiv", not pattern.is_2d)
    check(
        "array: toppforstarkning = scenariots peak_gain_dbi",
        close(
            pat_arr.gain_towards(0.0, 90.0, 0.0, 90.0),
            sc_arr.antenna.peak_gain_dbi,
            0.01,
        ),
        f"fick {pat_arr.gain_towards(0.0, 90.0, 0.0, 90.0):.2f} dBi",
    )
    check(
        "array: straalbredden raeknas fram ur moenstret",
        10.0 < pat_arr.beamwidth_3db_deg < 60.0,
        f"fick {pat_arr.beamwidth_3db_deg:.1f} grader",
    )

    # 6d. Grating lobes: en extra lob hamnar innanfor den synliga regionen
    #     sa fort elementavstandet overstiger en halv vaglaengd.
    def peak_outside_mainlobe(nx: int, ny: int, d: float, u0: float, bits=None) -> float:
        worst = 0.0
        steps = 3000
        for i in range(steps + 1):
            u = 0.55 + (1.0 - 0.55) * i / steps
            worst = max(worst, array_factor(nx, ny, d, u, 0.0, u0, 0.0, bits))
        return worst

    grating_1 = peak_outside_mainlobe(4, 4, 1.0, 0.0)
    grating_half = peak_outside_mainlobe(4, 4, 0.5, 0.0)
    check(
        "array: grating lobe vid spacing 1,0",
        grating_1 > 0.9,
        f"hogsta AF utanfor huvudloben {grating_1:.3f}",
    )
    check(
        "array: ingen grating lobe vid spacing 0,5",
        grating_half < 0.4,
        f"hogsta AF utanfor huvudloben {grating_half:.3f}",
    )

    # 6e. Fasfoenkantisering. Tva saker galler, och en galler INTE:
    #     * toppforstarkningen tappar naestan inget (4 bit ~0,03 dB vid styrning
    #       bort fran bredsidan; exakt mot bredsidan ar styrfasen redan 0)
    #     * de ideala nollorna fylls igen — dar syns kvantiseringen tydligt
    #     * toppsidoloben hojs daremot INTE for en 4x4-array, for den uniforma
    #       belysningens egen sidolob ligger redan hogre an kvantiseringens.
    #       Den sitter pa -11,30 dB, vilket verifieras mot den analytiska
    #       formeln nedan i stallet for mot ett handplockat tal.
    ideal_peak = array_factor(4, 4, 0.5, 0.3, 0.0, 0.3, 0.0, None)
    q4_peak = array_factor(4, 4, 0.5, 0.3, 0.0, 0.3, 0.0, 4)
    q4_loss_db = 20.0 * math.log10(q4_peak / ideal_peak)
    check(
        "array: 4 bit kostar under 0,1 dB topp",
        abs(q4_loss_db) < 0.1,
        f"fick {q4_loss_db:+.4f} dB",
    )

    null_u = 0.3 + 0.5  # ideal nolla: 2*(u-u0) = 1
    null_ideal = array_factor(4, 4, 0.5, null_u, 0.0, 0.3, 0.0, None)
    null_q4 = array_factor(4, 4, 0.5, null_u, 0.0, 0.3, 0.0, 4)
    check(
        "array: kvantiseringen fyller de ideala nollorna",
        null_ideal < 1e-6 and null_q4 > 1e-3,
        f"ideal {20 * math.log10(max(null_ideal, 1e-12)):.0f} dB, "
        f"4 bit {20 * math.log10(max(null_q4, 1e-12)):.1f} dB",
    )
    q3_peak = array_factor(4, 4, 0.5, 0.3, 0.0, 0.3, 0.0, 3)
    check(
        "array: 3 bit tappar mer topp an 4 bit",
        20.0 * math.log10(q3_peak / ideal_peak) < q4_loss_db,
        f"3 bit {20 * math.log10(q3_peak / ideal_peak):+.3f} dB mot "
        f"4 bit {q4_loss_db:+.3f} dB",
    )

    # Toppsidoloben: den sitter pa v=0 eftersom faktorn aer separabel
    # (AF(u,v) = AFx(u)*AFy(v)), sa en scan langs u raecker — och en 2D-scan kan
    # aldrig ge hogre an 1D-sidoloben. Jaemfoer mot den analytiska formeln
    # |sin(N*pi*d*u)/(N*sin(pi*d*u))|, inte mot ett tal ur luften: en tidigare
    # version av rapporten angav -5,6 dB, vilket aer fel.
    def _ref_1d(n: int, d: float, u: float) -> float:
        psi = math.pi * d * u
        if abs(math.sin(psi)) < 1e-12:
            return 1.0
        return abs(math.sin(n * psi) / (n * math.sin(psi)))

    best_af, best_u = 0.0, 0.0
    for k in range(201):
        u = -1.0 + 2.0 * k / 200.0
        if abs(u) < 0.5:
            continue  # innanfor huvudloben (forsta nollan vid |u| = 0,5)
        af = array_factor(4, 4, 0.5, u, 0.0, 0.0, 0.0)
        if af > best_af:
            best_af, best_u = af, u
    ref_af = max(_ref_1d(4, 0.5, 0.5 + 0.5 * k / 20000.0) for k in range(20001))
    check(
        "array: toppsidoloben matchar analytisk (-11,3 dB)",
        abs(best_af - ref_af) < 2e-3,
        f"modell {20 * math.log10(best_af):.2f} dB vid u={best_u:.2f}, "
        f"analytisk {20 * math.log10(ref_af):.2f} dB",
    )

    # 6f. Elektronisk svepning. Utan GPS ar acquisitionen det som avgor allt.
    arr_seeds = list(range(201, 209))

    def arr_stats(scenario) -> dict[str, float]:
        runs = [run(scenario, seed=s) for s in arr_seeds]
        out: dict[str, float] = {}
        for key in ("lock_time_s", "rx_gain_loss_mean_db", "loss_fraction", "scan_time_s"):
            values = [r.summary[key] for r in runs]
            usable = [v for v in values if v == v]
            out[key] = sum(usable) / len(usable) if usable else float("nan")
        return out

    nogps = replace(sc_arr, tracker=replace(sc_arr.tracker, gps_available=False))
    s_arr_el = arr_stats(nogps)
    s_arr_mech = arr_stats(replace(nogps, tracker=replace(nogps.tracker, scan_mode="mechanical")))
    s_arr_sim = arr_stats(
        replace(nogps, tracker=replace(nogps.tracker, simultaneous_beams=True))
    )

    check(
        "array: elektronisk svepning laser minst 3x snabbare an mekanisk",
        s_arr_el["lock_time_s"] * 3.0 < s_arr_mech["lock_time_s"],
        f"elektronisk {s_arr_el['lock_time_s']:.2f} s mot "
        f"mekanisk {s_arr_mech['lock_time_s']:.2f} s",
    )
    check(
        "array: elektronisk svepning ger mindre pekforlust an mekanisk",
        s_arr_el["rx_gain_loss_mean_db"] < s_arr_mech["rx_gain_loss_mean_db"],
        f"{s_arr_el['rx_gain_loss_mean_db']:.2f} mot "
        f"{s_arr_mech['rx_gain_loss_mean_db']:.2f} dB",
    )
    check(
        "array: simultana stralar ger lasningstid 0",
        close(s_arr_sim["lock_time_s"], 0.0, 1e-9),
        f"fick {s_arr_sim['lock_time_s']:.2f} s",
    )
    check(
        "array: elektroniskt svep ar kortare an mekaniskt",
        s_arr_el["scan_time_s"] < s_arr_mech["scan_time_s"] / 5.0,
        f"{s_arr_el['scan_time_s']:.1f} s mot {s_arr_mech['scan_time_s']:.1f} s",
    )

    print()
    print("  Fasstyrd 2x2-array kontra 2,4 GHz-yagin (samma band, samma toppvinst)")
    print("  (bada pekar raett — skillnaden aer moenstret, inte pekfelet):")
    print("    elevation     array      yagi   skillnad")
    pat_24 = make_pattern(sc_24.antenna)
    for el in (90, 60, 30, 15, 10, 5):
        ga = pat_arr.gain_towards(0.0, el, 0.0, el)
        gy = pat_24.gain_towards(0.0, el, 0.0, el)
        print(f"    {el:6d}     {ga:6.2f}    {gy:6.2f}    {ga - gy:+7.2f} dB")

    print()
    print("  2,4 GHz-arrayen utan GPS, medel oever 8 seed:")
    print("    svepning        lasning   pekforlust   forlust    svep")
    for label, st in (
        ("mekanisk", s_arr_mech),
        ("elektronisk", s_arr_el),
        ("simultana", s_arr_sim),
    ):
        print(
            f"    {label:<12} {st['lock_time_s']:7.2f} s"
            f" {st['rx_gain_loss_mean_db']:9.2f} dB"
            f" {st['loss_fraction'] * 100:8.1f} %"
            f" {st['scan_time_s']:7.1f} s"
        )

    # 6g. Bakatskompatibilitet for de tre ursprungliga scenarierna.
    #
    #     Tva av vardena har andrats med flit, och det ar en rattelse, inte en
    #     regression: lasningen jamfors nu med den **faktiska** gimbalriktningen
    #     och kraver en dwell i positionen. Tidigare jamfordes den med den
    #     *kommenderade* sveppositionen, sa gimbalen kunde "lasa" pa en riktning
    #     den annu inte hunnit fram till — 3,2 s var tiden da *kommandot* nadde
    #     zenit, inte da antennen gjorde det. Med 30 grader/s tar svepet fran
    #     el=0 till el=90 tre sekunder extra, och en dwell tillkommer.
    check(
        "bakatskompatibilitet: 868 med GPS ger 2,0 s",
        close(s_868_gps["lock_time_s"], 2.0, 0.05),
        f"fick {s_868_gps['lock_time_s']:.2f} s",
    )
    check(
        "bakatskompatibilitet: 868 utan GPS ger 5,8 s (gimbalens sveptid inraknad)",
        close(s_868_nogps["lock_time_s"], 5.8, 0.1),
        f"fick {s_868_nogps['lock_time_s']:.2f} s",
    )
    check(
        "bakatskompatibilitet: 2,4 utan GPS ger 35,4 s (gimbalens sveptid inraknad)",
        close(s_24_nogps["lock_time_s"], 35.4, 0.1),
        f"fick {s_24_nogps['lock_time_s']:.2f} s",
    )
    _dwell_868 = run(load_scenario("scenarios/cansat_868.json"), 1).summary["scan_dwell_s"]
    check(
        "bakatskompatibilitet: lasningstiden ar minst en dwell",
        s_868_nogps["lock_time_s"] >= _dwell_868 - 1e-9,
        f"lasning {s_868_nogps['lock_time_s']:.2f} s, dwell {_dwell_868:.2f} s",
    )
    check(
        "bakatskompatibilitet: 868 tappar inga paket (marginalen aeter attityden)",
        s_868_gps["loss_fraction"] < 0.02 and s_868_nogps["loss_fraction"] < 0.02,
        f"868 GPS {100 * s_868_gps['loss_fraction']:.2f} %, "
        f"utan {100 * s_868_nogps['loss_fraction']:.2f} %",
    )
    # Med attitydmodellen pa plats ar detta inte langre sant for 2,4 GHz, och det
    # ar en av de viktigaste upptackterna: nar stationen star nastan rakt under
    # burken ar monopolen i sin nolla (-14,9 dB) OCH den inkommande vagens E-
    # vektor horisontell, sa en vertikal yagi som pekar at horisonten ar
    # korspolariserad mot den (-14,9 dB till). Tillsammans ~-30 dB i apogeum.
    check(
        "attityd: 2,4 GHz-yagin tappar paket i apogeum (nolla + korspolarisation)",
        s_24_nogps["loss_fraction"] > 0.05,
        f"forlust {100 * s_24_nogps['loss_fraction']:.1f} %",
    )

    # 7. Hybrid — array PA gimbal
    # ------------------------------------------------------------------
    print()
    print("7. Hybrid — array pa gimbal, gimbalen grovpekar och arrayen finjusterar")

    from sim.antenna import make_pattern as _mk  # noqa: PLC0415
    from sim.config import AntennaConfig as _AC  # noqa: PLC0415

    hyb_cfg = load_scenario("scenarios/cansat_24_hybrid.json").antenna
    hyb_pat = _mk(hyb_cfg)
    arr_pat = _mk(load_scenario("scenarios/cansat_24_array.json").antenna)

    # 2x2 med 8 dBi-patch: 8 + 10log10(4) = 14,02 dBi. Inte yagins 17,8 — den
    # ska fortjanas, inte antas.
    check(
        "hybrid: topp = element + 10log10(N) = 14,02 dBi",
        close(hyb_pat.peak_gain_dbi, 8.0 + 10.0 * math.log10(4), 0.01),
        f"fick {hyb_pat.peak_gain_dbi:.2f} dBi",
    )
    try:
        _AC.from_dict(
            {
                "model": "hybrid",
                "array_nx": 2,
                "array_ny": 2,
                "spacing_lambda": 0.5,
                "peak_gain_dbi": 17.8,
            }
        )
        rejected = False
    except ConfigError:
        rejected = True
    check("hybrid: avvisar en peak_gain_dbi som inte stammer med elementet", rejected)

    # Med gimbalen riktad mot malet ska forstarkningen vara toppen vid ALLA
    # elevationer. Det ar precis vad en array utan gimbal inte klarar.
    for el in (5.0, 30.0, 90.0):
        g = hyb_pat.gain_towards(0.0, el, 0.0, el)
        check(
            f"hybrid: {el:.0f} graders elevation ger toppforstarkning",
            close(g, hyb_pat.peak_gain_dbi, 0.05),
            f"fick {g:.2f} dBi",
        )

    a5 = arr_pat.gain_towards(0.0, 5.0, 0.0, 5.0)
    h5 = hyb_pat.gain_towards(0.0, 5.0, 0.0, 5.0)
    check(
        "array utan gimbal faller vid 5 graders elevation",
        a5 < 1.0,
        f"fick {a5:.2f} dBi",
    )
    check(
        "hybrid vinner minst 12 dB over array utan gimbal vid 5 grader",
        h5 - a5 > 12.0,
        f"skillnad {h5 - a5:.1f} dB",
    )

    # Utanfor konen: gimbalen 60 grader fel, arrayen kan bara styra 45. Da star
    # elementet 60 grader fran bredsidan = 12*(60/65)^2 = 10,22 dB, PLUS det
    # kvarvarande pekfelet pa 15 grader i arrayfaktorn.
    #
    # Det har testet befaste tidigare en bugg: elementet utvarderades vid den
    # KLAMDA vinkeln (45 grader) i stallet for vid observationsvinkeln (60), sa
    # forlusten blev 5,9 dB i stallet for 10,4. Ett mal 90 grader bort fick da
    # nastan samma forstarkning som ett pa 45 — hybriden blev orealistiskt bra.
    g60 = hyb_pat.gain_towards(0.0, 0.0, 0.0, 60.0)
    loss60 = hyb_pat.peak_gain_dbi - g60
    check(
        "hybrid: 60 graders fel kostar ~10,4 dB (elementet vid 60, inte 45)",
        close(loss60, 10.37, 0.25),
        f"fick {loss60:.2f} dB",
    )
    # Och det ska rasa vidare utat: ett mal 90 grader fran bredsidan far INTE ha
    # samma forstarkning som ett pa 45.
    g45 = hyb_pat.gain_towards(0.0, 45.0, 0.0, 0.0)
    g90 = hyb_pat.gain_towards(0.0, 90.0, 0.0, 0.0)
    check(
        "hybrid: 90 graders fel ar minst 15 dB samre an 45 graders",
        g45 - g90 > 15.0,
        f"45 grader {g45:.2f} dBi, 90 grader {g90:.2f} dBi, skillnad {g45 - g90:.2f} dB",
    )
    check(
        "hybrid: elementforlusten vid 90 grader ar storre an 20 dB",
        hyb_pat.peak_gain_dbi - g90 > 20.0,
        f"fick {hyb_pat.peak_gain_dbi - g90:.2f} dB",
    )
    # Utan kommando styr arrayen mot malet. Med ett kommando som inte ar malet
    # (svepning) ska pekforlusten bli storre — annars ar arrayen ett orakel som
    # pekar ratt innan den hittat nagot.
    g_steered = hyb_pat.gain_towards(0.0, 30.0, 0.0, 0.0, 0.0, 30.0)
    g_sweeping = hyb_pat.gain_towards(0.0, 30.0, 0.0, 0.0, 0.0, 0.0)
    check(
        "hybrid: kommando skilt fran mal ger storre pekforlust (inget orakel)",
        g_sweeping < g_steered - 1.0,
        f"styrd {g_steered:.2f} dBi, svepande {g_sweeping:.2f} dBi",
    )
    check(
        "hybrid: ar 2D (tva riktningar kravs)",
        hyb_pat.is_2d,
    )
    check(
        "array: straalbredden ar full bredd, inte halva",
        40.0 < arr_pat.beamwidth_3db_deg < 55.0,
        f"fick {arr_pat.beamwidth_3db_deg:.1f} grader",
    )

    # Langre fram i flygningen: bada kan peka, men elementet sitter olika nara
    # sin bredsida. Det ar hela skillnaden. Vid 5 graders elevation star
    # elementet 85 grader fran bredsidan, sa array-only tappar 12*(85/65)^2 =
    # 20,5 dB av sitt 8 dBi — den hamnar under 0 dBi trots att den pekar ratt.
    expected_a5 = 8.0 + 10.0 * math.log10(4) - 12.0 * (85.0 / 65.0) ** 2
    check(
        "array utan gimbal vid 5 grader: elementet 85 grader fran bredsidan",
        close(a5, expected_a5, 0.3),
        f"fick {a5:.2f} dBi, formeln ger {expected_a5:.2f} dBi",
    )

    # SX1280:s bandbreddstrappa ar inte 3 dB per dubblering: databladet ger 4 dB
    # for 203 -> 812 kHz, inte 6.
    check(
        "SX1280 SF9/203 kHz = -121 dBm",
        close(modulation.sensitivity_dbm(9, 203.0, 2400.0), -121.0, 0.1),
        f"fick {modulation.sensitivity_dbm(9, 203.0, 2400.0):.1f}",
    )
    check(
        "SX1280 SF9/812 kHz = -117 dBm (databladet, inte -123)",
        close(modulation.sensitivity_dbm(9, 812.0, 2400.0), -117.0, 0.1),
        f"fick {modulation.sensitivity_dbm(9, 812.0, 2400.0):.1f}",
    )
    check(
        "lufttid SF9/812 kHz, 20 byte = 28,5 ms",
        close(modulation.airtime_s(9, 812.0, 20), 0.0285, 0.001),
        f"fick {modulation.airtime_s(9, 812.0, 20) * 1000:.1f} ms",
    )

    # Utan GPS: hybriden laser nastan direkt, yagin sveper i nastan en minut.
    hyb_scn = load_scenario("scenarios/cansat_24_hybrid.json")
    hyb_nogps = replace(hyb_scn, tracker=replace(hyb_scn.tracker, gps_available=False))
    h_sum = run(hyb_nogps, hyb_scn.seed).summary
    check(
        "hybrid: laser utan GPS pa under 1 s",
        h_sum["lock_time_s"] < 1.0,
        f"fick {h_sum['lock_time_s']:.2f} s",
    )
    check(
        "hybrid: haller sig inom sin elektroniska kon",
        h_sum["outside_scan_fraction"] < 0.05,
        f"fick {100 * h_sum['outside_scan_fraction']:.1f} %",
    )
    # Lasningstiden far inte vara en artefakt av tidssteget: konen kan ta ett
    # tag att svepa igenom, och innan den gjort det ar sandaren inte hittad.
    check(
        "hybrid: lasningstiden ar minst en dwell (inte 0,00 s)",
        h_sum["lock_time_s"] >= h_sum["scan_dwell_s"] - 1e-9 > 0.0,
        f"lasning {h_sum['lock_time_s']:.3f} s, dwell {h_sum['scan_dwell_s']:.3f} s",
    )

    # Rastret far inte lamna en sandare oatkomlig, oavsett max_scan. Den gamla
    # konstruktionen (jamt utspridda rader mellan 0 och 90) lamnade 12-47 % av
    # himlen otackt och da hittades aldrig en sandare i de riktningarna.
    for ms in (15.0, 30.0, 45.0, 60.0):
        ras = covering_raster(ms)
        cov = raster_coverage(ras, ms)
        check(
            f"hybrid: rastret tacker himlen vid max_scan {ms:.0f} grader",
            cov >= 0.95,
            f"fick {100 * cov:.2f} % med {len(ras)} positioner",
        )

    # Parkeringsartefakten. I en tidigare version tvingades yagin svepa fran
    # horisonten trots att den stod parkerad i uppskjutningsriktningen, och
    # hybridens fordel i samsta marginal blev ~15 dB av det skalet allena. Med
    # parkera-och-hall krymper gapet till några dB — det ar den arliga siffran.
    y_scn = load_scenario("scenarios/cansat_24.json")
    y_free = run(y_scn, y_scn.seed).summary["margin_min_db"]
    y_park = run(
        replace(y_scn, tracker=replace(y_scn.tracker, park_and_hold=True)),
        y_scn.seed,
    ).summary["margin_min_db"]
    check(
        "yagi: parkera-och-hall forbedrar samsta marginalen markant",
        y_park - y_free > 5.0,
        f"utan parkering {y_free:.1f} dB, med {y_park:.1f} dB",
    )
    def _mean_margin_min(scn, n=5) -> float:
        vals = [run(scn, s).summary["margin_min_db"] for s in range(1, n + 1)]
        return sum(vals) / len(vals)

    y_park_avg = _mean_margin_min(
        replace(y_scn, tracker=replace(y_scn.tracker, park_and_hold=True))
    )
    h_park_avg = _mean_margin_min(
        replace(hyb_scn, tracker=replace(hyb_scn.tracker, park_and_hold=True))
    )
    check(
        "hybridens fordel mot yagin ar under 5 dB med parkering (ingen artefakt)",
        h_park_avg - y_park_avg < 5.0,
        f"hybrid {h_park_avg:.1f} dB, yagi {y_park_avg:.1f} dB, "
        f"gap {h_park_avg - y_park_avg:.1f} dB",
    )

    # 8. Burkens attityd — monopolen har noll mot bade zenit och nadir
    print()
    print("8. Burkens attityd — monopolen har noll mot bade zenit och nadir")

    from sim import attitude as _att  # noqa: PLC0415
    from sim.config import AttitudeConfig as _AtC  # noqa: PLC0415

    # Kontrollsumma: elevation 79,7 grader fran stationen ger theta = 169,7 och
    # -14,9 dB. Det ar den siffra uppdraget angav, och den ska modellen reproducera.
    _to_st = _att.unit_from_az_el(0.0, -79.7)
    _axis = _att.axis_vector(0.0, _AtC())
    _loss = _att.pattern_loss_db(_axis, _to_st, -20.0)
    check(
        "attityd: apogeum (elev 79,7) kostar -14,9 dB",
        close(_loss, -14.95, 0.15),
        f"fick {_loss:.2f} dB",
    )
    # Nollan sitter pa BADA sidor om axeln: rakt uppifran och rakt nedifran.
    check(
        "attityd: nollan ar symmetrisk (zenit och nadir ger samma forlust)",
        close(
            _att.pattern_loss_db((0.0, 0.0, 1.0), (0.0, 0.0, 1.0), -20.0),
            _att.pattern_loss_db((0.0, 0.0, 1.0), (0.0, 0.0, -1.0), -20.0),
            1e-9,
        ),
        "olika forlust mot zenit och nadir",
    )
    check(
        "attityd: nollan klipps vid floor_db",
        close(_att.pattern_loss_db((0.0, 0.0, 1.0), (0.0, 0.0, 1.0), -20.0), -20.0, 1e-9),
        "klipptes inte",
    )
    # I horisonten (theta = 90) ar sin^2 = 1 och forlusten noll.
    check(
        "attityd: horisonten kostar inget",
        close(_att.pattern_loss_db((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), -20.0), 0.0, 1e-9),
        "forlust i horisonten",
    )

    # Polarisationen: en vertikal monopol mot en vertikalt polariserad yagi som
    # pekar at samma hall ska ge ~0 dB. Satte man E = axeln i stallet for
    # tvarkomponenten blev det ~-15 dB har, vilket dubbelraknade nollan.
    _pol = _att.polarization_loss_db(_axis, _to_st, 0.0, 79.7, _AtC())
    check(
        "attityd: vertikal monopol mot vertikal yagi ger ~0 dB polarisation",
        close(_pol, 0.0, 0.6),
        f"fick {_pol:.2f} dB",
    )
    check(
        "attityd: polarisationsforlusten ar aldrig positiv",
        all(
            _att.polarization_loss_db(_axis, _to_st, az, el, _AtC()) <= 1e-9
            for az in (0.0, 90.0, 180.0)
            for el in (10.0, 45.0, 80.0)
        ),
        "positiv forlust",
    )

    # Tre scenarier: stillastaende, snall pendling, varsta fall.
    _att_cases = {}
    for _f, _lab in (
        ("cansat_24_hybrid_att_still", "still"),
        ("cansat_24_hybrid_att_gentle", "snall"),
        ("cansat_24_hybrid_att_worst", "varst"),
    ):
        _scn = load_scenario(f"scenarios/{_f}.json")
        _rs = [run(_scn, s) for s in range(1, 6)]
        _att_cases[_lab] = {
            "att_mean": sum(x.summary["can_attitude_loss_mean_db"] for x in _rs) / len(_rs),
            "att_max": sum(x.summary["can_attitude_loss_max_db"] for x in _rs) / len(_rs),
            "pol_mean": sum(x.summary["polarization_loss_mean_db"] for x in _rs) / len(_rs),
            "m_min": sum(x.summary["margin_min_db"] for x in _rs) / len(_rs),
            "loss": sum(x.summary["loss_fraction"] for x in _rs) / len(_rs),
        }
        check(
            f"attityd: {_lab} kor och tapper inga paket",
            _att_cases[_lab]["loss"] < 0.02,
            f"forlust {100 * _att_cases[_lab]['loss']:.2f} %",
        )
    # Pendlingen gor saken varre i *djupaste* ogonblick (axeln kan passera
    # narmare exakt nadir an den statiska vertikalen, som ar last vid 169,7
    # grader) men battre i *medel*, eftersom axeln da bara ar i nollan en del av
    # tiden. Bada riktningarna ska halla.
    check(
        "attityd: pendlingen nar djupare an stillastaende i samsta ogonblick",
        _att_cases["varst"]["att_max"] > _att_cases["still"]["att_max"] + 1.0,
        f"still {_att_cases['still']['att_max']:.1f} dB mot "
        f"varst {_att_cases['varst']['att_max']:.1f} dB",
    )
    check(
        "attityd: stillastaende kostar mer i medel an pendling",
        _att_cases["still"]["att_mean"] > _att_cases["varst"]["att_mean"] + 0.5,
        f"still {_att_cases['still']['att_mean']:.2f} dB mot "
        f"varst {_att_cases['varst']['att_mean']:.2f} dB",
    )
    check(
        "attityd: pendling kostar mer i polarisation an stillastaende",
        _att_cases["varst"]["pol_mean"] > _att_cases["still"]["pol_mean"] + 1.0,
        f"still {_att_cases['still']['pol_mean']:.2f} dB mot "
        f"varst {_att_cases['varst']['pol_mean']:.2f} dB",
    )
    print()
    print("  Burkens attityd, medel over 5 seed (dB forlust):")
    print(f"    {'scenario':10s} {'attityd':>16s} {'polarisation':>14s} {'samsta marginal':>16s}")
    for _lab, _d in _att_cases.items():
        print(
            f"    {_lab:10s} {_d['att_mean']:7.2f}/{_d['att_max']:<7.2f}"
            f" {_d['pol_mean']:>13.2f} {_d['m_min']:>15.1f}"
        )

    # ------------------------------------------------------------------
    total = time.perf_counter() - started
    print()
    print(f"=== {PASS} PASS, {FAIL} FAIL  ({total:.1f} s) ===")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
