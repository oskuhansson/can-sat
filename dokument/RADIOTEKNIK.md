---
tags: [cansat, radio, grunder]
status: referens
updated: 2026-11-07
---

# Radioteknik — snabbkurs i termerna (för er CanSat/mark-RX)

*Skapad 2026-11-03. En nybörjarvänlig genomgång av de radiotekniska begreppen ni stött
på — SNR, Eb/N₀, modulering och ESP-NOW — kopplade till er design (monopol i burken +
markmottagare). Målet är förståelse, inte formell teori.*

---

## 1. Grunden: hur radio funkar i ett nötskal

En radiosignal är elektromagnetiska vågor. Två saker avgör om en mottagare "hör" meddelandet:

1. **Signalstyrkan vid mottagaren** — hur stark signalen är när den kommer fram (i dBm).
   Varje fördubbling av avståndet gör signalen ~6 dB svagare (invers-kvadratlagen).
2. **Bruset** — all mottagare producerar en grundnivå av oönskad elektrisk störning
   ("brusgolvet", noise floor). En mottagare kan bara tolka signalen om den ***tydligt
   sticker ut ovanför bruset***.

Det viktiga är alltså inte bara *hur stark* signalen är, utan **signalens styrka i
förhållande till bruset**. Det är där SNR kommer in.

---

## 2. SNR — Signal-to-Noise Ratio (signal-till-brus-förhållande)

**Definition (enkelt):** förhållandet mellan **användbar signal** och **brus**, uttryckt
i **dB**.

```
SNR (dB) = Psignal (dBm) − Pbrus (dBm)
```

- +20 dB = signalen är 100× starkare än bruset; +10 dB = 10×; +3 dB ≈ 2×.
- **Ju högre SNR, desto "renare" mottagning.** Under en viss tröskel kan mottagaren inte
  tyda signalen alls (den drunknar i brus).

Praktiskt för er mark-RX:
- En mottagare behöver t.ex. **SNR ≥ −5…−20 dB** (beroende på teknik) för att lyckas.
  Märkligt nog kan **LoRa** funka på **negativt SNR** (signalen svagare än bruset!) tack
  vare sin robusta modulering (se §4) — det är därför LoRa når kilometerlångt avstånd
  där WiFi ger upp.
- **RSSI är inte SNR.** RSSI (Received Signal Strength Indicator) visar bara signalstyrkan
  (dBm), men säger inget om hur brusigt det är. Två platser med samma RSSI kan ha olika
  SNR om brusnivån skiljer sig.

> **Kom ihåg:** dBm = absolut effekt i dB mot 1 mW. dB (utan "m") = förhållande. SNR är
> ett förhållande → enhetslöst, alltid i dB.

---

## 3. Eb/N₀ — "signal per bit" — och hur den skiljer sig från SNR

SNR mäter signal vs brus **över hela kanalens bandbredd**. Finkalibrigare: **Eb/N₀** mäter
signalenergin per **informationsbit** mot brusets spektrala täthet.

- **E_b** = energi per bit = signaleffekten × tiden för en bit = P_signal / datatakt (R_b).
- **N₀** = bruseffekt per hertz bandbredd (W/Hz).

**Varför Eb/N₀?** Den tar bort effekten av *hur snabbt* och *hur brett* man sänder:
- Ett snabbt system (hög datatakt R_b) har liten energi per bit → högre Eb/N₀ behövs.
- Ett långsamt, smalbandigt system (t.ex. LoRa med låg SF) har stor energi per bit →
  klarar sig med låg Eb/N₀.

**Relationen mellan SNR och Eb/N₀:**

```
Eb/N0 = SNR × (bandbredd B) / (datatakt R_b)

i dB:  Eb/N0 (dB) = SNR (dB) + 10·log10(B / R_b)
```

Eftersom **B / R_b ofta är > 1** (man sänder i en bredare kanal än datatakten) är
**Eb/N₀ högre än SNR** i dB. Det förklarar varför "högt SNR krävs" i snabbfk-kanaler men
"lågt SNR räcker" i långsamma.

**Praktiskt:** Eb/N₀ är ingen slutsiffra du läser av en mottagare — det är ett
**design- och jämförelsemått**: alla moduleringar har en känd "vad som krävs"-tröskel i
Eb/N₀. Notera att LoRa-rapporter visar bland annat **MDS/sensitivity** (t.ex. −137 dBm)
snarare än Eb/N₀, eftersom CSS-moduleringens prestanda ofta anges via känslighet och SNR-
tröskel, inte direkt via Eb/N₀.

**Per avståndshoppet i er mark-RX:** med 868 MHz LoRa (SF12, 125 kHz) är den
effektiva datatakten mycket låg (hundratals bit/s) men känsligheten superb (−120…−137 dBm).
Det är *precis* poängen: långsam + robust = låg data per bit = mycket lägre SNR-tröskel →
kilometerlång räckvidd.

---

## 4. Modulering — hur information läggs på bärvågen

"Modulering" = hur mottagaren mappar 0:or och 1:or (eller analog signal) till
variationer i radiosignalen. Olika moduleringar ger olika bandbredd, robusthet och
datatakt.

### a) Digitala basmoduleringar (enkla varianter)
- **ASK (Amplitude Shift Keying):** byter amplitud (styrka) — 1 = stark, 0 = svag.
  Enkelt men känsligt för brus/dämpning.
