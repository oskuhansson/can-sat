# Simulering av länk och gimbalpekning

En generisk simulator för radiosystem med **riktantenn på marken** som följer en
**fallande sändare**. Byggd för CanSat-projektet, men inget i koden är
CanSat-specifikt: att byta system är en ny scenariofil eller en ny registrerad
antennmodell.

Svarar på frågan simuleringen finns för: **hur stort blir pekfelet, hur mycket
antennvinst tappar vi, och hur många paket försvinner** — över tid, och i värsta
fallet.

```
python run.py scenarios/cansat_868.json
python run.py scenarios/cansat_868.json --runs 200
python run.py scenarios/cansat_24.json --runs 50 --plot
```

Kräver **numpy** och **pandas**. `matplotlib` är valfritt — finns det skrivs ett
PNG, annars hoppas det bara över. **CSV skrivs alltid.**

---

## Vad simuleringen visar

Med de marginaler projektet har (65–72 dB på 868 MHz) är **paketförlusten noll i
alla scenarier** — även när gimbalen sveper blint över himlen. Skillnaden mellan
banden syns i stället i **pekförlusten** och i **hur lång tid det tar att hitta
sändaren**. Det är en ärlig och något överraskande slutsats: länken är inte
begränsningen, pekningen är det, och marginalen äter upp pekfelen.

Medelvärden över 20 seed (från `test_sim.py`):

| Scenario | Förlust | Pekförlust | Låsningstid | Sämsta marginal |
|---|---|---|---|---|
| 868, GPS | 0,0 % | **0,5 dB** | 2,0 s | 42,4 dB |
| 868, ingen GPS | 0,0 % | **0,8 dB** | 3,2 s | 40,6 dB |
| 2,4 GHz, GPS | 0,0 % | **0,9 dB** | 2,0 s | 13,4 dB |
| 2,4 GHz, ingen GPS | 0,0 % | **7,8 dB** | 33,6 s | 10,6 dB |

Tre saker att läsa ut ur den tabellen:

1. **Utan GPS kostar den smala strålen 7,8 dB mot 0,8 dB.** Samma absoluta pekfel
   straffar en 17,5°-lob mycket hårdare än en 48,4°-lob: `12*(θ/θ₃dB)²` ger
   15 dB vid 20° fel för den smala, 2 dB för den breda.
2. **Sveptiden skiljer sig med en faktor fem.** En 2,4 GHz-lob behöver ~126
   strålpositioner för att täcka himlen, 868-loben ~16. Med 0,4 s per position
   blir det 50 s mot 6 s — och flygningen varar ~110 s.
3. **2,4 GHz har 27 dB mindre marginal** (13,4 dB mot 42,4 dB) eftersom FSPL är
   8,8 dB högre och känsligheten sämre. Det är fortfarande tillräckligt, men
   marginalen är inte längre självklar.

---

## Så är den uppbyggd

```
run.py              CLI
test_sim.py         självtester (52 kontroller)
scenarios/          indata — all systemspecifik information bor här
sim/
  config.py         dataklasser + JSON-inläsning, avvisar okända fält
  geometry.py       position -> az/el/räckvidd, bana, lövsträcka
  antenna.py        mönstermodeller, registrerbara
  propagation.py    FSPL, vegetation, skuggning, markreflexion
  linkbudget.py     Friis-kaskad, känslighet, marginal
  gimbal.py         svepgräns, glapp, upplösning, sveptid
  tracker.py        GPS-grov + RSSI-fin, acquisition, tappat läge
  modulation.py     LoRa-tabeller, lufttid, PER
  engine.py         run(scenario, seed) -> tidsserie
  report.py         CSV, sammanfattning, PNG
```

Varje tidssteg går i samma ordning:

```
sann position -> vad trackern tror -> vart gimbalen pekar -> pekfel
             -> antennvinst -> vägförlust -> mottagen effekt -> marginal -> PER
```

