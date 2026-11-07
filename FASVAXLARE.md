---
tags: [cansat, beamforming, komponenter, priser]
status: referens
updated: 2026-11-07
---

# Fasväxlare — vad som fungerar på 868 MHz och 2,4 GHz

*Fasväxlare är hjärtat i en analog beamforming-array. **Viktigast: kontrollera alltid frekvenstäckningen i databladet** — fel band är den dyraste fällan.*

---

## Del 1 — 868 MHz: begränsat utbud


*Undersökt 2026-11-06. Syfte: hitta en billig fasväxlare som faktiskt fungerar på
868 MHz, med styrkor/svagheter. **Läs §1 först — det finns en fälla.***

---

### 1. 🚨 Huvudfyndet: inga vanliga MMIC-fasväxlare täcker 868 MHz

Alla standardkretsar hos Digi-Key/Mouser börjar på **1,1–1,2 GHz**. 868 MHz ligger
*under* dem. Köper man på måfå får man en krets som inte fungerar.

#### ❌ Köp INTE dessa (fel frekvens)

| Komponent | Frekvens | Pris | Probleem |
|---|---|---|---|
| [HMC928LP5E](https://www.omo-ic.com/chip/f10/hmc928lp5e-analog-devices.html) (analog) | **2–4 GHz** | $22,84 (5k st) / **$118 (1 st)** | 2,3× för hög frekvens |
| [HMC936ALP6E](https://thepartsdirect.com/part/hmc936alp6e~analogdevices) (6-bit digital) | **1,2–1,4 GHz** | **$112–147** | Fel band + mycket dyr |
| [PE44820](https://psemi.com/products/rf-phase-amplitude-control/phase-shifters/pe44820/) (8-bit) | 1,7–2,2 GHz (utökad **1,1–3,0**) | — | 868 MHz < 1,1 GHz → utanför |
| [QPC2110](https://www.qorvo.com/products/p/QPC2110) (6-bit) | 8–11,5 GHz | — | Helt fel band |
| [HMC247](https://www.analog.com/en/products/hmc247-die.html) (analog die) | 5–18 GHz | — | Fel band + bare die |

**Prisexempel:** en HMC936 kostar **$112–147**. Fyra stycken (för 4 element) =
**$450–590** — hela budgeten på en komponent som *ändå inte fungerar*.

**Referens (för jämförelse av prestanda):**

| Komponent | Frekvens | Bit | IL | RMS fasfel | Styrning |
|---|---|---|---|---|---|
| HMC928LP5E | 2–4 GHz | analog | 3,5–4 dB | ±5° | 0–13 V |
| HMC936ALP6E | 1,2–1,4 GHz | 6 | låg (±0,5 dB variation) | 1,2° | 0/+5 V |
| PE44820 | 1,7–2,2 GHz | 8 | 6 dB | 1,0° | seriell/parallell |

---

### 2. ✅ Färdiga kretsar som faktiskt täcker 868 MHz

Bara **Daico** har färdiga kretsar i 500–1000 MHz:

| Komponent | Frekvens | Bit | Steg / max | IL | Effekt | Kapsel |
|---|---|---|---|---|---|---|
| [DPS42028](https://daico.com/control-components/phase-shifter-bi-phase-modulator/) | **500–1000 MHz** | 4 | 11,25° / **max 168,75°** | 2,1 dB | 13 dBm | DIP-38 |
| [DPS89082](https://daico.com/control-components/phase-shifter-bi-phase-modulator/) | **500–1000 MHz** | 8 | 1,4° / 358,6° | 4,4 dB | 13 dBm | SMA |

**Styrka:** fungerar direkt på 868 MHz, internmatchad 50 Ω.
**Svaghet:** Daico är militär/industri-försäljning — **inte på Mouser**, kräver offert.
DPS42028 ger bara **168,75°** (inte 360°). DPS89082 kräver **15 V / 200 mA** och SMA-kapsel.

---

### 3. ⭐ Rekommenderad väg: switched-line på PCB (billigast, beprövad)

[NASA:s översikt](https://ntrs.nasa.gov/api/citations/20080001449/downloads/20080001449.pdf)
beskriver switched-line som standardmetod under X-band. Principen: **växla mellan två
kabellängder** med RF-switchar. En äkta sann tidsfördröjning (true time delay).

#### 3.1 Matematiken för 868 MHz

$$
\lambda_0 = \frac{c}{f} = \frac{3\cdot10^{8}}{868\cdot10^{6}} = 34{,}6\ \text{cm}
$$

På FR4 ($\varepsilon_r \approx 4{,}4$, $\varepsilon_{\text{eff}} \approx 3{,}3$):

$$
\lambda_g = \frac{\lambda_0}{\sqrt{\varepsilon_{\text{eff}}}}
= \frac{34{,}6}{\sqrt{3{,}3}} \approx 19{,}0\ \text{cm}
$$

Kabellängd per bit:

$$
\Delta L = \lambda_g \cdot \frac{\Delta\varphi}{360°}
$$

| Bit | Fassteg | Kabellängd $\Delta L$ |
|---|---|---|
| 1 (LSB) | 22,5° | **1,19 cm** |
| 2 | 45° | 2,37 cm |
| 3 | 90° | 4,75 cm |
| 4 (MSB) | 180° | 9,50 cm |

**Fullt görbart på ett ~15 × 10 cm PCB.** (Jämför: [Monash-designen på 1,4 GHz](https://researchmgt.monash.edu/ws/portalfiles/portal/283732665/283161009_oa.pdf)
blev 10 × 6 cm med 4 bitar.)

#### 3.2 Switcharna som gör det billigt

| Switch | Frekvens | IL | Isolering | P1dB | IIP3 | Pris |
|---|---|---|---|---|---|---|
| [**PE4259**](https://octopart.com/part/psemi/4259-63) (SPDT) | 10 MHz–3 GHz | **0,35–0,6 dB** | 19–30 dB | 30,5 dBm | 55 dBm | **$0,11–0,89** ⭐ |
| [ADG918](https://www.analog.com/en/products/adg918.html) (SPDT, absorptiv) | DC–1 GHz | 0,8 dB @1GHz | **43 dB** @1GHz | — | — | $2,08 |
| [ADG919](https://www.analog.com/en/products/adg918.html) (SPDT, reflektiv) | DC–1 GHz | — | hög | — | — | ~$2 |
| [ADG901](https://octopart.com/part/analog-devices/ADG901BRMZ) (SPST) | DC–4,5 GHz | — | 40 dB @1GHz | 17 dBm | — | $2,67 |

#### 3.3 Kostnad

| Post | Antal | Pris | Summa |
|---|---|---|---|
| PE4259 (2 per bit × 4 bit) | 8 | $0,11–0,89 | **$1–5** |
| PCB (JLCPCB, 5 st) | 1 | $5–15 | $5–15 |
| **Per kanal** | | | **~$10–25** |
| **4 kanaler (4 element)** | | | **~$40–100** ✅ |

**Ryms i 500 €-budget.**

---

### 4. Styrkor och svagheter per val

#### PE4259 (huvudtips)
**Starka sidor:**
- **Extremt billig** (~$0,11–0,20 hos LCSC, ~$0,44–0,89 Digi-Key)
- Täcker 10 MHz–3 GHz med god marginal över 868
- Låg IL (0,35–0,6 dB) → liten systemförlust
- Hög linjäritet: **IIP3 55 dBm**, P1dB 30,5 dBm
- Snabb omkoppling (1,5 µs)
- Liten SC-70-6, lätt att löda

**Svaga sidor:**
- **Bara SPDT** → behöver 2 per bit (8 totalt för 4 bitar)
- Isolering "bara" ~19–30 dB → läckage mellan vägarna ger fasfel
- Passiv → adderar förlust (dock liten)
- Kräver **egen PCB-design** (mikrostripp, 50 Ω)

#### ADG918 / ADG919
**Starka sidor:**
- **43 dB isolering** @1 GHz — mycket bättre än PE4259 → mindre fasfel
- <1 µA strömförbrukning
- Absorptiv (ADG918) = bättre impedansmatchning
- Enkel CMOS/LVTTL-styrning, ingen extern kringelektronik

**Svaga sidor:**
- Bara DC–1 GHz (räcker till 868, men liten marginal)
- Dyrare: ~$2/st → **$16** för 8 st

#### Varaktor (analog, kontinuerlig) — alternativ C
En [publicerad design på 900 MHz med FR4](https://doi.org/10.1109/icmmt.2007.381435)
(branchline-koppling + 2 varaktorer) ger:

- **115° kontinuerlig** fasvridning
- **IL < 1,5 dB**
- **RL > 15 dB**

**Starka sidor:** kontinuerlig (inte stegvis), få komponenter, billiga varaktorer, låg förlust.

**Svaga sidor:** bara ~115° per enhet (kaskad behövs för 360°); **starkt frekvens- och
temperaturberoende**; kräver noggrann trimmning; svårare att kalibrera än digital.

---

### 5. Jämförelse av alla vägar

| Väg | Frekvens OK? | Kostnad (4 elem) | Svårighet | Rekommendation |
|---|---|---|---|---|
| HMC936ALP6E | ❌ (1,2–1,4) | $450–590 | lätt att använda | **köp ej** |
| PE44820 | ❌ (≥1,1) | — | lätt att använda | **köp ej** |
| Daico DPS42028 | ✅ | offert (dyrt) | lätt | bara om budget finns |
| **Switched-line + PE4259** | ✅ | **$40–100** | medel (PCB) | ⭐ **bästa vägen** |
| Switched-line + ADG918 | ✅ | ~$80–120 | medel (PCB) | bra om isolering viktig |
| Varaktor branchline | ✅ | $20–60 | medel–hög | bra för kontinuerlig |
| Fasta SMA-kablar (byta manuellt) | ✅ | ~$0 | trivialt | proof-of-concept |

---

### 6. Praktisk inköps- och byggplan

1. **Köp inte en fasväxlare-IC förrän du verifierat frekvensen.** Allt över 1,1 GHz går bort.
2. **Beställ 10 × PE4259** (kostar ~$2–9 totalt) — billigt nog att experimentera med.
3. **Bygg en 1-bit (180°) först** på ett litet PCB. Mät S21-fas i VNA (eller lånad VNA).
   - Om fasen växlar ~180° vid 868 MHz → konceptet fungerar.
4. **Kalibreringen är det verkliga jobbet**, inte kretsen:
   - varje kabellängd måste mätas (ΔL noggrannhet ~±0,5 mm för <1° fel),
   - switcharnas isolering ger fasfel,
   - temperatur påverkar FR4 ($\varepsilon_r$ driver).
5. **Bygg sedan 4 bitar**, verifiera 16 tillstånd, och kaskadkoppla.

#### Kalibreringsnoggrannhet (varför det är svårt)

$$
\Delta\varphi = \frac{2\pi}{\lambda_g}\Delta L
\quad\Rightarrow\quad
\Delta L = \frac{\Delta\varphi \cdot \lambda_g}{2\pi}
$$

För $\Delta\varphi = 1°$ vid $\lambda_g = 19$ cm:

$$
\Delta L = \frac{(\pi/180)\cdot 0{,}19}{2\pi} \approx 0{,}53\ \text{mm}
$$

Alltså: **kabellängderna måste hållas inom ~0,5 mm** för 1° noggrannhet. Det är fullt
görbart med PCB-mikrostripp (där längden är exakt definierad av layouten) — men inte med
handklippta koaxialkablar.

---

### 7. Källor

- [Analog Devices — HMC928LP5E / HMC929 / HMC936 lansering (fasväxlare, frekvenser)](https://www.microwavejournal.com/articles/16352-hmc928lp5e-hmc929lp4e-hmc936lp6e-mmic-phase-shifters)
- [Analog Devices — HMC936A datablad (1,2–1,4 GHz, 6-bit)](https://www.analog.com/en/products/hmc936a.html)
- [pSemi — PE44820 datablad (8-bit, 1,7–2,2 GHz, utökad 1,1–3,0)](https://www.psemi.com/pdf/datasheets/pe44820ds.pdf)
- [Qorvo — QPC2110 (8–11,5 GHz)](https://www.qorvo.com/products/p/QPC2110)
- [Daico — fasväxlare, parametertabell (DPS42028/DPS89082, 500–1000 MHz)](https://daico.com/control-components/phase-shifter-bi-phase-modulator/)
- [NASA/TM—2007-214906 — Array Phase Shifters: Theory and Technology (switched-line)](https://ntrs.nasa.gov/api/citations/20080001449/downloads/20080001449.pdf)
- [Monash — 1,4 GHz lågkostnads PIN-diodfasväxlare (4-bit, IL <2 dB, RMS <1°)](https://researchmgt.monash.edu/ws/portalfiles/portal/283732665/283161009_oa.pdf)
- [ICMMT 2007 — lågförlust varaktor-fasväxlare på 900 MHz (115°, IL <1,5 dB)](https://doi.org/10.1109/icmmt.2007.381435)
- [Octopart — PE4259 pris/stock (SPDT, 10 MHz–3 GHz)](https://octopart.com/part/psemi/4259-63)
- [Analog Devices — ADG918/ADG919 (SPDT, DC–1 GHz, 43 dB isolering)](https://www.analog.com/en/products/adg918.html)
- [Octopart — ADG901 (SPST, DC–4,5 GHz)](https://octopart.com/part/analog-devices/ADG901BRMZ)

---

*Levande dokument. Uppdatera med faktiska mätresultat när ni bygger. Verifiera alltid
frekvenstäckningen i databladet innan köp — det är den vanligaste och dyraste fällan.*

---

## Del 2 — 2,4 GHz: gott utbud


*Undersökt 2026-11-06. Komplement till del 1 i denna fil.
**Goda nyheter: 2,4 GHz är mycket bättre täckt än 868 MHz** — här finns riktiga färdiga
kretsar i rimlig prisklass.*

---

### 1. Färdiga fasväxlare som täcker 2,4 GHz

| Komponent | Frekvens | Bit | Steg | IL | RMS-fasfel | Styrning | Kapsel | Pris (1 st) |
|---|---|---|---|---|---|---|---|---|
| ⭐ **MACOM MAPS-010144** | **2,3–3,8 GHz** | 4 | 22,5° | **2,5 dB** | 2,2° | seriell/parallell | 4 mm PQFN-24 | **$35,25** |
| **MACOM MAPS-011019** | **2,4–5,1 GHz** | 6 | 5,625° | 4,5 dB | 4,0° | seriell/parallell | 4 mm PQFN-24 | ej verifierat |
| **Qorvo TGP2108-SM** | **2,5–4 GHz** ⚠️ | 6 | 5,625° | 5 dB | <2° | 0/+3…+5 V | 5×5 mm QFN | ej verifierat |
| **ADI HMC928LP5E** (analog) | **2–4 GHz** | analog | kontinuerlig 450° | 3,5–4 dB | ±5° | 0–13 V analog | 32-QFN 5×5 | **$71,88** |
| pSemi PE44820 | 1,7–2,2 (utökad 1,1–3,0) | 8 | 1,4° | 6 dB | 1,0° | seriell/parallell | 32-L QFN 5×5 | ej verifierat |

#### 1.1 Prisexempel (verifierade)

| Komponent | 1 st | 10 st | 100 st | 5 000 st |
|---|---|---|---|---|
| MAPS-010144 | $35,25 | $30,23 | **$27,00** | — |
| HMC928LP5E | $71,88 | — | $48,85 | **$22,84** |

Källor: [MAPS-010144 (datasheets.com)](https://www.datasheets.com/macom/maps-010144-tr0500), [HMC928LP5E (alldatasheet)](https://www.alldatasheet.com/distributor/view.jsp?Searchword=MC928)

---

### 2. ⚠️ Varningar innan köp

#### TGP2108-SM börjar på 2,5 GHz
**2,4 GHz ligger 100 MHz UNDER dess spec.** Den kan fungera i praktiken (prestanda
degraderar gradvis utanför bandet), men du är utanför garanterat område.
**Köp inte utan att mäta först.**

#### PE44820 kräver "utökad" drift
Nominellt 1,7–2,2 GHz. 2,4 GHz ligger i det **utökade** området (1,1–3,0 GHz) som bara
gäller **narrowband** enligt appnot 45. Dessutom IL 6 dB — sämst i klassen.

#### HMC928LP5E är dyr vid enstaka köp
$71,88 för 1 st, men $22,84 vid 5 000 st. Bra krets (analog, kontinuerlig 450°) men
priset straffar små ordrar.

#### Negativ spänning
MAPS-010144 kräver **VEE = −5,0 V** utöver VCC 3,0–5,5 V. En liten laddningspump
(t.ex. ICL7660, ~$1) löser det. TGP2108-SM är enklare: **bara 0/+3…+5 V**.

---

### 3. 🏆 Rekommendation: MAPS-010144

| Egenskap | Värde | Varför det spelar roll |
|---|---|---|
| **IL bara 2,5 dB** | lägst av alla | minst systemförlust |
| 2,3–3,8 GHz | 2,4 GHz **100 MHz in** i bandet | god marginal, ingen tvekan |
| **Integrerad CMOS-drivare** | slipper extern logik | bara matning + 4 styrpinnar |
| 50 Ω internmatchad | inga externa komponenter | enkel layout |
| IIP3 47 dBm, P1dB 25 dBm | hög linjäritet | tål starka signaler |
| RMS fasfel 2,2° | bra noggrannhet | litet strålfel |
| 4×4 mm PQFN-24 | liten | ryms lätt |
| **$35,25** (100 st: $27) | överkomligt | 4 kanaler = $141 |

**Fullständig spec:** 360° i 22,5°-steg, VSWR 1,3:1, TRISE/TFALL 50 ns,
VCC 3,0–5,5 V, VEE −5,0 V, kontrollström 1 µA, quiescent 2 µA, −40…+85 °C.
Se [MACOM-databladet](https://cdn.macom.com/datasheets/MAPS-010144.pdf).

#### Alternativ om man vill ha 6 bitar
**MAPS-011019** (2,4–5,1 GHz, 6 bit, 5,625° steg) — bättre upplösning, men IL 4,5 dB
och 2,4 GHz ligger i **underkanten** av bandet. Kolla pris innan.

---

### 4. 💡 Den stora fördelen med 2,4 GHz: switched-line blir 2,8× mindre

Bygger man själv (som diskuterat för 868 MHz) är 2,4 GHz **mycket mer kompakt**.

$$
\lambda_g = \frac{\lambda_0}{\sqrt{\varepsilon_{\text{eff}}}}
= \frac{12{,}5\ \text{cm}}{\sqrt{3{,}3}} = 6{,}88\ \text{cm}
$$

*(FR4, $\varepsilon_r \approx 4{,}4$, $\varepsilon_{\text{eff}} \approx 3{,}3$)*

#### 4.1 Kabellängd per bit

| Bit | Steg | **2,4 GHz** | 868 MHz |
|---|---|---|---|
| 1 | 22,5° | **0,43 cm** | 1,19 cm |
| 2 | 45° | **0,86 cm** | 2,37 cm |
| 3 | 90° | **1,72 cm** | 4,75 cm |
| 4 | 180° | **3,44 cm** | 9,50 cm |
| **Totalt (4 bitar)** | 337,5° | **6,45 cm** | 17,8 cm |

En komplett 4-bit switched-line ryms alltså på ett **litet PCB** — mot 17,8 cm på 868 MHz.

#### 4.2 Switcharna fungerar

**PE4259** (10 MHz–3 GHz) täcker 2,4 GHz med marginal. IL 0,35–0,6 dB, isolering
19–30 dB, P1dB 30,5 dBm, IIP3 55 dBm, **$0,11–0,89**.
Se del 1 i denna fil §3.

#### 4.3 Kostnadsjämförelse

| Väg | Kostnad per kanal | Arbete |
|---|---|---|
| **MAPS-010144** (färdig) | **$35,25** | minimalt |
| DIY switched-line + PE4259 | **$10–25** | mycket (PCB-design, kalibrering) |

**För 4 kanaler:** MAPS-010144 = $141 · DIY = $40–100 + många timmar.

---

### 5. Kalibreringstolerans

$$
\Delta L = \frac{\lambda_g}{360°} = \frac{68{,}8\ \text{mm}}{360}
= \mathbf{0{,}19\ \text{mm per grad}}
$$

Jämför 868 MHz: 0,53 mm/grad. **Tuffare på 2,4 GHz**, men fullt görbart med
PCB-mikrostripp eftersom längden definieras exakt av layouten — inte av handklippta
koaxialkablar.

---

### 6. Sammanställning: vad ska man välja?

| Situation | Val |
|---|---|
| **Vill ha det att bara fungera** | **MAPS-010144** ($35,25) ⭐ |
| Vill ha 6 bitars upplösning | MAPS-011019 (kolla pris) |
| Vill ha kontinuerlig analog styrning | HMC928LP5E (dyr vid 1 st) |
| Har tid och vill lära sig | DIY switched-line + PE4259 |
| Budget under $30 totalt | DIY är enda vägen |

**För CanSat-projektet:** MAPS-010144 är det sunda valet — $35 per kanal, 2,5 dB
förlust, integrerad drivare, och 2,4 GHz ligger bekvämt inne i bandet.

---

### 7. Källor

- [MACOM MAPS-010144 — 4-bit, 2,3–3,8 GHz (datablad)](https://cdn.macom.com/datasheets/MAPS-010144.pdf)
- [MACOM MAPS-010144 — produktsida/specifikation](https://www.macom.com/products/product-detail/MAPS-010144)
- [MACOM MAPS-011019 — 6-bit, 2,4–5,1 GHz](https://www.macom.com/products/product-detail/MAPS-011019)
- [MAPS-010144-TR0500 — priser ($35,25 / $27 vid 100)](https://www.datasheets.com/macom/maps-010144-tr0500)
- [Qorvo TGP2108-SM — 6-bit, 2,5–4 GHz](https://www.qorvo.com/products/r/ra004543)
- [Qorvo — parametertabell för alla fasväxlare (13 st)](https://www.qorvo.com/products/control-products/phase-shifters/parametric-table)
- [Analog Devices HMC928LP5E — analog, 2–4 GHz](https://www.omo-ic.com/chip/f10/hmc928lp5e-analog-devices.html)
- [pSemi PE44820 — 8-bit, 1,7–2,2 GHz (utökad 1,1–3,0)](https://psemi.com/products/rf-phase-amplitude-control/phase-shifters/pe44820/)

---

*Levande dokument. Verifiera pris och lagerstatus hos Digi-Key/Mouser innan köp — de
flesta av dessa kretsar har 10–26 veckors ledtid.*

