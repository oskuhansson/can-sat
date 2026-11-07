"""Länkbudget: brusfaktor genom kaskaden, känslighet, mottagen effekt, marginal.

Två saker som är lätta att göra fel och som därför är explicita här:

1. **Känsligheten i ett datablad gäller chippens egen brusfaktor.** Sätter man en
   LNA framför förbättras systembrusfaktorn, och då förbättras känsligheten med
   skillnaden — den är inte konstant.
2. **En passiv komponent har brusfaktor lika med sin dämpning.** En dämpare på
   10 dB har NF 10 dB. Att ange NF 0 för en dämpare är ett vanligt misstag som
   gör länkbudgeten optimistisk.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .config import RadioConfig, Stage


def _db_to_linear(db: float) -> float:
    return 10.0 ** (db / 10.0)


def cascade_noise_factor(stages: list[Stage]) -> float:
    """Friis kaskadformel: F_tot = F1 + (F2-1)/G1 + (F3-1)/(G1*G2) + ...

    Formeln säger att det som sitter **först** dominerar. En LNA med NF 0,4 dB
    direkt efter antennen gör att allt bakom den — koax, dämpare, mottagarchip —
    nästan slutar bidra.
    """
    if not stages:
        raise ValueError("kaskaden behöver minst ett steg")

    f_total = 0.0
    gain_cumulative = 1.0
    for index, stage in enumerate(stages):
        f = _db_to_linear(stage.noise_figure_db)
        if index == 0:
            f_total = f
        else:
            f_total += (f - 1.0) / gain_cumulative
        gain_cumulative *= _db_to_linear(stage.gain_db)
    return f_total


def full_chain(radio: RadioConfig) -> list[Stage]:
    """Mottagarkedjan inklusive själva radion, som är sista steget."""
    return list(radio.rx_stages) + [
        Stage("receiver", 0.0, radio.receiver_noise_figure_db)
    ]


@dataclass(frozen=True)
class ReceiverChain:
    """Sammanfattning av mottagarkedjan, för rapporten."""

    noise_factor: float
    noise_figure_db: float
    chip_noise_figure_db: float
    sensitivity_improvement_db: float


def analyse_chain(radio: RadioConfig) -> ReceiverChain:
    f_total = cascade_noise_factor(full_chain(radio))
    nf = 10.0 * math.log10(f_total)
    return ReceiverChain(
        noise_factor=f_total,
        noise_figure_db=nf,
        chip_noise_figure_db=radio.receiver_noise_figure_db,
        sensitivity_improvement_db=radio.receiver_noise_figure_db - nf,
    )


def noise_floor_dbm(bandwidth_hz: float, noise_figure_db: float) -> float:
    """Termiskt brusgolv i en bandbredd: -174 + 10log10(BW) + NF.

    -174 dBm/Hz är k*T vid 290 K. Varje dubblering av bandbredden kostar 3 dB.
    """
    return -174.0 + 10.0 * math.log10(bandwidth_hz) + noise_figure_db


def effective_sensitivity_dbm(
    datasheet_sensitivity_dbm: float,
    chain: ReceiverChain,
) -> float:
    """Känslighet för hela kedjan, inte bara chippen.

    Databladets siffra är uppmätt med chippens NF. Byter man ut fronten mot en
    bättre förbättras känsligheten lika mycket som NF förbättrades.
    """
    return datasheet_sensitivity_dbm - chain.sensitivity_improvement_db


def received_power_dbm(
    eirp_dbm: float,
    path_loss_db: float,
    rx_gain_dbi: float,
    shadowing_db: float = 0.0,
) -> float:
    """P_rx = EIRP - förlust + antennvinst - skuggning."""
    return eirp_dbm - path_loss_db + rx_gain_dbi - shadowing_db


def margin_db(received_dbm: float, sensitivity_dbm: float) -> float:
    """Hur många dB överkänsligheten signalen ligger. Negativt = ingen länk."""
    return received_dbm - sensitivity_dbm


def pointing_loss_db(off_angle_deg: float, beamwidth_3db_deg: float) -> float:
    """Pekförlust relativt bomriktningen: 12*(theta/theta3dB)^2.

    Bara en referens — den riktiga beräkningen görs av antennmodellen, som kan
    ha sidolober. Härledd för att kunna jämföra scenarier mot projektets siffror.
    """
    return 12.0 * (off_angle_deg / beamwidth_3db_deg) ** 2


def tolerance_angle_deg(beamwidth_3db_deg: float, loss_db: float = 1.0) -> float:
    """Hur stort pekfel man tål innan förlusten når `loss_db`.

    Invertering av pekförlustformeln: theta = theta3dB * sqrt(L/12).
    Vid 1 dB blir det 0,289*theta3dB — för en 17,5-graderslob alltså bara 5,1
    grader, medan en 48,4-graderslob tål 14,0 grader.
    """
    return beamwidth_3db_deg * math.sqrt(loss_db / 12.0)