Att trackern får veta om signalen hördes i **föregående** steg är medvetet: en
RSSI-följare kan inte veta något om ett paket den ännu inte fått.

### Antennmodeller

Registrerade i `antenna.py`, väljs med `"model"` i scenariofilen:

| Modell | Formel | Användning |
|---|---|---|
| `isotropic` | konstant | isolera resten av kedjan; visar att pekfel är irrelevant för en rundstrålande antenn |
| `gaussian` | `G_max − 12(θ/θ₃dB)²` | **samma formel som projektets pekförlust** |
| `cosn` | `G_max·cosⁿθ` | horn eller patch |
| `yagi` | huvudlob + sidolober + baklob | grov yagi |
| `array` | elementmönster + arrayfaktor med faskvantisering | plan fasstyrd array, se nedan |
| `file` | interpolerad tabell | riktigt NEC-mönster |

Ny modell = en funktion med `@register_model("namn")`. Ingen annan fil behöver
ändras.

### Plan fasstyrd array

`"model": "array"` lägger en plan array i horisontalplanet, styrd elektroniskt i
stället för mekaniskt. Den kräver fyra fält utöver de vanliga:

| Fält | Betydelse |
|---|---|
| `array_nx`, `array_ny` | antal element i respektive led |
| `spacing_lambda` | elementavstånd i våglängder; **över 0,5 ger grating lobes** |
| `phase_bits` | fasväxlarens upplösning. 4 = 22,5° steg (MAPS-010144). Utelämnas = ideal fas |
| `element_beamwidth_3db_deg` | det enskilda elementets lob, default 70° |

`peak_gain_dbi` betyder samma sak som för alla andra modeller: förstärkningen i
bredsidesriktningen. Elementets egen vinst räknas fram ur den, som
`element = peak − 10log₁₀(nx·ny)`, så att alla scenarier går att jämföra på samma
siffra.

Två saker som modellen gör rätt och som är lätta att missa:

- **Koherent summering ger `10log₁₀(N)`**, inte `20log₁₀(N)`. 2×2 ger +6,02 dB,
  4×4 ger +12,04 dB.
- **Elementmönstret gör arrayen svag mot horisonten.** En horisontell array har
  bredsidan rakt upp; ett element som sitter på 90° zenitvinkel ligger på sin egen
  nollnivå. Det är fysikaliskt riktigt — och det är därför en array förlorar mot en
  yagi sent i nedfarten.

Strålbredden **räknas fram ur mönstret** med bisektion i stället för att anges,
eftersom den beror på både arrayfaktorn och elementets lob. Att skatta den ur
förstärkningen som för de andra modellerna skulle ge fel antal sveppositioner.

#### Kvantiseringens effekt — och varför den inte syns där man tror

4-bitars fasväxlare kostar **0,034 dB** toppförstärkning (vid styrning bort från
bredsidan; exakt mot bredsidan är styrfasen redan 0 och förlusten är noll). Man
kunde tro att de också höjer sidoloberna, och det gör de: ideala nollor fylls
igen, från −240 dB till −31,9 dB. Men **toppsidoloben höjs inte** för en 4×4-array
med `d = 0,5λ`, eftersom den uniforma belysningens egen sidolob redan ligger på
**−11,3 dB** — högre än kvantiseringens. Slutsatsen är att 4-bitars fasväxlare
räcker gott här: det är belysningen, inte kvantiseringen, som sätter
sidolobenivån. Amplitudtaper hade sänkt den, och då hade kvantiseringen blivit
synlig.

> **−11,3 dB är kontrollerat** mot den analytiska formeln för en uniform linjär
> array, `|sin(Nπdu)/(N sin(πdu))|`, som ger −11,30 dB vid `u = 0,732` för N = 4
> och `d = 0,5λ`. Eftersom 2D-faktorn är separabel (`AF(u,v) = AFx(u)·AFy(v)`) är
> 2D-arrayens högsta sidolob densamma som 1D-sidoloben — den kan aldrig bli
> högre. En tidigare version av det här avsnittet angav −5,6 dB; det var fel.

