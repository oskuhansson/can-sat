"""Modulering: känslighet, lufttid och paketfelsannolikhet.

LoRa-tabellerna nedan är referenspunkter, inte en fullständig modell. De räcker
för att svara på frågan simuleringen ställer — *hur många dB över brusgolvet
ligger vi, och hur ofta tappas ett paket* — men de är inte en bitnoggrann
implementering av CSS-demoduleringen. Vill man ha det senare ska man köra
gr-lora_sdr mot riktig hårdvara i stället.
"""

from __future__ import annotations

import math
import re

# Känslighet vid PER 1 % för LoRa på sub-GHz, 125 kHz bandbredd.
# Källa: Semtech SX126x-datablad. SF9 = -129 dBm är den siffra projektet använder.
SUBGHZ_SF125 = {
    7: -124.0,
    8: -126.5,
    9: -129.0,
    10: -131.5,
    11: -134.0,
    12: -137.0,
}

# Känslighet för SX1280 (LoRa på 2,4 GHz) vid 203 kHz bandbredd.
# Källa: Semtech SX1280-datablad, PER 1 %, CR 4/5, 10 byte.
WIDE_SF203 = {
    5: -109.0,
    6: -112.0,
    7: -115.0,
    8: -118.0,
    9: -121.0,
    10: -124.0,
    11: -127.0,
    12: -130.0,
}

_MODE_RE = re.compile(r"^lora_sf(?P<sf>\d+)_bw(?P<bw>\d+)$")


def parse_mode(spec: str) -> tuple[int, float]:
    """Tolka `"lora_sf9_bw125"` till (spreading factor, bandbredd i kHz)."""
    match = _MODE_RE.match(spec.strip().lower())
    if not match:
        raise ValueError(
            f"okänd moduleringssträng '{spec}'. Väntade t.ex. 'lora_sf9_bw125'"
        )
    return int(match.group("sf")), float(match.group("bw"))


def reference_sensitivity_dbm(sf: int, frequency_mhz: float) -> tuple[float, float]:
    """Referenskänslighet och referensbandbredd för rätt band.

    Returnerar (känslighet_dBm, referensbandbredd_kHz) så att anroparen kan
    räkna om till sin egen bandbredd.
    """
    if frequency_mhz < 1000.0:
        if sf not in SUBGHZ_SF125:
            raise ValueError(f"SF{sf} finns inte i sub-GHz-tabellen")
        return SUBGHZ_SF125[sf], 125.0
    if sf not in WIDE_SF203:
        raise ValueError(f"SF{sf} finns inte i 2,4 GHz-tabellen")
    return WIDE_SF203[sf], 203.0


def sensitivity_dbm(sf: int, bandwidth_khz: float, frequency_mhz: float) -> float:
    """Känslighet vid godtycklig bandbredd.

    Varje dubblering av bandbredden kostar 3 dB: brusgolvet är -174 + 10log10(BW).
    """
    base, ref_bw = reference_sensitivity_dbm(sf, frequency_mhz)
    return base + 10.0 * math.log10(bandwidth_khz / ref_bw)


def airtime_s(
    sf: int,
    bandwidth_khz: float,
    payload_bytes: int,
    coding_rate: int = 1,
    preamble_symbols: int = 8,
    crc: bool = True,
    explicit_header: bool = True,
) -> float:
    """Lufttid för ett LoRa-paket, enligt Semtechs formel.

    Symboltiden är 2^SF/BW. Antalet symboler är preamble + 4,25 för synk samt
    payloadens symboler, som beror på hur många bitar som får plats per symbol.
    `coding_rate` 1..4 motsvarar 4/5..4/8.
    """
    tsym = (2**sf) / (bandwidth_khz * 1000.0)

    # LDRO slås på automatiskt när symboltiden överstiger 16 ms.
    de = 1 if tsym > 0.016 else 0

    numerator = (
        8 * payload_bytes
        - 4 * sf
        + 28
        + (16 if crc else 0)
        - (20 if explicit_header else 0)
    )
    denominator = 4 * (sf - 2 * de)
    # Semtechs formel multiplicerar med (CR+4)/4, alltså 1,25 för 4/5 — inte med
    # (CR+4). Utan divisionen blir payloaden fyra gånger för lång: 185 ms i
    # stället för 108 ms för 20 byte på SF9/125 kHz, vilket gör att varje
    # duty cycle-slutsats blir fel åt det strängare hållet.
    payload_symbols = 8 + max(math.ceil(numerator / denominator) * (coding_rate + 4) / 4.0, 0)

    return (preamble_symbols + 4.25 + payload_symbols) * tsym


def packet_error_rate(margin_db: float) -> float:
    """Paketfelsannolikhet som funktion av marginalen över känsligheten.

    Känsligheten är definierad vid PER 1 %, alltså är PER = 0,01 vid marginal 0.
    Därifrån faller den med ungefär en dekad per 2 dB — det stämmer någorlunda
    med LoRa-waterfallen i Semtechs kurvor. Modellen är monoton och går mot 1 när
    marginalen blir negativ, vilket är det beteende simuleringen behöver.

    Det här är en **approximation**. Riktiga PER-kurvor har en brantare knä och
    beror på interferens, frekvensfel och paketlängd.
    """
    per = 0.01 * 10.0 ** (-margin_db / 2.0)
    return min(1.0, max(1e-6, per))


def duty_cycle_fraction(airtime_s_value: float, interval_s: float) -> float:
    """Andel av tiden som sändaren är på luften."""
    if interval_s <= 0:
        return 1.0
    return min(1.0, airtime_s_value / interval_s)
