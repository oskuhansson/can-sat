---
tags: [cansat, qa, tävling]
status: referens
updated: 2026-11-07
---

# QA — kunskapsquiz, kvalitetssäkring och kritik

*Förberedelse inför tävlingen: testa lagets kunskap, verifiera fakta och öva på tuffa bedömarfrågor.*

---

## Del 1 — Kunskapsquiz och kvalitetssäkring


*Två delar. **Del A** är en kunskapsquiz (frågor & svar) så laget kan testa att de
förstått översikterna [CANSAT-GRUND.md](CANSAT-GRUND.md), denna fil
och denna fil. **Del B** är en kvalitetsverifiering
(faktakontroll av de viktigaste siffrorna/reglerna inför tävlingen).*

---

# Del A — Kunskapsquiz (frågor & svar)

*Svara först utan att kika på svaren. Facit står i slutet av varje fråga.*

### A.1 CanSat i allmänhet

**1. Vad står CanSat för och varför kallas den "satellit" när den inte är i omloppsbana?**
> *Svar:* CanSat = "Can" + "Sat" (burk + satellit). Den byggs som en riktig minisatellit
> med elektronik, sensorer, batteri och radio, men faller rakt ner från ~1 km höjd —
> den går aldrig i omloppsbana.

**2. Hur högt går burken och hur snabbt faller den?**
> *Svar:* Apogeum ~750–1100 m (750 m 2026). Nedfart **5–12 m/s** (rekommenderat
> 8–11 m/s). Hela mätuppdraget blir bara ~70–120 s.

**3. Varför är mättiden så kort — och vad betyder det för designen?**
> *Svar:* För att burken faller snabbt från relativt låg höjd. Designen måste sampla ofta,
> logga data lokalt och säkra nedlänken, eftersom man bara har ~1–2 minuter.

**4. Hur mycket får burken väga och hur mycket får man lägga ut?**
> *Svar:* Massa **300–350 g** inkl. batteri. Budget **≤ 500 €**.

**5. Vilken acceleration måste allt tåla?**
> *Svar:* Kravet är 20 G, men verklig uppmätt acceleration i Vasa har nått ~30 G → bygg
> för 30 G.

### A.2 Regler

**6. Vad är "4,5 cm-locket" och varför spelar det roll för antennerna?**
> *Svar:* Det axiala utrymmet i raketen ovanför burken är bara **4,5 cm** (fallskärm +
> fäste + antenner). Därför kan man inte ha en stor antenn som sticker ut — antennerna
> måste rymmas i det locket (eller vara utanpå burken).

**7. Vilka ämnen är absolut förbjudna i en CanSat?**
> *Svar:* Sprängämnen, tändare/pyroteknik, brandfarliga material, farliga ämnen och
> biologiska nyttolaster. Brandfarliga ämnen (t.ex. alkohol) är bara tillåtna med
> **skriftligt specialtillstånd**.

**8. Hur viktas poängen? (vilken post väger mest?)**
> *Svar:* Teknik 35 %, vetenskapligt värde 30 %, professionella kompetenser 25 %,
> outreach 10 %. Teknik väger alltså mest.

**9. Vilka är de tre obligatoriska dokument/milstolparna efter urvalet?**
> *Svar:* Projektrepresentation + videopitch (11.12.2026), urval meddelat (21.12.2026),
> och **Pre-Launch Report (max 15 sidor, engelska) 20.2.2027**.

**10. Vad måste man göra innan 30.10.2026 och varför är det kritiskt nu?**
> *Svar:* Förregistreringen. Deadlinen är redan passerad (t.o.m. 3.11.2026) — man måste
> verifiera med ESERO Finland att laget hann med, annars är sista möjlighet
> projektrepresentationen 11.12.2026.

### A.3 Moduler och bygge

**11. Vilken mission är obligatorisk i en CanSat?**
> *Svar:* Primärmissionen: mäta **temperatur och lufttryck** → beräkna höjd med
> barometrisk formel.

**12. Nämn tre saker en CanSat-grundmodell måste innehålla (utöver sensorerna).**
> *Svar:* Huvudprocessor (t.ex. ESP32), batteri + lättåtkomlig strömbrytare, radio/nedlänk,
> mekanik/strutktur med fallskärm, och återfinnbarhet (GPS/blipp).

