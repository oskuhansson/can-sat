# WiFi-hotspot i CanSat — forskningsöversikt

*Skapad 2026-11-02. Syfte: undersöka om det är genomförbart att göra CanSaten till en
"WiFi-hotspot från himlen" (Starlink-liknande) — en high-gain-antenn på burken som ger
telefoner på marken trådlös uppkoppling under nedfärden, med plats kvar för annan
elektronik och sensorer. Dokumentet ersätter cloud-chamber-spåret som primärt uppdrag.*

---

## 1. Uppdraget och målbilden

**Målet:** CanSaten bär en accesspunkt (WiFi-hotspot) som telefoner på marken kan
ansluta till när den faller, "lite som Starlink". Lagets fokus: en robust antenn med
tillräckligt hög gain som ryms i/får plats på burken, eventuellt styrbar, plus gott om
plats för övrig elektronik/sensorer.

**Viktig ärlighet direkt:** en CanSat har *ingen internetupling*. Phones som ansluter
till hotspoten får alltså inte "riktig" internet — de når CanSatens **egen webbserver**
(live-telemetri, grafer, kamerabilder, m.m.). Det är fortfarande ett utmärkt och väldigt
synligt uppdrag ("anslut till satelliten från din telefon!"), men jämförelsen med
Starlink gäller *tekniken att ge marken uppkoppling från en rörlig plattform*, inte
internetåtkomst. (Googles [Project Loon](https://www.technologyreview.com/technology/project-loon/)
använde för övrigt **LTE**, inte WiFi, bland annat därför att WiFi-bandet är trångt —
och Loon hängde på ~20 km höjd med 40 km täckningsradie.)

**Realistisk kärna att utvärdera:**
1. Når WiFi-signalen telefonerna alls från ~1 km (länkbudget)?
2. Vilken antenndesign ryms på/i en 66 mm-burk och ger mest nytta?
3. Behöver antennen styras, och kan det göras robust med motorer — eller är ett fast
   nedåtriktat fält bättre?
4. Var hamnar elektroniken, antennen och styrningen i 300–350 g-budgeten?

## 2. Fysiken — länkbudgeten är gynnsammare än man tror

**Fri rymd-vägdämpning (FSPL) — kärnsiffran:**

| Avstånd | 2,4 GHz | 5 GHz |
|---|---|---|
| 250 m | 88 dB | 95 dB |
| 500 m | 94 dB | 102 dB |
| 1000 m | **100 dB** | **108 dB** |

FSPL = 20·log₁₀(4πdf/c) [rftools](https://rftools.io/calculators/rf/rf-link-budget/).
**6 dB per fördubblad distans**, 6 dB mellan 2,4 och 5 GHz → **2,4 GHz är rätt band**.
Obs: +0,5 dB atmosfärisk förlust per km, försumbar; markreflexion/multipath kan kosta
~3–10 dB i öppet fält utanför idealfallet.

**Länkbudget uppifrån (burken) till telefon (marken):**

| Väg | Uppifrån→ner (EIRP 20 dBm) | Telefon→upp (TX ~15 dBm) |
|---|---|---|
| Avsändare | 20 dBm EIRP (lagstak, se §4) | ~15 dBm EIRP (telefoner är svaga) |
| FSPL 1 km | −100 dB | −100 dB |
| Mottagar-antennkl| tel. ~0 dBi | burkens antenn G dB |
| Mottager vid 1 km | **~−80 dBm** | **−85 + G dBm** |
| Kan telefon+användare klara det? | WiFi −80 dBm = *marginal till att fungera* (1–6 Mb/s) | med G≥10 dBi: −75 dBm — bra |

Slutsats: **redan en obetydlig antenn (0–3 dBi) ger WiFi-uppkoppling på låg hastighet
runt ~500 m–1 km slantavstånd.** En high-gain-antenn (10 dBi+) gör stor skillnad på
*upplänken* (telefon → burk), som annars är flaskhalsen, och fokuserar utsändningen mot
marken. Distributed 2,4 GHz-hastigheter vid −80 dBm ≈ 1–6 Mb/s — räcker för
telemetri-sidor och bilder, inte storskalig surf.

**Tidsfönstret:** apogeum 750–1100 m + nedfärd 8–11 m/s ger ~70–120 s där slantavståndet
till marktelefoner krymper. Den bästa "Starlink-stunden" uppstår sista ~30 s ned mot
landning när slantavståndet < 300–500 m. Flyghöjden i [finska CanSat](https://www.esero.fi/cansat-kilpailu)
är ~1 km (750 m 2026), dvs. väsentligt lägre än Loon — det *hjälper* oss (kortare FSPL).

## 3. Regler — det lagliga EIRP-taket ändrar "high gain"-strategin

**Det viktigaste fyndet:** i Finland (EU/CEPT [Regulation 15](https://traficom.fi/en/radio-licences-and-frequencies/users-radio-equipment/buying-and-using-radio-equipment))
är effektgränsen för 2,4 GHz WLAN **EIRP ≤ 100 mW (20 dBm)** — det är *strålad* effekt
inklusive antennförstärkning. Konsekvenser:

- Man får **inte lovligt skicka 30 dBm EIRP** bara för att man har en 12 dBi-antenn;
  TX-utgången måste dämpas så att EIRP ≤ 20 dBm.
- **High gain är därför inte till för att "blåsa ut mer power"** utan för att (a) ta emot
  telefonens svaga upplänk (det är där vinsten är stor), (b) fokusera den tillåtna
  20 dBm mot marken (mindre energi åt fel håll → effektivare), och (c) reducera
  störningar från andra riktningar.
- **Frequency channels i Finland** ([Wi-Fi RegDB](https://regdb.lizardsystems.com/country/FI)):
  2,4 GHz kanal 1–13 (13/14 användbara), 20 dBm. 5 GHz: 5150–5250 = 200 mW men
  **indoor-only** (−5 GHz-användning utomhus begränsad), 5250–5350 = 100 mW + DFS radar,
  5470–5725 = 500 mW + DFS, 5725–5875 = 25 mW. → **2,4 GHz är det robusta valet utomhus**;
  5 GHz 5470–5725 kräver DFS-loggning som är jobbig i en fallande burk.
- CE-märkning + EU-deklaration krävs (Traficom); en egenbyggd sändare måste uppfylla
  EN 300 328 — håll dig här till färdiga, CE-märkta WiFi-moduler (ESP32/Raspberry Pi
  Zero + modul) med fastappliserade antenner, inga förstärkare.

**CanSat-antenregler (finskt):** antenner får vara **utanpå burken** (som GPS/LoRa), och
utrymmet ovanför burken är **4,5 cm axialt** (fallskärm + fäste + antenner måste rymmas)
— se [finska guiden](https://www.esero.fi/finnish-cansat-competition-guidelines). Det
betyder att en stor panelantenn antingen måste vika ihop innanför Ø66 mm tills den
lämnat raketen, eller klara sig i ≤4,5 cm-locket.

## 4. Antennalternativ som får plats

| Typ | Gain | Storlek som ryms? | Bedömning |
|---|---|---|---|
| **Patch (kvartsvågsplattor), 1–4 element** | 3–8 dBi | 30–80 mm → **ryms i burken!** | ⭐ **Basrekommendation** — billig, robust, inga rörliga delar |
| Mikrostrip-array (liten) | 5–7 dBi | ~60–80 mm → ryms | Bra upplänkshjälp, enkelt |
| **Täthopbekränkt panel, 8–12 dBi** (t.ex. [LevelOne WAN-2121](https://www.level1.com/level1_en/wan-2121-12dbi-2-4ghz-directional-panel-antenna-54046107), 140×166×30 mm / [Taoglas FG.27](https://www.taoglas.com/product/fg-27-a-super-compact-12dbi-2-4ghz-directional-panel-antenna/) 210×210 mm) | 10–12 dBi | **Större än burken**, >0,3 kg | Kräver utfällbar mekanik → komplicerat och tungt |
| Yagi (kickad, 8–10 element) | 8–10 dBi | ~60–120 cm lång | För lång; måste fällas ut efter utkast — riskabelt |
| **Omni-stav** (1/2–5/8 λ) | 2–3 dBi | ~10–30 mm Ø, kort stav | Enkelt, men når bara ~500 m–1 km marginal |
| **Phased array** (2,4 GHz) | teoretiskt → $ via beamforming | λ/2 ≈ 62 mm/el → 4×2 kräver ~25×13 cm | **Ryms inte** + komplex + (se §6) |

**Slutsats:** det som *faktiskt får plats i en 66 mm-burk* är små patch/mikrostrip-
antenner på **~3–8 dBi**. Det är fullt tillräckligt för att lyfta upplänken och för
hotspot-tänket (länkbudgeten ovan visar att även 0 dBi räcker på låg hastighet). Att
jaga >10 dBi kräver en utfällbar panel som (a) inte får sticka ut ur Ø66 mm före
utkast, (b) måste tåla 20–30 G vid utlösning, (c) tar nästan hela 4,5 cm-locket.

**Nyckelinsikt:** en **fast nedåtriktad patch-array i burkens botten**, som "tittar mot
marken under hela nedfärden", ger i praktiken en högriktad täckning mot där telefonerna
är — utan motorer och utan styrning. Gungning under fallskärm vidgar bara lampkonen
(hur mycket beror på pendelvinkeln, se §5).

## 5. Att peka antennen — motorer vs fast fält

**Fallskärmsgungningen är det verkliga problemet** (samma som i §8.1 i
FORSKNING.md): CanSaten gungar och roterar under fallskärmen. Ett fast "nedåt"
antennfält i botten täcker konen där marken alltid befinner sig så länge gungningen
moderat. Mät data: pendelvinklar ökar konutbredningen.

| Lösning | Fördelar | Nackdelar |
|---|---|---|
| **Fast nedåtriktad patch** | Robust, 0 W mekanik, inget som kan fastna | Täckning = kon under burken; sämst om spinn/vingel stort |
| **Pan-tilt med mikroservon** ([Adafruit kit](https://www.adafruit.com/product/1967), ~37 g, SG-90-servon) | Kan följa en specifik markstation | Kräver IMU + 2-axlig reglerloop mot ett snurrande/gungande fällande objekt — **svårt**; servot slår vid 20–30 G; ~37–50 g extra |
| Profesjonella pan-tilt-steg (t.ex. [OES PT60](https://www.oesincorp.com/motorized-multi-axis-stages/motorized-pan-tilt-mounts.htm)) | Precisionsstyrning | Långt över mass/kostnadsbudget (paket 10 kg-klass) — **ej CanSat** |
| **Phased array** | Elektronisk styrning, inga rörliga delar | Ryms inte (se §4); komplex; dyr |

**Bedömning:** för 2027-uppdraget rekommenderas **fast nedåtriktad antenn** — robusthet
vinner, och 20 dBm-EIRP-taket gör att den extra directionella vinsten mest märks på
upplänken. **Motorer/gimbal blir ett stretch-mål eller numeriskt äventyr**, inte
bärlinje. Om ni verkligen vill följa en markstation, titta på bärbara "auto-tracking"
patch-servomoduler för drönare — men dimensionera för G-belastningen och testa på
skakbordet.

## 6. Phased array — bedömning (lagets hypotes "lovande men dyr")

Hypotesen stämmer: **phashed arrays är fortfarande inte rätt för en CanSat-burk:**

1. **Storlek:** λ/2-avståndet vid 2,4 GHz ≈ 62 mm. En användbar array (≥8 element,
   ≥~6 dBi + bearning) blir 25×13 cm (t.ex. [ESPARGOS One, 4×2, €350](https://espargos.net/espargos-one/)).
   Den **ryms inte i Ø66 mm** och tar nästan all massa.
2. **Kostnad:** ESPARGOS One €350 (inkl. 8 dubbelpolära antenner, [ethernet/PoE, ~3,5 W](https://espargos.net/espargos-one/))
   *nästan* i 500 €-budgeten, men det är **forsknings-/sensigutrustning** (CSI/IQ-analys,
   radar) — inte en färdig accesspunkt som telefoner kan ansluta till. Att bygga om den
   till en hotspot-serverande AP + beamforming-FW är ett fullständigt eget projekt.
3. **Juridik:** TX-beamforming kräver sändningstillstånd (amatörradio/licens) enligt
   ESPARGOS-dokumentation — strider mot "licensfri 20 dBm"-vägen för skoluppdrag.

**Slutsats:** phased array är rätt svar för "swarm/measurement" i större formfaktorer,
inte för en 330 ml-burk som ska ge telefoner WiFi 2027. Anteckna som "framtida
utvecklingsspår" snarare än plan A.

## 7. Elektronik, plats för sensorer och massbudget

WiFi-lösningen är **enklare och mycket mer platsvänlig** än cloud-chambern (ingen
PCM, ingen isolering, ingen kamera-optik):

| Komponent | Typisk post/kostnad | Massa |
|---|---|---|
| Processer + WiFi (ESP32-modul, ~2,4 GHz, 20 dBm) | ~5–15 € | ~5–15 g |
| Alternativ: Raspberry Pi Zero 2W + USB WiFi (~30 €) | ~15–40 € | ~15–25 g |
| Antenn (patch 3–8 dBi, IPEX) | ~3–15 € | ~5–15 g |
| Pan-tilt-servon (valfritt, se §5) | ~10–30 € | ~37–50 g |
| Primärmissionstab (T/P, IMU, GPS) + radio (LoRa) | ~25–60 € | ~20–40 g |
| **Valfri sensor-lägg** (kamera, magnetometer, strålning) | budget | 10–40 g |
| Batteri (2S LiPo ~10 Wh) | ~15–30 € | 50–70 g |
| Struktur/fallskärm | ~20–40 € | 70–90 g |
| **Summa (utan servo, sparsam)** | **~100–200 €** | **~180–270 g** ✅ |
| **Summa (med servo-styrning)** | ~130–230 € | ~220–320 g ✅ |

→ **Det finns gott om plats** för extra sensorer och för att leka med antenn/gimbal,
samtidigt som ±< 350 g-kravet hålls. Effekten: ESP32-modul drar ~0,1–0,3 W (lite åt
gången), RPi Zero 2W ~0,5–1,5 W — 2S LiPo räcker långt över 2 h-kravet (finskt) / 4 h
(ESA-internationellt, [Luxemburg-manualen](https://www.esero.lu/wp-content/uploads/2026/02/Teams-Manual-2025-2026-Luxembourg-CanSat-Competition-v3.pdf)
kräver 4 h).

**Sensorer som blir naturliga kompisar:** temperatur/tryck (primär), IMU + GPS
(attityd → antenntäckningsanalys!), fotosensor, magnetometer, kamera. IMU-GPS är
speciellt värdefulla: de låter er korrelera **när uppkopplingen fungerade** med burkens
attityd — det blir en riktigt bra "vetenskaplig" del av missionen.

## 8. Förebilder och tidigare bevis

- **[Project Loon](https://www.technologyreview.com/technology/project-loon/)** —
  största beviset på "uppkoppling från himlen till telefoner"; men valde **LTE** (inte
  WiFi) bl.a. p.g.a. WiFi-bandets störningskänslighet. Vår poäng: de *absoluta* avstånden
  här (~1 km) är 20–40× kortare än Loon, vilket kompenserar WiFi:s sämre räckvidd.
- Länkbudget/verktyg: [rftools.linkbudget](https://rftools.io/calculators/rf/rf-link-budget/)
  och SprintWave-FSPL-guiden — bekräftar siffrorna i §2.
- Långdistans-WiFi-bryggor (t.ex. [TP-Link Beam Bridge 5, 15 km @ 23 dBi](https://www.omadanetworks.com/us/business-networking/omada-wifi-wireless-bridge/beam-bridge-5-ur-kit/))
  visar att WiFi *kan* nå mycket långt med riktningsantenner — men de kräver stora
  antenner och låga EIRP-tak tillämpas inte alltid. Dessa är referens för "vad som är
  fysikaliskt möjligt om man hade plats", inte för vår burk.
- Ingen hittad offentlig finsk CanSat har gjort en WiFi-hotspot tidigare → stark
  nyhet/outreach.

## 9. Rekommendation

1. **Baslinje:** ESP32 med **2,4 GHz 20 dBm**, fast **nedåtriktad patch-antenn 3–8 dBi**
   i burkens botten → telefonernas captive-portal visar live-telemetri/webbserver.
   Robust, enkel, inom 500 € och 350 g med stor marginal.
2. **Förstärkt variant (samma dag):** lägg till IMU+GPS och en andra omni-antenn, mät
   faktisk prestanda mot attityd.
3. **Stretch (om tid):** motoriserad pan-tilt till en specifik markstation — med tydlig
   dokumentation att det är ett mekatroniskt riskuppdrag (testas på skakbord + i -20 °C).
4. **Ej nu:** phased array (ryms inte, för komplex, licensfråga) och >10 dBi-paneler
   (kräver utfällning som är riskabel vid 20–30 G och konflikt med 4,5 cm-locket).
5. **Regler att fråga arrangören:** exakt antennbekrivning i Pre-Launch Report
   (SDS-nivå: max 15 sidor, engelska, deadl. 20.2.2027); att en egenbyggd WiFi-sändare med
   fastappliserad antenn och CE-märkt modul är acceptabel; att telefonkoppling inte
   stör LoRa-telemetrin (kanalval); och att hotspot-användningen rapporteras enligt
   Regulation 15.

## 10. Öppna frågor att ställa arrangören

1. Accepteras en **fast applikantenn utanpå burken** som överskrider Ø66 mm *efter*
   utkast (utfällbar), eller måste allt hålla Ø66 mm hela tiden?
2. Får telefoner registreras mot hotspoten (enligt Regel 15-intentionen) eller endast
   för test?
3. Krockar 2,4 GHz-hotspot med tilldelade LoRa-frekvenser/andra lag (kanalplan)?
4. Får vi en **andra frekvens/tid** för WiFi om LoRa kräver 868–915 MHz-länken?
5. Finns krav på att hotspoten stängs av i markläge (landning) eller får den fortsätta?

## 11. Källförteckning

- [Traficom, "Buying and using radio equipment" (licensfritt WLAN, CE, Regulation 15)](https://traficom.fi/en/radio-licences-and-frequencies/users-radio-equipment/buying-and-using-radio-equipment)
- [Wi-Fi RegDB Finland (kanaler/EIRP: 2,4 GHz 20 dBm; 5 GHz DFS/indoor-begränsningar)](https://regdb.lizardsystems.com/country/FI)
- [RF Link Budget Calculator (FSPL, EIRP, marginer)](https://rftools.io/calculators/rf/rf-link-budget/)
- [SprintWave, "Free Space Path Loss" (FSPL förklarat, 2,4 vs 5 GHz)](https://www.sprintwave.co.uk/ccnp-wireless/rf_fundamentals/fspl)
- [Project Loon översikt (MIT Tech Review)](https://www.technologyreview.com/technology/project-loon/)
- [Project Loon tekniskt (Network World: LTE 2,2/2,6 GHz, 40 km radie)](https://www.networkworld.com/article/940020/two-years-on-googles-project-loon-drifts-into-focus.html)
- [LevelOne WAN-2121 12 dBi 2,4 GHz panel (storlek/vikt)](https://www.level1.com/level1_en/wan-2121-12dbi-2-4ghz-directional-panel-antenna-54046107)
- [Taoglas FG.27 12 dBi panelantenn](https://www.taoglas.com/product/fg-27-a-super-compact-12dbi-2-4ghz-directional-panel-antenna/)
- [ESPARGOS One — 2,4 GHz phas ed array, €350, 4×2, PoE](https://espargos.net/espargos-one/)
- [Adafruit Mini Pan-Tilt Kit (37 g, mikroservon)](https://www.adafruit.com/product/1967)
- [OES motoriserad pan-tilt (60 mm, precisionsteg)](https://www.oesincorp.com/motorized-multi-axis-stages/motorized-pan-tilt-mounts.htm)
- [TP-Link Beam Bridge 5 UR (15 km @ 23 dBi — vad WiFi kan med plats)](https://www.omadanetworks.com/us/business-networking/omada-wifi-wireless-bridge/beam-bridge-5-ur-kit/)
- [Finska CanSat-guiden (4,5 cm-utrymme, regler, PLR)](https://www.esero.fi/finnish-cansat-competition-guidelines)
- [Luxemburg CanSat Teams Manual (4 h-batteri-regel)](https://www.esero.lu/wp-content/uploads/2026/02/Teams-Manual-2025-2026-Luxembourg-CanSat-Competition-v3.pdf)

---

## 12. Ny idé: satelliten som relä (bent-pipe) mellan två markstationer 📡

*Utvecklad 2026-11-02. Eftersom en live-demo för telefoner komprimeras för mycket av
~2 minuters flygtid, flyttas fokus till den klassiska "satellittelefonin": **två
högförstärkta markantenner på marken, och CanSaten vidarebefordrar signaler mellan
dem** — precis som en verklig transponder-satellit.*

### 12.1 Konceptet — och att det redan är beprövat

Det här är **exakt** vad amatörradiosatelliter gör: [AO-91 (Fox-1B)](https://www.amsat.org/two-way-satellites/ao-91/)
och [ISS FM-repeatern](https://www.amsat.org/live-fm-satellites/) tar emot på en
frekvens (upplänk) och återsänder på en annan (nedlänk) — en **cross-band/bent-pipe
repeater**. Två radiostationer som inte hör varandra direkt kan prata *genom* satelliten.
Tekniken är väletablerad och pedagogiskt tydlig ("satelliten reläerar min signal!").

Inom CanSat-världen finns redan ett konkret bevis: [CanSat 2003 (Stanford/Morehead)](https://scholarworks.moreheadstate.edu/cgi/viewcontent.cgi?article=1289&context=twiggs_education_collection)
demonstrerade en **ProbeSat → RelaySat → Ground Station-kedja** (fjärrkänslans
temperature levererades till basstationen via en relä-Cansat). Detta är alltså inte
teori — det har gjorts i en CanSat förr.

**Nyckel: high-gain-antennerna sitter PÅ MARKEN, inte i burken.** Den tidigare
lättaste antennbegränsningen i §4 (66 mm-burken) försvinner: markstationerna "äger"
21–33 dBi-diskar/yagis av godtycklig storlek ([TP-Link Beam Bridge 23 dBi](https://www.omadanetworks.com/us/business-networking/omada-wifi-wireless-bridge/beam-bridge-5-ur-kit/),
[LevelOne 12 dBi](https://www.level1.com/level1_en/wan-2121-12dbi-2-4ghz-directional-panel-antenna-54046107)).
CanSaten behöver bara en liten omni/patch som ryms i burken. Det lämnar gott om plats
för annan elektronik/sensorer.

### 12.2 Två-hopp-länkbudget (upplänk + nedlänk)

En relä-länk är **två separata enkelhopp** (mark A → satellite, satellite → mark B).
Vid 750–1100 m-missionsprofilen:

| Enkelhopp (2,4 GHz) | Antagande | Resultat |
|---|---|---|
| FSPL vid ~1,5 km slantavstånd | ~103 dB (rftools) | — |
| Upplänk: mark A (TX 20 dBm + 12 dBi) → burken (0–5 dBi) | ~35 dBm EIRP − 103 dB + 5 dBi | **~−63 dBm vid burken** — god marginal |
| Nedlänk: burken (TX 20 dBm EIRP) → mark B (12–23 dBi) | 20 dBm EIRP − 103 dB + 12…23 dBi | **~−71…−60 dBm vid mark B** — mycket god |
| Slutsats | — | ✔ **Länken sluter med 20–30 dB marginal** |

Viktigt: SFDR-tak skiljer sig mellan upp-/nedlänk — även här är burkens 20 dBm EIRP
begränsningen på **nedlänken**, men höga markantenner kompenserar (>12 dBi). Resultatet:
med två markantenner på >10 dBi blir **bent-pipe-reläet robust över hela nedfärden** —
och det är just den high-gain-idé som *i marken* är praktisk, inte i burken.

**Lägre frekvens = ännu enklare:** på **868 MHz LoRa** (som flesta CanSat-länkar redan
använder) är FSPL ~20 dB lägre (~85 dB vid 1,5 km) och mottagarkänsligheten mycket
bättre (−137 dBm jämfört med WiFi ~−85). Med 868 MHz + 12 dBi-markantenn når man även
nedlänken med enorm marginal, och man kan använda **kryssband** (868 upp, 2,4 GHz ner)
som amatörsatelliterna gör.

### 12.3 När ger reläet faktiskt ett mervärde? (ärlig fråga) 🤔

En två-hopp-länk är **sämre än en direktlänk** om markstationerna hör varandra direkt.
Reläet "lönar sig" när:

1. **Markstationerna inte har fri sikt till varandra** — ett terräng-/byggnadshinder,
   eller avstånd där jordkrökningen/Fresnelzonen bryter direktlänken. CanSaten på ~1 km
   gör att en högpunkt *ovanför* hindret kopplar ihop sidorna — samma princip som
   bergstopp-reläer/eldar.
2. **Missionen är en teknisk demonstration** av "satellitkommunikation i mini": även om
   direktkommunikation vore möjlig är *utmaningen* att visa att signalen gick via
   satelliten (telemetri-verifiering: RSSI-tider + GPS-spår i bägge ändarna).
3. **Store-and-forward (halvrelä):** burken tar emot data under hela flygningen (inte
   bara i realtid), sparar och skickar vidare när den andra marken har kontakt — så att
   tidsfönstret inte är 2 minuter utan nästan hela nedfärden. (Jämför CubeSat
   [store-and-forward/data-mule-studier](http://users.csc.calpoly.edu/~bellardo/pubs/wc10.pdf).)

### 12.4 Regler (868 MHz + 2,4 GHz, licensfritt)

- **868 MHz (CETP/EU SRD, [EFIS-annex 1](https://efis.cept.org/adhoc_grabber.jsp?annex=4)):**
  klubbarna räknas på *e.r.p. (dBd)* — inte e.i.r.p. — och e.r.p. = dBi − 2,15.
  Vanligaste lägen: **h1.5/h1.4 25 mW e.r.p., ≤1 % driftcykel** eller **h1.7
  (869,4–869,65 MHz) 500 mW e.r.p., ≤10 % driftcykel** ([Domca-regelbukett](https://docs.domca.nl/en/usage/regulations/)).
  För en reläe-demo räcker 25 mW gott; mem 500 mW-läget ger längre räckvidd men kräver
  ≤10 % sändtid (enkelt: korta paket + väntan).
- **2,4 GHz:** 20 dBm EIRP (§4) — fritt utomhus, 13/14 kanaler.
- **Kryssband (868 upp / 2,4 ner) är både praktiskt och juridiskt rent** (olika band,
  ingen självblockering). Att *återsända* (relä) är tillåtet för utrustning som uppfyller
  EN 300 328/EN 300 220 — använd CE-märkta moduler, inga förstärkare.
- Självblockering/återkoppling ("feedback") är det klassiska repeterproblemet: på
  samma frekvens kan nedlänken träffa upplänksmottagaren. → Använd **kryssband** eller
  **tid-delning (TDD)** med CE-moduler som gör det internt.

### 12.5 Föreslagen arkitektur (markantennerna bär vinsten)

```
 Mark A (TX/RX)  ──►  CanSat-relä (cross-band, ev. store-forward)  ──►  Mark B (RX/TX)
  868/2,4 GHz           liten omni/patch i burken                          höga antenner
  höga antenner         ~1,7 W effektbudget                               (>12 dBi)
```

- **Markstationer:** två höga 868 MHz-yagis (≥12 dBi, ~30–40 €/st) eller 2,4 GHz-paneler
  (≥12 dBi), vardera kopplade till en SDR/RF-modul + enkel PC. Billigt, och allt ligger
  kvar på marken (ingen mass- eller volymeffekt i burken).
- **CanSat:** bara en befintlig LoRa/WiFi-modul + liten antenn; relä/forward-släms funktion
  i firmware; ~+5–15 g extra. Ingen phased array, inga motorer, inga stora antenner.
- **Datavy: "kanal mellan stationerna" via RSSI/GPS-loggar i båda ändar + en bevis-ton**
  (t.ex. ett testmeddelande "HELLO via CanSat <id>") som bägge sidor loggar. Detta blir
  missionens vetenskapliga/tekniska del — väldokumenterad och verifierbar.

### 12.6 Bedömning och rekommendation

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

### 12.7 Är upplänk olaglig i Finland? — nej, det är en vanlig missuppfattning ✅

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

### 12.8 Begrepp förklarade (radioteknik för nybörjare) 📖

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
  - **ERP:** samma men mot dipol (dBd): **ERP = EIRP − 2,15 dB**. Därför är 25 mW ERPA
    = ~40 mW EIRPA; och 25 mW e.r.p. ≈ **14 dBm ERP ≈ 16 dBm EIRP**.
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

### 12.9 Nedlänk-only ("beacon") — den enklaste, helt lagliga varianten

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

## 13. Källförteckning (tillägg för relä-versionen)

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