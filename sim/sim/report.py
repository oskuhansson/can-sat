"""Rapportering: CSV (obligatoriskt), sammanfattning i terminalen, PNG om det går.

CSV är den enda utdata som alltid finns. matplotlib är valfritt — saknas det
skrivs ingen bild, och det ska inte vara ett fel.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .engine import SimulationResult


def to_frame(result: SimulationResult) -> pd.DataFrame:
    """Tidsserien som DataFrame, en rad per tidssteg."""
    return pd.DataFrame(result.rows())


def write_csv(result: SimulationResult, path: str | Path) -> Path:
    """Skriv tidsserien till CSV och returnera sökvägen."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    to_frame(result).to_csv(path, index=False, float_format="%.4f")
    return path


def write_summary_csv(results: list[SimulationResult], path: str | Path) -> Path:
    """En rad per körning — underlaget för Monte Carlo-statistiken."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for r in results:
        row = {"run": r.seed, "scenario": r.scenario_name}
        row.update(r.summary)
        rows.append(row)
    pd.DataFrame(rows).to_csv(path, index=False, float_format="%.4g")
    return path


def _line(label: str, value: str, note: str = "") -> str:
    base = f"  {label:<34} {value:>12}"
    return f"{base}   {note}" if note else base


def _fmt_seconds(value: float) -> str:
    """Sekunder, eller 'aldrig' om laget aldrig lastes."""
    try:
        if value != value:  # nan
            return "aldrig"
    except TypeError:
        return str(value)
    return f"{value:.1f} s"


def format_summary(result: SimulationResult) -> str:
    """Läsbar sammanfattning av en körning."""
    s = result.summary
    c = result.constants
    out: list[str] = []

    out.append(f"Scenario: {result.scenario_name}  (seed {result.seed})")
    out.append("")
    out.append("Radio")
    out.append(_line("Frekvens", f"{c['frequency_mhz']:.0f} MHz"))
    out.append(_line("EIRP", f"{c['eirp_dbm']:.1f} dBm"))
    out.append(_line("Systembrusfaktor", f"{s['noise_figure_db']:.2f} dB"))
    out.append(
        _line(
            "Känslighet (kaskad)",
            f"{s['sensitivity_dbm']:.1f} dBm",
            f"chippen {s['sensitivity_chip_dbm']:.1f}",
        )
    )
    out.append(_line("Lufttid per paket", f"{s['airtime_s'] * 1000:.0f} ms"))
    out.append(_line("Duty cycle", f"{s['duty_cycle'] * 100:.1f} %"))
    budget = s.get("airtime_budget_s", float("nan"))
    if budget == budget:  # inte nan, dvs en gräns är satt
        status = "OK" if s["duty_cycle_ok"] else "ÖVER BUDGET"
        out.append(
            _line(
                "Lufttid under flygningen",
                f"{s['airtime_total_s']:.1f} / {budget:.0f} s",
                status,
            )
        )

    out.append("")
    out.append("Antenn och pekning")
    out.append(_line("Strålbredd (3 dB)", f"{s['beamwidth_3db_deg']:.1f}°"))
    out.append(
        _line(
            "Tål pekfel för 1 dB",
            f"±{s['tolerance_1db_deg']:.1f}°",
            "12*(theta/theta3dB)^2 = 1",
        )
    )
    out.append(_line("Låsningstid", _fmt_seconds(s["lock_time_s"])))
    if s["scan_time_s"] > 0:
        # Två decimaler: med heltal blev ett svep på 0,46 s "0 s", vilket ser ut
        # som om ingen sveptid finns alls.
        out.append(_line("Fullt svep tar", f"{s['scan_time_s']:.2f} s", "utan GPS"))
    out.append(
        _line("Pekfel, medel (låst)", f"{s['pointing_error_locked_mean_deg']:.2f}°")
    )
    out.append(_line("Pekfel, max", f"{s['pointing_error_max_deg']:.1f}°"))
    out.append(_line("Pekfel, P95", f"{s['pointing_error_p95_deg']:.1f}°"))
    out.append(_line("Antennvinstförlust, max", f"{s['rx_gain_loss_max_db']:.2f} dB"))
    out.append(_line("Antennvinstförlust, medel", f"{s['rx_gain_loss_mean_db']:.2f} dB"))

    out.append("")
    out.append("Länk")
    out.append(_line("Marginal, medel", f"{s['margin_mean_db']:.1f} dB"))
    out.append(
        _line(
            "Marginal, sämst",
            f"{s['margin_min_db']:.1f} dB",
            f"vid t = {s['margin_min_at_s']:.0f} s",
        )
    )
    out.append(_line("Andel tid under 0 dB", f"{s['margin_below_zero_fraction'] * 100:.1f} %"))
    out.append(_line("Vegetationsförlust, max", f"{s['vegetation_max_db']:.1f} dB"))

    out.append("")
    out.append("Paket")
    out.append(
        _line(
            "Skickade / tappade",
            f"{s['packets_sent']:.0f} / {s['packets_lost']:.0f}",
        )
    )
    out.append(_line("Förlust", f"{s['loss_fraction'] * 100:.1f} %"))
    out.append(
        _line(
            "Längsta sammanhängande",
            f"{s['longest_loss_run_s']:.1f} s",
            "datahål",
        )
    )
    out.append(
        _line(
            "Förlust sista 25 %",
            f"{s['tail_loss_fraction'] * 100:.1f} %",
            "där vegetationen biter",
        )
    )
    return "\n".join(out)


def format_monte_carlo(results: list[SimulationResult]) -> str:
    """Sammanställning över flera körningar."""
    if not results:
        return "Inga körningar."
    if len(results) == 1:
        return "Monte Carlo: bara en körning — kör med --runs för statistik."

    frame = pd.DataFrame([r.summary for r in results])
    out = [f"Monte Carlo: {len(results)} körningar", ""]

    def stat(column: str, label: str, unit: str = "", scale: float = 1.0) -> None:
        values = frame[column].astype(float) * scale
        out.append(
            _line(
                label,
                f"{values.mean():.2f}{unit}",
                f"P5 {values.quantile(0.05):.2f}  P95 {values.quantile(0.95):.2f}  max {values.max():.2f}",
            )
        )

    stat("loss_fraction", "Paketförlust, medel", " %", 100.0)
    stat("longest_loss_run_s", "Längsta datahål", " s")
    stat("margin_min_db", "Sämsta marginal", " dB")
    stat("pointing_error_p95_deg", "Pekfel P95", "°")
    stat("tail_loss_fraction", "Förlust sista 25 %", " %", 100.0)

    bad = (frame["loss_fraction"].astype(float) > 0.10).mean()
    dead = (frame["loss_fraction"].astype(float) > 0.50).mean()
    out.append("")
    out.append(_line("Körningar med >10 % förlust", f"{bad * 100:.0f} %"))
    out.append(_line("Körningar med >50 % förlust", f"{dead * 100:.0f} %"))
    return "\n".join(out)


def plot(result: SimulationResult, path: str | Path) -> Path | None:
    """Två diagram: pekfel och marginal över tiden.

    Returnerar sökvägen, eller None om matplotlib saknas. Att bilden uteblir är
    inte ett fel — CSV:n är den data som gäller.
    """
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None

    frame = to_frame(result)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

    ax1.plot(frame["t_s"], frame["pointing_error_deg"], lw=1.2)
    if "tolerance_1db_deg" in result.summary:
        ax1.axhline(
            result.summary["tolerance_1db_deg"],
            ls="--",
            lw=0.9,
            color="tab:red",
            label="1 dB pekförlust",
        )
    ax1.set_ylabel("Pekfel (grader)")
    ax1.set_title(f"{result.scenario_name} — pekfel och länkmarginal")
    ax1.legend(loc="upper right", fontsize=8)
    ax1.grid(alpha=0.3)

    ax2.plot(frame["t_s"], frame["margin_db"], lw=1.2)
    ax2.axhline(0.0, ls="--", lw=0.9, color="tab:red", label="känslighetsgräns")
    ax2.set_ylabel("Marginal (dB)")
    ax2.set_xlabel("Tid (s)")
    ax2.legend(loc="upper right", fontsize=8)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path
