---
tags: [cansat, gimbal, mekanik, cad]
status: aktuell
updated: 2026-11-07
---

# Gimbal — byggplan och CAD för markstationen

*Markgimbalen pekar hög-gain-antennen mot burken. Här finns byggplanen, CAD-specifikationen och den färdiga modellen.*

---

## Del 1 — Byggplan steg för steg


*Konkret, steg-för-steg plan för att bygga markgimbalen som följer burken. Bygger på
gimbalkraven i denna fil §5.3 och
denna fil. CAD-skiss i Onshape ("Gimbal-antenntest").*

---

### 1. Mål och krav

Gimbalen ska hålla en **yagi-antenn (12–15 dBi)** och vinkla den i **två axlar**
(azimut + elevation) för att följa en fallande burk från ~1 km till marken.

| Krav | Värde | Källa |
|---|---|---|
| Antenn | yagi 12–15 dBi, ~0,3–1 kg | WIFI §6 |
| Axlar | 2 (azimut + elevation) | §5.3 |
| Vinkelhastighet | bara några °/s (8–11 m/s fall) | §5.3 |
| Uppdatering | 1–5 Hz styring (GPS/RSSI) | §5.3 |
| Pekfel | ±2–5° räcker (12–15 dBi HPBW ~30–65°) | §5.3 |
| Miljö | utomhus mars, 0–10 °C, ev. blåst | CANSAT-GUIDEN |
| Effekt | lågspänning (t.ex. 5 V / 12 V) | — |

**Designprincip:** allt tungt/svårt på marken. Burkens sändare är bara en monopol; alla
pek-rörelser görs här.

---

### 2. Arkitektur (översikt)

```
 PC (styrlogik: GPS→az/el + RSSI-peak)
      │
      ▼
 Styrenhet (ESP32/Uno) ──►  azimut-motor (y-axel) ──►  elevation-motor (x-axel) ──►  yagi-antenn
      │
      ▼
 Strömförsörjning (statv/PSU)
```

Delarna i ordning uppifrån:
1. **Antenfäste** — håller yagin (klämma + kort rör).
2. **Elevation-led** — lutar antennen (motor på höjarbom).
3. **Azimut-led** — roterar hela överdelen horisontellt (motor på höjarbom).
4. **Höjarstatv** — bär motorerna + antennen, står på marken.

---

### 3. Komponentlista (med ungefärlig kostnad — se ovan)

| # | Komponent | Val / spec | Prisklass |
|---|---|---|---|
| 1 | Yagi-antenn | 12–15 dBi, 868 MHz | 15–50 € |
| 2 | Azimut-motor | stegmotor + drivare eller hobby-servo (360°) | 10–25 € |
| 3 | Elevation-motor | stegmotor/servo (liten last, -90…+90°) | 10–25 € |
| 4 | Motorhållare | 3D-printad eller metall | 0–15 € (om 3D-print) |
| 5 | Styrenhet | ESP32 (har vi) eller Arduino Uno | 5–10 € |
| 6 | Motor-drivkort | t.ex. A4988 / L298N (steg) eller direkt-servo | 5–15 € |
| 7 | Strömförsörjning | 12 V PSU (steg) eller 5 V batteri (servo) | 10–25 € |
| 8 | Stativ | kamerastativ/självbyggd | 10–40 € |
| 9 | Kablage + kontakter | ström + signal | 5–20 € |
| **Summa** | | | **~50–190 €** |

> 💡 **Första prototyp:** använd 1–2 hobby-servon (SG90/MG996) som test av styr- och
> spårlogik innan steg, eftersom servo är enklare (ingen drivare, PI-styrning inbyggd).
> Uppgradera till stegmotor om man vill känna bättre precision/vridmoment och
> positionsåterkoppling specifikt för yagin.

---

### 4. Steg-för-steg uppbyggnad

#### Steg 0 — Verktyg/material
- Lödstation, tråd, skruvmejsel, insex, nylon-/metallskruv, varmlim (snabb fästning).
- 3D-printade delar (filament) eller köpta aluminiumprofiler — beroende på åtkomst.

#### Steg 1 — Basskiss i CAD (Onshape)
- [x] **Klar!** Se denna fil för fullständig dokumentation av 3D CAD-modellen i Onshape ("Gimbal-antenntest").
- Modellerad med 36 delar: **höjarstativ & basplatta → azimut-led (360°) → elevation-gaffel & motor (-10°…+90°) → antennvagga & motvikt → 7-elements Yagi-antenn (868 MHz)**.
- Fullt parametriserad med `azimuthAngle` och `elevationAngle` för dynamisk pekning i Part Studio 1.

#### Steg 2 — Stativ + höjarbom
1. Montera vertikalstång/pelare på stativet (klämma).
2. Fäst **azimut-motorn** högt upp så hela överdelen roterar runt vertikalen.
3. Montera **elevation-motorn** på en liten bom/vinkel fäst på azimut-axeln.

#### Steg 3 — Elevation-led + antennfäste
1. Fäst elevation-motorn på höjarbommen (solid – klarar yagins ~0,3–1 kg).
2. Montera **antenfäste** (klämma) på elevation-axeln.
3. Säkra yagin i fästet — stramt men förlåtande vid ev. stöt.

#### Steg 4 — Elektronik
1. Koppla motor(ar) till drivkort/direkt till styrenheten.
2. Koppla styrenheten till PC (USB/serial).
3. Strömförsörjning: 12 V→drivkort (steg) eller 5 V-signal (servo). Jord kopplas gemensamt.

#### Steg 5 — Styrprogram (mjukvara)
1. **Manuellt läge först:** knappar/kommandon för att svänga az/el — verifiera att
   motorerna rör sig åt rätt håll och till rätt vinklar.
2. **GPS-spår:** ta in burkens GPS → räkna az/el i PC → skicka vinkel till gimbal.
3. **RSSI-peak (bonus):** om nedlänken ger RSSI, svep/peak-parkera runt di sitt mål för
   att finjustera pekningen.
4. **Stöd 1–5 Hz:** uppdatera vinkel vid den takt som burken faller.

#### Steg 6 — Test på marken (kritisk!)
1. **Stativtest:** svep az/el manuellt, kolla verklig vinkel vs kommando.
2. **Blindtest med sändare:** sätt en separat burk-sändare på ~100–500 m, kör
   RSSI-spåning och se att antennen landar på rätt pek.
