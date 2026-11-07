---
tags: [cansat, beamforming, antenn, matematik]
status: referens
updated: 2026-11-07
---

# Beamforming — metoder, hårdvara och matematik

*Hur man elektroniskt styr en antennstråle med flera element. Del 1 förklarar metoderna och vad de kräver i hårdvara; del 2 ger matematiken.*

---

## Del 1 — Metoder, hårdvara och kostnader


*Sammanställd 2026-11-06. Bygger vidare på diskussionen om phased-array/"digital
kombinering av signaler" på mark-RX-sidan. Förklarar principerna, de olika
behandlingsmetoderna och vad varje metod kräver av hårdvara + vad det kostar.*

---

### 1. Vad är digital beamforming? (kort)

**Digital beamforming = att ta emot signalen på FLERA antenner, digitalisera varje
signal för sig, och i mjukvara väga + få ihop dem så att man får en "fingrad, styrbar
stråle" — eller lägger nollor på störare — utan att flytta antennen fysiskt.**

Till skillnad från en enda yagi/dish (som fysiskt pekas av en gimbal) ger beamforming
**elektronisk styrning**: du "rör" strålen genom att ändra komplexa vikter i programmet,
inte genom att vrida en motor. Effekten: du kan scan-svep, följa ett mål, eller
undertrycka störningar — allt i realtid.

**Nyckelvillkor: koherens.** Alla element måste sampla *samtidigt med samma klocka/
fase-referens*. Annars summerar signalerna inte som tänkt.

---

### 2. Signalen i en array — vad "kombinera" egentligen betyder

Tänk dig en radiovåg som kommer in från riktning med våglängd λ. När våglängden når varje
element i en rad (avstånd `d` mellan element) färdas den en **lite olika sträcka** → den
når elementen vid **olika fas**:

```
   våg kommer från ~här (riktning θ)
                    ↓
      o      o      o      o
   elem1   elem2   elem3   elem4   (rad, avstånd d)
```

Fasskillnaden mellan två grannar = `2π · d · sin(θ) / λ`.

- För att **samla signalen** mot riktning θ tar du varje elements signal och lägger på
  en **motriktad fasjustering** så alla "hamnar i takt", sedan **summerar**.
- Den komplexa vikt per element = `wₙ = aₙ · e^(−j·2π·n·d·sinθ/λ)`
  (`aₙ` = amplitud, `e^(…)` = fasjustering).

Resultatet av summan kallar man **array-faktorn**. Genom att ändra sättet du väljer `wₙ`
får du olika "mottagningsmönster" — smalare stråle, nollor i bestämda riktningar, osv.

---

### 3. De olika metoderna (från enkel → avancerad)

#### Metod A — Delay-and-sum (lättaste, grundläggande)
- Justera deformationsfas per element så alla riktas mot θ, summera.
- **Vad den gör:** en styrbar stråle mot en riktning. Ingen dokument.
- **När: lokal far**: att elektroniskt peka mot burken / svepa för att hitta signalens
  topp (som en "elektronisk RSSI-peak").
- **Kostnad/krav:** kan göras med en enkel fas-styrbar mottagare; behöver tillräcklig fas-
  synk, men ingen tung DSP.
- **Resultat:** du får **+10·log10(N) dB** koherent vinst (4 elem → +6 dB; 8 → +9 dB).

#### Metod B — Null-steering (undertrycka störning)
- Lägg vikter så att array-faktorn har **nollor (nulls)** mot en eller flera störa-källor
  (t.ex. en annan sändare, en stark reflektion från marken).
- **När:** mark-RX i ett brusigt/störande läge — ta bort en störkälla som annars skulle
  förstöra burk-signalen.
- **Krav:** fler element än antalet nollor + mål (så att antal frihetsgrader räcker).
- **Resultat:** bättre SNR i brusig miljö — liknar det du annars försöker lösa med
  manuell antennval.

#### Metod C — Capon / MPMV (MVDR) — optimal stråle
- Minst signaleffekt från alla riktningar utom målet samtidigt som man behåller
  målet. "Optimal" viktbaserad på den observerade störmatrisen (ko-varianset).
- **När:** avancerad, högre SNR, adaptiv mot förändrad störning i realtid.
- **Krav:** matrisinvertering i DSP, fler kanaler ger bättre resultat.