#### Svepning: mekanisk, elektronisk eller simultan

`tracker.scan_mode` avgör hur strålen flyttas mellan sveppositionerna:

| `scan_mode` | Dwell per position | Modellerar |
|---|---|---|
| `"mechanical"` (default) | `scan_dwell_s` | gimbal med svephastighet, glapp, upplösning |
| `"electronic"` | `max(switch_time_s, lufttid)` | fasstyrd array, ingen mekanik alls |

Elektronisk svepning är **inte momentan**: för att *upptäcka* sändaren i en riktning
måste man lyssna där minst ett helt paket. Antalet positioner är detsamma som för
mekanisk svepning, eftersom strålbredden är densamma — det är bara dwellen som
skiljer. `switch_time_s` (default 1 ms) är den tid själva omslaget tar.

`simultaneous_beams: true` modellerar en digital array med flera mottagarkedjor som
lyssnar i alla riktningar samtidigt. Låsningstiden blir då 0 — den undre gränsen,
inte ett byggbart system i den här budgeten.

### Fysiken

| Storhet | Formel | Källa |
|---|---|---|
| FSPL | `32,44 + 20log₁₀(f_MHz) + 20log₁₀(d_km)` | — |
| Vegetation | `A = A_m(1 − e^(−d·γ/A_m))` | ITU-R P.833-10 ekv. 1 |
| Bruskaskad | `F_tot = F₁ + (F₂−1)/G₁ + …` | Friis |
| Pekförlust | `12(θ/θ₃dB)²` | parabolisk huvudlob |
| Lufttid | `(preamble + 4,25 + n_payload)·2^SF/BW` | Semtech |
| PER | `0,01·10^(−marginal/2)` | approximation, se nedan |

Vegetationen modelleras som ett lövbälte kring mottagaren: strålen är i lövverket
så länge `r·tan(el) < trädhöjd`, upp till bältets djup. Därför kostar låg
elevation mer än hög — det är mekanismen bakom ett datahål sent i en nedfart.

---

## Vad simuleringen **inte** modellerar

Det här är viktigare att veta än vad den gör.

- **Ingen vågutbredning i 3D.** Ingen diffraktion, ingen terräng, inga byggnader.
  Fri rymd plus en vegetationssiffra plus lognormalskuggning.
- **Ingen bitnoggrann LoRa.** Känslighet och PER kommer från tabeller och en
  monoton approximation, inte från en CSS-demodulator. Modellen fångar *trenden*
  i att PER faller med marginalen, inte den exakta knäpunkten. Vill man ha riktig
  LoRa-PHY ska man köra `gr-lora_sdr` mot hårdvara.
- **Ingen multipath som default.** Tvåvägsmodellen finns (`"model": "two_ray"`)
  men är avstängd: en riktig markreflexion har spridning och frekvensberoende som
  en enkel tvåvägsmodell inte fångar, och nollställena flyttar sig snabbare än
  tidssteget.
- **Ingen interferens.** Ingen WiFi, inga andra LoRa-sändare, ingen co-channel.
- **Ingen antennkonstruktion.** Mönstret är en modell, inte ett NEC-resultat.
  Vill man veta hur yagin faktiskt ser ut ska man köra 4NEC2 och använda
  `"model": "file"`.
- **Ingen ömsesidig koppling mellan arrayelementen**, ingen amplitudtaper och
  inget riktigt elementmönster. Arrayen använder den gaussiska modellen för sitt
  element; en riktig patch har en annan lob och en cross-pol-nivå som inte finns
  här. Arrayfaktorn själv är däremot exakt.
- **Ingen IMU, ingen pendling, ingen rotationsdynamik** i burken.
- **Ingen tidsynkronisering eller paketförluster i protokollet** utöver PER.
- **Banan är rak** med konstant sjunkhastighet och konstant vind.
- **RSSI-följningen är en modell av en toppjakt**, inte en implementerad
  reglerloop. Dess noggrannhet är en konfigurerad bråkdel av strålbredden.
