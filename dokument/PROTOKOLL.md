---
tags: [cansat, radio, protokoll, priser]
status: aktuell
updated: 2026-11-07
---

# Protokollval: tillförlitlighet + bandbredd på 2,4 GHz

*Undersökt 2026-11-06. Fråga: går det att få **både** LoRas tillförlitlighet **och** bra
bandbredd på 2,4 GHz (för beamforming)? Svar: ja — men det kräver att man förstår *varför*
LoRa är robust.*

---

## 1. Rättelse av ett tidigare påstående

Tidigare sades att 2,4 GHz kostar "~18 dB" jämfört med 868 MHz. **Det var fel.**

$$
\text{FSPL}_{2.4\text{GHz}} - \text{FSPL}_{868\text{MHz}}
= 20\log_{10}\!\left(\frac{2400}{868}\right) \approx \mathbf{8{,}8\ dB}
$$

Skillnaden är frekvensberoende och gäller på **alla** avstånd. 8,8 dB är **återvinningsbart**
med antennförstärkning — särskilt på 2,4 GHz där elementen är små och arrayer är praktiska.

---

## 2. Vad är LoRas tillförlitlighet egentligen? (två oberoende delar)

| Komponent | Vad den ger | Följer med till 2,4 GHz? |
|---|---|---|
| **CSS-moduleringen** — chirp spread spectrum, spridningsfaktor, FEC | Brustålighet, co-channel rejection, processvinst | ✅ **Ja** |
| **Sub-GHz-utbredningen** | Diffraktion kring hinder, penetration, låg FSPL | ❌ **Nej** (−8,8 dB) |

**Slutsats:** "LoRa på 2,4 GHz" = robust modulering **utan** sub-GHz-räckviddsfördelen.
Man behåller det som gör LoRa bruståligt och tappar det som ger maximal räckvidd.

### Processvinsten (varför CSS tål brus)

$$
G_p = 10\log_{10}\!\left(\frac{R_c}{R_b}\right)
$$

Med spridningsfaktor $SF$: $R_c/R_b = 2^{SF}$ (chips per symbol). Varje +1 i SF ger
**~3 dB** processvinst — det är därför SF12 tål mycket mer brus än SF5.

---

## 3. 🎯 Den största vinsten med 2,4 GHz: duty cycle

Duty cycle mäts över **en timme**, inte per flygning — ETSI EN 300 220-2 V3.3.1 §4.4.3.2:
*"Unless otherwise specified, T_obs is 1 hour"*. 1 % = **36 s lufttid per timme** (samma
siffra som [REGELVERK.md](REGELVERK.md) §1 anger).

| Band | Duty cycle (Finland) | Airtime per timme |
|---|---|---|
| **868 MHz**, 25 mW e.r.p. | **≤ 1 %** | **36 s** |
| **868 MHz**, 500 mW (sub-band P) | ≤ 10 % | 360 s |
| **2,4 GHz** | **ingen gräns** | **obegränsad** |

**Detta är avgörande.** 36 s/h är en budget man delar över **hela evenemanget** — inte
bara över den 120 s långa nedfärden. Ett 20-byte-paket på SF9/125 kHz tar **185 ms**
lufttid, så 36 s räcker till ≈ **194 paket per timme**. Att skicka 2 paket/s under en
110 s-flygning kostar 41 s och **spräcker budgeten** — gränsen ligger vid ~1,8 paket/s.
Och samma budget ska räcka till marktester, kalibrering och hela tävlingsdagen. **Bredbandig
telemetri eller video får inte plats alls**: 1 % räcker till en smal ström av korta paket,
inte till en dataström. På 2,4 GHz kan man sända **kontinuerligt** — det löser
låg-bandbreddsproblemet utan att offra moduleringens robusthet.

---

## 4. SX1280 / SX1281 — LoRa CSS på 2,4 GHz

