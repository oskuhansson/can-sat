---
tags: [cansat, radio, antenn, länkbudget, polarisation]
status: aktuell
updated: 2026-11-07
---

# Kommunikation: monopol-antenn i burken + markgimbal — forskningsöversikt

*Uppdaterad 2026-11-07. **Aktuellt fokus:** CanSaten sänder en **nedlänk-beacon** med en
**enkel monopol-antenn** inuti burken, medan marken använder en **hög-gain-antenn på en
gimbal** som följer burken (GPS + RSSI). Hela lösningens tyngd ligger på marken; burken
är minimal och robust med plats för sensorer. Dokumentet började som en
WiFi-hotspot/relä-undersökning — de delarna är arkiverade i
[arkiv/KOMMUNIKATION-HISTORIK.md](../arkiv/KOMMUNIKATION-HISTORIK.md).*

---

## A. Aktuell design (sammanfattning)

```
 Burken: Tx-monopol (omni) ──►  Mark: high-gain-antenn + gimbal-tracker ──►  PC/logg
 868 MHz LoRa (25 mW e.r.p.)      12–23 dBi-yagi (eller medeldish)          RSSI + telemetri
                                  GPS + RSSI-baserad följning
```

- **Designen i korthet:** **§5** (fokuserad design: monopol + markgimbal), **§6**
  (mark-RX-antennval), **§6.1** (dish + GPS) och **§7** (anslutningslös dubbel:
  ESP-NOW broadcast + LoRa-backup).
- **Länkbudget:** 868 MHz LoRa ger 60–80 dB marginal över nedfärden (§5.2);
  2,4 GHz ~25–30 dB.
- **Regler:** nedlänk (och upplänk) är licensfria i Finland om utrustningen är CE-godkänd
  och håller sig inom effekt-/sändningstidsgränserna (§2). RX-gain på marken är oreglerad.
- **Begrepp:** upplänk/nedlänk, dBm, EIRP vs ERP, antennförstärkning — förklaras i §3.

**Innehåll:**

| Del | Sektion | Vad |
|---|---|---|
| **1** | §1–§7 | **Den aktuella designen** ⭐ |
| **2** | — | Mark-RX-antennprojektet (snabböversikt) |
| **3** | — | Polarisation och antennmönster i burken |
| — | Källor | Källförteckning |

---


> **Var hittar jag vad?** Detta dokument beskriver den **aktuella designen**.
> Äldre bakgrund (WiFi-hotspot-idén, relä-konceptet, massbudget) finns i
> [arkiv/KOMMUNIKATION-HISTORIK.md](../arkiv/KOMMUNIKATION-HISTORIK.md).
> Grundbegrepp finns i [RADIOTEKNIK.md](RADIOTEKNIK.md).

---

## Del 1 — Designen

### 1 Relä vs nedlänk-only — avvägningen

> **Historisk not:** detta var bedömningen när *relä-idén* utreddes. Vi valde senare
> **nedlänk-only med monopol i burken + gimbal på marken** (se §5). Avsnittet sparas
> som beslutsunderlag — det förklarar varför reläet valdes bort.

- **Starkt uppdrag:** robust (markantenner kompenserar burkens begränsningar), beprövat
  (CanSat 2003, AO-91/ISS), regelmässigt enkelt (licensfritt, cross-band), pedagogiskt
  med det klassiska "satelliten reläerar mellan två stationer", och det kräver nästan
  ingen volym/massa i burken → gott om plats för sensorer.
- **Rekommenderad bärlinje:** **868 MHz LoRa till modul + 12 dBi yagi på vardera
  markstation, cross-band (868 upp / 2,4 ner) eller store-and-forward**, betyg-målet
  "teknisk demonstration av satellitkommunikation" — med ett explicit verifierat bevis
  (meddelande + RSSI + GPS) snarare än "live bredband".
- **Förbättringar jämfört med hotspot-versionen:** ingen live-timing-stress
  (store-forward + alla nedfärdsminuter), inga telefoner att jaga, markantenner = godtycklig
  förstärkning, och den adresserar exakt målgruppens kärnfråga ("varför behövs en satellit?").

### 2 Är upplänk olaglig i Finland? — nej, det är en vanlig missuppfattning ✅

**Kort svar: upplänk är fullt tillåten i Finland** på de licensfria banden — både från
marken (upplänk) och från burken (nedlänk). Reglerna begränsar **effekten och
sändningstiden**, inte att man "får sända".

