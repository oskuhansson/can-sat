---
tags: [cansat, budget]
status: aktuell
updated: 2026-11-07
---

# Kostnader — hela CanSat-projektet

*Alla kostnader på ett ställe. Budgettaket är **≤ 500 €**. Sammanställd 2026-11-07 genom att slå ihop tre tidigare kostnadsfiler.*

---

## Del 1 — Snabböversikt (tabell)


*En enda överblick. Detaljerad uppdelning och scenarier: ovan.*

### Total uppdelning

| # | Post | Komponent | Min (€) | Max (€) |
|---|---|---|---|---|
| 1 | **A. Burk — el** | Huvudprocessor (ESP32) | 5 | 15 |
| 2 | | LoRa-modul (868 MHz) | 8 | 25 |
| 3 | | 2,4 GHz-antenn (ESP-NOW) | 3 | 10 |
| 4 | | GPS-mottagare | 5 | 15 |
| 5 | **B. Sensorer** | Temperatur/tryck (primär) | 5 | 15 |
| 6 | | IMU (attityd/G-kraft) | 5 | 15 |
| 7 | | GPS (om ej i post 4) | 5 | 15 |
| 8 | | Kamera / fotosensor (valfritt) | 10 | 30 |
| 9 | | Magnetometer (valfritt) | 5 | 10 |
| 10 | **C. Ström** | 2S LiPo-batteri | 15 | 30 |
| 11 | | Strömhantering + strömbrytare | 5 | 15 |
| 12 | **D. Struktur** | Burk/fäste | 5 | 15 |
| 13 | | Fallskärm + linor + fäste | 10 | 25 |
| 14 | | Monteringsdetaljer (skruvar, distanser) | 5 | 10 |
| 15 | **E. Mark-RX** | Yagi-antenn (12–15 dBi) | 15 | 50 |
| 16 | | Mottagarmodul (RX) | 10 | 40 |
| 17 | | Gimbal (2-axlig) | 15 | 50 |
| 18 | | Styrkort + strömförsörjning | 10 | 30 |
| 19 | | PC-visualisering | 0 | 20 |
| 20 | **F. Verktyg** | Lödning/elektronik | 10 | 20 |
| 21 | | 3D-print/filament | 5 | 25 |
| 22 | | Testmaterial | 10 | 30 |
| 23 | **Reserv** | Extra komponenter (~10 %) | 20 | 55 |
| 24 | **Sträck** | Outreach, utskrifter, frakt | 0 | 60 |
| | | **TOTALT** | **~190** | **~555** |

### Typiska totalsummor

| Scenario | Totalt |
|---|---|
| **Sparsam grundversion** (ESP32 + LoRa + T/P + GPS + batteri + struktur + enkel yagi) | **≈ 150–260 €** ✅ |
| **Full version** (aktuell ESP-NOW + LoRa + sensorer + kamera + gimbal + yagi + verktyg + reserv) | **≈ 250–450 €** ✅ |
| **Budgettak (tävlingen)** | **≤ 500 €** |

### Efter komponent-grupp (block-summor)

| Block | Min (€) | Max (€) |
|---|---|---|
| A. Burk (el + antenner) | 50 | 130 |
| B. Sensorer | 30 | 90 |
| C. Ström | 20 | 45 |
| D. Struktur + fallskärm | 20 | 40 |
| E. Mark-RX | 40 | 150 |
| F. Verktyg/material | 30 | 100 |
| Reserv | 20 | 55 |
| Sträck | 0 | 60 |
| **Total** | **~190** | **~555** |

*Priserna är typiska EU-priser 2026 exkl. frakt/moms (~10–25 % extra). Uppdatera mot
faktura innan [Pre-Launch Report 20.2.2027](CANSAT-GRUND.md).*

---

## Del 2 — Detaljerad budget per block


*Sammanställd 2026-11-03. Budgetkrav från tävlingen: **≤ 500 € totalt**. Siffrorna är
typiska EU-priser (exkl. frakt) och får justeras mot faktura/leverantör. Se
[WIFI-FORSKNING.md §7](KOMMUNIKATION.md) för massbaksidan och husmonopol-detajjer.*

---

### Överblick

| Del | Intervall (€) | Kommentar |
|---|---|---|
| **A. Burken (elektronik + antenner)** | 50–130 € | ESP32, LoRa, GPS/IMU, monopol + antennfäste |
| **B. Sensorer (primär + sekundär)** | 30–90 € | T/P, IMU, GPS, ev. kamera |
| **C. Ström (batteri)** | 15–30 € | 2S LiPo |
| **D. Struktur + fallskärm** | 20–40 € | Mekanik, fästet, lina |
| **E. Mark-RX (antenn + gimbal)** | 40–150 € | Yagi, mottagare, gimbal, PC-ev. |
| **F. Verktyg/material (utveckling)** | 30–100 € | Lödning, 3D-print, test |
| **Reserv (~10 % )** | 20–55 € | Extra komponenter vid byte |
| **LÖSNING/STRÄCK**: Lokalt + utveckling | 0–60 € | Outreach, utskrifter, frakt |