Källa: [Semtech SX1280/SX1281 datablad rev 3.2](https://media.digikey.com/pdf/Data%20Sheets/Semtech%20PDFs/SX1280-81_Rev3.2_Mar2020.pdf)

### 4.1 Känslighet (dBm), PER 1 %, CR 4/5

| Bandbredd | SF5 | SF6 | SF7 | SF8 | SF9 | SF10 | SF11 | SF12 |
|---|---|---|---|---|---|---|---|---|
| 203 kHz | −109 | −111 | −115 | −118 | −121 | −124 | −127 | **−130** |
| 406 kHz | −107 | −110 | −113 | −116 | −119 | −122 | −125 | −128 |
| 812 kHz | −105 | −108 | −112 | −115 | −117 | −120 | −123 | −126 |
| 1625 kHz | −99 | −103 | −106 | −109 | −111 | −114 | −117 | −120 |

*(High-sensitivity-läge ger ytterligare ~2 dB: SF12/BW203 → **−132 dBm**)*

### 4.2 Rå datahastighet (kb/s)

| Bandbredd | SF5 | SF7 | SF12 |
|---|---|---|---|
| 203 kHz | 31,72 | 11,1 | 0,595 |
| 406 kHz | 63,44 | 22,2 | 1,19 |
| 812 kHz | 126,88 | 44,41 | 2,38 |
| **1625 kHz** | **253,91** | 88,87 | 4,76 |

### 4.3 Störningstålighet

- **Co-channel rejection:** SF7 = 7,5 dB, **SF12 = 19,5 dB**
- **Blocking immunity:** SF12, ±1 MHz = 60 dB; ±10 MHz = 81 dB
- **ACR** (adjacent channel): 37 dB

### 4.4 Vad SX1280 ger utöver data

- **Ranging-motor** — mäter rundturstid (time-of-flight) → **avstånd mellan två enheter**.
  Direkt användbart för gimbal-trackern (avstånd + riktning utan enbart GPS).
- **Ingen duty-cycle-gräns** i 2,4 GHz.
- Liten antenn (λ/2 = 6,2 cm vid 2,4 GHz) → **beamforming praktiskt**.

### 4.5 Styrka / svaghet

**Starkt:** både 254 kb/s (SF5) **och** −132 dBm (SF12) på samma chip; CSS-brusrobusthet;
ranging; fri duty cycle; små antenner.

**Svagt:** 2,4 GHz-bandet är **trångt** (WiFi, BLE, mikrovågsugn) → intermittent störning;
Tx-effekt bara +11,5…+13 dBm (mot +22 dBm sub-GHz); tappar 8,8 dB FSPL.

---

## 5. 🏆 LR1121 — den strategiska lösningen (slipp välja)

Källa: [Semtech LR1121](https://www.semtech.com/products/wireless-rf/lora-connect/lr1121)

| Egenskap | Värde |
|---|---|
| Sub-GHz | **150–960 MHz**, PA **+22 dBm** |
| **2,4 GHz ISM** | **✅**, PA **+11,5 dBm** |
| S-band | 2 GHz |
| L-band | 1,55 GHz |
| LR-FHSS | ✅ (frekvenshoppande spread spectrum) |
| Kompatibel med | SX1261/2/8 + LoRaWAN |
| Generation | Tredje generationens LoRa-transceiver |

**Varför detta löser din fråga:** ett chip, samma firmware, **båda banden**. Man kör
**adaptivt**:

```
 Stark/långt bort  →  868 MHz   (max räckvidd, 1 % duty cycle räcker för telemetri)
 Nära/stark signal →  2,4 GHz   (254 kb/s, fri duty cycle, beamforming-vänligt)
```

Det ger *både* tillförlitlighet *och* bandbredd — inte genom att välja, utan genom att
byta band efter behov. LR-FHSS ger dessutom extra robusthet genom frekvenshoppning.

---

## 6. Alla alternativ jämförda

| Teknik | Band | Max data | Känslighet | Brusrobusthet | Kostnad | Kommentar |
|---|---|---|---|---|---|---|
| **SX1280 (LoRa 2,4)** | 2,4 | **254 kb/s** | **−132 dBm** | ⭐⭐⭐ CSS | låg | + ranging, fri duty cycle |
| **LR1121** | 150–960 + 2,4 | 254 kb/s | −132 dBm | ⭐⭐⭐ | låg–medel | **bästa helhetsvalet** |
| **BLE 5 LE Coded S=8** | 2,4 | 125 kb/s | −103 dBm | ⭐⭐ FEC | **lägst** | 1,6 km bevisat, överallt |
| **BLE LE Coded S=2** | 2,4 | 500 kb/s | ~−97 dBm | ⭐⭐ | lägst | mer data, kortare räckvidd |
| **BLE LE 1M/2M** | 2,4 | 1–2 Mb/s | −93/−97 dBm | ⭐ | lägst | kort räckvidd |
| **802.15.4 / Thread** | 2,4 | 250 kb/s | ~−100 dBm | ⭐⭐ DSSS | låg | mesh, känsligare för störning |
| **ESP-NOW / WiFi** | 2,4 | hög | ~−90 dBm | ⭐ | låg | ingen brusrobusthet |
| **LoRa 868 (SX1262)** | 868 | 37,5 kb/s | −137 dBm | ⭐⭐⭐ | låg | bäst räckvidd, men 1 % duty |

### 6.1 Varför LoRa slår 802.15.4 vid störning

[Studie (Uppsala Univ.)](https://sonri.org/publications/Files/PID4982007.pdf) visar:

> "LoRa is resilient enough to get high PRR even when the strength of an interfering
> IEEE 802.15.4g signal is considerably higher… at low data rates LoRa tolerates up to
> **16 dB** higher interference power."

Orsaken: **CSS sprider energin över hela bandbredden**, medan GFSK/O-QPSK koncentrerar
den till få frekvenser och därför träffas hårdare av smalbandig störning.

### 6.2 BLE 5 LE Coded — underskattat

Källor: [Bluetooth SIG Core 5.0](https://www.bluetooth.com/wp-content/uploads/2019/03/Bluetooth_5-FINAL.pdf), [TI appnot](https://www.ti.com/lit/ta/ssztag2/ssztag2.pdf)

| PHY | Protokollhastighet | FEC | Räckviddsmultiplikator |
|---|---|---|---|
| LE 1M | 1 Mb/s | nej | 1× |
| LE Coded S=2 | 500 kb/s | ✅ | ~2× |
| **LE Coded S=8** | **125 kb/s** | ✅ | **~4×** |

Två delar av vinsten (~12 dB):
- **9 dB** från att datatakten sänks till 1/8 → varje bit bär 8× mer energi
- **3 dB** från FEC (konvolutionell kod + mönstermappning)

TI demonstrerade **1,6 km faktisk räckvidd** med CC2640R2F på 125 kb/s i stadsmiljö.
Link budget 108 dB med +5 dBm.

---

## 7. Rekommendation

### Bärlinje
**SX1262 (868 MHz)** för telemetri/GPS — bevisad, billig, −137 dBm, laglig.

### Bandbreddsbenet
**SX1280 (2,4 GHz)** för hög datatakt + fri duty cycle + ranging.

### Om man vill ha ett chip
**LR1121** — sub-GHz + 2,4 GHz i samma krets, samma firmware, adaptiv bandväxling.

### Vad man INTE ska göra
Inte tro att "LoRa på 2,4 GHz" ger samma räckvidd som 868. Det ger samma *brusrobusthet*
men 8,8 dB sämre länk — vilket är acceptabelt om man kompenserar med antenn/array.

---

## 8. Konsekvens för beamforming-valet

2,4 GHz är **rätt band för arrayen** eftersom:

$$
\lambda_{2.4} = \frac{3\cdot10^8}{2{,}4\cdot10^9} = 12{,}5\ \text{cm}
\qquad
\frac{\lambda}{2} = 6{,}25\ \text{cm}
$$

Mot 868 MHz där λ/2 = 17,3 cm. **Elementen blir 2,8× mindre** → en 4-elementarray får plats
på ~19 cm istället för ~52 cm. Därför: **beamforming på 2,4 GHz + LoRa 868 som backup**
är en koherent arkitektur.

---

## 9. 💰 Aktuella priser (2026-11-06, USD exkl. frakt/moms)

### 9.1 Kretpriser — bara kretsen (kräver eget RF-kort)

| Krets | 1 st | 100 st | 3 000 st | Distributör |
|---|---|---|---|---|
| **SX1280IMLTRT** (LoRa 2,4 GHz) | **$7,24** | $5,48 | $4,13 | [DigiKey](https://www.alldatasheet.com/distributor/view.jsp?Searchword=SX1280) |
| SX1280IMLTRT | **$10,32** | $7,81 | $6,40 | [Mouser](https://au.mouser.com/c/?tradename=LoRa) |
| **LR1121IMLTRT** (sub-GHz + 2,4) | **$8,19** | $6,20 | $4,79 | [DigiKey](https://www.digikey.com/en/products/detail/semtech-corporation/LR1121IMLTRT/17874420) |
| LR1121IMLTRT | **$7,61** | $5,77 | $4,79 | [Symmetry](https://www.symmetryelectronics.com/products/semtech/lr1121imltrt/) |
| **SX1262IMLTRT** (LoRa 868) | **$9,04** | $6,86 | $5,71 | [DigiKey](https://www.digikey.com/en/products/detail/semtech-corporation/SX1262IMLTRT/8564369) |

**LR1121 specificerad:** känslighet **−144 dBm** (sub-GHz), max 250 kb/s, +22 dBm sub-GHz,
+11,5 dBm 2,4 GHz, 32-QFN 5×5 mm, 8 kB RAM.

### 9.2 Modulpriser — radio + MCU + antenn + certifiering

| Modul | Pris (1 st) | Räckvidd (tillverkarens mätning) | Anmärkning |
|---|---|---|---|
| **Fanstel BT840** | **$6,88** | 100 m @1Mbps | nRF52840, integrerad PCB-antenn |
| **Fanstel BT840E** | **$8,28** | **3 400 m @125 kbps** | u.FL extern antenn, FCC-certifierad |
| Fanstel BT840F | $8,81 (1k st) | **2 300 m @125 kbps** | +8,49 dBm |
| Fanstel BT840N | — | — | med **nRF21540 PA, +19,1 dBm** |
| **MinewSemi MS88SF23** | **$6,90** | 300 m | nRF52840, u.FL, fullt certifierad |

Källor: [Fanstel BT840-serien](https://www.fanstel.com/bt840), [MinewSemi MS88SF23](https://store.minewsemi.com/product/bluetooth-modules-nrf52840-ms88sf23/)

### 9.3 Systemkostnad per enhet (inte bara kretspriset!)

Kretspriset är bara toppen. En **bar krets** kräver dessutom:

- egen PCB med 50 Ω RF-layout
- matchningsnätverk
- TCXO (frekvensstabilitet)
- **en separat MCU**
- QFN-lödning (reflow)

En **modul** innehåller allt detta färdigt.

| Väg | Krets | Tillkommande | **Per enhet** |
|---|---|---|---|
| SX1280 bara krets | $7,24 | TCXO + passiva + PCB + MCU ≈ $15–25 | **~$22–32** |
| LR1121 bara krets | $8,19 | samma ≈ $15–25 | **~$23–33** |
| SX1262 + SX1280 (två radio) | $16,28 | två RF-kedjor ≈ $25–35 | **~$41–51** |
| ⭐ **nRF52840-modul** | $6,88 | bara bärarkort ≈ $2–5 | **~$9–12** |
| Mix: nRF52840 + SX1262-modul | $6,88 + ~$12 | bärarkort ≈ $5 | ~$24 |

**Projektkostnad (burk + mark + 1 reserv = 3 enheter):**

| Väg | 3 enheter |
|---|---|
| nRF52840-moduler | **~$28–36** ✅ |
| LR1121 bara krets | ~$70–100 |
| SX1262 + SX1280 bara krets | ~$125–155 |

### 9.4 Slutsats om pris

**nRF52840-modulen (BT840, $6,88) är den billigaste och enklaste vägen** — radio, MCU,
antenn och certifiering i ett för priset av en krets. Börja där.

**LR1121 ($8,19)** är billig för vad den gör (två band + LR-FHSS i ett chip), men
kräver eget RF-kort — räkna ~$25–33/enhet färdig.

---

## 10. Källor

- [Semtech SX1280/SX1281 datablad rev 3.2 (2,4 GHz LoRa, känslighet, datahastigheter)](https://media.digikey.com/pdf/Data%20Sheets/Semtech%20PDFs/SX1280-81_Rev3.2_Mar2020.pdf)
- [Semtech LR1121 — multi-band sub-GHz + 2,4 GHz + S-band + LR-FHSS](https://www.semtech.com/products/wireless-rf/lora-connect/lr1121)
- [Semtech LR1121 datablad (Richardson RFPD)](https://shop.richardsonrfpd.com/docs/rfpd/LR1121_DS_H1_V1_2.pdf)
- [Bluetooth SIG — Core 5.0 Feature Enhancements (LE Coded PHY, S=2/S=8)](https://www.bluetooth.com/wp-content/uploads/2019/03/Bluetooth_5-FINAL.pdf)
- [TI — How does Bluetooth 5 increase range? (12 dB, 1,6 km test)](https://www.ti.com/lit/ta/ssztag2/ssztag2.pdf)
- [Uppsala Univ. — Interference between LoRa and IEEE 802.15.4g (16 dB tolerans)](https://sonri.org/publications/Files/PID4982007.pdf)
- [UNICAMP — Experimental comparison of LPWAN technologies (LoRa vs 802.15.4g)](https://doi.org/10.47749/t/unicamp.2020.1157966)
- [DigiKey — SX1280IMLTRT (pris/stock)](https://www.alldatasheet.com/distributor/view.jsp?Searchword=SX1280)
- [DigiKey — LR1121IMLTRT (pris/stock/parametrar)](https://www.digikey.com/en/products/detail/semtech-corporation/LR1121IMLTRT/17874420)
- [DigiKey — SX1262IMLTRT (pris/stock)](https://www.digikey.com/en/products/detail/semtech-corporation/SX1262IMLTRT/8564369)
- [Fanstel BT840-serie — nRF52840-moduler, räckviddsmätningar](https://www.fanstel.com/bt840)
- [MinewSemi MS88SF23 — nRF52840-modul med u.FL](https://store.minewsemi.com/product/bluetooth-modules-nrf52840-ms88sf23/)

---

*Levande dokument. Uppdatera när protokollvalet är fastställt och verifierat i fält.*

---

## Se även

- [KOMMUNIKATION.md](KOMMUNIKATION.md) — länkbudgeten för valt band (§5.2)
- [BEAMFORMING.md](BEAMFORMING.md) — varför 2,4 GHz är bättre för arrayer
- [FASVAXLARE.md](FASVAXLARE.md) — komponenterna som arrayen kräver
- [KOSTNADER.md](KOSTNADER.md) — radio- och modulkostnad
- [POLARISATION.md](POLARISATION.md) — burkens rotation och polarisationsförlust
