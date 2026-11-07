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

## 6. Bandbredd vs datahastighet — och varför bredare inte är gratis

**Två helt olika storheter som lätt blandas ihop:**

| | **Bandbredd** | **Datahastighet** |
|---|---|---|
| Enhet | **Hz** (kHz) | **bit/s** (kb/s) |
| Vad det är | Hur mycket **spektrum** signalen tar | Hur mycket **information** som kommer fram |
| Analogi | Bredden på röret | Vattenflödet genom det |
| Styrs av | Kanalvalet | Kanalval **+** spridningsfaktor |
| Regleras | Ja — du äger bara din kanal | Nej |

**Bandbredd är en resurs. Datahastighet är ett resultat.** En FM-station använder 200 kHz
för att skicka musik — bandbredden är kostnaden, inte innehållet.

### 6.1 Formeln som binder dem samman

För LoRa (CSS) är chiphastigheten numeriskt lika med bandbredden. Varje symbol bär $SF$
bitar men tar $2^{SF}$ chips:

$$
R_s = \frac{BW}{2^{SF}}
\qquad\Longrightarrow\qquad
\boxed{R_b = SF \cdot \frac{BW}{2^{SF}}}
$$

Kontroll mot SX1280-databladet (SF5, BW 1625 kHz):

$$
R_b = 5 \cdot \frac{1\,625\,000}{2^5} = 253\,906\ \text{bit/s} = \mathbf{253{,}9\ kb/s}\ ✓
$$

### 6.2 Känsligheten — de två rattarna ger båda 3 dB

$$
P_{\text{min}} = -174 + 10\log_{10}(BW) + NF + \text{SNR}_{\text{min}}(SF)
$$

| Ratt | Ändring | Effekt på känslighet |
|---|---|---|
| **Bandbredd** | $\times 2$ | **+3 dB** (sämre) — brusgolvet $N = kTB$ fördubblas |
| **SF** | $+1$ | **−3 dB** (bättre) — processvinst $10\log_{10}(2)$ |

SX1280:s känslighet vid 2,4 GHz (PER 1 %, CR 4/5, 10 byte):

| BW \ SF | SF5 | SF6 | SF7 | SF8 | SF9 | SF10 | SF11 | SF12 |
|---|---|---|---|---|---|---|---|---|
| 203 kHz | −109 | −111 | −115 | −118 | −121 | −124 | −127 | **−130** |
| 406 kHz | −107 | −110 | −113 | −116 | −119 | −122 | −125 | −128 |
| 812 kHz | −105 | −108 | −112 | −115 | −117 | −120 | −123 | −126 |
| **1625 kHz** | **−99** | −103 | −106 | −109 | −111 | −114 | −117 | −120 |

Kontroll: SF5→SF12 vid 203 kHz är 7 steg $\times$ 3 dB = 21 dB (−109 → −130) ✓
Och 203→1625 kHz är $\log_2(8) = 3$ dubbleringar $\times$ 3 dB = 9 dB (−130 → −120) ✓

### 6.3 ⚠️ Myten: "bredare bandbredd ger mer data gratis"

Det ser ut så i tabellen om man läser slarvigt:

| Inställning | Känslighet | Datahastighet |
|---|---|---|
| 203 kHz, SF7 | −115 dBm | 11,1 kb/s |
| 1625 kHz, SF10 | −114 dBm | **15,9 kb/s** |

Samma känslighet, 43 % mer data — men **8× mer spektrum**. Är det gratis?

**Nej. Teorin säger exakt noll.** Dubbla BW ger +3 dB brus; höj SF ett steg ger −3 dB
tillbaka. Och datahastigheten:

$$
BW \times 2 \Rightarrow R_b \times 2
\qquad\text{men}\qquad
SF + 1 \Rightarrow R_b \times \frac{SF+1}{2\,SF} \approx \div 2
$$

**Netto noll.** 1 dB-skillnaden i tabellen är databladets avrundning. Kontrollera med
203/SF7 mot 406/SF8:

$$
11{,}1 \cdot \frac{2 \cdot 8/2}{7} = 12{,}7\ \text{kb/s}\ ✓
\qquad(\text{tabellen: } {-115} \to {-116}\ \text{dBm, alltså 1 dB})
$$