- **FSK (Frequency Shift Keying):** byter **frekvens** — 1 = en ton, 0 = en annan ton.
  Robustare än ASK (störningar ändrar mest styrkan, inte tonen).
- **PSK (Phase Shift Keying) / QAM (Quadrature Amplitude Modulation):** byter **fas**
  och/eller **amplitud**; används i hög-hastighets-länkar (WiFi, satellitupplänkar).
  Högre ordningar (t.ex. 64-QAM) packar många bitar per symbol men kräver högt SNR.

### b) LoRa — CSS (Chirp Spread Spectrum) 🥇 (er val)
LoRa använder en **fjäril-liknande "chirp"** (frekvens som glider upp/ner) för att
representera data över en bred bandbredd:
- Extremt robust mot brus och väg-reflektioner (multipath) → låg SNR-tröskel.
- **Spreading Factor (SF):** högre SF (SF12) = långsammare men mer robust; lägre SF (SF7)
  = snabbare men kortare räckvidd. Data rate för 125 kHz: ~0,3 kb/s (SF12) → ~11 kb/s (SF7).
- **Bandbredd (BW):** bredare = snabbare men mindre känslig; 125/250/500 kHz.

Praktiskt för er burk: vill ni ha **maximal räckvidd**, kör SF12/BW125 (långsamt men
80 dB link-marginal, §5.2). Vill ni skicka **mer GPS/telemetri-data**, kör SF7–SF9.

### c) WiFi — OFDM
WiFi (802.11) använder **OFDM/QAM** — många delbärare, hög datatakt. Perfekt för stora
datamängder på kort avstånd, men kräver **högt SNR** (~−85…−90 dBm känslighet) → kort
räckvidd. Jämför med LoRa: samma 20 dBm skickar WiFi ~100 m, LoRa ~2–10 km (lägre data).

**Sammanfattning avvägning:**

| Teknik | Modulering | SNR-tröskel | Datatakt | Räckvidd (20 dBm) |
|---|---|---|---|---|
| LoRa 868 | CSS | mycket låg (negativ dB) | ~0,3–11 kb/s | **km-klass** ✅ |
| WiFi 2,4 | OFDM/QAM | hög (−85…−90 dBm) | Mb/s | ~100 m |
| ESP-NOW | (WiFi-fysik) ≈ OFDM | hög | ~1–2 Mb/s | ~10–200 m |

---

## 5. ESP-NOW — vad är det?

[ESP-NOW](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/network/esp_now.html)
är ett **par-till-par-till (peer-to-peer) protokoll** från Espressif (tillverkaren av
ESP32-kopplingar):

- Går genom **WiFi-hårdvaran (2,4 GHz)** men **utan** en accesspunkt/router och utan
  handskakning/koppling. Två ESP32:or byter helt enkelt datapaket direkt.
- **Fördelar:** mycket enkel att programmera, låg latens, ingen WiFi-router behövs.
- **Nackdelar:** det är fortfarande **WiFi-fysik** → hög SNR-tröskel och **kort räckvidd**
  (~10–200 m beroende på antenner/omgivning). Det är **inte** lämpligt för er
  mark-RX på upp till 1+ km slantavstånd.
- **När det passar:** nim-till-nim test på bordet, två enheter i samma rum, korta demo,
  ESP32-eksampler — inte som nedlänk från en fallande burk på kilometers avstånd.

**Så:** ESP-NOW är ett *fjärr-kopplingsprotokoll*, inte en längdjord radiosansluttar
mekanism. För kilometersäckande mark-RX vill ni ha **LoRa (868 MHz)** — betydligt lägre
SNR-tröskel och därför mycket längre räckvidd. (Det som gör att EQ-NOW har "kort räckvidd"
är att den ärvär WiFi:arkitekturen, som kräver högt SNR.)

---

## 6. Hur allt hänger ihop med er design (mark-RX)

| Koncept | Var det dyker upp i erat uppdrag |
|---|---|
| **SNR** | Det som mottagaren i markstationen faktiskt upplever; RSSI-loggen är bara signalstyrkan |
| **Eb/N₀** | Jämförelsemått; förklarar varför långsam LoRa (låg bit-energikrav) klarar km-avstånd |
| **Modulering (CSS/LoRa)** | Er bärlina: 868 MHz, SF/BW-väljare styr räckvidd vs data |
| **ESP-NOW** | Bara för bordstest/demo — inte för nedlänken från burken |

**Rekommendation:** kör **868 MHz LoRa (CSS, SF7–SF12)** i burken + 12–23 dBi markantenn.
ESP-NOW/WiFi är utmärkta för prototypning på kort avstånd, men för den faktiska
nedlänken på ~1+ km vinner LoRa med hela link-marginalen (60–80 dB, §5.2).

Ett praktiskt sätt att se skillnaden live: prova att skicka samma paket på WiFi (ESP-NOW)
och på LoRa från balkongen — WiFi tappar signalen efter några tiotals meter,
LoRa når hundratals meter–kilometrar vid låg SF.

---

## Se även

- [KOMMUNIKATION.md](KOMMUNIKATION.md) — där begreppen används i praktiken (§3 och §5.2)
- [PROTOKOLL.md](PROTOKOLL.md) — moduleringsvalen i detalj
- [BEAMFORMING.md](BEAMFORMING.md) — när man går från en antenn till flera
- [QA.md](QA.md) — testa om du förstått begreppen (Del A)