---

### A. Burken (elektronik + antenner)

| Post | Typ-artikel | Pris | Massa |
|---|---|---|---|
| Huvudprocessor | ESP32 (WiFi + BLE), <5 €–15 € | 5–15 € | 5–15 g |
| LoRa-modul + monopol-antenn | 868 MHz, t.ex. SX1276/SX1262-modul | 8–25 € | 5–12 g |
| 2,4 GHz-antenn (ESP-NOW) | monopol/omni, IPEX | 3–10 € | 3–8 g |
| GPS-mottagare (om ej i sensorpaket) | NEO-6M/8M | 5–15 € | 3–10 g |
| **Del A, sparsam** | | **~50–80 €** | |
| **Del A, med dubbla radio + GPS-modul** | | **~100–130 €** | |

*Alternativ: Raspberry Pi Zero 2W (~30 €) istället för ESP32 — bara om man vill köra
WiFi-station/livevideo; för vår ESP-NOW + LoRa-lösning räcker ESP32.*

### B. Sensorer (primär + sekundär)

| Post | Typ-artikel | Pris |
|---|---|---|
| Primärmission (obligatorisk) | Temperatur- + trycksensor (BMP280/BME280) | 5–15 € |
| IMU (attityd/acceleration) | MPU-6050/ICM-20948 | 5–15 € |
| GPS (om ej i del A) | NEO-6M/8M | 5–15 € |
| Kamera / fotosensor (sekundär/valfritt) | liten JPEG-modul / fototransistor | 10–30 € |
| Magnetometer (valfritt) | HMC5883/MAG3110 | 5–10 € |
| **Del B** | | **~30–90 €** |

### C. Ström

| Post | Typ-artikel | Pris | Massa |
|---|---|---|---|
| Batteri | 2S LiPo ~7,4–11 Wh | 15–30 € | 50–70 g |
| Strömhantering + huvudströmbrytare | regulator/huvudknapp | 5–15 € | 5–10 g |
| **Del C** | | **~20–45 €** | |

### D. Struktur + fallskärm

| Post | Typ-artikel | Pris |
|---|---|---|
| Burk/struktur + fläktmönster | läskburk, fäste | 5–15 € |
| Fallskärm + linor + fäste (≥50 N) | CanSat-fallskärm | 10–25 € |
| Monteringsdetaljer | skruvar, distanser, ev. 3D-print | 5–10 € |
| **Del D** | | **~20–40 €** |

### E. Mark-RX (antenn + gimbal + PC)

| Post | Typ-artikel | Pris |
|---|---|---|
| Mark-RX-antenn | **Yagi 12–15 dBi** (868 MHz) eller 2,4 GHz-panel | 15–50 € |
| Mottagarmodul (RX) | LoRa/SX1268-modul + ev. SDR | 10–40 € |
| Gimbal (2-axlig) | hobby-servon/steppers + stativ | 15–50 € |
| Styrkort + strömförsörjning | Uno/ESP32 + PSU | 10–30 € |
| PC-visualisering | (befintlig PC räcker; loggning) | 0–20 € |
| **Del E** | | **~40–150 €** |

### F. Verktyg/material (utveckling — delas ofta mellan lag)

| Post | Typ-artikel | Pris |
|---|---|---|
| Löd/elektronik | lödstativ, tråd, krympslang | 10–20 € |
| 3D-print/filament | om laget har skrivare | 5–25 € |
| Testmaterial | multimeter, högtalare/blipp, extra x kretskort | 10–30 € |
| **Del F** | | **~30–100 €** |

---

### Två färdiga scenarier

#### Sparsam grundversion (endast obligatoriskt + robust nedlänk)
- ESP32 + LoRa-monopol + T/P-sensor + GPS + batteri + struktur + fallskärm + enkel RX-yagi.
- **≈ 150–260 €** ✅ — klarar 500 €-taket med god marginal.

#### Full version (aktuell dubbel-arkitektur)
- ESP32 + LoRa-monopol + ESP-NOW-2,4 GHz + T/P + IMU + GPS + kamera + batteri +
  struktur/fallskärm + gimbal + yagi-markantenn + verktyg + reserv.
- **≈ 250–450 €** ✅ — fortfarande under 500 €-taket.

> ✅ **Båda scenarier är under 500 €-taket.** Huvudrisker att ha marginal för: GPS-modul
> och markantenn (billigast att dubblera), samt eventuell seponerad komponent.

---

