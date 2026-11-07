---
tags: [cansat, regler, traficom, juridik]
status: aktuell
updated: 2026-11-07
---

# Regler och gränser — vad som är tillåtet i Finland

*Utdraget ur [KOMMUNIKATION.md](KOMMUNIKATION.md) 2026-11-07. Det här är det en
bedömare eller arrangör oftast frågar om — håll det separat och verifierat.*

**Kort svar: både upplänk och nedlänk är tillåtna i Finland** på de licensfria
banden. Reglerna begränsar **effekt och sändningstid**, inte rätten att sända.

---


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


---

## Snabbtabell

| Band | Max strålad effekt | Duty cycle | Luftanvändning |
|---|---|---|---|
| 868 MHz (868,0–868,6) | 25 mW e.r.p. | ≤ 1 % | ✅ tillåten |
| 868 MHz (869,4–869,65) | 500 mW e.r.p. | ≤ 10 % | ✅ tillåten |
| 2,4 GHz WLAN | 100 mW EIRP (20 dBm) | ingen gräns | ✅ tillåten |

## Att verifiera före Pre-Launch Report (20.2.2027)

- [ ] Att våra CE-moduler + antenner håller EIRP-taket **tillsammans**
- [ ] Att ingen förstärkare sitter mellan sändare och antenn
- [ ] Att duty cycle för 868 MHz räknas korrekt i firmware
- [ ] Att frekvensplanen är rapporterad till arrangören

---

## Se även

- [KOMMUNIKATION.md](KOMMUNIKATION.md) — systemdesignen som reglerna begränsar
- [QA.md](QA.md) — Del B: faktakontroll av just de här siffrorna
- [PROTOKOLL.md](PROTOKOLL.md) — 2,4 GHz har ingen duty-cycle-gräns, 868 har 1 %