#### Metod D — MUSIC / riktningsskattning (DoA-estimering)
- Gissar **varifrån** signalen kommer genom att analysera egenvärden/egenvärdesrummet av
  den mottagna kovariansen.
- **När:** vill man **skatta burkens riktning** (elev/azimut) direkt från signalen —
  dubbel nytta: peka strålen OCH få en riktning utan GPS.
- **Krav:** behöver **fler element än källorna** (typ ~8 för stabil estimaering) och
  gedigen kalibrering av fasen mellan kanalerna.

| Metod | Komplexitet | Data att beräkna | När använda |
|---|---|---|---|
| Delay-and-sum | låg | fas-vikter + summering | hitta/styra mot mål |
| Null-steering | låg–med | vikter med nollorna | ta bort störkälla |
| Capon (MVDR) | medel | matrisinvers av kovarians | adaptiv, högre SNR |
| MUSIC / DoA | hög | egenvärdesanalys | skatta riktning |

---

### 4. Hårdvaruarkitektur (vilka delar som alltid krävs)

Oavsett metod behövs samma grundskalade kedja:

```
 N antenner → N lågbrusförstärkare (LNA) → N mottagningskanaler → (analog nedkonvertering)
   → koherent ADC (flera kanaler, delad klocka) → DSP-host → resultat (stråle/riktning)
```

| Block | Vad det gör | Spec/kommentar för er (868 MHz) |
|---|---|---|
| **N antenner** | fånga signalen per element | N yagi/patch/omni i rad; avstånd `d` bestämmer strålbredd & styrning (se §2) |
| **N LNA** | förstärka svag signal innan ADC | en per element, lågt brus |
| **N mottagningskanaler** | nedkonvertera till basband/IQ | en per element |
| **Koherent ADC / flerkanalsradios** | digitalisera alla kanaler med samlad tid | **delad LO + delad klocka/fas-referens** — minst krav |
| **DSP-host** | beräkna vikter + summering | PC/GNU Radio / MATLAB / Python |

**Det svåraste kravet är alltså inte mjukvaran, utan att få flera mottagarkanaler
fas-koherenta.** Det styr i praktiken vad som är billigt vs dyrt (nästa avsnitt).

---

### 5. Hårdvara per metod + kostnader (ärligt)

> Kostnaderna är ungefärliga EU-priser 2026 och **exkluderar** den antenn/lina som ni
> redan eventuellt har. För varje steg anger jag om det passar en skol-budget (≤500 €).

#### Nivå 1 — Billig "mjukvara-lösning" som INTE ger riktig beamforming (varnar)
| Del | Kostnad | Problem |
|---|---|---|
| 2–4 × RTL-SDR / HackRF | ~20–40 €/st | **Inte fas-koherenta** (egen oscillator varje) → kan visa *signal-nivå per antenn*, men kan inte summera koherent / göra stråle. NB: bara för demonstration av RSSI per element. |

> ⚠️ Vanlig fälla: man köper flera billiga SDR:er och tror det ger beamforming. Det gör
> det bevisligen inte p.g.a. avsaknad av fas-synk. Använd dessa bara för att logga
> RSSI/riktningsgrova värden per enhet.

#### Nivå 2 — Fas-koherent flerkanals-SDR (riktig beamforming, delay-and-sum/null)
| Del | Kostnad | Krav |
|---|---|---|
| Flerkanalig koherent SDR (t.ex. USRP N300/N310, eller liknande 2–4-kanalsmottagare med delad LO) | **~1500–4000 €** | Delad klocka; 2–4 kanaler |
| 2–4 LNA + RF-kedja | ~50–200 € | lågt brus |
| DSP-host + GNU Radio/MATLAB | ~0 (befintlig PC) | — |
| **Totalt Nivå 2** | **~1600–4200 €** | — |

#### Nivå 3 — Billigare koherent OEM-radio / utvecklingskort (kreativ väg)
| Del | Kostnad | Krav |
|---|---|---|
| Ett utvecklingskort med ≥2 RX-kanaler + delad klocka (t.ex. ett AD936x-kort, flera AD9361 synkade) | ~300–1000 € | kräver egen synk. design/loop |
| 1 extern 10 MHz-referens + splitt till varje RF-kort | ~50–150 € | fas-synk via gemensam referens |
| Flera LoRa/SDR-moduler synkade via referens | ~100–400 € | svårt men billigare |
| **Totalt Nivå 3** | **~450–1500 €** | mest arbete, men vägen under 500 € är svår |