3. **Kyla/ute:** testa i ute-temp + lite vind; se att servon/steg inte tappar position.
4. **Stress:** kör kontinuerligt ~1 timme för att hitta överhettning/slitage.

#### Steg 7 — Verifiering & dokumentation
- Logga az/el + RSSI + GPS under tester → bygg en liten rapport med grafer.
- Spara "proof": att gimbalen höll antennen på målet under hela simulerad nedfärd.

---

### 5. Riskanalys & fallback

| Risk | Sannolikhet | Åtgärd / fallback |
|---|---|---|
| Motor position tappas (steg) | låg-medel | servon med positionsfeedback, eller steg + hem-switch vid start |
| Servo för svag för yagi | låg | uppgradera till stegmotor/MG996 (högre vridmoment) |
| GPS-fel gör att pekningen svajar | medel | kombinera med RSSI-peak; mjuk medel/typ |
| Kyla gör servo långsamt/ställt | låg | testa i kyla; värmetåligt servo eller lägre hast. krav |
| Vind/kraftig blåst stör pekningen | medel | kraftigt stativ + moderat hast; RSSI-peak-baserad stabilisering |

**Fallback om gimbalen misslyckas:** yagin kan riktas manuellt/hållas på en kanal; LoRa-
backupen (via omnigiv) ger ändå telemetri/GPS via en separat låg-gain-ruta (§7).

---

### 6. Lämpliga steg att göra härnäst (checklista)

- [x] CAD-skiss på gimbal (i Onshape — "Gimbal-antenntest") med 2 roterande leder (se denna fil)
- [ ] Välj servo vs steg (börja servo för styrlogik-test)
- [ ] Bygg stativ + höjarbom
- [ ] Bygg elevation + antennfäste
- [ ] Koppla elektronik + manuell styrning
- [ ] Implementera GPS→az/el konvertering i PC
- [ ] RSSI-peak spårning (bonus)
- [ ] Marktest med separat sändare + kyla/ute-test
- [ ] Skriv resultatrapport + förbered för PLR (20.2.2027)

---

*Se även: denna fil §5.3 (gimbalkrav),
ovan (budget), del 1 i denna fil (hur vi
svarar på kritik om gimbalen).*

---

## Del 2 — CAD-plan v2 (detaljspecifikation)


*Konkret, detaljerad plan för att bygga om gimbalen i Onshape med **NEMA 17-stegmotorer, TMC2209-drivare och GT2-drivremmar (inga kugghjul)**. Ersätter den förenklade modellen i denna fil (v1). Bygger på kraven i denna fil och denna fil §5.3.*

> **Status:** plan, ännu inte modellerad. Alla mått är *startvärden* som ska bli parametrar i Onshape. Allt som markeras ⚠️ ska kontrolleras mot datablad/leverantör innan beställning eller utskrift.

---

### 0. Beslut som är fattade

| Område | Beslut |
|---|---|
| Antenn | 868 MHz Yagi, 7 element, 600 mm bom (2020-profil), ca 0,5–0,65 kg |
| Motorer | 2 × NEMA 17 **17HS19-2004S1** (42×42×48 mm, 0,59 N·m, 2 A/fas) |
| Drivare | 2 × **TMC2209** (BIGTREETECH V1.3-modul), UART-läge, StealthChop, 16 mikrosteg med 256-interpolation |
| Transmission | **GT2, 2 mm delning, 6 mm bred sluten rem. Utväxling 5:1 på båda axlarna.** Inga kugghjul |
| Tillverkning | 3D-print (PETG, ASA vid utomhusbruk) + aluminiumprofil **2020 V-slot** + standardlager |
| Azimutlager | 2 × **6808-2RS** (40×52×7 mm), dubbla lager med 40 mm mellanrum, dödaxel av Ø40×3 aluminiumrör |
| Hemning | Hall-sensor (A3144) + magnet på respektive remskiva. Azimut ±200° med kabelslinga genom ihåligt rör |
| Effekt | 12 V DC |

#### Det som ändras jämfört med v1

| v1 (befintlig modell) | v2 (denna plan) |
|---|---|
| Direktdrivna motorer, ingen utväxling | GT2-rem 5:1 på båda axlar |
| Bom 16×16×565 *och* 18×18×600 i samma dokument | Bom = 2020-profil, **600 mm**, enda sanningskälla |
| Torn 18×44×90 mm i tabellen, 18×50×110 mm i översikten | Ett enda tornmått (se §3.4) |
| Vertikal Ø40-mast med lagerhus | Ø40×3-rör som dödaxel + 2 lager i roterande trumma |
| 36 delar utan inköpsdelar | ca 60 delar inkl. inköpta komponenter, med artikelnummer |
| Counterweight-låda bakom axeln | Axeln placeras vid antennens tyngdpunkt, vagnen kan skjutas ±60 mm för trimning |

---

### 1. Verifierade komponentdata (hämtade 2026-11-04)