**13. Varför måste batteri- och huvudströmbrytaren vara lättåtkomlig?**
> *Svar:* Säkerhetskrav — man ska snabbt kunna stänga av systemet (t.ex. före/nach
> hantering, landning).

### A.4 Radio och mark-RX

**14. Vad är skillnaden mellan upplänk och nedlänk?**
> *Svar:* **Nedlänk** = burken → marken. **Upplänk** = marken → burken.

**15. Vad betyder dB, dBm, dBi och dBd?**
> *Svar:* dB = logaritmiskt mått på förhållande (10 dB = 10×). dBm = effekt i dB relativt
> 1 mW (+20 dBm = 100 mW). dBi/dBd = antennförstärkning mot isotrop antenn / dipol.
> **dBd = dBi − 2,15.**

**16. Vad är EIRP/ERP och varför skiljer de sig?**
> *Svar:* Båda är "strålad effekt" = sändareffekt + antennförstärkning − kabel. De skiljer
> sig i referensantenn: EIRP mot isotrop, ERP mot dipol. **ERP ≈ EIRP − 2,15 dB.**

**17. Vilka två radioben använder vi, och vad gör var och en?**
> *Svar:* **ESP-NOW (2,4 GHz, broadcast)** = GPS + telemetri + RSSI + sporadiska bilder
> (högre takt). **LoRa (868 MHz, monopol)** = GPS + nödtelemetri som robust backup över
> hela nedfärden.

**18. Varför är det en fördel att båda benen är "anslutningslösa broadcast"?**
> *Svar:* Burken bara sänder ut — inget handshake/association att koppla upp och tappa.
> Vid en fallande, gungande burk är det mycket tåligare än WiFi-station-läge.

**19. Hur följer markgimbalen burken?**
> *Svar:* (1) **RSSI-peak** — signalen toppar när antennen pekar rätt på burken.
> (2) **GPS** — burken skickar position → marken räknar elev/azimut och pekar.
> Två axlar: azimut + elevation.

**20. Varför kan markantennen göras stor/effektiv utan problem, men inte burkens?**
> *Svar:* För att **RX-förstärkning (mottagningen) på marken är laglig och "gratis"** —
> det kostar ingen sändareffekt och det finns ingen storleks-/viktgräns på marken.
> Burken är bara 115×66 mm och ska klara 30 G, så den behöver en liten enkel antenn.

**21. Vilken typ av markantenn rekommenderar vi som förstaval, och hur mycket gain?**
> *Svar:* **Yagi ~12–15 dBi (på 868 MHz)** — bra förstärkning med en hanterbar stråle
> som är lätt att rikta mot burken.

**22. Ungefär hur stor link-marginal ger 868 MHz-systemet över nedfärden?**
> *Svar:* **~60–75 dB** — mycket robust.

---

# Del B — Kvalitetssäkring / faktakontroll inför tävlingen

*Kontrollera följande mot de officiella källorna (ESERO Finland, Traficom) innan PLR
skickas in. Markera friska/för att åtgärda.*

### B.1 Hårddata att verifiera (head → ESERO Finland)

| # | Punkt | Värde i översikterna | Verifieringsdatum | Status |
|---|---|---|---|---|
| 1 | Volym | Europeisk läskburk 115×66 mm (~330 ml) |  |  |
| 2 | Massa | 300–350 g (inkl. batteri) |  |  |
| 3 | Budget | ≤ 500 € |  |  |
| 4 | Fallskärmsfäste | ≥ 50 N (ESA rek. 200 N) |  |  |
| 5 | 4,5 cm-locket | ≤ 4,5 cm axialt i raketen |  |  |
| 6 | Ström | 2 h (ESA int. 4 h) |  |  |
| 7 | Acceleration | 20 G (verklig ~30 G) |  |  |
| 8 | Nedfartshastighet | 5–12 m/s (rek. 8–11 m/s) |  |  |
| 9 | Apogeum | 750 m (2026) / 900–1100 m (2024–25) |  |  |
| 10 | Poängviktning | Teknik 35 / Vet 30 / Proffskompetenser 25 / Outreach 10 |  |  |

### B.2 Datum att bekräfta

| # | Milstolpe | Datum | Verifierat? |
|---|---|---|---|
| 1 | Förregistrering | 30.10.2026 (❓ redan passerat — bekräfta status!) |  |
| 2 | Projektrepresentation + videopitch | 11.12.2026 |  |
| 3 | Urval meddelat | 21.12.2026 |  |
| 4 | Pre-Launch Report (max 15 sidor, eng.) | 20.2.2027 |  |
| 5 | Tävling | 11–14.3.2027 (Vasa) |  |

