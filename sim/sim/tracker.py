"""Trackern: vad gimbalen ska sikta på.

Tre lägen, och övergångarna mellan dem är själva poängen med simuleringen:

* **acquire** — innan låsning sveper gimbalen himlen. Utan GPS finns ingen
  riktning att räkna på, så antennen måste leta. Pekfelet är då vinkeln mellan
  sveppositionen och sändaren, vilket nästan alltid är stort.
* **gps** — sändarens position finns i telemetrin. Trackern räknar om den till
  azimut/elevation med samma geometri som sanningen, men från en **brusig**
  position. Felet blir därför automatiskt stort på nära håll och litet på långt
  håll — precis som i verkligheten.
* **rssi** — ingen GPS. Trackern följer RSSI-toppen med en noggrannhet som är en
  bråkdel av strålbredden.

Två olika RSSI-noggrannheter används med flit. En **sökning** över hela himlen
kan bara skilja ut ungefär en tiondel av strålbredden. En **finjustering** kring
en topp man redan hittat — vilket är vad som sker när GPS:en gett riktningen —
löser mycket bättre, ungefär en femtiondel. Att använda sökningens noggrannhet
också för finjusteringen gör GPS-läget orimligt dåligt: 4,8° jitter på en 48°-lob
förvandlar ett pekfel på 0,3° till 2,1°.

Läget **hold** inträder när signalen försvinner: en RSSI-följare kan inte
toppjaga något den inte hör. Då hålls den senaste vinkeln, och felet växer i takt
med att sändaren rör sig.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .config import TrackerConfig
from .geometry import az_el_range, pointing_error_deg


@dataclass
class TrackerOutput:
    az_deg: float
    el_deg: float
    phase: str
    gps_used: bool


class Tracker:
    def __init__(
        self,
        cfg: TrackerConfig,
        beamwidth_deg: float,
        station_position: tuple[float, float, float],
        rng: np.random.Generator,
        airtime_s: float = 0.0,
    ):
        self.cfg = cfg
        self.station = station_position
        self.rng = rng
        self.beamwidth = beamwidth_deg
        self.electronic = cfg.scan_mode == "electronic"

        # Sökning respektive finjustering har olika noggrannhet.
        search_sigma = (
            cfg.rssi_fine_sigma_deg
            if cfg.rssi_fine_sigma_deg is not None
            else max(0.3, beamwidth_deg / 10.0)
        )
        self.rssi_sigma_search = search_sigma
        self.rssi_sigma_fine = max(0.2, search_sigma / 5.0)

        # Tiden man måste stå still i varje strålposition.
        #
        # Mekaniskt: gimbalens dwell, som är en mekanisk tidskonstant.
        # Elektroniskt: strålen flyttas på mikrosekunder, men för att UPPTÄCKA
        # sändaren måste man lyssna minst ett helt paket i riktningen. Därför
        # max(switch_time, lufttid) — och därför är elektronisk svepning snabb
        # men inte momentan. Det är hela poängen att simulera.
        self.scan_dwell_s = (
            max(cfg.switch_time_s, airtime_s) if self.electronic else cfg.scan_dwell_s
        )

        # Svepet: azimuten varv runt, sedan nästa elevation.
        self.n_az = max(1, math.ceil(360.0 / beamwidth_deg))
        self.n_el = max(1, math.ceil(90.0 / beamwidth_deg))
        self.scan_time_s = self.n_az * self.n_el * self.scan_dwell_s

        self.lock_time_s: float = math.nan
        self._rssi_offset = 0.0
        self._rssi_rho = 0.9
        self._held: tuple[float, float] | None = None

    # ------------------------------------------------------------------
    def _sweep_position(self, t_s: float) -> tuple[float, float]:
        """Var antennen står i svepet vid tiden t.

        Azimuten stegar ett steg per dwell och går varv runt innan elevationen
        höjs ett steg. Sekvensen är deterministisk — samma seed ska ge samma
        svep. Sekvensen är identisk för mekanisk och elektronisk svepning; det är
        bara dwellen som skiljer, eftersom arrayen har samma strålbredd och
        därför samma antal positioner.
        """
        dwell = max(1e-6, self.scan_dwell_s)
        total = self.n_az * self.n_el
        step = int(t_s / dwell) % total

        # Azimuten stegar varv runt; elevationen delas jamnt mellan 0 och 90
        # grader. Att stega elevationen med straalbredden lamnar ett glapp mot
        # zenit: med tva rader hamnar de pa 0 och 48 grader, och en sandare i
        # zenit syns da aldrig i huvudloben. Raster med jamn fordelning tacker
        # alltid himlen, aven nar straalbredden inte gar jamnt upp i 90.
        az = (step % self.n_az) * (360.0 / self.n_az)
        row = step // self.n_az
        el = 45.0 if self.n_el == 1 else 90.0 * row / (self.n_el - 1)
        return az, el

    def _drift(self, sigma: float) -> float:
        innovation = float(self.rng.normal(0.0, sigma))
        self._rssi_offset = (
            self._rssi_rho * self._rssi_offset
            + math.sqrt(1.0 - self._rssi_rho**2) * innovation
        )
        return self._rssi_offset

    def _gps_position(self, true_pos: tuple[float, float, float]) -> tuple[float, float, float]:
        sx = float(self.rng.normal(0.0, self.cfg.gps_horizontal_sigma_m))
        sy = float(self.rng.normal(0.0, self.cfg.gps_horizontal_sigma_m))
        sz = float(self.rng.normal(0.0, self.cfg.gps_vertical_sigma_m))
        return (true_pos[0] + sx, true_pos[1] + sy, true_pos[2] + sz)

    # ------------------------------------------------------------------
    def command(
        self,
        t_s: float,
        true_pos: tuple[float, float, float],
        signal_ok: bool = True,
    ) -> TrackerOutput:
        """Vilken azimut/elevation gimbalen ska styras mot vid tiden t."""
        cfg = self.cfg
        true_az, true_el, _ = az_el_range(self.station, true_pos)

        # 0. Digital array med flera mottagarkedjor lyssnar i alla riktningar
        #    samtidigt. Då finns riktningen från första stunden och det finns
        #    ingen acquisitionsfas alls — låsningstiden blir noll. Det är den
        #    undre gränsen, inte ett system i den här budgeten.
        if cfg.simultaneous_beams and math.isnan(self.lock_time_s):
            self.lock_time_s = t_s

        # 1. Har vi GPS? Då är riktningen känd så fort första paketet kommit.
        gps_active = cfg.gps_available and (
            cfg.gps_dropout_after_s is None or t_s < cfg.gps_dropout_after_s
        )
        if gps_active and t_s >= cfg.lock_delay_s:
            if math.isnan(self.lock_time_s):
                self.lock_time_s = t_s
            noisy = self._gps_position(true_pos)
            az, el, _ = az_el_range(self.station, noisy)
            fine = self._drift(self.rssi_sigma_fine) * 0.5
            self._held = (az + fine, el + fine)
            return TrackerOutput(az + fine, el + fine, "gps", True)

        # 2. Utan GPS: svep tills strålen träffar. Låsningen sker när antennens
        #    riktning ligger inom en halv strålbredd från sändaren — det är då
        #    länken bär, oavsett om ett paket råkade avkodas just då.
        if math.isnan(self.lock_time_s):
            az_sweep, el_sweep = self._sweep_position(t_s)
            error = pointing_error_deg(az_sweep, el_sweep, true_az, true_el)
            if error <= self.beamwidth / 2.0:
                self.lock_time_s = t_s
            else:
                return TrackerOutput(az_sweep, el_sweep, "acquire", False)

        # 3. Låst utan GPS: följ RSSI-toppen, men bara om signalen hörs.
        if not signal_ok and self._held is not None:
            az, el = self._held
            return TrackerOutput(az, el, "hold", False)

        offset = self._drift(self.rssi_sigma_search)
        az = true_az + offset
        el = true_el + offset * 0.5
        self._held = (az, el)
        return TrackerOutput(az, el, "rssi", False)