> **Du kan inte köpa datahastighet med bandbredd.** Du flyttar bara samma växel mellan
> två rattar — och gör det med bredare bandbredd blir det **rent slöseri**: samma
> prestanda, mer spektrum.

### 6.4 Den eleganta detaljen: bandbredden kancellerar

Spektral effektivitet = datahastighet per Hz:

$$
\frac{R_b}{BW} = \frac{SF}{2^{SF}}
$$

**Bandbredden försvinner.** Det betyder att **SF** bestämmer hur effektiv moduleringen är,
medan bandbredden bara skalar hela systemet upp eller ner.

| SF | Effektivitet | Jämför |
|---|---|---|
| SF5 | 0,156 bit/s/Hz | |
| SF7 | 0,055 | |
| SF10 | 0,010 | |
| SF12 | **0,003** | WiFi: 2–6 bit/s/Hz |

0,003 bit/s/Hz är extremt lågt. **LoRa köper känslighet genom att slösa spektrum** — det är
hela poängen med tekniken.

### 6.5 Nackdelarna med hög bandbredd

| Nackdel | Detalj |
|---|---|
| **Ryms inte på 868 MHz** | Sub-bandet är **600 kHz brett** (868,0–868,6 MHz). BW ≥ 812 kHz är fysiskt omöjligt. |
| **Mer störningsexponering** | En 1625 kHz-kanal på 2,4 GHz överlappar större delen av en WiFi-kanal (20 MHz) → fångar fler *riktiga* störare |
| **Högre ström** | SX1280: **5,5 mA** vid 203 kHz mot **7,5 mA** vid 1625 kHz (+36 %) |
| **Sämre känslighet vid samma SF** | 3 dB per fördubbling → 10 dB mellan 203 och 1625 kHz ≈ **3× kortare räckvidd** |
| **Ingen effektivitetsvinst** | $SF/2^{SF}$ är oförändrat — du får inget extra per Hz |

### 6.6 Ryms bandbredden i bandet? (avgörande vid 868 MHz)

| BW | Ryms i 868,0–868,6 MHz? |
|---|---|
| 203 kHz | ✅ |
| 406 kHz | ✅ (knappt) |
| 812 kHz | ❌ |
| 1625 kHz | ❌ |

**1625 kHz är fysiskt omöjligt på 868 MHz.** Därför använder LoRaWAN i EU 125 och 250 kHz.
På 2,4 GHz är det inget problem — kanalerna ligger 5 MHz isär.

### 6.7 ✅ Den enda ärliga vinsten: kortare lufttid

Med bred bandbredd går paketet ut snabbare. Ett 20-byte-paket:

$$
T_{\text{air}} \approx \frac{8 \cdot n_{\text{byte}}}{R_b}
$$

| Inställning | Datahastighet | Lufttid |
|---|---|---|
| SF12 / 203 kHz | 0,595 kb/s | **~270 ms** |
| SF10 / 203 kHz | 1,98 kb/s | ~81 ms |
| SF10 / 1625 kHz | 15,87 kb/s | **~10 ms** |

Vid 868 MHz med **1 % duty cycle** (36 s/timme) är detta skillnaden mellan ~130 paket i
timmen och tusentals. **Har du länkmarginal att spare är bred bandbredd + låg SF det som
ger mest telemetri inom duty-cycle-budgeten.**

Notera: vinsten handlar om **tid**, inte om känslighet.

### 6.8 Beslutsregel

| Band | Välj | Varför |
|---|---|---|
| **868 MHz** | Smalast möjliga BW, hög SF | Max räckvidd; bandet är bara 600 kHz; duty cycle 1 % tvingar fram korta paket |
| **2,4 GHz** | Bredast möjliga BW, låg SF | Ingen duty-gräns, gott om spektrum, korta lufttider → mer data |

**Tumregel:** *bandbredd är hur mycket spektrum du bränner, datahastighet är vad du får ut
— och i LoRa är det SF, inte bandbredden, som avgör hur effektivt du omvandlar det ena
till det andra.*

---

## 7. Hur allt hänger ihop med er design (mark-RX)

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