#### Nivå 4 — Riktig MUSIC/DoA + många element (bäst resultat, dyrast)
- 8 element rad, 8-kanalig koherent SDR, kraftig host, kalibreringsmodul.
- Kostnad: **~5000–15000 €+** — långt över skolbudget, snarare en labbedemo.

---

### 6. Konkret tabell: metod → minsta N → hårdvara → ungefärlig kostnad

| Metod | Min N | Hårdvara som behövs | Kostnad (din budget?) |
|---|---|---|---|
| **RSSI per element (inte beamforming)** | 2–4 | 2–4 × RTL-SDR (osynkad) | ~50–150 € ✅ billigt, men ger ingen stråle |
| **Delay-and-sum (enkel stråle)** | 2–4 | koherent 2–4-kanals SDR | ~1600–4000 € ❌ över 500 |
| **Null-steering** | 3–4 | koherent SDR | ~1600–4000 € ❌ |
| **Capon/MVDR** | 4–6 | koherent SDR | ~2000–5000 € ❌ |
| **MUSIC / DoA (riktning)** | ~8 | 6–8-kanal koherent SDR | ~5000–15000 € ❌ |

**Slutsats för er:** en **riktig digital beamforming-demo kräver en fas-koherent
flerkanalsmottagare på 1500 €+** — klart över 500 €-taket. Det som *går* inom budget är
bara "RSSI per element" (flera billiga SDR:er), men det ger inte stråle/null.

---

### 7. Realistiska sätt att jobba med konceptet på skolbudget

1. **Simulera i mjukvara (gratis, stor pedagogisk vinst):** skapa vågdata i MATLAB/Python/
   GNU Radio och kör delay-and-sum, Capon, MUSIC på *simulerade* arrayer. Man förstår hela
   beamforming-principen utan hårdvara. → **rekommenderat första steg.**
2. **Hårdvara för RSSI-per-element** med billiga SDR:er → logga signalstyrka på varje
   antenn och gör en **grov vinkelskattning** (triangulera riktning via olika RSSI-nivåer)
   — billigt, men inte riktig stråle.
3. **Fas-koherent mini-DUO:** ett enda utvecklingskort med **2 koherenta RX-kanaler** + en
   gemensam referens ger en *2-element* demo (enkel null/delay-and-sum) → billigaste vägen
   till ÄKTA beamforming men ändå 500–1500 € och mycket byggsata.

> För tävlingen 2027: **håll gimbal + yagi/dish (868/2,4 GHz) som bärlinjen** och behandla
> digital beamforming som **simulerings-/outreach-demo**. Lovande och utmanande framtid
> som passar i teknik/outreach-poäng utan att riskera missionen.

---

### 8. Källförteckning (bakgrund)

