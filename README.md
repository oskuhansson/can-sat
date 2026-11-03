# can-sat-cloud-chamber

CanSat-uppdrag: **enkel monopol-antenn i burken** (nedlänk-beacon) + **markbaserad
hög-gain-antenn på gimbal** som följer burken. Allt som är svårt (gain, pekning) ligger
på marken; burken förblir minimal och robust med gott om plats för sensorer.

## Dokumentation

- **WIFI-FORSKNING.md** — huvudöversikt: [monopol-antenn i burken + high-gain-gimbal på marken (link budget, antennval, regler, begrepp — §12.10–12.11)](WIFI-FORSKNING.md)
- **RADIOTEKNIK.md** — [radioteknik-snabbkurs (SNR, Eb/N₀, modulering, LoRa vs WiFi, ESP-NOW)](RADIOTEKNIK.md)
- **FORSKNING.md** — äldre cloud chamber-forskning arkiverad (ej i fokus längre)

## Status

- [x] Forskning: monopol i burken + markgimbal (hög-gain-antenn) — allt svårt på marken; 60–75 dB marginal på 868 MHz; inget i burken som kan peka fel
- [x] Forskning: GPS-spårning + LoRa-backup för gimbalens pekning (dish blir då möjlig)
- [ ] Kontakta arrangören (antennregler, frekvensplan, Pre-Launch Report 20.2.2027)
- [ ] Prototyp: LoRa-beacon + markgimbal-tracker (RSSI + GPS-följning)
- [ ] Kapsla in i CanSat-burk (115 mm × 66 mm, 300–350 g)