- **Duty cycle kontrolleras bara som en budget** — modellen vet inte om
  sändaren faktiskt håller sig inom den.

---

## Scenarier

| Fil | System |
|---|---|
| `cansat_868.json` | CanSat 868 MHz, SF9/125 kHz, 15 dBi yagi, GPS-tracker, vegetation |
| `cansat_24.json` | Samma bana på 2,4 GHz, 17,8 dBi (samma fysiska apertur), 17,5° lob |
| `cansat_24_array.json` | Samma bana och radio, men **plan 2×2-array** med 4-bitars fasväxlare och elektronisk svepning |
| `generic_example.json` | **Inte CanSat**: radiosond på 433 MHz, rundstrålande antenn, ingen vegetation |

Den sista filen finns för att bevisa generiken, och självtesterna kör den. Att
den ger **noll pekförlust** är själva poängen: med en rundstrålande antenn spelar
det ingen roll vad gimbalen gör.

### 868-scenariet och duty cycle

868 MHz har **1 % duty cycle** (≈36 s lufttid per timme, ETSI EN 300 220-2
§4.4.3.2 — mätt över en timme, inte per flygning). Ett paket på 20 byte tar
**108 ms** på SF9/125 kHz, så 0,5 s intervall ger 220 paket och 23,9 s lufttid
under en 110 s-flygning: **inom** budgeten. Simulatorn skriver ut det på raden
`Lufttid under flygningen`.

Gränsen går vid ungefär **3 paket/s** (0,33 s intervall ≈ 36 s). Det är alltså
inte 2 paket/s som är problemet — det var en felräkning i en tidigare version av
`airtime_s`, där formeln använde `(CR+4)` i stället för `(CR+4)/4` och gav 185 ms.

2,4 GHz har ingen sådan gräns, vilket är hela skälet att bandet är intressant.

---

## Lägga till ett eget system

1. Kopiera en scenariofil och ändra band, EIRP, antenn, bana.
2. Kör. Okända fält avvisas med namn, så en stavning tystnar inte.
3. Behöver du en antennmodell som inte finns: skriv en funktion i `antenna.py`
   med `@register_model("dittnamn")`.

Konfigurationen validerar att obligatoriska fält finns och att talen är rimliga
(positiv frekvens, `max_elevation > min_elevation`, korrelation i `[0,1)`).

---

## Tester

```
python test_sim.py
```

52 kontroller i fem grupper: fysik mot kända värden, alla scenarier, determinism,
acquisition utan GPS, och att konfigurationsfel fångas. Exit-kod 1 om något
fallerar.

Determinismen är testad: samma seed ger bit-identisk tidsserie.

---

## Utdata

```
out/<scenario>/
  <scenario>_run000.csv      tidsserien, en rad per tidssteg
  <scenario>_summary.csv     en rad per körning
  <scenario>_plot.png        om matplotlib finns
```

CSV-kolumnerna är avsiktligt råa: `pointing_error_deg`, `rx_gain_dbi`,
`vegetation_db`, `margin_db`, `per`, `packet_lost`, `phase`. Man ska kunna göra
sin egen analys utan att läsa koden.

---

## Kända osäkerheter

- **SX1280:s maximala insignal är inte verifierad.** För 868 MHz är SX1262:s
  gränser kända (+10 dBm absolut, 0 dBm rekommenderat) och LNA:n med 10 dB pad
  håller sig under dem. För 2,4 GHz saknas motsvarande kontroll.
- **2,4 GHz-känsligheten** bygger på SX1280-tabellen vid 203 kHz omräknad till
  812 kHz med 3 dB per bandbreddsdubbling. Verifiera mot databladet.
- **PER-modellen är en approximation.** Den är monoton och rimlig, inte uppmätt.