### B.3 Regler/radio att dubbelkolla (→ Traficom / ESERO)

- [ ] 868 MHz LoRa: **25 mW e.r.p.**, duty ≤1 % — bekräfta aktuell määräys.
- [ ] 2,4 GHz (ESP-NOW/WLAN): **20 dBm EIRP** — licensfritt, luftanvändning tillåten.
- [ ] Bekräfta att luftanvändning är tillåten för både SRD (868) och WLAN (2,4) inför PLR.
- [ ] CE-märkta moduler — inga förstärkare får kopplas mellan sändare och antenn.
- [ ] Både upplänk och nedlänk är licensfria om utrustningen håller sig inom gränserna.

### B.4 Innehållskontroll av översikterna

- [ ] CANSAT-GRUND.md: siffror och datum stämmer med officiella krav.
- [ ] KOMMUNIKATION.md (del 2): arkitektur (ESP-NOW + LoRa, yagi+gimbal) speglar
      WIFI-FORSKNING.md §5–7.
- [ ] WIFI-FORSKNING.md: §7-dubbelarkitekturen korrekt beskriven.
- [ ] Stavfel/orden i översikterna korrigerade.
- [ ] Länkarna i filerna pekar på rätt dokument.

---

*Uppdateras efter varje verifiering. B1/B2 datum ska kollas mot officiella källor före
Pre-Launch Report 20.2.2027.*

---

## Del 2 — Kritik av systemet: tuffa frågor och hur vi svarar


*Syfte: förbereda laget på den troliga kritiken/bedömarfrågorna kring vårt
kommunikationssystem (monopol i burken + mark-gimbal, ESP-NOW-broadcast + LoRa-backup).
Varje fråga har ett **ärligt svar** och en **svaghet som erkänns**. Uppdatera när
bedömare testar. Baseras på denna fil och
del 1 i denna fil.*

---

### 1. Radio & räckvidd

**"Varför så liten antenn i burken? Kan ni inte skicka starkare/större?"**
> **Svar:** Burkens antenn är en monopol (omni) för att klara rotation + 30 G utan att
> peka själv. All gain läggs på marken (12–15 dBi-yagi + gimbal), där den är laglig och
> "gratis" (RX-gain är oreglerad). Burken håller sig under EIRP-taket, vi får 60–75 dB
> marginal på 868 MHz.
> **Svaghet:** Nedlänken har massor av marginal, men upplänken (mark → burk) är svag
> eftersom burkens antenn är liten — symmetrisk höghastighetsdubbelriktning saknas.

**"Två radiosystem (ESP-NOW + LoRa) — störa de varandra?"**
> **Svar:** De ligger i olika band (2,4 GHz och 868 MHz) och har olika RX-moduler → ingen
> självblockering i praktiken. I firmware kan vi tidstyra sändningarna (LoRa paket + väntan
> uppfyller drifcykeln ≤1 %).
> **Svaghet:** Två system = dubbel plats/energi i burken och dubbla felkällsområden; var
> yta och ström budgeteras.

**"868 MHz har bara ~1 Mbit/s (egentligen ~0,3 kb/s vid SF12) — hur är det 'hög bandbredd'?"**
> **Svar:** Det är det inte — LoRa är vår **robusta backup**, inte det höga bandbreddsbenet.
> Bandbredd och 2,4 GHz höga MCS-nivåer får vi genom ESP-NOW (2,4 GHz) när markgimbalen
> pekar rätt och avståndet krymper.
> **Svaghet:** "Hög bandbredd" gäller bara nära marken och kräver hög SNR; i början av
> nedfärden (långt bort) får vi bara låg takt.

**"ESP-NOW default är bara 1 Mbps — det är väl inte högt?"**
> **Svar:** Rätt, default PHY är 1 Mbps ([Espressif](https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/esp-now.html)).
> Men ESP-NOW stödjer att konfigurera högre WiFi-MCS-hastigheter (upp till WiFi 6-rates) per
> peer via `esp_now_set_peer_rate_config()` — det är den vägen till högre bandbredd när
> SNR räcker.
> **Svaghet:** Högre MCS → känsligare för störningar och avstånd. Man kan inte bara "skruva
> upp" takten; det måste matcha faktisk link-marginal.

