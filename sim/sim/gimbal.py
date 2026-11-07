"""Gimbalen: svepgräns, glapp och upplösning.

Modellen har två lager, och det är skillnaden mellan dem som gör att den är värd
att ha:

* **Motorn** rör sig mot målvinkeln så fort den orkar, men aldrig fortare än
  svephastigheten. Det är eftersläpningen: en gimbal som svänger 360 grader på
  30 grader/s hinner inte med en sändare som far över himlen.
* **Antennen** sitter efter en växellåda med glapp. När motorn vänder måste den
  först ta upp spelet innan antennen rör sig alls. Det syns som ett dödband på
  `backlash_deg` och gör att små korrigeringar aldrig når fram.

Ordningen är medveten: svep -> glapp -> kvantisering. Kvantiseringen ligger sist
eftersom det är antennens faktiska vinkel som blir stegad.
"""

from __future__ import annotations

import math

from .config import GimbalConfig


def wrap_angle_deg(angle_deg: float) -> float:
    """Normalisera till [0, 360)."""
    return angle_deg % 360.0


def angular_difference_deg(from_deg: float, to_deg: float) -> float:
    """Kortaste vinkeln från `from` till `to`, i intervallet (-180, 180].

    Utan det här tar gimbalen omvägen över fel håll när målet passerar norr.
    """
    return (to_deg - from_deg + 180.0) % 360.0 - 180.0


class Gimbal:
    """Tvåaxlig gimbal med svepgräns, glapp och stegupplösning."""

    def __init__(self, cfg: GimbalConfig, initial_az_deg: float = 0.0, initial_el_deg: float = 45.0):
        self.cfg = cfg
        self.motor_az = wrap_angle_deg(initial_az_deg)
        self.motor_el = self._clamp_el(initial_el_deg)
        # Antennen börjar i samma läge som motorn — glappet är tomt från start.
        self.az = self.motor_az
        self.el = self.motor_el

    # -- hjälpare ----------------------------------------------------------
    def _clamp_el(self, el_deg: float) -> float:
        return max(self.cfg.min_elevation_deg, min(self.cfg.max_elevation_deg, el_deg))

    def _quantise(self, value_deg: float) -> float:
        res = self.cfg.resolution_deg
        if res <= 0:
            return value_deg
        return round(value_deg / res) * res

    # -- steg --------------------------------------------------------------
    def step(self, dt_s: float, target_az_deg: float, target_el_deg: float) -> tuple[float, float]:
        """Flytta gimbalen ett tidssteg mot målet. Returnerar (az, el) i grader."""
        if dt_s <= 0:
            return self.az, self.el

        # 1. Svepgräns. Motorn går mot målet, men högst rate*dt.
        max_az_step = self.cfg.az_slew_deg_per_s * dt_s
        max_el_step = self.cfg.el_slew_deg_per_s * dt_s

        az_delta = angular_difference_deg(self.motor_az, target_az_deg)
        self.motor_az = wrap_angle_deg(
            self.motor_az + max(-max_az_step, min(max_az_step, az_delta))
        )

        el_delta = target_el_deg - self.motor_el
        self.motor_el = self._clamp_el(
            self.motor_el + max(-max_el_step, min(max_el_step, el_delta))
        )

        # 2. Glapp. Antennen följer motorn genom ett dödband på backlash_deg.
        #    Är skillnaden mindre än halva spelet händer ingenting alls — det är
        #    därför en gimbal kan stå stilla trots att styrsignalen ändras.
        half = max(0.0, self.cfg.backlash_deg) / 2.0
        if half > 0:
            az_gap = angular_difference_deg(self.az, self.motor_az)
            if az_gap > half:
                self.az = wrap_angle_deg(self.az + (az_gap - half))
            elif az_gap < -half:
                self.az = wrap_angle_deg(self.az + (az_gap + half))

            el_gap = self.motor_el - self.el
            if el_gap > half:
                self.el = self.el + (el_gap - half)
            elif el_gap < -half:
                self.el = self.el + (el_gap + half)
        else:
            self.az = self.motor_az
            self.el = self.motor_el

        # 3. Upplösning — stegmotorns eller enkoderens minsta steg.
        self.az = wrap_angle_deg(self._quantise(self.az))
        self.el = self._quantise(self._clamp_el(self.el))

        return self.az, self.el


def scan_duration_s(beamwidth_deg: float, dwell_s: float, elevation_span_deg: float = 90.0) -> float:
    """Hur lång tid ett fullt svep av himlen tar med en given strålbredd.

    Antalet strålpositioner är (360/theta) * (span/theta): man måste täcka
    azimuten varv runt och elevationen från horisont till zenith, och varje
    position måste överlappa grannen för att inte missa sändaren mellan två
    strålar.

    Det här är den enda platsen i simuleringen där en smal stråle är *sämre* på
    ett sätt som inte syns i pekförlusten: en 48,4-graderslob behöver ~14
    positioner för att täcka himlen, en 17,5-graderslob ~106. Med 0,4 s per
    position blir det 6 s mot 42 s — och flygningen varar bara ~110 s.
    """
    bw = max(1.0, beamwidth_deg)
    positions = math.ceil(360.0 / bw) * max(1, math.ceil(elevation_span_deg / bw))
    return positions * dwell_s