### Summor samlade

| Block | Min (€) | Max (€) |
|---|---|---|
| A. Burk (el + antenner) | 50 | 130 |
| B. Sensorer | 30 | 90 |
| C. Ström | 20 | 45 |
| D. Struktur + fallskärm | 20 | 40 |
| E. Mark-RX | 40 | 150 |
| F. Verktyg/material | 30 | 100 |
| **Grundsumma** | **190** | **555** |
| Reserv (~10 %) | 20 | 55 |
| Sträck (outreach/frakt) | 0 | 60 |
| **Totalt typfall** | **~210** | **~480** |

---

### Anteckningar / osäkerheter

- **Priser är intervall** baserade på typiska EU-lärceller (2026). Omfrakt och moms kan
  lägga ~10–25 % på slutsumman.
- **Markantennen kan bytas ned** (kollinär 3–5 dBi ~10–30 €) om man vill slippa gimbalen
  helt, men lägre gain → mindre marginal (§5.2).
- **Verktyg/maskiner (F) delas** ofta mellan gruppens lag → kan kvitta ut i verklig
  kostnad per lag.
- **Cloud chamber (om sekundärmission väljs):** egenbyggd passiv kylplatta ~60 € eller
  färdigt kit ~150 €+ — se [arkiv/CLOUD-CHAMBER.md](../arkiv/CLOUD-CHAMBER.md) §2. Det är en separat post om man
  väljer det, men **inryms i 500 €-taket** med sparsam grundversion.
- **Uppdatera mot faktura:** fyll i verkliga priser vartefter man köper; kontrollera att
  totalsumman håller sig ≤ 500 € innan Pre-Launch Report (20.2.2027).

---

*Se även [WIFI-FORSKNING.md §7](KOMMUNIKATION.md) (massbudget) och
[QA.md Del B](QA.md) (verifiering av siffror). Uppdatera mot faktiska inköp.*

---

## Del 3 — Markutrustningen i detalj


*Fokus: allt som behövs för **markmottagningen och gimbal-tracking** (burkens delar
ligger i ovan). Priser = typiska EU 2026 exkl.
frakt/moms. Uppdatera mot faktura.*

### Komponenter

| # | Post | Detaljer | Min (€) | Max (€) |
|---|---|---|---|---|
| 1 | **Markantenn — Yagi** | 12–15 dBi (868 MHz) — förstaval | 15 | 50 |
| 2 | Självvald alternativ antenn | 2,4 GHz-panel (10–20 dBi) | 20 | 60 |
| 3 | **Mottagarmodul** | LoRa-modul (t.ex. SX1268) | 10 | 40 |
| 4 | **Gimbal (2-axlig)** | hobby-servon/steppers + hållare | 15 | 50 |
| 5 | **Gimbal-styrkort** | ESP32/Uno + drivare | 10 | 30 |
| 6 | **Strömförsörjning (mark)** | PSU/batteri + kablage | 10 | 25 |
| 7 | **Stativ/fäste** | stativ för yagi + gimbal | 10 | 40 |
| 8 | **PC/loggningshårdvara** | (befintlig PC räcker; ev. adapter/SDR) | 0 | 60 |
| 9 | **Kablage/kontakter** | SMA/koax, ström, USB | 5 | 20 |
| 10 | **Reserv (mark)** | extra antenn/modul ~10 % | 10 | 30 |
| | **TOTALT (mark)** | | **~85** | **~350** |

### Typiska scenarier (mark)

| Scenario | Beskrivning | Totalt |
|---|---|---|
| **Enkel** | Yagi + mottagarmodul + styrkort, ingen/trivial gimbal | **~50–110 €** |
| **Standard** (rekommenderad) | Yagi 12–15 dBi + mottagarmodul + 2-axlig gimbal + stativ + ström + reserv | **~85–200 €** |
| **Full (med PC/SDR)** | Standard + SDR/adapter + fler reservantenner | **~150–350 €** |

### Summor per block (mark)

| Block | Min (€) | Max (€) |
|---|---|---|
| Antenn (yagi/patch) | 15 | 60 |
| Mottagning (modul/SDR) | 10 | 60 |
| Gimbal (servon + styrkort + drivare) | 25 | 80 |
| Stativ/fäste + ström + kablage | 25 | 85 |
| PC/loggning | 0 | 60 |
| Reserv | 10 | 30 |
| **Totalt (mark)** | **~85** | **~350** |

---

*Obs: mark-RX-förstärkning är laglig och oreglerad (ingen sändareffekt krävs), så
antennens pris bestämmer bara hur mycket link-marginal man får — en 12–15 dBi-yagi i
15–50 €-klassen räcker gott för vår lösning ([WIFI-FORSKNING.md §5.2](KOMMUNIKATION.md)).*