Vad som kan ha fört dig vilse: *vissa* radiosammanhang kräver tillstånd:
- **Amatörradio** (OH-anropssignaler, repeater) kräver ett **amatörradio-tillstånd**
  ([Traficom: radioamatööritoiminta](https://traficom.fi/fi/radioluvat-ja-taajuudet/radiotaajuuksien-kaytto/radioamatooritoiminnan-patevyydet-ja-taajuudet))
  — men **det är inte det som behövs här**.
- **Licensfria "kollektiva frekvenser"** ("yhteistaajuudet"/"luvasta vapaat") kräver
  **inget tillstånd** — bara att utrustningen är CE-godkänd och håller sig inom effekt-
  och sändningstidsgränserna. Traficoms määräys ([Regulation 15 AR/15AV](https://www.traficom.fi/files/media/regulation/Regulation%2015AV2025M.pdf),
  aktuell version från 31.3.2025/2026) definierar exakt detta.

**Vad som är tillåtet för vår burk (licensfritt, inget tillstånd):**

| Band | Max strålad effekt | Sändningstid (duty cycle) | Källa |
|---|---|---|---|
| 868 MHz SRD, 868,0–868,6 MHz (LoRa-standard) | **25 mW e.r.p.** (≈14 dBm) | **≤1 %** (≈36 s/h) | [Finlex määräys §10.1](https://www.finlex.fi/api/media/authority-regulation/535594/mainPdf/main.pdf?timestamp=2025-03-26T22%3A00%3A00.000Z&typeDiscriminator=traficom-communications), [The Things Network](https://www.thethingsnetwork.org/docs/lorawan/regional-limitations-of-rf-use/) |
| 868 MHz SRD, 869,4–869,65 MHz (sub-band P) | **500 mW e.r.p.** | ≤10 % | [CEPT EFIS](https://efis.cept.org/adhoc_grabber.jsp?annex=4) |
| **2,4 GHz WLAN/WAS-RLAN** | **100 mW EIRP (20 dBm)** | ingen (driftcykel) krav | [Traficom §9.1](https://www.traficom.fi/files/media/regulation/Regulation%2015AV2025M.pdf) |

Viktigt: **användning i luften är explicit tillåten** för både SRD (868 MHz) och WLAN
(2,4 GHz) — "Käyttö on sallittu myös ilmassa olevassa ilma-aluksessa" (§10.1 och §9.1 i
määräyksen). Alltså är **både upplänk och nedlänk lagliga**, även från en flygande burk.

> ⚠️ Obs: effektgränserna är för **varje sändare** (hela systemet = sändare + antenn +
> kabel). En **förstärkare får inte kopplas** mellan sändare och antenn om inte hela
> sammansättningen är CE-godkänd tillsammans ([määräys §4](https://www.traficom.fi/files/media/regulation/Regulation%2015AV2025M.pdf)).
> Använd därför **CE-märkta moduler med inbyggd/medföljande antenn** och beräkna att
> helheten håller sig under taket (ingen extern "booster").

### 3 Begrepp förklarade (radioteknik för nybörjare) 📖

- **Upplänk / nedlänk** — två riktningar i en radiokommunikation:
  - **Upplänk (uplink):** sändning *från marken till burken* (t.ex. mark A sänder "HELLO").
  - **Nedlänk (downlink):** sändning *från burken till marken* (t.ex. burken återsänder
    "HELLO via CanSat" till mark B).
  Tänk: "upplänk = kunden pratar, nedlänk = satelliten svarar".
- **dB, dBm, dBi, dBd, ERP, EIRP** (enheter för effekt/förstärkning):
  - **dB (decibel):** logaritmiskt mått på förhållande — 10 dB = 10×, 20 dB = 100×.
  - **dBm:** effekt i dB **relativt 1 mW**. +10 dBm = 10 mW, +20 dBm = 100 mW,
    +30 dBm = 1 W.
  - **dBi / dBd:** **antennförstärkning** mot två referensantenner. **dBi** mot en
    isotrop antenn (används på 2,4 GHz i EIRP-regeln); **dBd** mot en halvvågsdipol
    (används på 868 MHz i e.r.p.-regeln). **dBd = dBi − 2,15** — en "3 dBi-antenn" är
    alltså bara ~0,85 dBd.
  - **EIRP:** sändareffekt + antenn (dBi) − kabel = "strålad effekt som om antennen vore
    isotrop". En 16 dBm-sändare med 3 dBi-antenn → 19 dBm EIRP.
  - **ERP:** samma men mot dipol (dBd): **ERP = EIRP − 2,15 dB**. Därför är 25 mW ERP
    = ~40 mW EIRP; och 25 mW e.r.p. ≈ **14 dBm ERP ≈ 16 dBm EIRP**.
- **"Antennen för att förstärka" — vad gain faktiskt gör:** en passiv antenn *förstärker
  inte* — den **riktar om** energi. En yagi/dish koncentrerar utstrålningen i en smal
  stråle i stället för att strunta åt alla håll.
  - **TX-riktning (upplänk):** antennens gain läggs TILL i EIRP/ERP-taket → med hög
    gain-antenn måste man **sänka sändareffekten** för att hålla sig under taket.
    Vinsten: energin koncentreras dit den ska (bättre räckvidd åt rätt håll).
  - **RX-riktning (nedlänk):** **ingen laggräns alls** — mottagarantennens gain höjer
    bara mottagningskänsligheten ("syn" för svaga signaler) och kostar inget i
    effektlagstiftningen. Det är därför **markantenna på nedlänken görs så stor som
    möjligt (12–23 dBi)** medan burken kan nöja sig med en liten antenn.
  - **Slutsats:** "använd antennen för att förstärka" passar perfekt för **nedlänken** —
    du kan inte öka utsändningseffekten med en markantenn, men du kan höja
    mottagningskänsligheten nästan hur mycket som helst.
- **Radiated power / säteilyteho:** per Traficom = sändareffekt + antennförstärkning
  − kabel-/konnektorförlust ([määräys §6](https://www.traficom.fi/files/media/regulation/Regulation%2015AV2025M.pdf)).
- **Duty cycle (toimintasuhde):** andel av tiden en sändare får vara igång under en
  timme ([määräys §6](https://www.traficom.fi/files/media/regulation/Regulation%2015AV2025M.pdf),
  [The Things Network](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)).
  ≤1 % = max 36 s sändning/timme; ett LoRa-paket är 50–200 ms, så med ~1 s intervall och
  få paket klarar man det lätt. Viktigt att programvara räknar ihop lufttiden.
- **Länkbudget / link budget och känslighet:** mottagen effekt = EIRP(sändare) − FSPL
  + mottagarantenn. **Känslighet** = lägsta signalstyrka en mottagare kan tolka (ju
  lägre siffra, desto bättre): LoRa ≈ −120…−137 dBm, WiFi ≈ −85…−90 dBm. [S. Hum, Satellite
  Links](https://www.waves.utoronto.ca/prof/svhum/ece422/notes/23-satellite.pdf): uplink
  och downlink räknas alltid separat.

### 4 Nedlänk-only ("beacon") — den enklaste, helt lagliga varianten

Om du *vill* slippa upplänk och bara låta **burken sända** (beacon/telemetri) medan
marken tar emot med höga antenner — det är fullt tillåtet och robust:

- Burken sänder på 868 MHz (eller 2,4 GHz) med CE-modul, t.ex. LoRa-paket med
  temperatur/tryck/IMU + ID var ~1 s (inom duty cycle med korta paket).
- Två markstationer har **12–23 dBi-yagis** för att ta emot nedlänken extremt bra
  (RX-gain är fri — ingen laggräns).
- Mät och jämför: RSSI (signalstyrka) i båda ändarna, effekten av antenn/förstärkning,
  hur mottagningen varierar under nedfärden. Det blir en **mätbar "downlink-vetenskap"**
  (jämför omni vs yagi, avstånd vs signalstyrka).
- Vad man tappar mot relä-versionen: **ingen tvåpunkts-reläfunktion** — bägge stationerna
  lyssnar på samma utsändning i stället för att prata genom burken.

**Beslutsregel:** vill ni *beviset "satelliten reläerar mellan två stationer"* krävs
upplänk (868/2,4 GHz — laglig, se ovan). Vill ni istället ha *enkel och vattentät nedlänk*
(markantenner förstärker mottagningen) — kör beacon-lösningen. Båda är lagliga; valet
bestäms av vilken fråga som ska demonstreras.

### 5 Fokuserad design: monopol i burken + high-gain-antenn på marken med gimbal 🎯

*Det här är den variant som fokuseras i analysen: **burken har en enkel monopolantenn**
(omni), och **marken har en high-gain-antenn (t.ex. 12–23 dBi-yagi/patch) som sitter
på en gimbal** som följer burken under nedfärden. Allt svårt och tungt ligger på marken;
burken förblir minimal och robust.*

#### 5.1 Varför denna arkitektur är rätt val

- **Burken = enkel monopol (omni).** En monopolantenn är en rak tråd/pinne (~λ/4
  vertikalt ovanför en motviktsplatta) som strålar åt alla sidor — **ingen riktning,
  ingen pekning, inget gimbal i burken**. Den är billig (<5 €), tålig och klarar
  20–30 G + rotation under fallskärm utan att tappa kontakten (en riktad antenn skulle
  förlora signalen vid burkens rotation).
- **High-gain på marken.** En 12–23 dBi-yagi/patch på marken har **ingen storleks-,
  vikt- eller effektbegränsning** och ingen lagbunden RX-gräns (RX-gain är fri, §3).
  Med 23 dBi får man ~100× mottagarkänslighet jämfört med en enkel stav — det är
  *marken* som gör den tunga lyftkraften.
- **Gimbal på marken.** Där burkgimbalen (pan-tilt i 66 mm-burk + servon som ska klara
  20 G + rotation) var det svåraste i arkivets §5, är **markgimbalen trivial**: den står på ett
  stativ, drivs av vanliga hobby-servon/steppers och får väga hur mycket som helst. Den
  behöver bara rotera två axlar (azimut + elevation) för att följa burken.

#### 5.2 System och link budget

```
 Burken: Tx-monopol (omni)  ──►  Mark: high-gain-antenn + gimbal-tracker ──►  PC/logg
 868 MHz (eller 2,4 GHz)         12–23 dBi yagi på gimbal                  RSSI + telemetri
 25 mW / 20 dBm EIRP              GPS/RSSI-baserad följning
```

**Nedlänk-budget med burkens monopol (0–2 dBi) som sändare:**

| Steg | 868 MHz (LoRa) | 2,4 GHz (WiFi) |
|---|---|---|
| EIRP (max laglig) | **+16 dBm** (25 mW e.r.p.) | **+20 dBm** (100 mW EIRP) |
| FSPL vid 1,5 km slantavstånd | **−94,7 dB** | **−103,6 dB** |
| Markantenn 15 dBi (yagi, default) | +15 dBi | +15 dBi |
| Markantenn 23 dBi (dish) | +23 dBi | +23 dBi |
| **Mottaget, 15 dBi-yagi** | **~−64 dBm** | **~−69 dBm** |
| **Mottaget, 23 dBi** | **~−56 dBm** | **~−61 dBm** |
| Känslighet | −120…−137 dBm (LoRa) | −85…−90 dBm (WiFi) |
| **Marginal, 15 dBi** | **~56–73 dB** | **~16–21 dB** |
| **Marginal, 23 dBi** | **~64–81 dB** | **~24–29 dB** |

FSPL räknas som $32{,}44 + 20\log_{10}(f_{\text{MHz}}) + 20\log_{10}(d_{\text{km}})$
(se [rftools](https://rftools.io/calculators/rf/rf-link-budget/)).

> **Rättelse 2026-11-07:** en tidigare version angav FSPL **85 dB** för 868 MHz vid 1,5 km.
> Det var ~10 dB för lågt — korrekt värde är **94,7 dB**. Tabellen och marginalerna är
> omräknade. Slutsatsen står kvar: länken är rejält överdimensionerad.

→ Med monopolburk + **15 dBi-yagi** på 868 MHz finns **~56–73 dB marginal** över hela
nedfärden (mer med dish eller högre SF) — man kan till och med sänka effekten eller
använda mindre antenn. På 2,4 GHz med **WiFi-känslighet** är marginalen ~16–29 dB,
fortfarande robust. **Med LoRa 2,4 (SX1280, −132 dBm) blir den ~60 dB** — se
[PROTOKOLL.md](PROTOKOLL.md).

#### 5.3 Gimbalkrav och pekprecision

- **Två axlar (azimut + elevation):** burken faller från ~1 km till marken. Elevationen
  går från ~90° (apogeum rakt ovanför) ned mot några grader vid landning; azimuten beror
  på var markstationen står. En vanlig hobby 2-axlig pan-tilt räcker för en lätt yagi;
  en 12–23 dBi-yagi väger 0,3–1 kg → använd en tyngre metalstation
  ([OES PT60-klass](https://www.oesincorp.com/motorized-multi-axis-stages/motorized-pan-tilt-mounts.htm))
  eller en egenbyggd stepper-hållare.
- **Krävd pekprecision ≈ halva strålvinkeln:** en 23 dBi-yagi på 868 MHz har en stråle
  på ~10–15° (HPBW), en 12 dBi ~50°×40°. Med 12–23 dBi räcker ett pekfel på ±2–5°.
- **Styrdata:** följ burken via **telemetrin burken redan sänder** — RSSI-styrkan ger
  ett "peak"-spår för gimbalen; alternativt position/IMU från GPS i telemetrin och en
  beräknad vinkel. Bäst: kombination (GPS-prognos + RSSI-peak) för robust följning även
  vid fallskärmssvängning.
- **Uppdateringstakt:** burken faller 8–11 m/s; vinkeländringen är snabbast nära marken.
  1–5 Hz uppdatering räcker gott; markgimbalen behöver bara några grader/s.

#### 5.4 Fördelar och vad man får ut

1. **Robusthet först:** monopol i burken = inget som kan peka fel, klara 20–30 G och
   rotation; all komplexitet ligger i markens gimbal som är enkel att bygga/testa hemma.
2. **Laglighet enkel:** nedlänk-only (beacon) med fri RX-gain på marken (§2); ingen
   upplänk krävs (men den är laglig om ni vill testa senare).
3. **Plats för sensorer i burken:** monopolen tar minimal plats (en tråd/pinne) → gott
   om plats för elektronik/sensorer (arkivets §7).
4. **Mätbar vetenskap:** logga RSSI över tid från gimbalens mottagare + GPS-position i
   telemetrin → beräkna fri-rums-förlust, verifiera antennförstärkningen, visa när
   mottagningen var bäst — ett riktigt "downlink-tracking"-uppdrag.
5. **Showcase:** en markbaserad antenn-tracker som följer en fallande CanSat är i sig en
   imponerande teknikdemonstration (jfr. riktiga markstationer för satelliter).

#### 5.5 Nackdelar / att vara ärlig om

- **Inte ett "relä mellan två punkter"** — det är en enkelriktad mottagning i en marken
  (eller flera mottagarstationer utan reläfunktion).
- **Flera markstationers värde sjunker:** en gimbal pekar på burken åt gången; "två
  stationer pratar genom satelliten" faller bort (kräver upplänk, §1/§2).
- **Fallskärmssvängning:** burken gungar/roterar, men eftersom monopolen är omni spelar
  det ingen roll för sändningen — enda följden är att RSSI varierar lite.
- **868 MHz-yagi är en meterklass** (element ~30–80 cm) — inget problem på marken, men
  planera stativ.

### 6 Val av mark-RX-antenn (enkel jämförelsetabell)

| Typ | Gain | Strålvinkel (HPBW) | Storlek (868 MHz) | Storlek (2,4 GHz) | Kostnad | Lämplig för CanSat-RX |
|---|---|---|---|---|---|---|
| Isotrop/tråd (referens) | 0 dBi | 360° | — | — | — | Bara referens |
| **Omni-stav (monopol)** | 0–3 dBi | 360° (allt håll) | ~8 cm | ~3 cm | <10 € | Nej — ingen riktad förstärkning |
| Dipol | 2,1 dBi | ~360° × 40° | ~17 cm | ~6 cm | 5–15 € | Nej — halvkraftig omni |
| **Kollinär 3–5 dBi** | 3–5 dBi | ~15–30° (elev) | ~20–50 cm | ~10–20 cm | 10–30 € | Bara om man helt vill slippa gimbal |
| **Yagi** ⭐ | 8–15 dBi | ~30–65° × 30–60° | ~40–90 cm | ~10–25 cm | 15–50 € | **Bäst — hög gain + hanterbar stråle** |
| Patch-panel | 6–12 dBi | ~40–80° × 30–50° | ~25–40 cm | ~10–20 cm | 20–60 € | Bra om yagin för lång/omvänt |
| Disco/Dish | 20–33 dBi | ~5–15° | ~60–120 cm | ~30–60 cm | 50–200 € | Överkill — för smal stråle |

**Rekommendation för mark-RX + gimbal (§5):**
- **Primärt: Yagi 12–15 dBi på 868 MHz** (eller ~10–20 dBi på 2,4 GHz) — bra förstärkning
  med en stråle som är lätt att rikta mot burken (±2–5° pekfel räcker, §5.3).
- **Alternativ:** patch-panel 8–12 dBi om man vill ha lägre profil.
- **Undvik dish >20 dBi i defaultspåret** — strålen är för smal (5–15°) för att följa en
  fallande burk utan mycket mjuk pekning. Se dock §6.1 för dish + GPS-fallet.

### 6.1 Vad händer med dishen om man har GPS-spårning + LoRa-backup? 🛰️

**Kort svar: Ja, dishen blir då ett reellt och kraftfullt alternativ — GPS:en tar bort
dess största svaghet (pekning), men strålen förblir smal, så den kräver en *mjuk* gimbal
som följer positionen via GPS + RSSI-peak. Det är en gain-kompromiss, inte en
catch-all.**

Tanken: ett **sepatat backup-system (omni-antenn + LoRa)** skickar burkens GPS-koordinater
till marken. Då vet markgimbalen *ungefär* var burken är och kan räkna elev/azimut innan
den riktar dishen. Detta **löser inte** allt, men det förändrar ekvationen:

**Fördelar med dish + GPS:**
- Väsentligt högre gain (24–33 dBi jämfört med yagins 12–15) → **mer link-marginal,**
  ibland 20+ dB bonus som kan användas för högre datahastighet eller längre räckvidd.
- GPS + RSSI-peak ger en mjuk spårloop som *kan* hålla en medelstor dish på målet.

**Men tre nyckelrisker kvarstår:**

1. **Beamwidth vs fallskärmssvängning:** en 24–33 dBi-dish har bara ~5–10° stråle. Burkens
   gungning under fallskärmen kan deformera var burken "egentligen är" sett från marken
   mer än halva strålvinkeln. → Velj ett mjukt pekfel: medeldish ~24 dBi (8–10°) är
   klart tryggare än 30–33 dBi (5°).
2. **GPS-fel + uppdateringstakt:** GPS-positionen har några meters fel och kommer ~1 Hz.
   Under sista ~100 m (snabb vinkelförändring ~1–2°/s) krävs extrapolering; om GPS-hopp
   eller fördröjning blir stor tappar dishen signalen. → Den behöver en **prediktiv
   spårloop** (senaste banan + RSSI-peak som korrektur).
3. **Footprint vid avstånd:** en 9°-dish täcker ~150 m diameter vid 1 km, men bara ~16 m
   vid 100 m höjd — nära marken är luckan snäv.

**Slutsats:** dish + GPS är genomförbart och ger mer marginal, men **det villkorliga
pekmjukheten gör yagin fortfarande till det förstaval för 2027** — åtminstone initialt.
Bästa kompromissen om ni vill ha både: **medeldish ~24 dBi (2,4 GHz, ~1 m) + mjuk
GPS/RSSI-spårloop** i stället för en stor 33 dBi-dish. Kör först marktest med yagi, och
bygg sedan på dish-spårning som en "fri applikation".

**Konkret konkret arkitektur:**
```
 LoRa-backup (omni) ──► PC ──► gimbal-styrning (elev/azimut från GPS) ──► dish -> höghastighetsdata
 ↑ GPS-koordinater                                                eller yagi (default)
```

### 7 Anslutningslös dubbelarkitektur: ESP-NOW (broadcast) + LoRa-backup 🎯

*Beslut med laget 2026-11-03. Efter att ha utvärderat "WiFi-videoström" vs "ESP-NOW"
landade vi på en **dubbel och helt anslutningslös** downlink. Båda benen är **enkelriktad
broadcast** (burk → mark) — ingen av dem kräver den bräckliga tvåvägshandshake som WiFi-
station-läge (AP-association) behöver.*

**Varför ESP-NOW istället för WiFi-station/AP:**
- **WiFi station-läge kräver en tvåvägsanslutning** innan ett enda paket går: handshake/
  association, DHCP, ACK, anslutningstillstånd. Om länken bryts (fallskärmsgungning,
  antenn vinklas bort) rasar hela uppkopplingen och måste återetableras — bräckligt vid
  längre avstånd och för en fallande burk.
- **ESP-NOW är anslutningslös broadcast:** burken *sänder bara ut* — inget handshake, inget
  att tappa eller återkoppla. Den känner mark-RX:ns MAC och trycker ut paket direkt; varje
  paket står på egna ben. Vid svag/marginal länk **fortsätter den bara att sända** och
  marken tar emot det den hinner. Perfekt för en enkelriktad downlink.

**Taket att vara ärlig om:** ESP-NOW-paket är begränsade till ~250 byte → "video" via
ESP-NOW blir mycket låg fps / tunna stillbilder (320×240-JPEG med flera sekunder mellan).
Men för **GPS, telemetri, RSSI och sporadiska bilder** är det perfekt.

```
 Burken
   ├─ ESP-NOW (2,4 GHz, broadcast-mark-RX): GPS + telemetri + RSSI + sporadiska bilder
   └─ LoRa (868 MHz, monopol): GPS + nödtelemetri som robust redundancy HELA nedfärden
                                  (ingen tvåvägslänk alls, tåligast, 60–80 dB marginal §5.2)

 Marken
   ├─ mark-RX (yagi 12–15 dBi / medeldish on gimbal) ← ESP-NOW-benet
   └─ mark-RX (omni/yagi 868 MHz) ← LoRa-backup
   Gimbal-styrning: RSSI-peak (ESP-NOW) + GPS (LoRa) → elev/azimut
```

**Fördelar med dubbel-uppläggningen:**
- **Båda benen är anslutningslösa downlink** → ingen bräcklig handshake, så robust att
  det inte finns något att koppla upp/återansluta.
- **Redundans:** ESP-NOW för högre datatakt (telemetri + bilder), LoRa-monopolen för GPS/
  nödtelemetri över hela nedfärden även om 2,4 GHz-bredbenet störs (trångt band).
- **Gimbal-pekning funkar oavsett ben:** RSSI-peak från ESP-NOW *eller* GPS från LoRa ger
  elev/azimut — bägge pekar samma burk.
- **Lagligt:** 2,4 GHz 20 dBm EIRP (§2) + 868 MHz 25 mW e.r.p. (duty ≤1 %) — bägge
  licensfria, ingen upplänk krävs.

**Att tänka på:**
- Två radiosystem i burken = mest plats/ström (men har gott om budget, arkivets §7).
- 2,4 GHz-bandet är trångt (interferens) → ESP-NOW-benet är inte lika tåligt som LoRa på
  långa avstånd. Därför är LoRa **backupen/systemets "sanning"** och ESP-NOW det snabba
  extrabenet.
- Håller ni minskat behov → kör enbart LoRa-monopol (den enklaste, vattentäta nedlänken).


---

## Del 2 — Mark-RX-antennprojektet (snabböversikt)


*Kort version för nybörjare. Detaljer: denna fil och
[RADIOTEKNIK.md](RADIOTEKNIK.md).*

---

### Vad är det?

**Mark-RX-antennen är en höginsats antenn som står PÅ MARKEN och tar emot signalen från
burken** under hela nedfärden. Tanken: allt som är svårt och tungt läggs på marken —
burken förblir liten, enkel och robust.

```
 Burken (faller)                      Marken (står still)
 ─────────────────                    ─────────────────
 enkel monopol-antenn (omni)   ──►    hög-gain-antenn (12–15 dBi yagi)
 sänder telemetri + GPS               sitter på en gimbal som följer burken
                                      med en PC som loggar allt
```

---

### Varför är det en bra idé?

- **Burken behöver bara en enkel antenn** (en pinne/tråd) — inget som kan peka fel,
  klarar rotation + 30 G under fallskärmen.
- **Markantennen kan vara hur stor/stark som helst** — förstärkning på mottagningen
  är helt laglig och kostar ingen effekt.
- **Gimbalen står på ett stativ** — lätt att bygga och testa hemma, ingen storlek/tyngd-
  begränsning som i burken.
- **Robust marginal:** ~60–80 dB på 868 MHz över hela nedfärden.

---

### Hur följer gimbalen burken?

På två sätt som kan kombineras:
1. **RSSI** — signalstyrkan toppar när antennen pekar rätt på burken → "peak"-spår.
2. **GPS** — burken skickar sin position → marken räknar elev/azimut (vinklar) → pekar.

Båda ger gimbalen två axlar (azimut + elevation) för att hålla burken i sikte.

---

### Vad skickar burken till oss?

Två ben (se avsnitt 7):
- **ESP-NOW (2,4 GHz, broadcast):** GPS + telemetri + RSSI + sporadiska bilder (högre takt).
- **LoRa (868 MHz, monopol):** GPS + nödtelemetri som robust backup över hela nedfärden.

Båda är **enkelriktade** (burk → mark), så det finns inget bräckligt "koppla upp" att
tappa.

---

### Arbetsplan (litet)

1. **Bygg en yagi 12–15 dBi** på 868 MHz (eller 2,4 GHz-panel) på ett stativ.
2. **Koppla mark-RX till en mottagarmodul + PC** som loggar RSSI och telemetri.
3. **Bygg en 2-axlig gimbal** (hobby-servon/steppers) som kan peka åt två håll.
4. **Få in pekning:** först RSSI-peak, senare GPS → elev/azimut.
5. **Testa på marken** med en separat "burk"-sändare på avstånd — innan flygning.

---

*Kortversion — mer i denna fil (§5–7).*

---

## Del 3 — Polarisation och antennmönster i burken


*Skriven 2026-11-06. Burken roterar och gungar under fallskärmen — hur påverkar det
länken, och vad gör man åt det? Två problem som ofta blandas ihop: **polarisations-
mismatch** och **mönsternolla**. De har olika lösningar.*

---

### 1. Två olika problem

| Problem | Vad det är | Typisk förlust |
|---|---|---|
| **Polarisationsmismatch** | Burken sänder linjärt i en vinkel, marken tar emot i en annan | 0–30 dB beroende på vinkel |
| **Mönsternolla** | En monopol strålar inte längs sin egen axel | 10–20+ dB nära axeln |

Man måste hantera **båda** — och den mekaniska lösningen (att hänga rakt) löser
polarisationen men **inte** nollan.

---

### 2. Vad rotationen faktiskt gör

Polarisationsförlust mellan två linjärt polariserade antenner med vinkeln $\theta$
mellan sina polarisationsplan:

$$
\boxed{L_{\text{pol}} = 20\log_{10}\!\left(\cos\theta\right)\ \text{dB}}
$$

#### 2.1 Förlusttabell

| Rotation | $\theta$ | $L_{\text{pol}}$ | Kommentar |
|---|---|---|---|
| **Spin kring vertikalaxeln** | 0° | **0 dB** | ✅ **Kostar ingenting** |
| Pendel ±15° | 15° | −0,3 dB | försumbar |
| Pendel ±25° | 25° | −0,9 dB | försumbar |
| Måttlig lutning | 30° | −1,25 dB | liten |
| Kraftig lutning | 45° | −3,0 dB | märkbar |
| Hård lutning | 60° | −6,0 dB | betydande |
| Tumling | 75° | −11,7 dB | allvarlig |
| Vinkelrät | 90° | teoretiskt −∞ | praktiskt 20–30 dB |

#### 2.2 ⭐ Nyckelinsikten

**Spin kring den vertikala axeln kostar NOLL.**

En vertikal monopol som roterar kring sin egen axel är **fortfarande vertikalt
polariserad** — polarisationsplanet ändras inte av en rotation kring axeln. Det är
**bara tilt/tumbling** som kostar.

Det betyder att en burk som hänger lodrätt under fallskärmen och snurrar är
**polarisationsmässigt immun** — och snurrandet är dessutom det som händer mest.

---

### 3. Mitigering — i kostnadsordning

#### 🥇 A. Mekanisk: låt burken hänga vertikalt (0 €, störst effekt)

En CanSat hänger redan i fallskärmen — gravitationen gör att den hänger **lodrätt**.
Om monopolens axel är parallell med fallskärmslinan förblir antennen **vertikal hela
nedfärden**, oavsett svängning.

Svängningen är en pendelrörelse → lutning typiskt **±15–30°** →
$L_{\text{pol}} = 0{,}2\ldots1{,}3$ dB. **Försumbart.**

**Konstruktionskrav:**

| Krav | Varför |
|---|---|
| Monopolen monterad **längs burkens axel** (samma axel som fallskärmsfästet) | antennen följer linan |
| **Tyngdpunkten lågt** (batteriet i botten) | burken hänger stabilt, mindre pendel |
| **Undvik fenor** som ger tumling | fenor är gjorda för raket, inte fall |
| Kort fallskärmslina (≥2–3 m) | stabiliserar, minskar vinkelhastighet |

**Detta är den dominanta lösningen och kostar 0 €.**

#### 🥈 B. Marken: två korspolariserade antenner + switch (~$6)

Sätt **två antenner i ±45°** mot varandra och välj den starkare. Då är man **aldrig mer
än 45° fel** → **max 3 dB förlust** oavsett hur burken roterar.

| Konfiguration | Värsta fall |
|---|---|
| En vertikal antenn | **20–30 dB** |
| **Två antenner ±45° + switch** | **3 dB** ✅ |
| Fyra antenner 0/45/90/135° | 0,7 dB |

**Kostnad:** en extra patch (~$5) + en [PE4259-switch](FASVAXLARE.md) (~$0,50).

**Bästa nyttan per krona.** Kräver bara en switch + en GPIO, ingen extra mottagare.

#### 🥉 C. Cirkulär polarisation i burken (bäst, men bara 2,4 GHz)

En **CP-antenn** tar emot en linjär signal med **konstant 3 dB förlust, oavsett
rotation**. Man byter alltså en variabel förlust (0–30 dB) mot en fast (−3 dB).

$$
L_{\text{lin}\to\text{CP}} = 3\ \text{dB (konstant)}
$$

**Men det är bara praktiskt på 2,4 GHz:**

| Frekvens | $\lambda$ | Turnstile (korsade dipoler) | Ryms i Ø66 mm? |
|---|---|---|---|
| **868 MHz** | 34,6 cm | ~17 cm per arm | ❌ **Nej** |
| **2,4 GHz** | 12,5 cm | **~3,1 cm per arm** | ✅ **Ja, lätt** |

En **turnstile** (två korsade dipoler matade 90° förskjutet) på 2,4 GHz blir bara ~6 cm
— ryms utmärkt.

> **Viktigt:** CP-CP mellan burk och mark måste ha **samma riktning** (höger/vänster).
> Motsatt riktning ger −∞ (praktiskt 20–30 dB). Så byt inte handfallenhet på ena sidan.

#### D. Två ortogonala monopoler + kombinerare
Två monopoler i 90° i burken, kombinerade med 90° fasförskjutning → CP. Ryms på båda
banden men är pilligare än en turnstile.

---

### 4. Burkens elektriska storlek — ett starkare argument för 2,4 GHz

$$
\frac{D_{\text{burk}}}{\lambda} =
\begin{cases}
\dfrac{66\ \text{mm}}{346\ \text{mm}} = \mathbf{0{,}19\lambda} & \text{868 MHz}\\[6pt]
\dfrac{66\ \text{mm}}{125\ \text{mm}} = \mathbf{0{,}53\lambda} & \text{2,4 GHz}
\end{cases}
$$

| Frekvens | Burk i våglängder | Konsekvens |
|---|---|---|
| 868 MHz | 0,19 λ | **Elektriskt liten** → monopol får dålig verkningsgrad, litet jordplan, breda förluster |
| 2,4 GHz | **0,53 λ** | **Riktig radiator** → bra verkningsgrad, fungerande jordplan |

Vid 868 MHz är burken mindre än en femtedels våglängd — en monopol där är en kraftigt
kompromissad antenn. **Detta talar starkt för 2,4 GHz i burken.**

---

### 5. ⚠️ Det större problemet: mönsternollan

Detta är ofta **värre än polarisationen**. En vertikal monopol har en **nolla rakt upp
och rakt ner**. Markstationen ligger *under* burken → nära nollan.

Monopolmönster över ett jordplan:

$$
\boxed{G(\theta) = G_{\max}\sin^{2}\theta}
$$

där $\theta$ mäts från antennaxeln.

#### 5.1 Nolltabell

| Riktning till markstationen | $\theta$ från axeln | Dämpning |
|---|---|---|
| Horisontellt | 90° | 0 dB |
| 45° nedåt | 45° | −3,0 dB |
| 30° nedåt | 30° | −6,0 dB |
| 20° nedåt | 20° | **−9,3 dB** |
| 10° nedåt | 10° | **−15,2 dB** |
| Rakt ned | 0° | **−∞** |

#### 5.2 Varför det ändå ofta går bra

Geometrin hjälper: burken faller från ~1 km och **driver** med vinden. Markstationen
hamnar därför sällan rakt under.

$$
\phi_{\text{elev}} = \arctan\!\left(\frac{h}{d_{\text{drift}}}\right)
$$

Med 1 km höjd och 500 m drift blir infallsvinkeln $\arctan(1000/500) = 63°$ från
horisontalplanet → bara ~27° från vertikalen i monopoltermer → **~−7 dB**. Och med
60–80 dB systemmarginal (868 MHz) eller 23 dB (2,4 GHz vid 254 kb/s) är det **helt
absorberat**.

#### 5.3 Åtgärder mot nollan

| Åtgärd | Effekt | Kostnad |
|---|---|---|
| **Luta antennen 30–45°** bort från nollriktningen | +6–10 dB nedåt | 0 € |
| **Sleeve-monopol / top-loaded** | bredare mönster | liten |
| **Acceptera** med systemmarginal | — | 0 € |
| **Dipol istället för monopol** | nollor blir horisontella | 0 € |

---

### 6. Rekommendation

| Prioritet | Åtgärd | Kostnad | Vinst |
|---|---|---|---|
| **1** | Monopol längs fallskärmsaxeln + låg tyngdpunkt | **0 €** | tilt → ±25° → **<1 dB** |
| **2** | Två markantenner ±45° + PE4259-switch | **~$6** | värsta fall **3 dB** istället för 30 |
| **3** | Luta burkantennen 30° bort från nollan | 0 € | **+6–10 dB** mönster |
| **4** | CP-turnstile i burken (endast 2,4 GHz) | ~$2 | immun mot rotation |

**För under $10 får man en i praktiken polarisationssäker lösning.** Det mekaniska
(prioritet 1) gör ~80 % av jobbet gratis.

---

### 7. Sammanfattning i en tabell

| Åtgärd | Löser polarisation? | Löser nollan? | Kostnad |
|---|---|---|---|
| Hänga vertikalt under fallskärm | ✅ (80 %) | ❌ | 0 € |
| Två markantenner ±45° | ✅ (kapar vid 3 dB) | ❌ | ~$6 |
| CP-turnstile i burken (2,4 GHz) | ✅ (immun) | ❌ | ~$2 |
| Luta antennen 30–45° | ⚠️ (kostar lite) | ✅ (+6–10 dB) | 0 € |
| Acceptera med marginal | — | — | 0 € |

**Kombinationen 1 + 3** (häng vertikalt, luta 30°) ger både bra polarisation *och*
undviker nollan — utan att kosta något.

---

### 8. Källor och vidare läsning

- denna fil — §5 (monopol i burken), §3 (antennbegrepp)
- [PROTOKOLL.md](PROTOKOLL.md) — länkbudgetar för 2,4 GHz vs 868 MHz
- del 1 i denna fil — PE4259-switchen för polarisationsval
- Balanis, *Antenna Theory* — kapitel om monopol, jordplan, polarisation
- [Traficom — frekvensanvändning i luftfartyg](https://traficom.fi/en/radio-licences-and-frequencies/use-radio-frequencies/frequency-use-unmanned-aviation)

---

*Levande dokument. Uppdatera med mätresultat från marktest (RSSI vs uppmätt rotation)
när prototypen finns.*

---

## Källor

- [AMSAT, "Two-way satellites: AO-91 Fox-1B" (cross-band FM-repeater)](https://www.amsat.org/two-way-satellites/ao-91/)
- [AMSAT, "Live FM Satellites" (AO-91, ISS, SO-50 m.fl.)](https://www.amsat.org/live-fm-satellites/)
- [CanSat 2003 (Stanford/Morehead), ProbeSat→RelaySat→Ground demonstration](https://scholarworks.moreheadstate.edu/cgi/viewcontent.cgi?article=1289&context=twiggs_education_collection)
- [S. Hum (Univ. Toronto), "Satellite Links" — transponder, upp-/nedlänk, link budget](https://www.waves.utoronto.ca/prof/svhum/ece422/notes/23-satellite.pdf)
- [CEPT EFIS, "Annex 1: Non-specific Short Range Devices" (868 MHz h1.x, e.r.p.-nivåer)](https://efis.cept.org/adhoc_grabber.jsp?annex=4)
- [DOMCA, "Regulations & Duty Cycle" (868 MHz e.r.p., duty cycle, dBd vs dBi)](https://docs.domca.nl/en/usage/regulations/)
- [CalPoly, "Store-and-forward routing and data mules for CubeSats"](http://users.csc.calpoly.edu/~bellardo/pubs/wc10.pdf)
- [Traficom, Regulation 15 AR/15AV (licensfria kollektiva frekvenser, suljettu dokument PDF)](https://www.traficom.fi/files/media/regulation/Regulation%2015AV2025M.pdf)
- [Finlex, Traficom määräys (4 AF/2025M), licencfria kollektiva frekvenser (PDF)](https://www.finlex.fi/api/media/authority-regulation/535594/mainPdf/main.pdf?timestamp=2025-03-26T22%3A00%3A00.000Z&typeDiscriminator=traficom-communications)
- [The Things Network, "Regional limitations of RF use in LoRaWAN" (868 MHz, duty cycle, 16 dBm EIRP)](https://www.thethingsnetwork.org/docs/lorawan/regional-limitations-of-rf-use/)
- [The Things Network, "Duty cycle" (sändningstid per timme)](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)
- [Traficom, "Radioamatööritoiminnan pätevyydet ja taajuudet" (amatörradio kräver tillstånd — ej samma sak)](https://traficom.fi/fi/radioluvat-ja-taajuudet/radiotaajuuksien-kaytto/radioamatooritoiminnan-patevyydet-ja-taajuudet)
- [MathWorks, "DVB-S2 bent pipe simulation" (relä-länk, koncept)](https://www.mathworks.com/help/satcom/ug/dvbs2-bent-pipe-simulation-with-rf-impairments-and-corrections.html)

---

## Se även

- [PROTOKOLL.md](PROTOKOLL.md) — vilket protokoll och band som ger bäst tillförlitlighet + bandbredd
- [BEAMFORMING.md](BEAMFORMING.md) — elektronisk strålstyrning (teori, matematik, hårdvara)
- [FASVAXLARE.md](FASVAXLARE.md) — fasväxlarna en array kräver
- [GIMBAL.md](GIMBAL.md) — markgimbalens byggplan och CAD
- [KOSTNADER.md](KOSTNADER.md) — vad designen kostar
- [RADIOTEKNIK.md](RADIOTEKNIK.md) — begreppen om du är ny
- [MUONDETEKTOR.md](MUONDETEKTOR.md) — sekundärmissionen som använder nedlänken