| Komponent | Verifierade data | Källa |
|---|---|---|
| NEMA 17 17HS19-2004S1 | 0,59 N·m hållmoment, 2,0 A/fas, 1,4 Ω, 3,0 mH, 1,8°/steg, 42×48 mm, 0,40 kg, rotortröghet 82 g·cm². Omgivningstemp −10…+50 °C | [StepperOnline-datablad](https://omc-stepperonline.com/download/17HS19-2004S1.pdf) |
| TMC2209 (BTT-modul) | 4,75–28 V, 2 A RMS / 2,8 A topp, 256 mikrosteg (interpolering), StealthChop2, StallGuard4, STEP/DIR eller UART. Vref-formel: I_RMS = V_REF/√2 | [BIGTREETECH-dokumentation](https://neo.bttwiki.com/en/docs/accessories-docs/tmc-driver/tmc-2209/), [EZ2209](https://github.com/bigtreetech/docs/blob/master/docs/EZ2209.md) |
| Lager 6808 / 6810 | 6808: 40×52×7 mm, 6810: 50×65×7 mm | [Bearing Sizes](https://www.bearingworks.com/bearing_sizes/) |
| GT2-rem | 224-2GT-6: 112 tänder, 224 mm, 6 mm bred, 2 mm delning (finns i lager hos flera leverantörer) | [3DWare](https://www.3dware.ch/en/accessories/belt/3dware-ch-handelsware-01900920-224-gt2-belt-6mm-wide-224mm-long), [Technobots](https://www.technobotsonline.com/6mm-wide-gt2-2gt-2mm-pitch-rounded-tooth-profile-224mm-closed-belt.html) |

⚠️ Remlängden 280-2GT-6 (azimut), lagren 6001-2RS och A3144 är standarddelar men jag har inte verifierat lagerstatus. Alternativ med 300-2GT-6 finns i §4.2.

---

### 2. Systemarkitektur och koordinater

**Koordinatsystem:** Z upp, X framåt vid azimut 0°, origo i azimutaxelns centrum vid markplanet (underkant ram). Azimut positiv = moturs sett uppifrån. Elevation 0° = horisontell bom, +90° = rakt upp.

```
 Antenn (Yagi, 2020-bom)
   │  klämmas i vagga (CRADLE) på elevationsaxeln
   ▼
 Elevationsaxel Ø12 (levande axel, 2 × 6001-2RS i tornen)
   │  80T-remskiva ◄── GT2 224-2GT-6 ◄── 16T på EL-motor (fäst på vänster torn)
   ▼
 Yoke: bottenplatta + 2 torn (PETG), förskjutet 160 mm framför azimutaxeln
   │  bultas i trumman
   ▼
 Azimutrumma (AZ-DRUM) med 2 × 6808, roterar på stillastående rör Ø40×3
   │  100T-remskiva ◄── GT2 280-2GT-6 ◄── 20T på AZ-motor (står på basplattan)
   ▼
 Basram av 2020-profil 280×200 mm + basplatta (PETG) + styrbox
```

**Varför axeln är förskjuten 160 mm framför azimutaxeln:** när antennen pekar rakt upp hänger bomens bakre del (ca 250 mm) ner. Med axeln framför ramen svänger den fritt utanför basen. Se kollisionskontrollen i §9.

---

### 3. Delförteckning med mått (parametrar)

#### 3.0 Globala parametrar (Variable Studio `VS_Gimbal`)

| Variabel | Värde | Anmärkning |
|---|---|---|
| `#z_axle` | 300 mm | Höjd för elevationsaxeln över rambotten |
| `#x_axle` | 160 mm | Elevationsaxelns avstånd från azimutaxeln |
| `#boom_len` | 600 mm | |
| `#boom_s` | 20 mm | 2020-profil |
| `#az_teeth_motor` / `#az_teeth_out` | 20 / 100 | Utväxling 5:1 |
| `#el_teeth_motor` / `#el_teeth_out` | 16 / 80 | Utväxling 5:1 |
| `#belt_pitch` | 2 mm | GT2 |
| `#pulley_offset` | 0,254 mm | GT2 pitch-line differential |
| `#tooth_depth` | 0,764 mm | Tandens djup (⚠️ kontrollera mot vald profilgenerator) |
| `#bearing_az` | 40 / 52 / 7 | 6808-2RS |
| `#bearing_el` | 12 / 28 / 8 | 6001-2RS |
| `#clr_press` | +0,15 mm | Utskriftstolerans för presspassning (kalibreras med testring, §8) |
| `#clr_slide` | +0,30 mm | Glidpassning |
| `#az_limit` | ±200° | Mjukvarugräns, mekaniskt stopp vid ±210° |
| `#el_min` / `#el_max` | −10° / +90° | Mekaniskt stopp vid −15° / +95° |

#### 3.1 Serie 100 — Bas (`PS_Base`)

| ID | Del | Mått | Material / typ |
|---|---|---|---|
| 101 | `RAIL_X` ×2 | 2020 V-slot, L = 280, vid Y = ±90, Z 0–20 | Al, köpt |
| 102 | `RAIL_Y` ×2 | 2020 V-slot, L = 160, vid X = ±130, mellan rälsarna | Al, köpt |
| 103 | Hörnvinklar ×4 + T-muttrar M5 | Inre 2020-hörnvinkel | Köpt |
| 104 | `BASE_PLATE` | 200 (Y) × 140 (X) × 8 mm, Z 20–28. Centralhål Ø36 (kabel). 4 hål M5 för T-mutter i räls vid (±50, ±90). 4 inserts M4 på PCD 74 för pelarflänsen | PETG, 4 perimetrar, 40 % gyroid |
| 105 | `PILLAR_FLANGE` | Ø90 × 10 mm, Z 28–38. Centrumhål Ø40,2 + Ø34 genomgående. 4 × M4 | PETG |
| 106 | Gummifötter ×4 | Ø25 × 8 mm, M5 | Köpt, ej modellerade |
| 107 | `CTRL_SHELF` | Hylla 4 mm för styrboxen mellan ändbalk och basplatta | PETG |

Ramen: ytterkant 280 × 200 mm, inre fritt mått mellan långrälsarna 160 mm. Vikt ca 0,4 kg ram + 0,2 kg plattan.

#### 3.2 Serie 200 — Azimut (`PS_Az`)

| ID | Del | Mått och funktion |
|---|---|---|
| 201 | `PILLAR_TUBE` | Rör Ø40 × 3, **L = 135**, Z 28–163. Aluminium EN AW-6060/6063, dragen. ⚠️ Mät yttre diameter. Lagersätet kräver Ø40,0 ±0,1 |
| 202 | `AZ_COLLAR` | Printat stöd under nedre lagrets innerring: Ø46 × 4 mm, Z 93–97. Vilar på en M4×50-tvärbult genom röret (hål Ø4,1 vid Z 90) |
| 203 | `AZ_DRUM` | Ø64 × 54 mm, Z 97–151. Säten Ø52,15 × 7 djup i båda ändar, mittbor Ø46. Sex hål M4 på PCD 56 i vardera änden |
| 204 | `AZ_BEARING` ×2 | 6808-2RS. Nedre vid Z 97–104, övre vid Z 144–151 |
| 205 | `AZ_LID` | Ø64 × 4 mm, Z 151–155, bor Ø48, 6 × M4 |
| 206 | `AZ_PULLEY_100T` | **Utskriven GT2-remskiva, 100 tänder** (se §4.3), Z 83–97, bultas i trummans undersida med 6 × M4 |
| 207 | `AZ_MOTOR_PULLEY_20T` | Köpt aluminiumremskiva 20T GT2 6 mm, bor 5 mm. Remmens centrum vid Z = 88 |
| 208 | `AZ_MOTOR` | 17HS19-2004S1, **står på basplattan med axel uppåt**, Z 28–76, axel upp till Z 100 |
| 209 | `AZ_MOTOR_BRACKET` | Bord 4 mm, Z 76–80, med Ø22-pilothål och M3 på 31 mm, två stödväggar 5 mm. **Slitsar ±4 mm** radiellt för remspänning. Motorcentrum vid Y = +75,7 |
| 210 | `AZ_HALL_MOUNT` | Hållare för Hall-sensor på basplattan, vid remskivans kant |
| 211 | `AZ_STOP` | Stoppklack (print) på remskivan och motstopp i basen vid ±210° |

Axiell lastväg: trumman hänger på nedre lagret via remskivans bultplatta, innerringen vilar på `AZ_COLLAR`. Övre lagret flyter (spel ca 0,2 mm).

#### 3.3 Serie 300 — Yoke (`PS_Yoke`)

| ID | Del | Mått |
|---|---|---|
| 301 | `YOKE_BASE` | Platta 12 mm, Z 155–167. Cirkel Ø100 vid origo + arm i +X till X = 175, bredd 110. Kabelurtag Ø48 centralt. Revben 3 mm. Måste få plats på byggplattan: 215 × 110 mm |
| 302 | `TOWER_L`, `TOWER_R` | 30 (X) × 20 (Y) × 147 (Z, 167→314). Torn vid X = 160 ±15, Y = ±(35…55). Förtjockad nav Ø44 runt axelhålet. Axelcentrum Z = 300. Lagersäte Ø28,15 × 8 från utsidan. 4 × M4 i basfläns |
| 303 | `EL_MOTOR_BRACKET` | Distans 25 mm på vänster torn utsida, bär motorn, **slitsar ±4 mm** längs remlinjen. Motorcentrum: X = 117,1, Z = 257,1 (diagonalt bakåt-nedåt 60,6 mm från axeln) |
| 304 | `EL_HALL_MOUNT` | Hall-sensor vid 80T-skivans kant |

#### 3.4 Serie 400 — Elevation (`PS_El`)

Längs Y (vänster → höger): remskiva (−70…−58), vänster torn (−55…−35), vagga (−30…+30), höger torn (+35…+55), klämring (+55…+61).

| ID | Del | Mått |
|---|---|---|
| 401 | `EL_AXLE` | Ø12 × 135 rostfritt stål 304, Y −72…+62. Två tvärhål Ø4,2 för vaggan (vid Y = ±15), ett för remskivan (Y = −64) |
| 402 | `EL_BEARING` ×2 | 6001-2RS (12×28×8), i tornen |
| 403 | `CRADLE_LOWER` | 60 (Y) × 40 (X) × 38 (Z, från Z_axle −16 till +22). Axelhål Ø12,1. Bomspår 20,3 × 10 djup. Tvärbult M4×50 med mutter i sexkantsficka. Slits för att skjuta på bommen |
| 404 | `CRADLE_CAP` | 60 × 40 × 8, 4 × M4 vid Y = ±22. Klämmer bommen |
| 405 | `EL_PULLEY_80T` | Utskriven GT2, 80 tänder, Z-axel = Y-axel. Nav Ø24 × 12, tvärstift M4×30 genom axeln |
| 406 | `EL_MOTOR_PULLEY_16T` | Köpt GT2 16T 6 mm, bor 5 mm |
| 407 | `EL_MOTOR` | 17HS19-2004S1, flänsen vänd mot tornet |
| 408 | Klämring Ø12 ×1 | Axiellt stopp på höger sida |

Boms vertikala offset mot axeln: bomcentrum 22 mm över axelcentrum → gravitation ger ett litet extramoment (§6).

#### 3.5 Serie 500 — Antenn (`PS_Antenna`, parametrisk)

Alla längder är **startvärden från v1** (se denna fil) och ska verifieras med NEC-simulering (4nec2/xnec2c) och NanoVNA innan slutlig tillverkning ⚠️.

| ID | Element | X från bomens bakre ände (mm) | Längd (mm) |
|---|---|---|---|
| 502 | Reflektor | 20 | 176 |
| 503 | Drivet (dipol, 2×77 + 8 mm matgap) | 90 | 162 |
| 504 | D1 | 160 | 152 |
| 505 | D2 | 250 | 148 |
| 506 | D3 | 350 | 144 |
| 507 | D4 | 460 | 140 |
| 508 | D5 | 560 | 136 |

| ID | Del | Mått |
|---|---|---|
| 501 | `BOOM` | 2020 V-slot, 600 mm, T-spår nedåt (vagga) och uppåt (elementhållare) |
| 509 | `EH_1…7` | Elementhållare i PETG, klämmer i T-spåret med M5-bult + T-mutter, element 14 mm över bomens ovansida (isolerade, ingen bomkorrektion) |
| 510 | Element | Ø6 aluminiumstav |
| 511 | `FEEDBOX` | 40×30×25, balun/ferritchoke, SMA-anslutning |
| 512 | Koax | RG316, ≥ 1,2 m, slingas ner genom pelarröret |

**Beräknad antennmassa:** ca 0,51 kg (bom 270 g, element 81 g, hållare 56 g, matbox 60 g, koax 40 g). Med vagga ca 0,62 kg. **Tyngdpunkt ca 253 mm från bomens bakre ände.** Axeln ska ligga där (vaggan placeras vid X = 250).

#### 3.6 Serie 600 — Elektronik (`PS_Electronics`)

| ID | Del | Mått / funktion |
|---|---|---|
| 601 | `CTRL_BOX` | IP65 ABS 100×68×50 på hyllan, 2 kabelförskruvningar PG9 + 1 för 12 V |
| 602 | ESP32-S3-DevKitC-1 | styrenhet |
| 603 | 2 × TMC2209 V1.3 | AZ + EL |
| 604 | Buck 12→5 V | 1 A |
| 605 | Kondensator 470–1000 µF/25 V | nära drivarna |
| 606 | Hall A3144 ×2 | hem AZ + EL, öppen kollektor mot 3,3 V med 10 kΩ |
| 607 | Magneter Ø6×3 N35 ×2 | på remskivorna |

**Förslag på pinout (⚠️ bekräfta vid kodning):** AZ_STEP 4, AZ_DIR 5, EL_STEP 6, EL_DIR 7, EN 15 (delad), UART TX 17 / RX 18 (enkeltråd, 1 kΩ), AZ_HOME 8, EL_HOME 9, DIAG AZ 10, DIAG EL 11.

---

### 4. Transmission i detalj

#### 4.1 Beräknade remskivor (GT2)

Formler: PD = N·2/π, OD = PD − 0,508, rotdiameter = OD − 2 × 0,764.

| N | PD (mm) | OD (mm) | Rotdiameter (mm) | Användning |
|---|---|---|---|---|
| 16 | 10,186 | 9,678 | 8,150 | EL motor (köpt) |
| 20 | 12,732 | 12,224 | 10,696 | AZ motor (köpt) |
| 80 | 50,930 | 50,422 | 48,894 | EL utgående (printad) |
| 100 | 63,662 | 63,154 | 61,626 | AZ utgående (printad) |

#### 4.2 Remmar och axelavstånd

Remlängd: L = 2C + π(D+d)/2 + (D−d)²/(4C). Löst för C (numerisk kontroll):

| Axel | Rem | C (mm) | Omslutningsvinkel liten skiva | Tänder i ingrepp |
|---|---|---|---|---|
| Azimut | **280-2GT-6** (140 T) | **75,72** | 140,7° | 7,8 |
| Azimut (alt.) | 300-2GT-6 (150 T) | 86,24 | — | — |
| Elevation | **224-2GT-6** (112 T) | **60,57** | 140,7° | 6,3 |

Slitsarna i motorfästena (±4 mm) ger remspänning och tolerans. Rekommenderad förspänning: remmen ska ge ca 1 mm genomböjning vid 2 N på mittpunkten.

#### 4.3 Hur remskivorna modelleras i Onshape

Onshape har inget färdigt GT2-bibliotek ⚠️. Två sätt:
1. **Skiss + cirkulärt mönster (rekommenderas, parametriskt):** rita en rotcirkel (Ø enligt §4.1), skissa **en** tandlucka (bredd ≈ 1,49 mm, djup 0,764 mm, rundad), extrudera ut och använd *Circular pattern* med `#az_teeth_out` instanser. Tandbilden verifieras genom att lägga in en 3D-modell av en GT2-rem som referens.
2. **Importera STEP** från en OpenSCAD- eller FreeCAD-generator med profilen "GT2 2 mm". Mindre parametriskt men snabbt.

Utskriftsregler: axeln står lodrätt, tänder i XY-planet, lagerhöjd 0,12–0,16 mm, 5 perimetrar, 100 % fyllning i tandringen. Flänsar Ø70 (100T) / Ø58 (80T), 2 mm tjocka.

---

### 5. Onshape-struktur

**Dokument:** "Gimbal v2" (kopiera "Gimbal-antenntest" som version v1-arkiv först).

| Element | Typ | Innehåll |
|---|---|---|
| `VS_Gimbal` | Variable Studio | alla parametrar i §3.0 |
| `PS_Purchased` | Part Studio | motorer, lager, remmar, sensorer, rör, profiler (enkla solida modeller med exakta mått) |
| `PS_Base` | Part Studio | serie 100 |
| `PS_Az` | Part Studio | serie 200 |
| `PS_Yoke` | Part Studio | serie 300 |
| `PS_El` | Part Studio | serie 400 |
| `PS_Antenna` | Part Studio | serie 500, element via parametrisk lista |
| `ASM_Gimbal` | Assembly | alla delar med mates |
| `DRW_*` | Drawing | utvalda delar för tillverkning |

#### 5.1 Feature-ordning per del (de viktigaste)

**BASE_PLATE** (`PS_Base`)
1. Skiss på Top: rektangel 140 × 200, centrerad. Extrudera 8 (Z 20–28).
2. Skiss på ovansidan: hål Ø36 centralt, 4 × hål Ø5,3 vid (±50, ±90), 4 × hål Ø5,5 på PCD 74 (inserts M4: Ø5,6 × 6 djup).
3. Skiss: slitsar för AZ_MOTOR_BRACKET (längd 8, bredd 4,3) vid Y = 75,7 ±4.
4. Fillet R4 på hörn.

**AZ_DRUM** (`PS_Az`)
1. Skiss på Top (Z = 97): cirkel Ø64. Extrudera 54.
2. Skiss på ovansidan: cirkel Ø`bearing_az[1] + clr_press` = Ø52,15, skär 7 mm. Samma från undersidan.
3. Skiss: mittbor Ø46, skär genom.
4. Skiss: 6 hål M4 på PCD 56 i båda ändar (insert-hål Ø5,6 × 8).
5. Skiss: 2 spår för kabel.

**AZ_PULLEY_100T** (`PS_Az`)
1. Skiss: rotcirkel Ø61,626. Extrudera tandringens höjd 8 mm (Z 85–91).
2. Nedre fläns Ø70 × 2 (Z 83–85), övre fläns Ø70 × 2 (Z 91–93), bultplatta Ø70 × 4 (Z 93–97) med mittbor Ø48.
3. Skiss på tandringens översida: en tandlucka. Extruderat snitt genom ringen.
4. Circular pattern 100 instanser kring Z.
5. 6 hål Ø4,5 på PCD 56. Hall-magnetficka Ø6,1 × 3,1 på kanten vid 0°.

**YOKE_BASE + TOWER** (`PS_Yoke`)
1. Skiss på Z = 155: Ø100 cirkel ∪ rektangel 175 × 110 med en korsande linje. Extrudera 12.
2. Kabelurtag Ø48 centralt, 6 hål M4 på PCD 56 (genomgående).
3. Torn: skiss på Z = 167, extrudera 147. Hål för axeln Ø12,3 (spel för lagerhållaren), lagersäte Ø28,15 × 8.
4. Revben: skiss i XZ, 3 mm tjocka, extrudera mellan torn och platta.
5. Fillet R3 vid tornens fot.

**CRADLE_LOWER + CAP** (`PS_El`)
1. Skiss i XZ: profil 40 × 38. Extrudera 60 symmetriskt (Y ±30).
2. Axelhål Ø12,1 genom Y. Tvärhål Ø4,3 genom X vid Y = ±15, sexkantsficka M4 för mutter.
3. Bomspår 20,3 bred, 10 djup. Slitsar för att skjuta ±60 mm längs bommen (hål för M5 till T-mutter i bommens undre spår).
4. Cap: 60 × 40 × 8 med motsvarande spår 10 djup. 4 × Ø4,3 hål vid Y = ±22.

#### 5.2 Assembly-mates

| Mate | Typ | Gränser |
|---|---|---|
| Ram, plattan, pelarfläns, rör | Fastened | — |
| `AZ_DRUM` mot rör | **Revolute** kring Z | −200° … +200° |
| AZ-remskiva, lock, yoke mot trumma | Fastened | — |
| `EL_AXLE`, vagga, 80T mot yoke | **Revolute** kring Y vid Z = 300, X = 160 | −10° … +90° |
| Motorer mot fästen | Fastened (slits = fri skjutning till låst läge) | — |
| Remmar | Modelleras som statiska delar (exakt rembana i separat skiss). Rörelse styrs av revolute-mates via en *Gear relation* med förhållande 5:1 ⚠️ (kontrollera tecken, remmen ger samma rotationsriktning) | — |

---

### 6. Beräkningar

#### 6.1 Upplösning och hastighet

Utväxling 5:1 × 200 steg × 16 mikrosteg = **16 000 mikrosteg/varv → 0,0225° per mikrosteg**. Fullsteg på utgående axel: 0,36°.
Maxhastighet 30°/s → 1 333 mikrosteg/s. Det är långt under motorns gräns vid 12 V.

#### 6.2 Moment (konservativt)

| Storhet | Värde | Anmärkning |
|---|---|---|
| Motorström | 1,2 A RMS (60 % av märkström) | ger ca 0,35 N·m hållmoment |
| Utgående moment (η = 0,9, 5:1) | ca 1,6 N·m hållande, räknar med **1,0 N·m** dynamiskt | |
| Vindyta antenn (sida) | ≈ 0,02 m² (bom 0,012 + element 0,006 + hållare) | |
| Vindkraft 10 m/s, C_d = 1,2 | F = ½·1,225·100·1,2·0,02 ≈ **1,5 N** | |
| Vindkraft 15 m/s | ≈ **3,3 N** | |
| Azimut: vindmoment (arm ≈ 0,16 m) | 0,24 N·m (10 m/s), 0,53 N·m (15 m/s) | SF ≥ 1,9 vid 15 m/s |
| Elevation: tyngdmoment | 0,507 kg · 9,81 · 0,053 m ≈ **0,26 N·m** vid X = 200; **≈ 0 N·m** vid X = 253 (balanserat) | |
| Elevation: extra från 22 mm offset | 0,62 kg · 9,81 · 0,022 ≈ 0,13 N·m | |
| Elevation: vind + tyngd (värsta fallet) | ≈ 0,43 N·m | SF ≈ 2,3 |
| Remkraft elevation vid 0,43 N·m | 0,43 / 5 / 0,00509 m ≈ **17 N** | 6 mm GT2 klarar ≫ 50 N |
| Tröghet azimut | ≈ 0,033 kg·m² | |
| Acceleration 2 rad/s² (30°/s på 0,25 s) | 0,07 N·m på utgående axel | försumbart |

**Slutsats:** 17HS19-2004S1 med 5:1 räcker med god marginal. Idle-ström ställs till ca 30 % (TMC2209 `IHOLD`) för att hålla läget i blåst utan överhettning (verifiera motorns temperatur i test, max 80 °C stigning enligt datablad).

#### 6.3 Lagerlast och stelhet

Moment på azimutlagren: yokens och antennens massa (≈ 2 kg) · 9,81 · 0,16 m ≈ 3,1 N·m plus vind ≈ 0,5 N·m. Avstånd mellan lagercentrum 47 mm → radialkraft ≈ **77 N**. 6808 har statisk bärförmåga C₀ ≈ 4,2 kN (944 lbf enligt tabell). Marginal ≫ 10.
Rörets böjspänning: I = π/64·(40⁴ − 34⁴) ≈ 60 000 mm⁴ → σ ≈ 1,3 MPa vid 4 N·m. Försumbart.

#### 6.4 Massa (uppskattad)

Ram + platta 0,6 kg, pelare + trumma + lock + remskiva 0,5 kg, motorer 0,8 kg, yoke 0,35 kg, vagga + el-axel + lager 0,35 kg, antenn 0,51 kg, elektronik 0,4 kg ⇒ **ca 3,5–4 kg**. Vältgräns: vid 15 m/s ger vinden 3,3 N · 0,35 m ≈ 1,2 N·m mot ca 4 kg · 9,81 · 0,06 m ≈ 2,4 N·m från basen (fotavstånd i smalaste riktningen). **Marginal ca 2: förankra eller lägg ballast** (öppen fråga i §6).

---

### 7. Kablage och kabelhantering

* Kablar till elevationsmotor (4 ledare), Hall (3 ledare), koax: dras **inne i pelarröret** (Ø34 invändigt) mellan basens styrbox och yokens kabelurtag.
* Lämna ≥ 250 mm fri kabel i röret (tänk 2 × rörlängd) utan buntband. Kablarna lägger sig själva spiralformat vid ±200° rotation.
* Tåliga silikonledare 24–26 AWG, flertrådiga. Koax RG316.
* Koax från antennen: ≥ 120 mm slack-slinga vid vaggan, så att elevationsrörelsen inte drar.
* Mjukvarugränser ±200° (hemning vid 0°), mekaniskt stopp vid ±210°. TMC2209 StallGuard som sekundär nödstopp.

---

### 8. Tillverkningsplan (3D-utskrift)

⚠️ Antagande: byggplatta ≥ 220 × 220 mm. Om din skrivare är mindre, säg till så delar vi basplattan och yoken.

| Del | Material | Orientering | Perimetrar / fyllning | Anmärkning |
|---|---|---|---|---|
| `BASE_PLATE` | PETG | plant | 4 / 40 % gyroid | |
| `PILLAR_FLANGE` | PETG | plant | 5 / 50 % | |
| `AZ_DRUM`, `AZ_LID` | PETG (ASA vid kall/UV) | stående, 0,12 mm | 5 / 60 % | skriv ut **testring** för lagersätet först |
| `AZ_PULLEY_100T` | PETG | plant, tänder uppåt | 5 / 100 % i ring | 0,12 mm |
| `EL_PULLEY_80T` | PETG | plant | 5 / 100 % | |
| `YOKE_BASE` | PETG | plant | 5 / 40 % | |
| `TOWER_L/R` | PETG | **stående** (lager vinkelrätt mot belastning minimeras med 5 perimetrar) | 5 / 40 % | |
| `CRADLE_LOWER/CAP` | PETG | plant | 5 / 60 % | |
| `EH_1…7`, `FEEDBOX` | PETG/ASA | plant | 4 / 40 % | |
| `AZ_MOTOR_BRACKET`, `EL_MOTOR_BRACKET` | PETG | plant | 5 / 60 % | |

**Toleranskalibrering (görs först):** skriv en **testring** med 5 sätesdiametrar Ø52,00 / 52,10 / 52,15 / 52,20 / 52,30 och en motsvarande för Ø28 (6001). Välj den som ger lätt presspassning för lagren. Uppdatera `#clr_press`.

Insatser: värmeinsatser M3×5,7 (motorfästen), M4×6 (trumma, lock, torn), M5×8 (gummifötter, T-muttrar).

---

### 9. Verifiering i CAD

1. **Mass properties** på hela assemblyn. Mål: 3,5–4 kg. Kontrollera antennens tyngdpunkt vid X = 253 från bakkant.
2. **Interference** (hela assemblyn): inga träffar utom avsiktliga presspassningar.
3. **Svepkontroll:** kör azimut −200…+200° med elevation −10, 0, +45, +90°. Kontrollera spel till ram, yoke och mark.
4. **Vertikal kontroll:** vid el = +90° ska bomens bakre ände ha ≥ 30 mm luft mot marken. Förväntat Z ≈ 300 − 253 − 10 = **37 mm**.
5. **Remvägar:** kontrollera att remmarna inte skär andra delar och att motorfästenas slitsar rymmer ±4 mm.
6. **Exportera STEP** av hela assemblyn (arkivkopia). Exportera STL för varje utskriftsdel, namnge `PartID_namn_materiel.stl`.
7. **Dokumentera** i denna fil (ersätt v1-innehållet) och uppdatera denna fil.

---

### 10. Inköpslista (BOM, uppskattade priser, ⚠️ kontrollera aktuella)

| # | Artikel | Antal | Artikel/spec | Pris (ca) |
|---|---|---|---|---|
| 1 | NEMA 17 stegmotor | 2 | **17HS19-2004S1**, 42×48 mm, 0,59 N·m | 10–15 € st |
| 2 | TMC2209-drivare | 2 | BIGTREETECH TMC2209 V1.3 | 6–10 € st |
| 3 | GT2-remskiva 20T, bor 5 mm, 6 mm rem | 1 | aluminium | 2 € |
| 4 | GT2-remskiva 16T, bor 5 mm, 6 mm rem | 1 | aluminium | 2 € |
| 5 | GT2-rem sluten 280-2GT-6 | 2 | (1 reserv) | 2–3 € st |
| 6 | GT2-rem sluten 224-2GT-6 | 2 | (1 reserv) | 1,5–2 € st |
| 7 | Kullager 6808-2RS | 2 | 40×52×7 | 3–6 € st |
| 8 | Kullager 6001-2RS | 2 | 12×28×8 | 1,5–3 € st |
| 9 | Aluminiumrör Ø40×3, 135 mm | 1 | dragen, EN AW-6060 | 8–15 € |
| 10 | Axel Ø12 × 135, rostfri 304 | 1 | | 5–8 € |
| 11 | 2020 V-slot | 2 × 280, 2 × 160, 1 × 600 mm | ca 1,5 m total | 6–10 € |
| 12 | 2020 hörnvinklar + T-muttrar M5 | 4 + 30 | | 8–12 € |
| 13 | Klämring Ø12 | 1 | | 2–3 € |
| 14 | Hall A3144 (TO-92) | 2 | | 1–2 € |
| 15 | Neodymmagnet Ø6×3 N35 | 2 | | 2 € |
| 16 | ESP32-S3-DevKitC-1 | 1 | | 8–12 € |
| 17 | Buck 12→5 V | 1 | | 2–4 € |
| 18 | Kondensator 1000 µF 25 V | 1 | | 1 € |
| 19 | Nätdel 12 V 5 A | 1 | | 10–15 € |
| 20 | IP65-låda 100×68×50 + 3 förskruvningar | 1 | | 6–10 € |
| 21 | Silikonkabel 24–26 AWG (4+3 ledare) + RG316 1,2 m + SMA | | | 10–15 € |
| 22 | Ø6 aluminiumstav, 1 m | 1 | elementen | 3–5 € |
| 23 | Skruvar M3/M4/M5, muttrar, värmeinsatser | kit | | 15–25 € |
| 24 | PETG 1 kg + ASA 0,5 kg | | | 20–35 € |
| 25 | Skruvlåsning, gummifötter, buntband | | | 5–8 € |
| | **Summa** | | | **ca 145–230 €** |

Antennens RF-del (matbox/balun/NanoVNA-justering) tillkommer om du inte redan äger ett NanoVNA.

---

### 11. Tidsplan (arbetsordning)

| Steg | Innehåll | Resultat |
|---|---|---|
| 0 | Arkivera v1, skapa `Gimbal v2`, Variable Studio | Parametrar låsta |
| 1 | `PS_Purchased`: modellera inköpsdelar med exakta mått | Referensgeometri |
| 2 | `PS_Base` + `PS_Az` (ram, plattan, rör, trumma, remskiva, motorfäste) | Roterande azimut i assembly |
| 3 | `PS_Yoke` + `PS_El` (torn, axel, vagga, remskiva, motorfäste) | Elevation med gränser |
| 4 | `PS_Antenna` parametrisk + NEC-kontroll av element | Antenn på bommen |
| 5 | Remmar, kabelväg, elektronikbox | Komplett assembly |
| 6 | Verifiering §9, fixa kollisioner | Frisläppt version |
| 7 | Exportera STL, skriv testring, kalibrera passningar | Utskriftsklara filer |
| 8 | Utskrift, montering, hemning, test mot denna fil steg 5–7 | Fungerande gimbal |

---

### 12. Öppna frågor och risker

| # | Fråga / risk | Konsekvens | Standardantagande |
|---|---|---|---|
| 1 | Byggplattans storlek på din skrivare? | Delning av `BASE_PLATE` och yoke | ≥ 220 × 220 mm |
| 2 | Ska gimbalen stå på marken eller på ett stativ? | Behövs stativadapter (¼"-20 eller 3/8") | Marken, ballast + markpinnar |
| 3 | 12 V eller 24 V? | 24 V ger marginal vid snabb sväng, men ingen skillnad för 30°/s | 12 V |
| 4 | Antennens massa kan öka (kraftigare bom, fler element) | Elevationens moment växer | Dimensionerat för 1 kg |
| 5 | **Utskrivna remskivor** (100T/80T) har lägre noggrannhet än köpta | Glapp och slitage på remmen | Verifieras med testskiva, annars köp 80T i metall och skala om |
| 6 | Lagersätet i PETG kan krypa i värme | Lösa lager | Testa i 40 °C, ASA vid behov |
| 7 | Antennens RF-prestanda beror på exakta elementlängder och bomens påverkan | Förstärkning och SWR | NEC + NanoVNA, justera längderna |
| 8 | Kyla under mars (0–10 °C) | PETG blir styvare, motorn kallare | Test i kyla (steg 6 i byggplanen) |
| 9 | Remspänning relaxerar | Pekfel | Slitsar för omspänning, kontrollera efter 1 h |

---

### 13. Nästa steg

- [ ] Du bekräftar §7 (särskilt 1, 2 och 3).
- [ ] Ev. justering av utväxling, lager eller Hall-sensorer.
- [ ] När planen är godkänd: bygg modellen i Onshape enligt §5 och §6, och uppdatera denna fil med v2-bilder och delförteckning.

---

## Del 3 — CAD-design v2 (resultat i Onshape)


Onshape-dokument: **"Gimbal-antenntest"**, flikarna `Part Studio 1`, `Feature Studio 1` och `ASM_Gimbal`.

Modellen är en **kompakt, centrerad U-fork** där elevationsaxeln sitter direkt ovanpå azimutaxeln ($X = 0$, $Y = 0$). Det tar bort den fribärande armen helt, ger noll tippande böjmoment på azimutlagren och maximal symmetri.

---

### 1. Renderingar

#### Isometrisk vy (assembly)
![ASM_Gimbal isometrisk](<asm_clean.png>)

#### Framifrån — låg profil
![ASM_Gimbal front](<asm_front.png>)

#### Närbild: riktiga ISO 4762-skruvar i bomvaggan
![Fäste med riktiga skruvar](<bolts_zoom.png>)

---

### 2. Vad som ändrades i denna iteration

| Synpunkt | Åtgärd |
|---|---|
| "Why is it so tall?" | Elevationsaxeln sänkt från $Z = 280$ till $Z = 140\text{ mm}$. Total bygghöjd minskad från ca 350 mm till ca 185 mm. Maströret kortat från 120 till 50 mm, trumman från 53 till 24 mm. |
| "Remove unnecessary boxes" | Elektroniklåda, balunlåda och påhittade kontaktdummyer borttagna. Kvar är bara mekanik + en SMA-kontakt. |
| "Make the design cleaner" | Inga namnlösa "Part NN"-kroppar kvar (0 av 124). Dekorativa cylinder-"spokes" borttagna. Dubbletter av delar borta. |
| "Don't use cylinders for bolts" | Fejkade cylinder-"bultar" borttagna. Införda **4 × ISO 4762 M4×16** insexskruvar med rätt huvud (Ø7 × 4 mm), sexkantsfäste och gängad stam. |
| "Use real bolts in the assemblies tab" | `ASM_Gimbal` skapad med **124 instanser** (en per del, inga dubbletter), inklusive skruvarna som egna artikelnummer. |

---

### 3. Nyckelmått

| Parameter | Värde |
|---|---|
| Basram (2020 V-slot) | 220 × 180 mm |
| Basplatta | 150 × 170 × 6 mm |
| Azimutlager | 2 × 6808-2RS (40×52×7), $Z = 48$–55 och 65–72 |
| Azimuttrumma | Ø60 × 24 mm, $Z = 48$–72 |
| Azimutremskiva | 100T GT2, Ø63,15 mm, $Z = 42$–48 |
| Vridkrans | Ø88 × 8 mm, $Z = 72$–80 |
| Torn | $X = 0$, $Y = \pm 42$, $Z = 80$–154 |
| **Elevationsaxel** | **$X = 0$, $Z = 140$ mm**, Ø12 × 125 mm rostfri |
| Elevationslager | 2 × 6001-2RS (12×28×8) |
| Elevationsremskiva | 80T GT2, Ø50,42 mm |
| Axelavstånd rem | azimut $C = 75{,}72$ mm, elevation $C = 60{,}57$ mm (vertikalt) |
| Utväxling | 5:1 på båda axlarna |
| Upplösning | 0,0225°/mikrosteg |
| Bom | 2020 V-slot, 600 mm, klämd vid tyngdpunkten 253 mm från bakkant |
| Antenn | 7 element, 868 MHz, element Ø6 mm på $Z = 174$ mm |

---

### 4. Delar och struktur

`Part Studio 1` innehåller **124 solida delar**, alla namngivna enligt schema:

* **Serie 100** — bas: `101_RAIL_X_*`, `102_RAIL_Y_*`, `103_CORNER_BKT_*`, `104_BASE_PLATE`, `105_PILLAR_FLANGE`, `106_FOOT_*`
* **Serie 200** — azimut: `201_PILLAR_TUBE`, `203_AZ_DRUM`, `204_AZ_BEARING_*`, `206_AZ_PULLEY_100T_*`, `207_AZ_PULLEY_20T_*`, `208_AZ_MOTOR_*`, `209_AZ_MOTOR_BRACKET`, `AZ_BELT_280_LOOP`
* **Serie 300** — yoke: `301_TURRET_BASE_DISC`, `302_TOWER_L/R_*`, `303_EL_MOTOR_BRACKET`
* **Serie 400** — elevation: `401_EL_AXLE`, `402_EL_BEARING_*`, `403_CRADLE_LOWER`, `404_CRADLE_CAP`, `405_EL_PULLEY_80T_*`, `406_EL_PULLEY_16T_*`, `407_EL_MOTOR_*`, `408_SHAFT_COLLAR`, `EL_BELT_224_LOOP`
* **Serie 500** — antenn: `501_ANTENNA_BOOM_2020`, `502_REFLECTOR_ROD`, `503_DRIVEN_DIPOLE_*`, `504`–`508` director, `509_EH_*`, `511_SMA_CONNECTOR`, `512_BOOM_END_CAPS`
* **Fästelement** — `ISO4762_M4x16_A` … `_D` (plus `_SOCKET`, `_SHANK`, `_THREAD` underdelar)

---

### 5. Kinematik

Funktionen `Gimbal CAD Plan V2` i `Feature Studio 1` har två parametrar:

| Parameter | Gränser | Rörelse |
|---|---|---|
| `azimuthAngle` | −200 … +200° | Panorerar azimutgruppen kring $Z$ |
| `elevationAngle` | −10 … +90° | Tiltar bom, vagga och antenn kring $(0, 0, 140)$ |

---

### 6. Källkod

* [GimbalCADv2.fs](GimbalCADv2.fs) — FeatureScript för hela modellen inklusive fästelementsbibliotek
* [make_compact_clean.js](make_compact_clean.js) — generator för basgeometrin

Regenereringstatus i Onshape: **OK**, 0 fel, 0 namnlösa kroppar.

