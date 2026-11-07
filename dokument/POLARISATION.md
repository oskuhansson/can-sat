---
tags: [cansat, antenn, polarisation]
status: referens
updated: 2026-11-07
---

# Polarisation och antennmönster i burken

*Utdragen ur [KOMMUNIKATION.md](KOMMUNIKATION.md) 2026-11-07 — eget dokument eftersom det
är ett avgränsat antennafysik-område. Burken roterar och gungar under fallskärmen: hur
påverkar det länken, och vad gör man åt det?*

**Två problem som ofta blandas ihop:** *polarisationsmismatch* (0–30 dB) och
*mönsternolla* (10–20+ dB). De har olika lösningar — den mekaniska lösningen (att hänga
rakt) löser polarisationen men **inte** nollan.

---

## 1. Två olika problem

| Problem | Vad det är | Typisk förlust |
|---|---|---|
| **Polarisationsmismatch** | Burken sänder linjärt i en vinkel, marken tar emot i en annan | 0–30 dB beroende på vinkel |
| **Mönsternolla** | En monopol strålar inte längs sin egen axel | 10–20+ dB nära axeln |

Man måste hantera **båda** — och den mekaniska lösningen (att hänga rakt) löser
polarisationen men **inte** nollan.

---

## 2. Vad rotationen faktiskt gör

Polarisationsförlust mellan två linjärt polariserade antenner med vinkeln $\theta$
mellan sina polarisationsplan:

$$
\boxed{L_{\text{pol}} = 20\log_{10}\!\left(\cos\theta\right)\ \text{dB}}
$$

### 2.1 Förlusttabell

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

### 2.2 ⭐ Nyckelinsikten

**Spin kring den vertikala axeln kostar NOLL.**

En vertikal monopol som roterar kring sin egen axel är **fortfarande vertikalt
polariserad** — polarisationsplanet ändras inte av en rotation kring axeln. Det är
**bara tilt/tumbling** som kostar.

Det betyder att en burk som hänger lodrätt under fallskärmen och snurrar är
**polarisationsmässigt immun** — och snurrandet är dessutom det som händer mest.

---

## 3. Mitigering — i kostnadsordning

### 🥇 A. Mekanisk: låt burken hänga vertikalt (0 €, störst effekt)

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

### 🥈 B. Marken: två korspolariserade antenner + switch (~$6)

Sätt **två antenner i ±45°** mot varandra och välj den starkare. Då är man **aldrig mer
än 45° fel** → **max 3 dB förlust** oavsett hur burken roterar.

| Konfiguration | Värsta fall |
|---|---|
| En vertikal antenn | **20–30 dB** |
| **Två antenner ±45° + switch** | **3 dB** ✅ |
| Fyra antenner 0/45/90/135° | 0,7 dB |

**Kostnad:** en extra patch (~$5) + en [PE4259-switch](FASVAXLARE.md) (~$0,50).

**Bästa nyttan per krona.** Kräver bara en switch + en GPIO, ingen extra mottagare.

### 🥉 C. Cirkulär polarisation i burken (bäst, men bara 2,4 GHz)

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

### D. Två ortogonala monopoler + kombinerare
Två monopoler i 90° i burken, kombinerade med 90° fasförskjutning → CP. Ryms på båda
banden men är pilligare än en turnstile.

---

## 4. Burkens elektriska storlek — ett starkare argument för 2,4 GHz

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

## 5. ⚠️ Det större problemet: mönsternollan

Detta är ofta **värre än polarisationen**. En vertikal monopol har en **nolla rakt upp
och rakt ner**. Markstationen ligger *under* burken → nära nollan.

Monopolmönster över ett jordplan:

$$
\boxed{G(\theta) = G_{\max}\sin^{2}\theta}
$$

där $\theta$ mäts från antennaxeln.

### 5.1 Nolltabell

| Riktning till markstationen | $\theta$ från axeln | Dämpning |
|---|---|---|
| Horisontellt | 90° | 0 dB |
| 45° nedåt | 45° | −3,0 dB |
| 30° nedåt | 30° | −6,0 dB |
| 20° nedåt | 20° | **−9,3 dB** |
| 10° nedåt | 10° | **−15,2 dB** |
| Rakt ned | 0° | **−∞** |

### 5.2 Varför det ändå ofta går bra

Geometrin hjälper: burken faller från ~1 km och **driver** med vinden. Markstationen
hamnar därför sällan rakt under.

$$
\phi_{\text{elev}} = \arctan\!\left(\frac{h}{d_{\text{drift}}}\right)
$$

Med 1 km höjd och 500 m drift blir infallsvinkeln $\arctan(1000/500) = 63°$ från
horisontalplanet → bara ~27° från vertikalen i monopoltermer → **~−7 dB**. Och med
60–80 dB systemmarginal (868 MHz) eller 23 dB (2,4 GHz vid 254 kb/s) är det **helt
absorberat**.

### 5.3 Åtgärder mot nollan

| Åtgärd | Effekt | Kostnad |
|---|---|---|
| **Luta antennen 30–45°** bort från nollriktningen | +6–10 dB nedåt | 0 € |
| **Sleeve-monopol / top-loaded** | bredare mönster | liten |
| **Acceptera** med systemmarginal | — | 0 € |
| **Dipol istället för monopol** | nollor blir horisontella | 0 € |

---

## 6. Rekommendation

| Prioritet | Åtgärd | Kostnad | Vinst |
|---|---|---|---|
| **1** | Monopol längs fallskärmsaxeln + låg tyngdpunkt | **0 €** | tilt → ±25° → **<1 dB** |
| **2** | Två markantenner ±45° + PE4259-switch | **~$6** | värsta fall **3 dB** istället för 30 |
| **3** | Luta burkantennen 30° bort från nollan | 0 € | **+6–10 dB** mönster |
| **4** | CP-turnstile i burken (endast 2,4 GHz) | ~$2 | immun mot rotation |

**För under $10 får man en i praktiken polarisationssäker lösning.** Det mekaniska
(prioritet 1) gör ~80 % av jobbet gratis.

---

## 7. Sammanfattning i en tabell

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

## 8. Källor och vidare läsning

- [KOMMUNIKATION.md](KOMMUNIKATION.md) — §5 (monopol i burken), §3 (antennbegrepp)
- [PROTOKOLL.md](PROTOKOLL.md) — länkbudgetar för 2,4 GHz vs 868 MHz
- [FASVAXLARE.md](FASVAXLARE.md) — PE4259-switchen för polarisationsval
- Balanis, *Antenna Theory* — kapitel om monopol, jordplan, polarisation
- [Traficom — frekvensanvändning i luftfartyg](https://traficom.fi/en/radio-licences-and-frequencies/use-radio-frequencies/frequency-use-unmanned-aviation)

---

*Levande dokument. Uppdatera med mätresultat från marktest (RSSI vs uppmätt rotation)
när prototypen finns.*

---

## Se även

- [KOMMUNIKATION.md](KOMMUNIKATION.md) — systemdesign och länkbudget
- [BEAMFORMING.md](BEAMFORMING.md) — strålbredd och arrayfaktor (nollan är samma fenomen)
- [PROTOKOLL.md](PROTOKOLL.md) — varför 2,4 GHz är bättre för små burkantener
- [FASVAXLARE.md](FASVAXLARE.md) — PE4259-switchen för polarisationsval
