# Cloud chamber i CanSat — forskningsöversikt

*Sammanställd 2026-11-02. Syfte: kartlägga fysikaliska krav, regelverk och tekniska
alternativ för en cloud chamber som sekundärmission i en CanSat (CanSat Finland /
ESERO Finland).*

---

## 1. Uppdraget i korthet

En cloud chamber (diffusionskammare) gör joniserande strålning (kosmisk myon- och
elektronstrålning, radon-alfapartiklar) synlig som kondensspår i en övermättad
alkoholånga. Att bygga en sådan i en 330 ml-dryckesburk och flyga den i ~1 km höjd
är oprövat — vi har inte hittat någon dokumenterad CanSat med cloud chamber.
Närmaste föregångare är ballongburna studentexperiment (CADMUS/BEXUS 24 och AC2O,
se §5), där man **inte lyckades få bilder på partikelspår under flygning** trots
fungerande system. Det är viktigt att vara ärlig mot sig själv: största risken är
inte kylan utan **vibrationer/gungande fallskärm + kort mättid**.

## 2. Regler och begränsningar (CanSat Finland / ESERO Finland)

Källa: [esero.fi – Kilpailun vaatimukset](https://www.esero.fi/cansat-kilpailun-vaatimukset)
(obs: "tilapäisiä ohjeita" — slutgiltiga regler publiceras inför tävlingen) och
[ESA – What is a CanSat](https://education.esa.int/what_is_a_cansat/).

| Krav | Värde | Konsekvens för oss |
|---|---|---|
| Volym | Europeisk läskburk: **115 mm hög, 66 mm Ø** | Kammarens synfält blir ~45–50 mm Ø |
| Massa | **300–350 g** (totalt, inkl. batteri) | Mycket snäv budget; kylplatta + PCM måste vägas |
| Budget | **≤ 500 €** | Helt OK med passiv kylning (Arbor-metoden ~60 €) |
| Förbjudna ämnen | **"Räjähteet, sytyttimet, pyroteknik, *palonarat materiaalit*, farliga ämnen och biologiska nyttolaster är absolut förbjudna"** | ALLA alkoholer (isopropanol, etanol, metanol) är brandfarliga → kräver **skriftligt specialtillstånd** från arrangören. Vid misstanke begärs säkerhetsdatablad (SDS). |
| Ström | Batteri/solceller; systemen ska kunna vara på **2 h i sträck** | Peltier-kylning på 50–200 W går inte i 2 h; passiv förfryst kylplatta drar 0 W under flygning |
| Acceleration | Klarar **20 G** | Kammaren måste hållas ihop mekaniskt; vätska i filt fungerar |
| Flygtid | Rek. **≤ 120 s**, utfördesfart 8–11 m/s | Mättid ~60–90 s — mycket kort! |
| Övrigt | Lättåtkomlig batteri- och huvudströmbrytare, återfinnbarhet (GPS/blipp) | Kräver genomtänkt mekanik |

Tävlingen 2027: [Suomen CanSat -kilpailu i Vasa 11–14.3.2027](https://www.esero.fi/cansat-kilpailu),
anmälan 10.9–30.10.2026, lag om 3–5 elever 14+ år.

## 3. Hur en diffusionskammare fungerar (kraven)

Fysiken: [Thesis, Detection of particles with a cloud chamber (UPV/EHU)](http://hdl.handle.net/10810/17990),
[Bellevue College – How to Build a Cloud Chamber](https://www.bellevuecollege.edu/physics/resources/cloudchmbr/),
[Barrett 2024, Phys. Educ. 59 043010](https://iopscience.iop.org/article/10.1088/1361-6552/ad506c).

- **Varm topp** ~30–40 °C: alkohol avdunstar från filt/svamp (värmekälla behövs alltid;
  i mars i Vasa annars ~0–10 °C).
- **Kall botten**: övermättnad skapas av temperaturgradienten. Erfarenhetsvärden:
  - Isopropanol: botten ≈ **-25…-40 °C** (teoretisk analys säger -40 °C för optimalt;
    fungerande Peltier-byggen når -25…-33 °C).
  - **Etanol/metanol: fungerar med varmare botten** (Bellevue: -26 °C; UW-Madison:
    -21 °C förfryst saltvatten fungerar).
- Känsligt skikt är bara ~1 cm högt ovanför den kalla plattan → kammaren behöver vara
  **låg och bred** (petriskål-geometri), inte hög.
- Mörk botten, sidobelysning (LED) med snett infall, kamera ovanför/sidan.

### 3.1 Hur liten kan kammaren göras? (storleksanalys)

**Fysikens egentliga gräns är inte tekniken utan det känsliga skiktet och
träfffrekvensen:**

- **Höjden** bestäms av det övermättade (känsliga) skiktet, som är ~2–4 cm
  i små kammare (Wayne State: 2 cm liten, 4 cm stor; U. Mons: ~5 cm). Skiktet
  ska vara högre än kammarvolymens "döda" delar, men konvektion och dimma växer
  med höjden. Teoretiskt minimiavstånd från alkoholkälla (tråg) till känsligt
  skikt ≈ 1 cm (Bevan 1954), praktiskt behövs ~2–4 cm luft ovanför plattan för
  jämn ångfördelning.
- **Arean** bestämmer antalet spår per minut — myonflödet är ~1/cm²/min vid
  havsnivå, ~30 % högre vid 1 km. Se räkneexempel nedan.

**Dokumenterade minimikammare:**

| Exempel | Mått | Källa |
|---|---|---|
| Glaspetriskål (med α-källa) | Ø 100 mm × 10 mm hög (!) | [Zeze et al. 2012, arXiv:1202.2423](https://ar5iv.labs.arxiv.org/html/1202.2423) |
| Petriskål-kammare med monazitkälla | Ø 90 mm × ~15 mm | [Hayakawa et al., RADIOISOTOPES 61, 297](https://doi.org/10.3769/radioisotopes.61.297) |
| Luftkyld Peltier-kammare | 13×9×9 cm, kallyta 12×4 cm vid -30 °C | [Cloudylabs](http://www.cloudylabs.fr/wp/wp-content/uploads/2019/06/LittleAircooledCloudChamberv2.pdf) |
| Kommersiell kompakt (TEL-Atomic DCC600) | Ø 13–15 cm kallyta | [TEL-Atomic](https://www.telatomic.com/all-produts/tel-dcc-600-diffusion-cloud-chamber) |
| Känslig kammare utan källa (kyld kylfläns) | 134×134×20 mm botten | [Zeze et al. 2012](https://arxiv.org/pdf/1202.2423) |

Viktigt: de allra minsta (petriskål, 10 mm höga) fungerar **bara med en
radioaktiv källa inne i kammaren** — bakgrundsstrålningen ger bara "få spår per
minut i mycket mörkt rum" (Zeze). Utan källa, på ren kosmisk bakgrund, behövs
större yta och mörkare bakgrund.

**Räkneexempel för vår burk (66 mm Ø):**

- Kallyta Ø 50 mm → 20 cm². Myonflöde vid 1 km ≈ 1,3/cm²/min → ~25 myoner/min
  korsar skiktet, varav en bråkdel ger *synliga* spår (erfarenheter: 0,15–0,7
  synliga spår/cm²/min → **3–14 spår/min**).
- Under 60–90 s nedfärd: i storleksordningen **enstaka till ~10 spår** — om
  kammaren är stabil (se CADMUS-varningen §8).
- Krymper man till Ø 35 mm (≈10 cm²) halveras sannolikheten → risk att få **noll
  spår per flygning** ökar tydligt. Ø 45–50 mm är därför en bra kompromiss.

**Praktiska minimimått för vår CanSat-kammare:**
Ø 45–50 mm (kalla plattan), **höjd 40–50 mm totalt** (topp-alkoholfilt +
känsligt skikt + marginal). Under ~35 mm Ø eller ~30 mm höjd blir det en
"källkammare" — inte en kosmisk-strålningsdetektor. Två varningspunkter från
litteraturen: (1) kalla plattan ska inte vara större än nödvändigt och inte
sticka ut utanför kammaren — blottad yta = värmeläckage som förstör kylan
([Cambridge HEP](https://www.hep.phy.cam.ac.uk/outreach/cloud), [Bevan 1954](http://hep.ucsb.edu/people/hnn/cloud/articles/ARBevanJSI31_45_1954.pdf));
(2) nära väggarna finns en zon utan känslighet ([Lyapidevskii 1958](https://doi.org/10.3367/ufnr.0066.195809f.0111))
→ isolera sidoväggarna och håll kammaren så bred som möjligt relativt höjden.

**Kameravinkel:** vertikala myoner ger korta spår sett uppifrån (Wayne State:
"most cosmic rays enter vertically and are too short to be seen" i ett 4 cm
skikt) — sneda/långa spår syns bäst. I en 66 mm-burk är toppkamera + LED-ring
(petriskål-metoden) det kompakta valet; sidkamera genom fönster ger längre spår
men tar plats. Testa båda på markprototypen.

## 4. Kylkällan — alternativ och jämförelse

### 4.1 Torris (-78,5 °C) — troligen inte tillåtet, men fråga!
[CADMUS](https://doi.org/10.29311/2020.07) och [AC2O](https://ac2oubco.wixsite.com/ac2o/our-experiment)
flög med torris. Problem i CanSat-sammanhang: torris måste hanteras på startplatsen
(frostskador, CO₂), sublimerar (förseglad burk = övertryck!), och är logistiskt
jobbigt i Vasa i mars. `Kräver specialtillstånd` likt alkoholen. Se §7.

### 4.2 Peltier (TEC) — fungerar, men strömmen räcker inte till CanSat-regeln
Bevisat fungerande byggen:
- [Barrett 2024](https://iopscience.iop.org/article/10.1088/1361-6552/ad506c):
  två staplade Peltier → **-25 °C**, ~48 W (8 V/6 A), £40. 5 ml IPA räcker 2–3 h.
- [Elektor Peltier Cloud Chamber](https://www.elektormagazine.com/labs/peltier-cloud-chamber):
  en stor TEC + dubbeltorn CPU-kylare → **-33 °C**, ~85 W.
- [William Ivy – Thermoelectric Cloud Chamber](https://www.williamivy.com/posts/cloud-chamber):
  3-stegs TEC + vattenkylning → **-37,7 °C**.
- [MIT SB-thesis (Larson 2018)](http://hdl.handle.net/1721.1/119952):
  flerstegs-TEC + vätskekylning → **-40 °C på 2 min**, men **224 W**.

Slutsats: för att nå -25…-40 °C behövs ~50–200 W plus kylfläns/fläkt — **omöjligt**
mot batteribudgeten 2 h i 300–350 g burk. Endast intressant som **marktest-/hybridlösning**
(§6.3).

### 4.3 Passiv förfryst kylplatta / fasändringsmaterial (PCM) — BÄSTA KANDIDATEN ⭐
Precis som [Arbor Scientific Cloud Chamber](https://www.arborsci.com/products/cloud-chamber)
(”freezer-chilled cold plate”, ~1 h kyla, ~20 min spår per körning med etanol) och
[UW-Madison saltvatten-receptet](https://medphysics.wisc.edu/wp-content/uploads/2021/04/Cloud-Chamber-Lesson-Plan.pdf)
(-21 °C förfryst saltvatten fungerar i klassrum):

- **0 W effekt under flygning** — uppfyller 2 h-regeln och 500 €-budgeten.
- **Material: svart eloxerad aluminium** (inte koppar!) — platta 50 mm Ø × 3 mm väger
  bara **~16 g** mot kopparns **~53 g** (densitet 2,70 vs 8,96 g/cm³). Besparing ~37 g
  = över 10 % av CanSats massbudget. Kopparns bara ~2× bättre värmeledning (385–400
  mot ~170–230 W/m·K) spelar ingen praktisk roll vid den lilla värmelasten (1,5–3 W):
  temperaturfallet genom plattan blir <0,02 K för båda. Aluminium har dessutom ~2,3×
  högre specifik värmekapacitet per kg (900 mot 385 J/kg·K). Svart eloxering ger
  samtidigt den mörka bakgrund som behövs för spårkontrast (samma platta som
  [CERN](https://scoollab.web.cern.ch/sites/default/files/documents/20200521_JW_DIYManual_CloudChamber_v7.pdf)
  och [U. Mons](https://orbi.umons.ac.be/bitstream/20.500.12907/22502/1/Wilson_v1_red.pdf) använder).
  **Varning:** NaCl-brinen ger gropfrätning på aluminium (och korroderar även koppar) —
  brinen måste hållas **förseglad i en påse** (frys-/HDPE-påse, dubbelförseglad), aldrig
  i direkt kontakt med plattan.
- Massa: aluminiumplatta ~16 g + PCM-påse ~50–80 g.
- Fryses kvällen innan och transporteras i isolerad låda (styrox/kylbox) till
  startplatsen. **Varning: NaCl-brinen fryser först vid -21,2 °C** — en vanlig
  hemfrys (-18 °C) räcker inte för eutektisk koncentration; använd en svagare
  lösning (~20 %, fryspunkt ~-16 °C) i hemfrys, eller helst en riktig frysbox
  (snabbköps-/laboratoriefrys, ≤-25 °C) för full kylkapacitet
  ([Radebe & Huan 2023](https://www.sciencedirect.com/science/article/pii/S2352152X23003572)).
  Fråga skolan/arrangören om tillgång till kall frys på tävlingsorten!
- **Nyckelfråga: hur lång tid från frys till start?** Check-in → start kan vara
  timmar (se §7, fråga arrangören).
- Med -21 °C platta: välj **etanol** (fungerar varmare än IPA, [Bellevue](https://www.bellevuecollege.edu/physics/resources/cloudchmbr/),
  [UW-Madison](https://medphysics.wisc.edu/wp-content/uploads/2021/04/Cloud-Chamber-Lesson-Plan.pdf)).
- Isolera burken (styrox/XPS 1–2 cm) så håller plattan kall under väntan och flygning.

### 4.4 Miniatyrkompressor (12 V ångkompression) — för tung
[RIGID QX1401VDL](https://www.rigidhvac.com/12v-mini-compressor): 720 g, 82×56 mm,
300 W kyleffekt. Enbart kompressorn väger mer än dubbla hela CanSats massa. Avfärdad.

### 4.5 Kall luft på höjden — räcker inte
Vid 1 km är luften bara ~5–10 °C kallare än vid marken. ~-25 °C kräver aktiv kylning
eller förfryst massa. (Intressant dock: kall omgivning *hjälper* topp-→botten-gradienten
och minskar värmeläckaget in i plattan.)

### 4.6 Stirling-kylare / mikro-kryokylare — aktiv kylning i rymdklass (men för dyr och tung nu)
Mikro-kryokylare av Stirlingtyp är den teknik som kylsensorer i riktiga satelliter/IR-kameror.
Exempel: [LE-TEHNIKA SRI421](https://cryocoolers.eu/integral-miniature-stirling-cryogenic-cooler-025w/) —
12 V, **<5 W i drifthåll vid 80 K (= -193 °C!)**, <14 W under nedkylning (~5 min),
**<200 g**, MTBF >10 000 h. För en cloud chamber behövs bara ~-25…-40 °C (= ~230–250 K),
vilket Stirling-kylaren når med **avsevärt lägre effekt** än vid 80 K.
- Fördelar: rymdkvalitet, beprövad, nedkylning på minuter, klarar -40…+71 °C omgivning.
- Nackdelar: kostnad (~1500–1700 €/enhet enligt [Arctic-Tek MiniCool-serien](https://www.arctic-tek.com/store/categories/Stirling%20Cryocooler))
  → **långt över 500 €-budgeten**, plus vikt (~200 g + styrenhet) i en 300–350 g-burk.
- **Slutsats:** fysikaliskt idealisk, men för dyr och för tung för CanSat i dag. Värd att
  ha i bakfickan som referens och för en framtida campingkylare-baserad vidareutveckling.

### 4.7 CO₂-patron / Joule–Thomson — "torris på plats" 🧊
Joule–Thomson-expansion av flytande CO₂ från en sifonbehållare ger **torrissnö vid
-78 °C direkt på plats**, utan någon frys: bärbara "portable dry ice makers"
([Agar Scientific](https://mcprod.agarscientific.com/portable-dry-ice-maker),
[Bel-Art Frigimat](https://belart.com/products/cold-cryo/dry-ice-makers/frigimat-dry-ice-maker/))
producerar ~0,5–1 kg torrisblock på 1–2 minuter ur en flytande CO₂-cylinder med dykrör.
- **Detta löser logistikproblemet i §4.3:** i stället för att frakta torris (eller behöva
  en ≤-25 °C-frys) till startplatsen, **generera torrisen på plats** och packa den runt
  kylplattan eller som laddning av en lägre-tempererad PCM (§4.10).
- För CanSat: en liten **sifon-CO₂-patron** (t.ex. sodastream-/kolsyrepatron) räcker för
  att skapa torrissnö. Kräver hantering av -78 °C-snö (vantar, skyddsglasögon), tryckkärl
  (ADR-reglerad, fråga arrangören) och får inte medföras förseglat (övertryck om den töms i
  sluten volym).
- Slutsats: **utmärkt som "torrisrörligt lager" vid tävlingsorten** för att frysa en
  PCM-platta strax före start — kombineras med passiv metod.

### 4.8 Vortex-rör (Ranque–Hilsch) — kyla ur tryckluft
Ett [vortex-rör](https://www.sciencedirect.com/science/article/abs/pii/S1364032115007509)
separerar tryckluft i en varm och en kall ström — inga rörliga delar, ingen el, inget
köldmedium. Upp till **70 °C temperatursänkning**; kommersiella enheter kyler med luft
vid ~700 kPa; CO₂, syre och kväve ger lägre temperaturer än luft ([Oberlin-demo](https://www2.oberlin.edu/physics/catalog/demonstrations/thermo/vortextube.html):
Tc < 0 °C "easily").
- Lockande i teorin (cloud chamber nedkylning "gratis" ur tryckluft), men praktiskt för
  CanSat **olämpligt**: kräver en trycklufts-/gasbehållare med kontinuerligt flöde (tung,
  tar slut, bullrigt), separat varm-utlopp som måste frånluftas ur burken, och effektiv
  kylning av plattan kräver god värmeövergång. Bättre som **markdemonstration** (ingen
  Peltier, ingen frys behövs — kul fysiklek!).

### 4.9 Flytande kväve (LN₂) — snabbast, men bara för laboratorium/startplats
Standard i universitetsdemonstrationer: [UT Austin](https://lecturedemos.ph.utexas.edu/demo/311)
och [Vanderbilt](https://www.vanderbilt.edu/physicsdemonstration/davesdemos/demonstrations/demo106.htm)
häller LN₂ (-196 °C) i kärl under plattan — spår i 5–20 min per påfyllning, med etanol.
- För CanSat: **inte lämpligt ombord** — kokar bort (förseglad volym → övertryck), kräver
  dewarkärl, hantering runt skolungdom och raketbana är riskfyllt, och boil-off äter
  kylan snabbt. Däremot utmärkt **vid skolan/startplatsen** för att snabbt förfrysa en
  PCM-platta eller ladda en lägre-tempererad eutektik (§4.10) innan den isoleras — om en
  institution (universitet/sjukhus) kan låna ut dewarn.

### 4.10 Lägre-tempererade eutektiska PCM:er — nyckeln till isopropanol
Passiv PCM behöver inte stanna på -21 °C! Det finns kommersiella saltvatten-eutektika
ned till långt under noll:
- [Rubitherm SP-serien](https://www.rubitherm.eu/en/productcategory/anorganische-pcm-sp):
  **SP-24 (-23…-22 °C), SP-28 (-29…-28 °C), SP-30 (-30…-29 °C)** med ~250–260 kJ/kg,
  ända till SP-50 (-52…-48 °C, 190 kJ/kg).
- [PlusICE-katalogen](https://www.pcmproducts.net/files/eutectic_catalogue-2011-1.pdf)
  (PCM Products) har lösningar från -100 °C till +89 °C, i påsar/plattor; används i
  kylkedjor och lastbilar ([Mousazade & Rafee 2020](https://www.sciencedirect.com/science/article/abs/pii/S0140700720303753)
  testar E-26/E-29/E-32-paneler).
- **Konsekvens:** med en SP-30-platta kan plattan hålla ~-30 °C passivt → **isopropanol
  fungerar** (som kräver -25…-40 °C), och marginalen mot etanolens -21 °C blir stor.
- **Laddningskravet är den enda haken:** PCM:en måste frysas *under* sin smälttemperatur,
  dvs. SP-30 kräver ≤-30 °C (industrifrys, LN₂ eller torris — den senare skapas gratis
  med CO₂-patron-metoden i §4.7). Vanlig hemfrys (-18 °C) laddar bara NaCl-brinen (-21 °C).
- Slutsats: **passiv metod + lägre-tempererad eutektik (SP-24/28/30) laddad med torris/LN₂
  = bästa vägen till IPA**, om laddningslogistiken ordnas (§7, fråga 8).

### 4.10.1 Sammanfattning — alla kylmetoder på en gång

| Metod | Temp | Elbehov | Vikt/budget | Dom |
|---|---|---|---|---|
| **Passiv PCM (NaCl -21 °C, §4.3)** | -21 °C | 0 W | ~100–160 g, billig | ⭐ **Baslösning** — etanol, överallt |
| **Passiv PCM låg-temp (SP-24/28/30, §4.10)** | -24…-30 °C | 0 W | ~100–160 g, måttlig | ⭐ **om ni får IPA + kylmedel** — bästa kvalitet |
| Torris (§4.1) | -78 °C | 0 W | liten | Med lov; logistikbesvärlig |
| CO₂-patron/JT (§4.7) | -78 °C (snö) | 0 W | liten | 🧊 **Bra "torris på plats"** som stöd |
| Peltier-flersteg (§4.2) | -25…-40 °C | 50–200 W | ~100–200 g | Marktest/hybrid — inte ombord |
| Stirling-mikrokryo (§4.6) | -80 K-klass | <5–14 W | ≥200 g, 1500+ € | Rymdklass men för dyr/tung |
| Minikompressor (§4.4) | -25…-40 °C | 30–100 W | >720 g | För tung (dubbla CanSat!) |
| Vortex-rör (§4.8) | <0 °C (till ~-70 ΔT) | tryckluft | cylinder | Markdemonstration endast |
| LN₂ (§4.9) | -196 °C | 0 W | dewar | Bara labb/startplats (laddning) |
| Kall luft på höjden (§4.5) | ~-5…-10 °C | 0 W | 0 | Räcker inte |

## 4.11 Energi och värme — hur mycket drar burken, och blir värmen ett problem?

### 4.11.1 Energibudget (utan Peltier)

| Del | Effekt |
|---|---|
| MCU (Arduino/ESP32) | 0,1–0,5 W |
| Radio 1 Hz (LoRa) | 0,1–0,5 W |
| Sensorer + GPS | 0,05–0,2 W |
| Kamera + SD + LED | 0,6–2 W |
| Toppvärmare (termostat, PWM) | 0,5–2 W |
| **Totalt (~medel)** | **~2–4 W** |

- **2 h-regeln:** 2–4 W × 2 h = **4–8 Wh** → t.ex. 2S LiPo 1000–1500 mAh (7,4–11 Wh,
  50–70 g) räcker. Alternativt 2× 18650 (~18 Wh, ~100 g) med stor marginal.
- Jämför med Peltier (50–200 W): 2 h skulle kräva 100–400 Wh ≈ 1–4 kg batteri →
  **helt uteslutet**. Ännu ett skäl till passiv PCM-kylning.
- Slutsats: **energin är inget problem** så länge Peltier inte används. Värmen är det.

### 4.11.2 Värmen är problemet — på tre sätt

**(a) Värmeläckage in i kalla plattan — den kritiska budgeten.**
Kammaren ska ha +30…40 °C på toppen och -21 °C i botten, bara ~5 cm från varandra.
Läckaget ned mot plattan (räknat för Ø50 mm, höjd 50 mm):

| Väg | Uppskattat läckage |
|---|---|
| Genom luften i kammaren (konduktion) | ~0,06 W |
| Genom kammarväggen (akryl 3 mm) | ~0,1 W |
| Värmestrålning topp→botten | ~0,3–0,6 W |
| Konvektion inuti kammaren | 0,5–1,5 W (störst, svår att undvika) |
| PCM-paketets yta mot burkens insida (2 cm XPS) | ~0,3–0,5 W |
| **Summa på kallplattan** | **~1,5–3 W** |

Med mindre noggrann isolering/konvektion kan det bli 3–5 W — då är kylbudgeten slut
på nolltid.

**(b) PCM:ns kylbudget = livslängd för experimentet.**
NaCl-eutektikum 23,3 % smälter vid **-21,2 °C** med latent värme **228–257 kJ/kg**
([MDPI 2021](https://www.mdpi.com/1996-1074/14/11/3033), [Radebe & Huan 2023](https://www.sciencedirect.com/science/article/pii/S2352152X23003572)).

| PCM-massa | Latent energi | Tid till slut vid 2 W | vid 3 W |
|---|---|---|---|
| 60 g | ~15 kJ | ~2,1 h | ~1,4 h |
| 80 g | ~20 kJ | ~2,8 h | ~1,9 h |
| 100 g | ~25 kJ | ~3,5 h | ~2,3 h |

**Detta är dimensionerande:** check-in → start kan vara 1–4 h (officiellt ska CanSaten
vara inlämnad kl 12, lansering 13 → i värsta fall timmar i vila) + 2 min flygning.
Med 80–100 g PCM och ~2 W läckage klarar man 2–3 h — men marginalen är tunn. Tre
motåtgärder: (1) minimera läckaget (isolering, låg emissivitet på plattans ovansida,
hindra konvektion med tunn folie/lager), (2) håll kammaren **avstängd** (ingen
toppvärmare) tills strax före start så att gradienten bara byggs upp när det behövs,
(3) förvara den frysta enheten i en **isolerad transportlåda/kylbox ända fram till
integreringen**. Lägg till fråga till arrangören: när exakt integreras/startas burken?

**(c) Elektronikvärme i en isolerad burk — överhettning.**
2–4 W kontinuerligt i en **helt** isolerad 330 ml-burk (2 cm XPS överallt) ger
innertemperatur som kan stiga ~50 K över omgivningen — batteri och kamera mår dåligt
över 60–70 °C. Lösningar: isolera **endast kammaren/PCM**, låt elektronikdelen sitta
mot burkväggen av aluminium (värmeväg ut, typisk ΔT bara ~10–15 K i mars-väder) och/eller
ha små ventilationshål (fråga arrangören om det är tillåtet). Räkna också med
soluppvärmning på startplattan — den internationella CanSat-guiden kräver att burken
tål 60 °C i 2 h i värmekammare ([CanSat 2026-guide §3.3](https://cansatcompetition.com/docs/CanSat_Mission_Guide_2026e.pdf));
fråga om finska regler har motsvarande krav.

**(d) Bonus — låt elektroniken värma toppen.**
MCU + radio + kamera avger 1–2 W spillvärme. Placera elektroniken **i toppen av
kammaren**, så behövs bara en liten extravärmare (0,5–1 W) för att nå 30–40 °C — eller
ingen alls. Två flugor i en smäll: elektroniken kyls av den kalla omgivningen, och
toppen värms "gratis". (Detta var också CADMUS-lösningens andemening — se §8.)

## 5. Alkoholen — isopropanol vs etanol vs metanol, och tillståndsfrågan

| Ämne | Flampunkt | Botten-temp som krävs | För/nackdelar |
|---|---|---|---|
| **Isopropanol (IPA)** | 12 °C (H225, [TTL-OVA](https://ova.ttl.fi/isopropanoli)) | -25…-40 °C | Bäst fysik ([UPV/EHU](http://hdl.handle.net/10810/17990)), standard i Peltier-byggen; 70%-ig IPA duger **inte** ([Bellevue](https://www.bellevuecollege.edu/physics/resources/cloudchmbr/)), behöver 90–99 % |
| **Etanol** (95 %+) | 13 °C | -21…-26 °C | **Fungerar med varmare platta → passar förfryst PCM-platta**; flyktigare (tar slut snabbare, men flygningen är bara ~2 min); lätt att köpa (Eteka/apotek) |
| **Metanol** | 11 °C | ~-26 °C | Fungerar men **giftigt** — olämpligt i skolprojekt, försäljning reglerad i Finland ([Tukes](https://tukes.fi/kemikaalit/kemikaalien-vahittaismyynti)) |

**Regel 7 förbjuder "palonarat materiaalit" (lättantändliga ämnen) absolut.**
Alla tre alkoholerna är lättantändliga → **specialtillstånd krävs oavsett val**.
Strategi för att få tillståndet:

1. Kontakta ESERO Finland/arrangören **tidigt** med en skriftlig riskbedömning.
2. Argumentera med: **så liten mängd som möjligt (5–10 ml)** i en **förseglad kammare**
   (ingen läcka → ingen brandrisk), inga tändkällor i burken, SDS bifogas
   (arrangören begär SDS "i misstänkta fall" enligt regel 7 — ta initiativet).
3. Alternativ formulering: kammaren är en **förseglad modul** som hanteras av vuxen
   mentor; mängden understiger alla nationella transporttrösklar för brandfarlig vätska
   som medförs privat (< 1 l i originalförpackning, ADR-undantag för småmängder —
   verifiera).
4. Ha en **plan B-mission** redo (se §8) om tillståndet nekas.

Etanol rekommenderas i första hand p.g.a. varmare tillåten bottenplatta (passar passiv
frysplatta); IPA om ni ändå får lov och kör Peltier på marken.

## 6. Koncept och massbudget

### 6.1 Rekommenderat koncept (passivt)

```
┌────────────────────────────┐  ← topp: liten motståndsvärmare ~1–3 W (30–40 °C)
│  filt/svamp med 5–10 ml    │
│  etanol (eller IPA)        │
│  genomskinlig kupol        │  ← kammare Ø ~50 mm, höjd ~40–50 mm, tätad
│  (akryl/petriskål)         │
│  mörk eloxerad aluminiumplatta -21 °C │  ← kylplatta + PCM (förfryst), isolerad undersida
├────────────────────────────┤
│  LED-sidobelysning +       │
│  kamera (OV2640/OV5640)    │  ← ~15 g; SD-kort; video under flygning
│  MCU + radio + GPS/blipp  │
│  batteri (~10 Wh)          │
└────────────────────────────┘
```

- **Tillverkning/tester på marken först**: bygg omvänt (kammaren som petriskål ovanpå
  förfryst platta), verifiera spår med radonkälla/thoriumstav + kosmisk bakgrund.
- Värm elementet med litet motstånd (eller återanvänd varm platta från elektroniken —
  mät först).
- Kameran filmar hela nedfärden; bildanalys efteråt (spårräkning manuellt/med
  datorseende) — AC2O-metoden ([AC2O](https://ac2oubco.wixsite.com/ac2o/our-experiment)).

### 6.2 Massa (måste hamna i 300–350 g)

| Del | Massa |
|---|---|
| Kylplatta (eloxerad aluminium 50 mm Ø × 3 mm) + PCM (~50 ml saltvattenpåse) | ~70–100 g |
| Kammare (akrylkupol, tätning, filt, LED) | ~40 g |
| Kamera + SD | ~15 g |
| MCU + radio + sensorer (T/P, lutning) | ~25 g |
| Batteri ~10 Wh (2× 18650 eller LiPo) | ~60–80 g |
| Struktur + isolering (styrox + burk) | ~50–70 g |
| Fallskärm + fästanordning | ~20 g |
| **Summa** | **~310–380 g** → trimma med tunnare platta/PCM |

### 6.3 Hybrid (om tillstånd + logistik tillåter)
Peltier på marken för att förkyla plattan till -30…-40 °C strax före start, sedan
passivt under flygning. Kraftigare gradient → kan använda IPA. Men: kräver tillgång
till nätström/powerbank vid padden och bryter delvis mot "2 h på batteri" — fråga
arrangören.

## 6.4 RGB-strobe — tidsupplöst spårfotografering (idé: RGB-strobe-utlöst bildtagning)

*Idé från laget: en ljusdetektor i kammaren detekterar när en partikel passerar,
varefter RGB-strobar blixtrar en i taget under en enda kamerabild — så att spårets
utveckling (födelse → tillväxt → sjunkande droppar) syns som rött, grönt och blått
i samma bild.*

**Kortbedömning: idén är både genomförbar och vetenskapligt stark — med en viktig
korrigering av tidskalan: millisekunder, inte mikrosekunder.**

### 6.4.1 Händelseförloppet — varför µs är fel tidskala

| Tid efter passage | Vad händer | Rörelse |
|---|---|---|
| 0 (ns-skala) | Myonen passerar, ~230 joner/cm längs banan | ~c → ingen bildbar rörelse |
| ~10–200 ms | Droppar växer till synlig storlek (r²∝t, [Barrett & Germain 1947](https://pubs.aip.org/aip/rsi/article/18/2/84/296528/Growth-of-Drops-Formed-in-a-Wilson-Cloud-Chamber)) | ~stillastående |
| ~50–500 ms | Spåret är synligt; droppar faller med Stokes sluthastighet | **~1 cm/s vid r=10 µm**, r²∝v → ~9 cm/s vid r=30 µm ([Blackett 1934](https://royalsocietypublishing.org/rspa/article-pdf/146/857/281/28637/rspa.1934.0154.pdf), [UVic-ekvationer](https://particle.phys.uvic.ca/~jalbert/chamber.pdf)) |
| ~0,5–1 s | Droppar sjunkit ur det känsliga skiktet; skiktet återhämtar sig på några sekunder | — |

En 10 µm-droppe faller **10 nm per µs** — på mikrosekundnivå står allt helt stilla
(och partikeln själv avger dessutom inget ljus). *Det* µs-upplösning är bra för är
att frysa varje blixt (ingen rörelseoskärpa) — men den information som RGB-färgerna
ska visa (tillväxt + sjunkande droppar) utspelar sig på **10–500 ms**.

### 6.4.2 Ljusdetektorn — det fysikaliskt viktigaste valet

**Partikeln kan INTE detekteras av ljus** — den avger inte ljus i kammaren. Det
ljusdetektorn kan se är det spridda ljuset från dropparna *efter* att de vuxit
(~10–100 ms efter passage). Två möjligheter:

- **(a) Fotodiod/SiPM i mörkerfält** (rekommenderas, enkelt): en fotodiod med lins
  tittar på det känsliga skiktet bakifrån/ovanifrån; när spåret uppstår ökar det
  spridda ljuset abrupt → komparator → trigger. Fångar spåret redan i sin tidiga
  fas. Latens ~ms räcker gott (spåret lever ~0,1–0,5 s).
- **(b) Scintillator-matta + SiPM** (avancerat, historiskt!): två tunna
  scintillatorplattor över/under kammaren i koincidens detekterar **partikeln
  själv** på ns-skala — exakt den metod Blackett & Occhialini uppfann 1934
  ("counter-controlled cloud chamber", [Leone 2011, AJP](https://pubs.aip.org/aapt/ajp/article/79/5/454/1057670/Particles-that-take-photographs-of-themselves-The),
  [Blackett 1934](https://royalsocietypublishing.org/rspa/article-pdf/146/857/281/28637/rspa.1934.0154.pdf))
  och som användes för att upptäcka myonen 1937. Ger spåret från allra första
  tillväxtstart och **dubblerar dessutom som partikelräknare** (myonmätning!).
  Kostar ~30–60 € och ~15 g extra — värt att utreda som upgrade.

Tips: låt triggerljuset vara en **separat IR-LED + IR-fotodiod** — IR syns inte i
kamerans färgkanaler, så det kan stå på konstant utan att störa RGB-bilden.

### 6.4.3 Strobar och kamera — praktiskt utförande

- **RGB-strobar:** tre högströms-LED (röd ~660 nm, grön ~525 nm, blå ~450 nm, alltså
  inga fosfor-vita LED — fosforn eftersläpar µs-skala!). Överdriv 10–50×: LED klarar
  pulsströmmar på 10–200 A i µs–ms utan skada ([Wilson et al. 2014](https://doi.org/10.1007/s12650-014-0220-7),
  [frozentime.se-blixtbygget](http://frozentime.se/ljus/high_speed_leds.html) — 5 µs
  blixtar, RGB-filtrerade, med exakt den här metoden för att filma 10 µm-droppar!).
  Energi per händelse: ~0,1 J/färg → **~0,1 W i snitt** vid 10 spår/min. Försumbar.
  Kondensatorbank + MOSFET-drivare; skärma/EAV-skydda radion.
- **Sekvens:** R@t=0, G@t+20–50 ms, B@t+40–100 ms, pulsbredd 0,1–1 ms (fryser
  rörelsen: 1 cm/s × 1 ms = 10 µm oskärpa ≈ pixel). Tillväxt + fall ger tydliga
  färgförskjutningar på pixelnivå.
- **Kamera:** en exponering på ~150–300 ms som täcker hela RGB-sekvensen ger EN bild
  med tre färgsnapshot. Varning: rullande slutare (rolling shutter) gör att blixtarna
  hamnar på olika rader → "regnbågsband" — antingen synka blixtarna mot slutarens
  radfart eller (enklast) ta **3 korta exponeringar, en per färg**, och
  sammanfoga i programvara efteråt. Kameran behöver bara ~20 fps; spåret lever kvar
  över flera bildrutor.
- **Fallback (ännu enklare):** ingen trigger alls — cykla RGB kontinuerligt synkat
  med kamerans bildrutor och välj spårbilder i efterhand. Fungerar alltid, men ger
  mer data att sortera.

### 6.4.4 Vetenskapligt utbyte — bättre än en vanlig kammare

1. **Tidsupplöst spårutveckling i EN bild:** rött = ungt spår (små droppar),
   grönt = tillväxt, blått = sjunkna/längre hållna droppar.
2. **Mätbar fysik:** färgförskjutningen mellan kanalerna ger dropparnas fallhastighet
   → via Stokes lag → **droppstorlek** → indirekt skattning av övermättnaden.
3. **Myonräkning** (om scintillatorn version (b)): kompletterar kammaren som detektor.
4. Data per händelse = EN liten bild i stället för videoström — passar CanSats
   begränsade lagring/radio perfekt.

### 6.4.5 Risker

- **Falska triggers** (damm, vibrationer, ljusläckage — burken gungar under
  fallskärmen!): grindtriggern med accelerometern (endast aktiv under stabil nedfärd)
  och hysteres på komparatorn.
- **Rolling shutter-banding** — se ovan; testa på marken med en thoriumstav/radonkälla.
- **IR-störning:** kontrollera att IR-triggen inte läcker in i kamerans färgkanaler.
- Genomför **marktest på skolbänken först**: thoriumstav (svetsmunstycke) eller
  radon i källaren ger rikliga spår att öva triggerns tröskel och bildsekvensen på.

## 7. Frågor att ställa arrangören (innan designen låses)

1. Får vi flyga en **förseglad kammare med ≤ 10 ml etanol/isopropanol** om vi lämnar
   SDS + riskbedömning? (Regel 7: "i misstänkta fall begärs säkerhetsdatablad".)
2. Alternativt: är **torris med specialtillstånd** möjligt som kylkälla?
3. **Hur lång tid går det från check-in/integrering till start?** (Avgör om en
   förfryst platta utan kylskåp på plats håller. Kan vi få tillgång till frys/kylbox
   på tävlingsområdet, eller installera kylplattan sent?)
4. Gäller 2-h-regeln **hela systemet** eller bara telemetri/sensorsystemet?
   (Påverkar hybrid-Peltier-alternativet.)
5. Får kammaren vara **tät** (ingen tryckutjämning), och tål burken ~0,9 atm
   differenstryck vid 1 km + övertryck vid 20 G?
6. Är det OK att burken är **isolerad** (kan inte vara standardläskburkens väggtjocklek
   utan egen cylinder)?
7. Får vi **ventilationshål** i burken för elektronikkylning (eller ska all värme ledas
   ut via aluminiumväggen)?
8. Finns en **riktig frys (≤-30 °C)** eller **tillgång till torris/CO₂-patron/LN₂** på
   tävlingsområdet, och hur sent före start får kylplattan installeras? (Avgör om
   PCM-metoden fungerar och om vi kan använda lägre-tempererad eutektik/IPA — se
   §4.3, §4.7 och §4.10.)
9. Finns ett **krav på värmetest** (t.ex. 60 °C i 2 h som i internationella
   [CanSat-guiden](https://cansatcompetition.com/docs/CanSat_Mission_Guide_2026e.pdf))?
   Soluppvärmning på startplattan?
10. Electronicans **spillvärme** (1–2 W) — OK att den används för att värma
    kammartoppen?

## 8. Vad kan vi realistiskt mäta? (fysik, ärligt talat)

- Myonflöde vid havsnivå ≈ **1 myon/cm²/min** (~70 m⁻²s⁻¹sr⁻¹ vertikalt);
  vid 600 m ≈ +36 % ([IJMPA 2018](https://doi.org/10.1142/s0217751x18501750));
  tumregel ~+10 % per 300 m ([OSTI 1631248](https://www.osti.gov/servlets/purl/1631248)).
  Vid 1 km: **~30 % högre än vid marken** — inget dramatiskt, men mätbart om kammaren
  fungerar.
- Synfält ~20 cm² → i storleksordningen **tiotals myoner/minut genom det känsliga
  skiktet**; under 60–90 s nedfärd kan flera spår fångas — *om* kammaren är stabil.
- **Största risken: mekanisk störning.** [CADMUS](https://doi.org/10.29311/2020.07)
  (ballong, lugnt!) fick **inga spårbilder** p.g.a. försenade värmare + fokusändring
  när torrisen sublimerade. En gungande fallskärm vid 8–11 m/s stör övermättnadsskiktet.
  → Målbild: **teknikdemonstration** (gradienten fungerar under flygning, temperatur-
  loggning, video) med **spår som bonus**, inte huvudkrav. Det är redan ett starkt
  bidrag: ingen har gjort det i en CanSat tidigare.
- Alternativ vid nej-tillstånd: **scintillator/Geigerräknare** som strålningsmission
  (t.ex. [REXUS-25 PR3](https://doi.org/10.22323/1.358.0124): 1 dm³, 1 W, mäter
  höjdberoendet) — robust och billigt, men inte en cloud chamber. Kan kombineras:
  cloud chamber på marken som demonstration, Geiger i luften som data.

### 8.1 Hur resilient är en cloud chamber mot vibrationer? — den tuffaste frågan i projektet

**Kort svar: en diffusionskammare är en *stillastående-gasmätare*. Vibrationer och
accelerationer blandar gasen och förstör övermättnadsskiktet — resiliensen är LÅG
mot kontinuerlig vibration, men tolerabel mot korta transienter, *om* kammaren byggs
införstått.**

#### Fysiken: varför vibrationer är dödliga för diffusion

- Diffusionskammarens hela funktion bygger på **stillastående gas** med en stabil
  temperaturgradient; övermättnadsskiktet (2–5 cm högt) finns bara där ångan
  diffunderar lugnt nedåt. Allt som rör om gasen — vibration, gungning, rotation,
  accelerationsändringar — blandar varm/kall gas och skiktet kollapsar
  ([U. Mons](https://orbi.umons.ac.be/bitstream/20.500.12907/22502/1/Wilson_v1_red.pdf)).
- Skillnad mot expansionstypen: en **expansionskammare**, som Wilson/Anderson använde,
  är bara känslig i ett ögonblick efter en snabb expansion och tål rörelse mycket
  bättre — Anderson & Neddermeyer flög faktiskt en expansionkammare i en **B-29 bombplan**
  på 13 500 m höjd och tog 3 500 bilder (i ett tryckkabin, med konstant temperatur och
  snabb 4 ms-expansion). Vår **diffusionskammare** har ingen sådan "frys-ögonblick" -
  det är just detta som är den stora utmaningen ([Cowan 1949 RSIm str.](https://www.pp.rhul.ac.uk/~cowan/EWC/RevSciInstrum_20_492.pdf),
  [Adams, Caltech-thesis](https://doi.org/10.7907/dvvv-ts23)).
- De viktigaste skadenivåerna, uppifrån och ned:
  1. **Mekanisk sammanblandning av gasen** (> ~0,1 g, kontinuerlig): övermättnadsskiktet
     förstörs. Det är känsligare än man tror — även konvektionsströmmar av ren termisk
     natur stör kammaren; forskare har ägnat hela artiklar åt att eliminera "subtle
     convective flows" som stör nucleation ([Bertelsmann & Heist 1997](https://pubs.aip.org/aip/jcp/article/106/2/624/479112/Two-dimensional-transport-and-wall-effects-in-the),
     [Ferguson & Nuth 1999](https://pubs.aip.org/aip/jcp/article/111/17/8013/184268/The-influence-of-buoyant-convection-on-the)).
  2. **Accelerationsändringar mellan 0 och ~20 g** (raketstart → fritt fall): ändrad
     tyngdkraft gör att densitetsgränser i kammaren omfördelas, skiktet flyttar sig eller
     välter.
  3. **Vätskerörelse**: om flytande alkohol samlas på plattan slår den omkull vid 20 g
     och vid fallskärmsgungning.
  4. **Mekaniska trasor**: ram, fokus, kablar, filt som lossnar under vibration.
- Återhämtningstid: efter en störning återbildas övermättnadsskiktet först efter att
  gasen lugnat sig — i praktiken **sekunder till ~1 min** innan spår blir tydliga igen
  ([U. Mons](https://orbi.umons.ac.be/bitstream/20.500.12907/22502/1/Wilson_v1_red.pdf):
  återvinning ~min; droppar → synliga på ~100 ms, återcirkulering minuter).
  Det betyder att en kammare hinner bli användbar **mellan** stötar, inte **under** dem.

#### Vad CanSaten faktiskt utsätts för (mätbara siffror)

| Fas | Acceleration / vibration | Påverkan |
|---|---|---|
| Raketmotorn, ~2–4 s | upp till **20 G** axialt + bredbandsvibration | Skiktet förstörs omedelbart |
| Fyrsteg (coast) efter motorstopp | ~0 g (tyngdlöshet) | Skikt KAN återbildas i mikrograv, men droppar faller inte |
| Utkast/kapsel, apogeum | stötar vid utstötning | Kort störning |
| Fallskärmsöppning | kraftig ryck (~2× terminalkraft; kort stöt) | Störning |
| **Nedfärd, 90–125 s** | **8–11 m/s**, gungning/spinn i fallskärm, vind | **Kontinuerlig störare** — största hotet |
| Landning | hård stöt | efter avslutad mätning |

Källa för acceleration/vibration: CanSat-krav 20 G + vibrationsprov 0–233 Hz,
~20–29 G ([CanSat-guide §3.3](https://cansatcompetition.com/docs/CanSat_Mission_Guide_2026e.pdf),
[kanadensiska kraven](http://csdcms.ca/Docs/CSDC_CanSat_Requirements_2024-25.pdf)),
nedfärdsprofilen 8–11 m/s i [ESA parachute-guide](https://cansat.esa.int/wp-content/uploads/2023/09/T10_Parachute_Design_EN.pdf).

### 8.1.1 Vad det betyder i praktiken — och hur man maximerar chansen

**Realistisk slutsats:** i en skakande, gungande burk blir kammaren med stor
sannolikhet *inte* kontinuerligt känslig under nedfärden. Men det finns fyra konkreta
motåtgärder som kan rädda några spår:

1. **Vibrationsisolera kammaren från burken.** Häng kammarmodulen i flexibla
   montage/stötdämpare (silikon-/kork-/gummistudsar, eller en enkel "fjädrad plattform")
   så att hög vibration dämpas. I en liten burk är detta lätta montage kraftfulla: de
   låter kammaren "glida" relativt burken. *Viktigt:* isolera också från akustisk kanal
   — luftljud kan agera direkt på droppbildningen.
2. **Prova expansions-liknande fångstmoment i stället för kontinuerlig drift.**
   Inspireras av B-29-modellen: var bara känslig i korta fönster. T.ex. slå på
   trigger+strobe och ta bilder i 100–300 ms längre "lugna" luckor som detekteras med
   accelerometern (varje gång vibrationen < tröskel). RGB-strobe-idén (§6.4) kan fånga
   spår som *passerar* i en lugn lucka — kammarens "känsliga tid" kan vara kort men
   ändå räcka för ett enstaka linjeformat spår.
3. **Gör kammaren grund och bred** (lägre profil) → kortare diffusionsväg → skiktet
   återbildas snabbare och är mindre känsligt för vertikala blandningar.
4. **Registrera vibration/accelerometer parallellt** så att data kan
   korreleras/tidstämplas: om ett spår bildas i en lugn lucka ska man *veta* att det
   var lugnt då. Det förvandlar "inga spår" från opublicerbar till *mätbar*: man kan
   visa korrelationen (spår ↔ <låg acceleration).

**Ändå: bash-högra sanningen kvarstår.** CADMUS i ett lugnt ballongfäste lyckades
inte med bilder; en gungande fallskärm i 8–11 m/s är väsentligt tuffare. Därför är
**målbilden fortfarande teknikdemonstration + temperatur/vibrations-loggnings + video**,
med spår som bonus — vilket redan är en världspremiär för CanSat. Alla åtgärder i
§6.4 och här ökar bara sannolikheten för bonusen, de garanterar den inte.

## 9. Sammanfattning / beslutspunkter

1. **Kylkälla: passiv förfryst PCM-platta (frys-metoden)** — enda realistiska
   alternativet i 300–350 g och 500 €. Peltier = marktest/hybrid. Torris = bara med
   lov och god logistik.
2. **Alkohol: etanol 95 %+ i första hand** (fungerar med -21 °C platta), IPA om
   Peltier/tillstånd tillåter. **Specialtillstånd måste sökas skriftligt oavsett** —
   gör det nu (anmälan till tävlingen öppnar 10.9.2026).
3. **Tidslinje från frys till start är den kritiska okända** — fråga arrangören.
4. **Sätt rätt målbild**: teknikdemonstration + temperatursensorik + video;
   synliga partikelspår är bonus. Marktest först!
5. Läs också ESAs [Cloud chamber – radioactivity in a cosmic setting](https://education.esa.int/cloud-chamber-radioactivity-in-a-cosmic-setting-teach-with-space-p03/)
   (färdigt lektionsupplägg som grund för dokumentationen).

## 10. Källförteckning

- [CanSat Finland krav (esero.fi)](https://www.esero.fi/cansat-kilpailun-vaatimukset)
- [CanSat-tävlingen 2027 (esero.fi)](https://www.esero.fi/cansat-kilpailu)
- [ESA – What is a CanSat?](https://education.esa.int/what_is_a_cansat/)
- [ESA – Choose your mission](https://education.esa.int/choose_your_mission/)
- [Barrett 2024, "Cloud chamber using Peltier cooling" (Phys. Educ.)](https://iopscience.iop.org/article/10.1088/1361-6552/ad506c)
- [UPV/EHU, "Detection of particles with a cloud chamber"](http://hdl.handle.net/10810/17990)
- [Bellevue College, "How to Build a Cloud Chamber"](https://www.bellevuecollege.edu/physics/resources/cloudchmbr/)
- [UW-Madison Med. Physics, "DIY Cloud Chamber" (saltvatten-metoden)](https://medphysics.wisc.edu/wp-content/uploads/2021/04/Cloud-Chamber-Lesson-Plan.pdf)
- [Arbor Scientific Cloud Chamber (förfryst platta)](https://www.arborsci.com/products/cloud-chamber)
- [Elektor, "Peltier Cloud Chamber"](https://www.elektormagazine.com/labs/peltier-cloud-chamber)
- [William Ivy, "Thermoelectric Cloud Chamber"](https://www.williamivy.com/posts/cloud-chamber)
- [MIT SB-thesis, "Cloud chamber cooled by thermoelectric modules"](http://hdl.handle.net/1721.1/119952)
- [CADMUS-experimentet på BEXUS 24 (ballong, 2017)](https://doi.org/10.29311/2020.07)
- [AC2O, cloud chamber till stratosfären](https://ac2oubco.wixsite.com/ac2o/our-experiment)
- [Siena College, "Scaling up a Peltier-powered cloud chamber" (APS 2020)](https://meetings-archive.aps.org/apr/2020/d21/50/)
- [Leuven ASTG, "Hawfinch" (GM-rör-detektor för CubeSat)](https://astg.at/documents/20220816_Jakob_Faltisek_Hawfinch_abstract.pdf)
- [REXUS-25 PR3, scintillator-kosmiskt-detect (ICRC 2019)](https://doi.org/10.22323/1.358.0124)
- [Myonflöde vs höjd (IJMPA 2018)](https://doi.org/10.1142/s0217751x18501750)
- [Muon count rate vs altitude (OSTI 1631248)](https://www.osti.gov/servlets/purl/1631248)
- [TTL OVA: Isopropanoli (säkerhet)](https://ova.ttl.fi/isopropanoli)
- [Tukes – Kemikaalien vähittäismyynti (metyloitu sprit etc.)](https://tukes.fi/kemikaalit/kemikaalien-vahittaismyynti)
- [RIGID 12V Mini Compressor (QX-serien)](https://www.rigidhvac.com/12v-mini-compressor)
- [ESA Teach with space: Cloud chamber lesson](https://education.esa.int/cloud-chamber-radioactivity-in-a-cosmic-setting-teach-with-space-p03/)
- [Zeze et al. 2012, "A sensitive cloud chamber without radioactive sources" (arXiv)](https://ar5iv.labs.arxiv.org/html/1202.2423)
- [Hayakawa et al. 2012, "Petri dish-type cloud chamber" (RADIOISOTOPES)](https://doi.org/10.3769/radioisotopes.61.297)
- [Cloudylabs, "Little Air Cooled Cloud Chamber" (Peltier)](http://www.cloudylabs.fr/wp/wp-content/uploads/2019/06/LittleAircooledCloudChamberv2.pdf)
- [TEL-Atomic DCC600, kompakt diffusionskammare](https://www.telatomic.com/all-produts/tel-dcc-600-diffusion-cloud-chamber)
- [Bevan 1954, "Optimum and limiting operating conditions for downward diffusion cloud chambers"](http://hep.ucsb.edu/people/hnn/cloud/articles/ARBevanJSI31_45_1954.pdf)
- [Lyapidevskii 1958, "Diffusion cloud chambers" (Uspekhi)](https://doi.org/10.3367/ufnr.0066.195809f.0111)
- [Wayne State REU 1998, "A Continuously Sensitive Cloud Chamber"](https://www.classe.cornell.edu/public/reu/1998reports/pruitt-simpson.pdf)
- [Cambridge HEP outreach, "Cloud Chamber" (designtips)](https://www.hep.phy.cam.ac.uk/outreach/cloud)
- [CERN S'Cool LAB, "Cloud Chamber DIY manual"](https://scoollab.web.cern.ch/sites/default/files/documents/20200521_JW_DIYManual_CloudChamber_v7.pdf)
- [QuarkNet/Fermilab, "How to Build a Cosmic-Ray Cloud Chamber"](https://quarknet.fnal.gov/resources/QN_CloudChamberV1_4.pdf)
- [Stamatiou et al. 2021, "Experimental Characterization of PCMs for Refrigeration" (MDPI Energies — NaCl 23,3 %: -21,2 °C, ~257 kJ/kg)](https://www.mdpi.com/1996-1074/14/11/3033)
- [Radebe & Huan 2023, "Low-cost eutectic salts for cold storage" (J. Energy Storage — NaCl ~-21 °C, ~228 kJ/kg)](https://www.sciencedirect.com/science/article/pii/S2352152X23003572)
- [Rubitherm SP-seriens PCM (saltvatten, -21…-50 °C)](https://www.rubitherm.eu/en/productcategory/anorganische-pcm-sp)
- [CanSat Mission Guide 2026 (internationella regler: värmetest m.m.)](https://cansatcompetition.com/docs/CanSat_Mission_Guide_2026e.pdf)
- [Barrett & Germain 1947, "Growth of Drops Formed in a Wilson Cloud Chamber" (dropptillväxt r²∝t)](https://pubs.aip.org/aip/rsi/article/18/2/84/296528/Growth-of-Drops-Formed-in-a-Wilson-Cloud-Chamber)
- [Blackett 1934, "On the technique of the counter controlled cloud chamber" (fallhastighet ~1 cm/s, koincidensutlösning)](https://royalsocietypublishing.org/rspa/article-pdf/146/857/281/28637/rspa.1934.0154.pdf)
- [Leone 2011, "Particles that take photographs of themselves" (AJP — triggad kammare, historia)](https://pubs.aip.org/aapt/ajp/article/79/5/454/1057670/Particles-that-take-photographs-of-themselves-The)
- [UVic, "Cloud Chamber Equations" (Bethe-Bloch, Stokes, tillväxtekvation)](https://particle.phys.uvic.ca/~jalbert/chamber.pdf)
- [Wilson et al. 2014, "Performance evaluation of an overdriven LED for high-speed schlieren imaging" (LED-överdrivning 10–200 A)](https://doi.org/10.1007/s12650-014-0220-7)
- [Frozentime Images/Uppsala, "High-speed LED flashgun" (RGB-filtrerade µs-LED-blixtar på 10 µm-droppar)](http://frozentime.se/ljus/high_speed_leds.html)
- [LE-TEHNIKA SRI421, integrerad Stirling-mikrokryokylare 0,25 W (12 V, <200 g)](https://cryocoolers.eu/integral-miniature-stirling-cryogenic-cooler-025w/)
- [Arctic-Tek Stirling-kylare / MiniCool priser](https://www.arctic-tek.com/store/categories/Stirling%20Cryocooler)
- [Agar Scientific, "Portable Dry Ice Maker" (torris via Joule–Thomson)](https://mcprod.agarscientific.com/portable-dry-ice-maker)
- [Bel-Art Frigimat, "Dry Ice Maker" (454 g-block på 1–2 min)](https://belart.com/products/cold-cryo/dry-ice-makers/frigimat-dry-ice-maker/)
- [Subudhi & Sen 2015, "Review of Ranque–Hilsch vortex tube experiments using air"](https://www.sciencedirect.com/science/article/abs/pii/S1364032115007509)
- [Oberlin, "Hilsch-Ranque Vortex Tube" (demonstration)](https://www2.oberlin.edu/physics/catalog/demonstrations/thermo/vortextube.html)
- [UT Austin, "Cloud Chamber" (LN₂-demo)](https://lecturedemos.ph.utexas.edu/demo/311)
- [Vanderbilt, "Demonstration Cloud Chamber" (LN₂ + etanol)](https://www.vanderbilt.edu/physicsdemonstration/davesdemos/demonstrations/demo106.htm)
- [PCM Products, "PlusICE Eutectic Catalogue" (PCM:er -100…+89 °C)](https://www.pcmproducts.net/files/eutectic_catalogue-2011-1.pdf)
- [Mousazade & Rafee 2020, "Cold panels with PCM in a refrigerated truck" (E-26/E-29/E-32)](https://www.sciencedirect.com/science/article/abs/pii/S0140700720303753)
- [Cowan 1949, "A Large Cloud Chamber Using Rear Illumination" (flugit i B-29 på 13,5 km)](https://www.pp.rhul.ac.uk/~cowan/EWC/RevSciInstrum_20_492.pdf)
- [Adams (Caltech), "Cloud Chamber Studies in Cosmic Rays at an Altitude of 30,000 Feet"](https://doi.org/10.7907/dvvv-ts23)
- [Bertelsmann & Heist 1997, "Thermal diffusion cloud chamber. II. Stability of operation"](https://pubs.aip.org/aip/jcp/article/106/2/624/479112/Two-dimensional-transport-and-wall-effects-in-the)
- [Ferguson & Nuth 1999, "The influence of buoyant convection on the upward thermal diffusion cloud nucleation chamber"](https://pubs.aip.org/aip/jcp/article/111/17/8013/184268/The-influence-of-buoyant-convection-on-the)
- [ESA teach with space, "Parachute design for CanSat" (nedfärdsprofil 8–11 m/s)](https://cansat.esa.int/wp-content/uploads/2023/09/T10_Parachute_Design_EN.pdf)
- [Canadian CanSat Design Challenge 2024-25 Requirements (20 G, launch profile)](http://csdcms.ca/Docs/CSDC_CanSat_Requirements_2024-25.pdf)
