---
tags: [cansat, moc]
status: aktuell
updated: 2026-11-07
---

# CanSat — projektöversikt

CanSat-uppdrag för **Suomen CanSat -kilpailu i Vasa 11–14.3.2027**.

**Designen i en rad:** burken har en **enkel monopol-antenn** och sänder telemetri;
**allt svårt ligger på marken** — en hög-gain-antenn på en gimbal som följer burken.
Sekundärmission: **muondetektor** (scintillator + SiPM).

---

## Börja här

Läs i den här ordningen om du är ny i projektet:

| # | Fil | Vad den ger dig |
|---|---|---|
| 1 | **[CANSAT-GRUND.md](CANSAT-GRUND.md)** | Vad en CanSat är, regler, flygprofil, deadlines, moduler |
| 2 | **[RADIOTEKNIK.md](RADIOTEKNIK.md)** | Radio-grunder: SNR, Eb/N₀, modulering, LoRa vs WiFi |
| 3 | **[KOMMUNIKATION.md](KOMMUNIKATION.md)** | **Huvuddokumentet** — länkbudget, regler, antennval, polarisation |
| 4 | **[PROTOKOLL.md](PROTOKOLL.md)** | Vilket radioprotokoll vi väljer (LoRa / 2,4 GHz / BLE) |
| 5 | **[GIMBAL.md](GIMBAL.md)** | Markgimbalen — byggplan och CAD |
| 6 | **[MUONDETEKTOR.md](MUONDETEKTOR.md)** | Sekundärmissionen |

---

## Referens och förberedelse

| Fil | Innehåll |
|---|---|
| **[BEAMFORMING.md](BEAMFORMING.md)** | Beamforming: metoder, hårdvara, matematik (styrvektor, Capon, MUSIC) |
| **[FASVAXLARE.md](FASVAXLARE.md)** | Fasväxlare för 868 MHz och 2,4 GHz — vilka fungerar, priser, varningar |
| **[KOSTNADER.md](KOSTNADER.md)** | Hela budgeten mot taket ≤ 500 € |
| **[QA.md](QA.md)** | Kunskapsquiz, faktakontroll och svar på tuff kritik |

---

## Grunddata att hålla koll på

| Krav | Värde |
|---|---|
| Volym | 115 mm × 66 mm (europeisk burk, ~330 ml) |
| Massa | **300–350 g** inkl. batteri |
| Budget | **≤ 500 €** |
| Acceleration | 20 G krav, **~30 G verklig** |
| Nedfart | 5–12 m/s (rek. 8–11), apogeum 750–1100 m |
| Mättid | **~70–120 s** |
| Pre-Launch Report | **20.2.2027**, max 15 sidor, engelska |

⚠️ **Verifiera med ESERO Finland att laget är registrerat** — förregistreringen
stängde 30.10.2026.

---

## Designen i korthet

```
BURKEN                                   MARKEN
enkel monopol (omni)                     hög-gain-antenn på gimbal
  ├─ LoRa 868 MHz: GPS + telemetri         ├─ 12–23 dBi yagi/array
  └─ 2,4 GHz: hög datatakt, fri duty       ├─ RSSI + GPS följer burken
                                           └─ PC loggar allt
```

**Varför:** allt som är svårt (förstärkning, pekning, mekanik) hamnar på marken där det
inte finns massa-, volym- eller effektgränser. Burken förblir minimal och tål 30 G.

**Nyckeltal:** 868 MHz LoRa ger ~60–75 dB länkmarginal. 2,4 GHz ger ~20 dB vid max
datahastighet — men **ingen duty-cycle-gräns** (mot 1 % på 868 MHz).

---

## Arkiv

Övergivna spår, sparade för referens:

| Fil | Innehåll |
|---|---|
| [arkiv/CLOUD-CHAMBER.md](arkiv/CLOUD-CHAMBER.md) | Den ursprungliga cloud chamber-forskningen (ersatt av muondetektorn) |
| [arkiv/KOMMUNIKATION-HISTORIK.md](arkiv/KOMMUNIKATION-HISTORIK.md) | WiFi-hotspot-idén och bent-pipe-reläet (övergivna), men med användbar fysik och regulatorik |

---

## Status

- [x] Forskning: monopol i burken + markgimbal — 60–75 dB marginal på 868 MHz
- [x] Forskning: anslutningslös dubbel — ESP-NOW/LoRa broadcast (KOMMUNIKATION, avsnitt 7)
- [x] Forskning: protokollval och priser (PROTOKOLL)
- [x] Forskning: polarisation och mönsternolla (KOMMUNIKATION, del 3)
- [x] CAD: markgimbal i Onshape (GIMBAL)
- [ ] **Kontakta ESERO Finland** (registrering, antennregler, frekvensplan)
- [ ] Inköp: MAPS-010144 ×4 (bara 38 i lager — bråttom), LNA, radio
- [ ] Prototyp: LoRa-beacon + markgimbal-tracker (RSSI + GPS)
- [ ] Kapsla in i CanSat-burk (115 mm × 66 mm, 300–350 g)

---

## Arbeta i Obsidian

Den här mappen är förberedd som ett Obsidian-vault. Alla filer har YAML-frontmatter
med `tags`, `status` och `updated`.

**Inställningar (gör en gång):**

| Inställning | Värde | Varför |
|---|---|---|
| Files & Links → **Use Wikilinks** | **OFF** | så att relativa fil-länkar fungerar både här och på GitHub |
| Files & Links → New link format | **Relative path** | matchar befintliga länkar |
| Core plugins → Graph view, Backlinks, Tags, Canvas | **PÅ** | navigering och visualisering |
| Editor → Show line number | PÅ | för att kunna referera till rader |

**Bra att börja med:**

- **Graph view** (`Ctrl+G`) — visar hur dokumenten hänger ihop
- **Sök** (`Ctrl+Shift+F`) — söker i hela forskningen
- **Taggar** — filtrera på `#cansat`, `#radio`, `#beamforming`, `#arkiv`
- **Canvas** — rita systemarkitektur eller tidslinje på en oändlig yta

**Frivilligt — Dataview-plugin** (Settings → Community plugins) ger automatiska
översikter, t.ex. en tabell över alla dokument med `status: aktuell`.

> ⚠️ **OneDrive-varning:** ni ligger på en OneDrive-sökväg. Obsidian fungerar, men
> undvik att redigera samma fil på två enheter samtidigt — då kan `.obsidian/` och
> filerna synkkonflikta. `.obsidian/workspace.json` är redan i `.gitignore`.
