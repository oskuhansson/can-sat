#!/usr/bin/env python
"""Kommandorad för simuleringen.

    python run.py scenarios/cansat_868.json
    python run.py scenarios/cansat_868.json --runs 200
    python run.py scenarios/cansat_24.json --runs 50 --plot

Skriver CSV per körning och en sammanfattning i terminalen. Allt som skiljer
scenarierna åt står i JSON-filen — inget här är CanSat-specifikt.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sim import report  # noqa: E402
from sim.config import ConfigError, load_scenario  # noqa: E402
from sim.engine import run  # noqa: E402

# Windows-konsolen använder sin egen teckenuppsättning. Pipeas eller sparas
# utskriften blir å/ä/ö mojibake om vi inte tvingar UTF-8 — det syns som "T?l
# pekfel". En riktig konsol lämnas orörd, för där sköter Python kodningen själv.
if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Simulera en riktantenn på marken som följer en fallande sändare.",
    )
    parser.add_argument("scenario", help="sökväg till en scenariofil i JSON")
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="antal Monte Carlo-körningar (default 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="första seed; körning i får seed+i (default: scenariofilens seed)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="katalog för CSV (default: out/<scenarionamn>)",
    )
    parser.add_argument("--plot", action="store_true", help="skriv PNG om matplotlib finns")
    parser.add_argument("--quiet", action="store_true", help="bara Monte Carlo-sammanfattningen")
    args = parser.parse_args(argv)

    try:
        scenario = load_scenario(args.scenario)
    except ConfigError as exc:
        print(f"Fel i scenariofilen: {exc}", file=sys.stderr)
        return 2

    if args.runs < 1:
        print("--runs måste vara minst 1", file=sys.stderr)
        return 2

    out_dir = Path(args.out) if args.out else HERE / "out" / scenario.name

    results = []
    for i in range(args.runs):
        seed = (args.seed + i) if args.seed is not None else scenario.seed + i
        results.append(run(scenario, seed))

    if not args.quiet:
        print(report.format_summary(results[0]))
        print()

    for i, result in enumerate(results):
        report.write_csv(result, out_dir / f"{scenario.name}_run{i:03d}.csv")
    summary_path = report.write_summary_csv(results, out_dir / f"{scenario.name}_summary.csv")

    if args.runs > 1:
        print(report.format_monte_carlo(results))
        print()

    if args.plot:
        plotted = report.plot(results[0], out_dir / f"{scenario.name}_plot.png")
        if plotted:
            print(f"Diagram: {plotted}")
        else:
            print("matplotlib saknas — hoppar över PNG (CSV:erna är kvar)")

    print(f"CSV: {out_dir}")
    print(f"Sammanfattning: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