- [Matlab/Phased Array System Toolbox — delay-and-sum / Capon / MUSIC](https://www.mathworks.com/help/phased/index.html)
- [GNU Radio — mjukvarudefinierat radio (beamforming i Python/flödesgrafer)](https://www.gnuradio.org/)
- USRP/Ettus flerkanaliga koherenta SDR:er (fas-koherenta, delad LO) — officiell hårdvara för SDR-arrayer.
- IEEE-standarder MIMO/phased arrays (översiktsartiklar, se bibliotek).

---

*Levande dokument. Uppdateras om ni byter metod eller bestämmer hårdvara. Siffrorna är
uppskattningar — verifiera priser mot leverantör innan köp.*

---

## Del 2 — Matematiken (styrvektor, arrayfaktor, Capon, MUSIC)


*Skriven 2026-11-06. Detaljerad, lärande inriktad genomgång av digital beamforming.
Kompletterar del 1 i denna fil (metodöversikt, hårdvara,
kostnader) med den matematiska kärnan. Formlerna är skrivna i LaTeX och renderas i
Markdown-läsare som stöder `$…$` / `$$…$$`.*

---

### 0. Notation

| Symbol | Betydelse |
|---|---|
| $f$ | frekvens (Hz) |
| $\omega = 2\pi f$ | vinkelfrekvens (rad/s) |
| $\lambda = c/f$ | våglängd (m) |
| $k = 2\pi/\lambda$ | vågtal / spatial frekvens (rad/m) |
| $N$ | antal antennelement |
| $d$ | elementavstånd (m) |
| $\theta$ | infallsvinkel mot arrayens normal |
| $j$ | imaginärenheten, $j^2 = -1$ |
| $\mathbf{a}(\theta)$ | styrvektor (steering vector) |
| $\mathbf{w}$ | komplex viktvektor |
| $\mathbf{R}$ | kovariansmatris |
| $(\cdot)^{H}$ | konjugat-transponat (Hermitian) |

---

### 1. Vågen, vågtalet och fasskillnaden

Fasen hos en plan våg:

$$
\varphi(x,t) = \omega t - kx,
\qquad \omega = 2\pi f,
\qquad k = \frac{2\pi}{\lambda}.
$$

$k$ är den **spatiala frekvensen**: hur mycket fasen vrider sig per meter. Två punkter
med avståndet $d$ längs utbredningen får fasskillnaden

$$
\Delta\varphi = kd = \frac{2\pi d}{\lambda}.
$$

För en våg som infaller under vinkeln $\theta$ mot normalen projiceras avståndet till
$d\sin\theta$:

$$
\boxed{\Delta\varphi = k\,d\sin\theta = \frac{2\pi d \sin\theta}{\lambda}}
$$

---

### 2. Steering vector (styrvektor)

$$
\mathbf{a}(\theta) =
\begin{bmatrix}
1 \\
e^{jkd\sin\theta} \\
e^{j2kd\sin\theta} \\
\vdots \\
e^{j(N-1)kd\sin\theta}
\end{bmatrix}
\in \mathbb{C}^{N}
$$

Varje element innehåller den fasrotation elementet "ser" för en källa i riktningen
$\theta$. Med $e^{j\varphi} = \cos\varphi + j\sin\varphi$ (komplex rotator, amplitud 1)
bevaras både amplitud och fas.

---

### 3. Komplexa vikter och utsignalen

$$
w_n = A_n e^{j\phi_n},\quad n = 0,\dots,N-1
\qquad\Longrightarrow\qquad
y = \sum_{n=0}^{N-1} w_n x_n = \mathbf{w}^{H}\mathbf{x}
$$

$A_n$ = amplitudvikt, $\phi_n$ = fasvikt. Hermitian $\mathbf{w}^{H}$ "vänder" faserna så
att de summerar **i takt** (koherent).

---

### 4. Arrayfaktorn

$$
\mathrm{AF}(\theta) = \sum_{n=0}^{N-1} w_n e^{jnkd\sin\theta}
= \mathbf{w}^{H}\mathbf{a}(\theta)
$$

Att peka mot $\theta_0$ innebär $\mathbf{w} = \mathbf{a}(\theta_0)$:

$$
\mathrm{AF}(\theta_0) = \sum_{n=0}^{N-1} 1 = N .
$$

Sluten form för en ULA med likformiga vikter ($\psi = kd\sin\theta$):

$$
\mathrm{AF}(\theta) = \frac{\sin\!\left(\dfrac{N\psi}{2}\right)}
{\sin\!\left(\dfrac{\psi}{2}\right)}
$$

---

### 5. Koherens och koherent vinst

Delad **LO** + delad **klocka** ⇒ faserna är låsta ⇒ de $N$ signalerna adderar i fas.
Med amplitud $V$ per element:

$$
V_{\text{summa}} = NV
\qquad\Rightarrow\qquad
P \propto N^{2}V^{2}
$$

Den koherenta vinsten (jämfört med **ett** element):

$$
G_{\text{coh}} = 10\log_{10}N \ \text{dB}
$$

dvs. $+6$ dB för $N=4$ och $+9$ dB för $N=8$, utöver det enskilda elementets egen gain.

**Härledning — varför $10\log_{10}N$ och inte $20\log_{10}N$:** med *oberoende* brus i varje
kanal (eget LNA per element) adderar signalerna koherent men bruset okorrelerat:

$$
\text{SNR}_{\text{ut}}
= \frac{(NV_s)^2}{N\,V_n^2}
= N\cdot\frac{V_s^2}{V_n^2}
\;\;\Rightarrow\;\;
G = N
\;\;\Rightarrow\;\;
10\log_{10}N
$$

Samma resultat ger apertur-resonemanget: $N$ element ger $N$ gånger så stor effektiv
apertur, och direktiviteten skalar med aperturen.

> ⚠️ **$20\log_{10}N$ dyker upp först när total uteffekt också ökar $N$ gånger** (t.ex. en
> *sändar*-array där varje element matas med samma effekt som referensen). Det är inte
> fallet för vår mottagararray. Använd $10\log_{10}N$ i länkbudgeten.

**Utan koherens** (egen oscillator per kanal) blir fasfelen slumpmässiga och den
förväntade summan bara $\sqrt{N}\,V$ — ingen arrayvinst.

> **Verkligheten ger mindre än $10\log_{10}N$.** Vid $\lambda/2$-avstånd överlappar
> elementens effektiva aperturer ($A_e = G\lambda^2/4\pi$), och ömsesidig koppling
> förvränger mönstret. Med 4 riktade element är $+6$ dB därför ett **övre gränsvärde**;
> räkna realistiskt med $+3\ldots+5$ dB.

---

### 6. Mottagningskedjan: LNA → mixer → IQ → ADC

$$
\underbrace{x_{\text{RF}}(t)}_{\text{868 MHz}}
\;\xrightarrow{\ \text{LNA}\ }\;
\xrightarrow[\times\,e^{-j2\pi f_{\text{LO}}t}]{\ \text{mixer}\ }
\underbrace{I(t) + jQ(t)}_{\text{basband}}
\;\xrightarrow{\ \text{ADC}\ }\;
x_n[m]
$$

| Steg | Funktion | Nyckelbegrepp |
|---|---|---|
| **LNA** | första förstärkaren, nära antennen | lågt **brustal / noise figure**, hög gain före förluster |
| **Mixer** | multiplicerar med LO-tonen, flyttar till basband | nedkonvertering, bevarar fas |
| **IQ** | två 90°-förskjutna komponenter | bevarar **amplitud OCH fas** (krav för fasvikter) |
| **ADC** | digitaliserar | $f_s \ge 2B$ (**Nyquist**), **gemensam klocka** |

Fasbevarande verifiering: $x_{\text{RF}}(t) = A\cos(\omega t + \varphi)$ ger efter
nedkonvertering sampel med samma $\varphi$ — alltså ingen fasförlust.

---

### 7. Signalmodell

$$
\mathbf{x}[m] = \mathbf{a}(\theta_0)\,s[m] + \mathbf{n}[m]
$$

$s[m]$ = målets signal, $\mathbf{a}(\theta_0)$ = geometrisk fas, $\mathbf{n}[m]$ = brus
(LNA + omgivning). Beamforming = att skatta/dra nytta av $\theta_0$.

---

### 8. Delay-and-sum

$$
\boxed{y(\theta) = \mathbf{a}^{H}(\theta)\,\mathbf{x}}
$$

Ett **matchat filter** mot styrvektorn: multiplicera inkommande signal med
konjugatet av $\mathbf{a}(\theta)$ och summera. Enkelt, robust, ingen statistik krävs.

---

### 9. Kovariansmatrisen

$$
\mathbf{R} = \mathbb{E}\!\left[\mathbf{x}\mathbf{x}^{H}\right]
\approx \frac{1}{M}\sum_{m=1}^{M}\mathbf{x}[m]\mathbf{x}^{H}[m]
\in \mathbb{C}^{N\times N}
$$

Bär all spatiell statistik (mål + störare + brus). Hermitisk, positivt semidefinit.

---

### 10. Capon / MVDR (Minimum Variance Distortionless Response)

$$
\boxed{\mathbf{w}(\theta) =
\frac{\mathbf{R}^{-1}\mathbf{a}(\theta)}
{\mathbf{a}^{H}(\theta)\mathbf{R}^{-1}\mathbf{a}(\theta)}}
$$

Villkoret $\mathbf{w}^{H}\mathbf{a}(\theta)=1$ (distortionless mot målet) under minimering
av uteffekten $\mathbf{w}^{H}\mathbf{R}\mathbf{w}$. Ger **automatiska nollor** mot starka
störare. Kräver matrisinvers i realtid → mer DSP, fler element ger bättre resultat.

---

### 11. MUSIC (DoA-skattning)

Egenvärdesuppdelning med $K$ källor och $N$ element ($K<N$):

$$
\mathbf{R} = \mathbf{U}\boldsymbol{\Lambda}\mathbf{U}^{H},
\qquad
\mathbf{U} = \big[\underbrace{\mathbf{E}_s}_{K\ \text{kolumner}}\ \;
\underbrace{\mathbf{E}_n}_{N-K\ \text{kolumner}}\big]
$$

Brus-rymden $\mathbf{E}_n$ är ortogonal mot källornas styrvektorer. Spektrumet:

$$
\boxed{P_{\text{MUSIC}}(\theta) =
\frac{1}{\mathbf{a}^{H}(\theta)\,\mathbf{E}_n\mathbf{E}_n^{H}\,\mathbf{a}(\theta)}}
$$

Skarpa toppar vid källvinklarna. Kravet $N>K$ kommer av att $\dim\mathbf{E}_n = N-K$
måste vara positivt — därav "~8 element för stabil estimering".

---

### 12. Nollstyrning (null-steering)

Linjärt villkor:

$$
\mathbf{w}^{H}\mathbf{a}(\theta_{\text{mål}}) = 1,
\qquad
\mathbf{w}^{H}\mathbf{a}(\theta_{\text{stör}k}) = 0 \quad \forall k
$$

Varje nolla förbrukar en frihetsgrad ⇒ högst $N-1$ nollor utöver att behålla målet.

---

### 13. Strålbredd, apertur och grating lobes

**Apertur:** $L = (N-1)d$. Halveffektbredd (HPBW) för ULA:

$$
\text{HPBW} \approx \frac{0.886\,\lambda}{N d\cos\theta_0}\ \text{rad}
$$

**Grating lobes** undviks om

$$
\boxed{d \le \frac{\lambda}{2}}
$$

(då är mönstret entydigt för $|\theta|\le 90^\circ$). Amplitud-tapering (Hamming, Taylor)
sänker **sidelobes** men breddar huvudloben något. Vid stora styrvinklar minskar effektiv
apertur som $\cos\theta_0$ ⇒ **beam broadening**.

---

### 14. Allt ihop — varför villkoren ser ut som de gör

$$
\underbrace{d \le \lambda/2}_{\text{ingen grating lobe}}
\qquad
\underbrace{\text{delad LO + klocka}}_{\text{koherens}}
\qquad
\underbrace{\mathbf{w} = \mathbf{a}(\theta_0)}_{\text{pekning}}
\qquad
\underbrace{N \text{ stor}}_{\text{smal stråle, hög vinst}}
$$

---

### 15. Siffror för 868 MHz

$$
\lambda = \frac{c}{f} = \frac{3{,}00\cdot10^{8}}{868\cdot10^{6}}
\approx 0{,}346\ \text{m} = 34{,}6\ \text{cm}
$$

$$
\frac{\lambda}{2} \approx 17{,}3\ \text{cm},
\qquad
\frac{\lambda}{4} \approx 8{,}6\ \text{cm}
$$

| Apertur $L$ | $d$ | HPBW ($\theta_0{=}0$) | Styrbarhet | Grating lobes |
|---|---|---|---|---|
| 24 cm | $\approx 8$ cm ($\lambda/4$) | $\approx 62^\circ$ | bred ($\pm 60$–$70^\circ$) | nej |
| 52 cm | $\approx 17$ cm ($\lambda/2$) | $\approx 29^\circ$ | måttlig ($\pm 30$–$40^\circ$) | nej |
| valfri | $d > \lambda/2$ | smalast | begränsad | **ja** |

**Avvägningen:** stor apertur → smal stråle (bra upplösning, sämre svep); liten apertur
($\lambda/4$) → bred stråle men bred, ren styrning utan lober.

---

### 16. Referenser

- [MathWorks — Phased Array System Toolbox (delay-and-sum, Capon, MUSIC)](https://www.mathworks.com/help/phased/index.html)
- [GNU Radio — mjukvarudefinierad radio](https://www.gnuradio.org/)
- Van Loan, *Computational Frameworks for the Fast Fourier Transform* (FFT/array-bakgrund)
- Trees, *Optimum Array Processing* (Capon/MVDR, MUSIC, arrayteori)
- Balanis, *Antenna Theory* (apertur, strålbredd, grating lobes)

---

*Levande dokument. Utöka med härledningar när ni väljer metod. Se även
del 1 i denna fil för hårdvara och kostnader per metod.*

---

## Se även

- [FASVAXLARE.md](FASVAXLARE.md) — konkreta fasväxlare för 868 MHz och 2,4 GHz
- [PROTOKOLL.md](PROTOKOLL.md) — vilket band och protokoll arrayen ska byggas för
- [KOMMUNIKATION.md](KOMMUNIKATION.md) — länkbudgeten som arrayen ska förbättra
- [GIMBAL.md](GIMBAL.md) — mekanisk pekning, alternativet till elektronisk
