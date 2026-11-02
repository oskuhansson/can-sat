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
- Massa: koppar/aluminiumplatta 50 mm Ø × 3 mm ≈ 50 g + PCM-påse ~50–80 g.
- Fryses i vanlig frys (-18…-24 °C) kvällen innan, transporteras i isolerad låda
  (styrox/kylbox) till startplatsen. **Nyckelfråga: hur lång tid från frys till
  start?** Check-in → start kan vara timmar (se §7, fråga arrangören).
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
│  mörk kopparplatta -21 °C  │  ← kylplatta + PCM (förfryst), isolerad undersida
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
| Kylplatta (koppar 50 mm Ø × 3 mm) + PCM (~50 ml saltvattenpåse) | ~100–130 g |
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
