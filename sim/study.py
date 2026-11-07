"""Parameterstudie for hybridarkitekturen.

Tre undersokningar, alla med samma bana och samma radiofront som
scenarios/cansat_24_hybrid.json:

1. Arkitektur x fasvaexlarens dampning — LNA per element fore FV, eller en enda
   LNA efter kombiner. Bada med typ-IL (2,5 dB) och max-IL (4,5 dB), for en
   budget ska klara max och inte typ.
2. max_scan_deg x element_gain_dbi x gimbalhastighet. Utan GPS, eftersom det ar
   da forvarvstiden och scanforlusten faktiskt spelar roll.
3. Forstarkning vid 5, 30 och 90 graders elevation for de tre arkitekturerna.

Kor:  python study.py [--seeds N] [--out DIR]
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sim.antenna import make_pattern  # noqa: E402
from sim.config import Stage, load_scenario  # noqa: E402
from sim.engine import run  # noqa: E402

BASE = HERE / "scenarios" / "cansat_24_hybrid.json"
YAGI = HERE / "scenarios" / "cansat_24.json"
ARRAY_ONLY = HERE / "scenarios" / "cansat_24_array.json"

# Fasvaexlarens infogade dampning: typ och max ur MACOM MAPS-010144 rev V3.
FV_IL_TYP = 2.5
FV_IL_MAX = 4.5
KOMBINER_EXCESS = 1.0


def stage(name: str, gain_db: float) -> Stage:
    """En forlustkalla: dampning och brusfaktor ar samma tal i dB."""
    return Stage(name=name, gain_db=-gain_db, noise_figure_db=gain_db)


def rx_chain(architecture: str, fv_il: float) -> tuple[Stage, ...]:
    """Mottagarkedjan i den ordning komponenterna sitter."""
    ufl = Stage(name="U.FL", gain_db=-0.2, noise_figure_db=0.2)
    lna = Stage(name="LNA TQP3M9037", gain_db=19.1, noise_figure_db=0.43)
    fv = stage(f"FV MAPS-010144 ({fv_il:.1f} dB)", fv_il)
    comb = stage("Kombiner (excess)", KOMBINER_EXCESS)
    coax = stage("LMR-400 10 m", 2.2)
    pad = stage("10 dB pad", 10.0)

    if architecture == "A":
        # LNA per element FORE fasvaexlaren.
        return (ufl, lna, fv, comb, coax, pad)
    # B: FV och kombiner fore en enda LNA vid mottagaren.
    return (ufl, fv, comb, lna, coax, pad)


def averaged(scenario, seeds: int) -> dict:
    """Medel over `seeds` korningar."""
    keys = (
        "lock_time_s",
        "pointing_error_locked_mean_deg",
        "loss_fraction",
        "margin_min_db",
        "margin_mean_db",
        "outside_scan_fraction",
        "scan_loss_mean_db",
        "scan_loss_max_db",
        "noise_figure_db",
        "sensitivity_dbm",
    )
    totals = {k: 0.0 for k in keys}
    # Sämsta marginal EFTER låsning. Utan det jämförs yagins acquisition (där
    # den sveper förbi hela himlen och kan peka 90 grader fel) med hybridens
    # steady state, och då ser hybriden orimligt bra ut av fel anledning.
    # Medelvärdet över låsta steg är den robusta siffran: minimum fångar enstaka
    # transienter, och en smal lob straffas hårdare av dem än en bred — vilket är
    # sant men inte samma sak som steady state.
    locked_minima: list[float] = []
    locked_means: list[float] = []

    for i in range(seeds):
        res = run(scenario, scenario.seed + i)
        s = res.summary
        for k in keys:
            v = s.get(k, float("nan"))
            totals[k] += 0.0 if (isinstance(v, float) and math.isnan(v)) else float(v)
        locked = [st.margin_db for st in res.steps if st.phase != "acquire"]
        if locked:
            locked_minima.append(min(locked))
            locked_means.append(sum(locked) / len(locked))

    out = {k: v / seeds for k, v in totals.items()}
    out["margin_locked_min_db"] = (
        sum(locked_minima) / len(locked_minima) if locked_minima else float("nan")
    )
    out["margin_locked_mean_db"] = (
        sum(locked_means) / len(locked_means) if locked_means else float("nan")
    )
    return out


def study_architecture(base, seeds: int) -> list[dict]:
    rows = []
    for arch in ("A", "B"):
        for fv_il in (FV_IL_TYP, FV_IL_MAX):
            scn = replace(base, radio=replace(base.radio, rx_stages=rx_chain(arch, fv_il)))
            m = averaged(scn, seeds)
            rows.append(
                {
                    "arkitektur": "LNA per element" if arch == "A" else "FV fore LNA",
                    "fv_il_db": fv_il,
                    "nf_db": m["noise_figure_db"],
                    "sensitivity_dbm": m["sensitivity_dbm"],
                    "margin_min_db": m["margin_min_db"],
                    "loss_pct": 100.0 * m["loss_fraction"],
                }
            )
    return rows


def study_scan(base, seeds: int) -> list[dict]:
    rows = []
    ngain = base.antenna.array_nx * base.antenna.array_ny
    nogps = replace(base, tracker=replace(base.tracker, gps_available=False))
    for max_scan in (15.0, 30.0, 45.0, 60.0):
        for elem in (8.0, 9.0, 10.0, 11.0):
            for speed in (10.0, 30.0, 60.0):
                ant = replace(
                    nogps.antenna,
                    max_scan_deg=max_scan,
                    element_gain_dbi=elem,
                    peak_gain_dbi=elem + 10.0 * math.log10(ngain),
                )
                scn = replace(
                    nogps,
                    antenna=ant,
                    gimbal=replace(
                        nogps.gimbal,
                        az_slew_deg_per_s=speed,
                        el_slew_deg_per_s=speed,
                    ),
                )
                m = averaged(scn, seeds)
                rows.append(
                    {
                        "max_scan_deg": max_scan,
                        "element_gain_dbi": elem,
                        "gimbal_deg_per_s": speed,
                        "array_peak_dbi": elem + 10.0 * math.log10(ngain),
                        "lock_time_s": m["lock_time_s"],
                        "pointing_error_locked_deg": m["pointing_error_locked_mean_deg"],
                        "outside_scan_pct": 100.0 * m["outside_scan_fraction"],
                        "scan_loss_mean_db": m["scan_loss_mean_db"],
                        "scan_loss_max_db": m["scan_loss_max_db"],
                        "loss_pct": 100.0 * m["loss_fraction"],
                        "margin_min_db": m["margin_min_db"],
                    }
                )
    return rows


def study_elevation() -> list[dict]:
    """Forstarkning rakt i malet vid tre elevationer, for de tre arkitekturerna.

    Antennen antas peka sa bra den kan: gimbalen staller in sig mot malet. Det ar
    just det en array UTAN gimbal inte kan, och derfor syns hela skillnaden har.
    """
    patterns = {
        "yagi pa gimbal": make_pattern(load_scenario(YAGI).antenna),
        "array utan gimbal": make_pattern(load_scenario(ARRAY_ONLY).antenna),
        "hybrid pa gimbal": make_pattern(load_scenario(BASE).antenna),
    }
    rows = []
    for el in (5.0, 30.0, 90.0):
        row = {"elevation_deg": el}
        for name, pat in patterns.items():
            # Alla tre utvarderas med malet i den riktning antennen faktiskt kan
            # peka. En fasstyrd array styr elektroniskt aven utan gimbal, sa for
            # array-only ar skillnaden att ELEMENTET sitter 85 grader fran sin
            # bredsida vid lag elevation — inte att stralen pekar fel.
            row[name] = pat.gain_towards(0.0, el, 0.0, el)
        rows.append(row)
    return rows


def print_table(title: str, rows: list[dict]) -> None:
    if not rows:
        return
    cols = list(rows[0].keys())
    print(f"\n{title}")
    header = "  ".join(f"{c:>22s}" if i == 0 else f"{c:>12s}" for i, c in enumerate(cols))
    print(header)
    print("-" * len(header))
    for row in rows:
        cells = []
        for i, c in enumerate(cols):
            v = row[c]
            if isinstance(v, float):
                cells.append(f"{v:>22.2f}" if i == 0 else f"{v:>12.2f}")
            else:
                cells.append(f"{v:>22s}" if i == 0 else f"{v:>12s}")
        print("  ".join(cells))


def study_three(seeds: int) -> list[dict]:
    """De tre arkitekturerna sida vid sida, med och utan GPS."""
    rows = []
    for label, path in (
        ("yagi pa gimbal", YAGI),
        ("array utan gimbal", ARRAY_ONLY),
        ("hybrid pa gimbal", BASE),
    ):
        base = load_scenario(path)
        for gps in (True, False):
            scn = replace(base, tracker=replace(base.tracker, gps_available=gps))
            m = averaged(scn, seeds)
            rows.append(
                {
                    "arkitektur": label,
                    "gps": "ja" if gps else "nej",
                    "nf_db": m["noise_figure_db"],
                    "lock_time_s": m["lock_time_s"],
                    "pointing_locked_deg": m["pointing_error_locked_mean_deg"],
                    "outside_scan_pct": 100.0 * m["outside_scan_fraction"],
                    "loss_pct": 100.0 * m["loss_fraction"],
                    "margin_min_db": m["margin_min_db"],
                    "margin_locked_min_db": m["margin_locked_min_db"],
                    "margin_locked_mean_db": m["margin_locked_mean_db"],
                }
            )
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Parameterstudie for hybridarkitekturen.")
    ap.add_argument("--seeds", type=int, default=30, help="antal seed per punkt (default 30)")
    ap.add_argument("--out", default=None, help="katalog for CSV")
    args = ap.parse_args(argv)

    base = load_scenario(BASE)
    out = Path(args.out) if args.out else HERE / "out" / "study"

    print(f"Bas: {base.name}, {args.seeds} seeds per punkt")

    three = study_three(args.seeds)
    print_table("0. Tre arkitekturer, med och utan GPS", three)

    arch = study_architecture(base, args.seeds)
    print_table("1. Arkitektur x fasvaexlarens dampning", arch)

    scan = study_scan(base, args.seeds)
    print_table(
        "2a. max_scan 45, alla gimbalhastigheter (utan GPS)",
        [r for r in scan if r["max_scan_deg"] == 45.0],
    )
    print_table(
        "2b. max_scan 15, alla gimbalhastigheter (utan GPS)",
        [r for r in scan if r["max_scan_deg"] == 15.0],
    )
    print_table(
        "2c. Gimbal 30 grader/s, alla max_scan",
        [r for r in scan if r["gimbal_deg_per_s"] == 30.0],
    )

    elev = study_elevation()
    print_table("3. Forstarkning rakt i malet (dBi)", elev)

    out.mkdir(parents=True, exist_ok=True)
    import csv

    for name, rows in (
        ("three", three),
        ("architecture", arch),
        ("scan", scan),
        ("elevation", elev),
    ):
        if not rows:
            continue
        path = out / f"{name}.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\nCSV: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