### 2. Mekanik & pålitlighet

**"En gimbal som ska följa en fallande burk — hinner den? Vad om burken gungar?"**
> **Svar:** Burkens monopol är omni, så gungning/rotation spelar ingen roll för sändningen.
> Gimbalen behöver bara några grader/s vid 8–11 m/s fall; 1–5 Hz uppdatering + GPS/RSSI
> räcker. Markgimbalen är lätt att bygga/testa på stativ.
> **Svaghet:** Pekprecisionen avgör hur ofta antennen hamnar rätt. Vid kraftig pendling
> faller RSSI varierar; lösningen är GPS-prognos + RSSI-peakkombination.

**"Vad om gimbalmotorn slår/strular i kylan eller blåst i Vasa i mars?"**
> **Svar:** Märkta hobby-servon klarar 0–10 °C normalt; vi testar på kyla och stativ.
> Motorn behöver bara orientera lätt yagi (0,3–1 kg).
> **Svaghet:** Finns aldrig 100%; vi har LoRa-backup + en manuell pekläge för om
> motorgimbalen ger upp.

**"Vad om fallskärmen inte löser eller burken roterar så monopolantennen bryts?"**
> **Svar:** Monopolen är en robust pinne/tråd som tål 30 G och rotation; fallskärmen är
> standard CanSat-utrustning testad på ≥50 N.
> **Svaghet:** All mekanik är en risk; vi hårdkodar/enkapslar antennen och har GPS-blipp för
> återfinnbarhet även om nedlänken dör.

### 3. Regler & juridiskt

**"Är det lagligt att sända från en fallande burk i Finland?"**
> **Svar:** Ja. Traficom anger att 2,4 GHz (100 mW EIRP) och 868 MHz (25 mW e.r.p.) får
> användas licensfritt, och användning i luften är explicit tillåten för WAS-SRD
> ([Traficom UAS](https://traficom.fi/en/radio-licences-and-frequencies/use-radio-frequencies/frequency-use-unmanned-aviation)).
> Både upplänk och nedlänk är inom gränserna; vi använder CE-moduler utan förstärkare.
> **Svaghet:** Måste verifiera exakt att våra moduler/antennsammansättning håller EIRP-taket
> och rapportera i Pre-Launch Report.

**"Varför inte bara amatörradio (OH)? Det ger mer effekt."**
> **Svar:** Amatörradio kräver licens och anropssignal — det är en annan väg vi inte behöver.
> Vår licenfria kollektivfrekvensväg räcker gott (60–75 dB marginal) och är enklare för ett
> skollag.
> **Svaghet:** Om vi ville ha riktigt hög effekt/bandbredd hade amatörbandet gett mer —
> men det är inte vår kravbild.

### 4. Nytta & uppdragsvärde

**"Det här är väl bara 'satellit som nedlänkar' — vad är det vetenskapliga/tekniska?**
> **Svar:** Uppdraget är en **markbaserad antenn-tracker** som följer en fallande sändare —
> vi mäter RSSI över tid, GPS, och attityd, och verifierar link-budget + antennförstärkning i
> realtid. Det är en mätbar "downlink-tracking"-vetenskap som använder teknikpoäng.
> **Svaghet:** Om man vill "webbla live fire från himlen" når vi inte det — det är en specifik
> teknikdemonstration, inte en surfplattform.

**"Många lag kör bara sensorer — varför radio + gimbal?"**
> **Svar:** Det adderar en verklig teknikutmaning (pekning + link) och en imponerande
> show-case (en markstation som följer en fallande burk). Kombinationen skiljer laget åt
> i teknikpoäng + outreach.
> **Svaghet:** Mer komplexitet = fler saker som kan gå fel; vi siktar på robust nedlänk
> först och bygger satellitspårning som en bonusfunktion.

### 5. Kostnader & budget

**"Ryms allt under 500 €?"**
> **Svar:** Ja. Sparsam grundversion ~150–260 €, full version ~250–450 € — båda under taket
> (se ovan).
> **Svaghet:** Frakt/moms kan lägga ~10–25 %, och billiga reservkomponenter är bra att ha
> extra. Vi budgeterar reserv.

---

*Tips: öva att svara lugnt, erkänna svagheterna, och alltid peka på vilken mätning vi
gjort/planerar för att stödja påståendet. Det inger förtroende hos bedömare.*

