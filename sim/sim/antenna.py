"""Antennmönster: förstärkning som funktion av vinkeln från bomriktningen.

Alla modeller tar **en** vinkel: hur många grader pekar antennen fel. Det är
avsiktligt. En gimbal har två axlar, men antennen bryr sig bara om vinkeln mellan
där den pekar och där sändaren är — och den vinkeln räknas ut i geometry.py.

Pekförlusten i projektet skrivs `L = 12(θ/θ3dB)²`, vilket är exakt `gaussian`-
modellen nedan. Att de två stämmer är inte en slump: 12 dB-faktorn är den
paraboliska approximation som brukar användas för huvudloben.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np

from .config import AntennaConfig, ConfigError
from .geometry import direction_cosines, pointing_error_deg

# Standardnivå för sidolober när inget annat anges, relativt toppen.
DEFAULT_SIDELOBE_DB = -20.0
DEFAULT_BACKLOBE_DB = -25.0

# Strålbredd för ett enskilt arrayelement när scenariofilen inte anger någon.
# 70 grader är en typisk patch på jordplan.
DEFAULT_ELEMENT_BEAMWIDTH_DEG = 70.0

# Strålbredd för patch-elementet i hybriden. En 8 dBi-patch på jordplan ligger
# typiskt på 60-70 grader; 65 är mittpunkten och den siffra projektets
# scanförlusträkning utgår från (12*(45/65)^2 = 5,8 dB vid ±45 graders styrning).
DEFAULT_HYBRID_ELEMENT_BEAMWIDTH_DEG = 65.0


class AntennaPattern:
    """Ett mönster: mata in pekfel i grader, få förstärkning i dBi.

    Mönstret har två vägar, och den ena är ny:

    * `gain_dbi(off_angle)` — den ursprungliga. Räcker för varje antenn vars
      förstärkning bara beror på hur många grader fel den pekar.
    * `gain_towards(az, el, az_aim, el_aim)` — matar in **två** riktningar. Bara
      arrayen behöver den, eftersom en arrayfaktor beror på var i (u, v) felet
      ligger, inte bara hur stort det är. Kvantiseringens sidolober och grating
      lobes går inte att uttrycka som en funktion av en enda vinkel.

    Motorn anropar alltid `gain_towards`. För alla modeller utom arrayen räknar
    den om till samma vinkel och anropar `gain_dbi` — alltså exakt samma kodväg
    som före tillägget, vilket är skälet att de befintliga scenarierna ger
    oförändrade siffror.
    """

    def __init__(
        self,
        cfg: AntennaConfig,
        gain_fn: Callable[[float], float],
        beamwidth_deg: float,
        gain_fn_2d: Callable[[float, float, float, float], float] | None = None,
    ):
        self.cfg = cfg
        self.model = cfg.model
        self.peak_gain_dbi = cfg.peak_gain_dbi
        self.beamwidth_3db_deg = beamwidth_deg
        self._gain_fn = gain_fn
        self._gain_fn_2d = gain_fn_2d

    @property
    def is_2d(self) -> bool:
        """Sant om mönstret kräver två riktningar (array och hybrid)."""
        return self._gain_fn_2d is not None

    def gain_dbi(self, off_angle_deg: float) -> float:
        angle = abs(off_angle_deg)
        if self._gain_fn_2d is None:
            return float(self._gain_fn(angle))
        # Arrayen har ingen meningsfull 1D-väg: sidoloberna sitter i (u, v), inte
        # i vinkeln. Anropas den ändå används bredsidesvepet, som bara ger
        # huvudlobens form — motorn går alltid via gain_towards.
        return float(self._gain_fn_2d_from_angle(angle))

    def _gain_fn_2d_from_angle(self, off_angle_deg: float) -> float:
        u = math.sin(math.radians(off_angle_deg))
        return self._gain_fn_2d(u, 0.0, 0.0, 0.0)

    def gain_towards(
        self,
        az_true_deg: float,
        el_true_deg: float,
        az_aim_deg: float,
        el_aim_deg: float,
    ) -> float:
        """Förstärkning i den riktning sändaren faktiskt står, given var antennen pekar."""
        if self._gain_fn_2d is None:
            error = pointing_error_deg(az_true_deg, el_true_deg, az_aim_deg, el_aim_deg)
            return self.gain_dbi(error)
        u, v = direction_cosines(az_true_deg, el_true_deg)
        u0, v0 = direction_cosines(az_aim_deg, el_aim_deg)
        return float(self._gain_fn_2d(u, v, u0, v0))

    def __call__(self, off_angle_deg: float) -> float:
        return self.gain_dbi(off_angle_deg)


# ---------------------------------------------------------------------------
# Modeller
# ---------------------------------------------------------------------------

_MODELS: dict[str, Callable[[AntennaConfig], Callable[[float], float]]] = {}


def register_model(name: str):
    """Gör en ny mönstermodell tillgänglig via `"model": "<namn>"` i scenariofilen."""

    def decorator(fn: Callable[[AntennaConfig], Callable[[float], float]]):
        _MODELS[name] = fn
        return fn

    return decorator


def available_models() -> list[str]:
    return sorted(_MODELS)


@register_model("isotropic")
def _isotropic(cfg: AntennaConfig) -> Callable[[float], float]:
    """Ingen riktverkan alls — samma nivå åt alla håll.

    Används för att isolera resten av kedjan: om ett scenario med `isotropic`
    fortfarande tappar paket är det inte pekningen som är problemet.
    """
    return lambda _theta: cfg.peak_gain_dbi


@register_model("gaussian")
def _gaussian(cfg: AntennaConfig) -> Callable[[float], float]:
    """Parabolisk huvudlob: G(θ) = G_max - 12*(θ/θ3dB)².

    Gäller bara runt bomriktningen. Bortom `cutoff` faller modellen till en
    sidolobenivå, annars skulle den ge orimliga dämpningar (vid 180 grader blir
    uttrycket -12*(180/17.5)² = -1270 dB, vilket inte är en antenn).
    """
    bw = _require_beamwidth(cfg, "gaussian")
    floor_db = cfg.peak_gain_dbi + (
        cfg.backlobe_db if cfg.backlobe_db is not None else DEFAULT_BACKLOBE_DB
    )
    # Klipp vid ungefär första nollstället, där parabeln inte längre beskriver något.
    cutoff = cfg.exponent if cfg.exponent is not None else 1.5 * bw

    def gain(theta: float) -> float:
        if theta <= cutoff:
            return cfg.peak_gain_dbi - 12.0 * (theta / bw) ** 2
        return floor_db

    return gain


@register_model("cosn")
def _cosn(cfg: AntennaConfig) -> Callable[[float], float]:
    """G(θ) = G_max * cos^n(θ), noll utanför ±90 grader.

    En enkel modell för en horn- eller patchantenn. `exponent` är n; om den
    utelämnas räknas den fram ur strålbredden via cos^n(θ3dB/2) = 0.5.
    """
    bw = _require_beamwidth(cfg, "cosn")
    n = cfg.exponent
    if n is None:
        half = math.radians(bw / 2.0)
        n = math.log(0.5) / math.log(max(1e-6, math.cos(half)))
    floor_db = cfg.peak_gain_dbi + (
        cfg.backlobe_db if cfg.backlobe_db is not None else DEFAULT_BACKLOBE_DB
    )

    def gain(theta: float) -> float:
        if theta >= 89.9:
            return floor_db
        c = math.cos(math.radians(theta))
        return cfg.peak_gain_dbi + 10.0 * math.log10(max(1e-12, c**n))

    return gain


@register_model("yagi")
def _yagi(cfg: AntennaConfig) -> Callable[[float], float]:
    """Yagi-approximation: huvudlob, sidolober och baklob.

    Huvudloben är parabolisk intill bomriktningen, därefter ett platt fält av
    sidolober. Modellen är grov — den fångar att en yagi har tydliga sidolober,
    inte var de sitter. Vill du ha det riktiga mönstret: kör NEC och använd
    `"model": "file"`.
    """
    bw = _require_beamwidth(cfg, "yagi")
    side = cfg.peak_gain_dbi + (
        cfg.sidelobe_db if cfg.sidelobe_db is not None else DEFAULT_SIDELOBE_DB
    )
    back = cfg.peak_gain_dbi + (
        cfg.backlobe_db if cfg.backlobe_db is not None else DEFAULT_BACKLOBE_DB
    )
    first_null = 1.25 * bw

    def gain(theta: float) -> float:
        if theta < first_null:
            return max(side, cfg.peak_gain_dbi - 12.0 * (theta / bw) ** 2)
        if theta < 110.0:
            return side
        return back

    return gain


@register_model("file")
def _file(cfg: AntennaConfig) -> Callable[[float], float]:
    """Mönster inläst från textfil: två kolumner, `vinkel_grader förstärkning_dbi`.

    Filen ska ha stigande vinkel från 0 (bomriktning) till 180 (rakt bakåt).
    Värden mellan punkterna interpoleras linjärt; utanför intervallet används
    ändpunkterna.
    """
    if not cfg.pattern_file:
        raise ConfigError("antenna: modellen 'file' kräver 'pattern_file'")

    path = Path(cfg.pattern_file)
    if not path.is_file():
        raise ConfigError(f"antenna: hittar inte mönsterfilen {path}")

    table = np.loadtxt(path)
    if table.ndim != 2 or table.shape[1] < 2 or table.shape[0] < 2:
        raise ConfigError(f"{path}: väntade minst två rader med två kolumner")
    angles = table[:, 0]
    gains = table[:, 1]

    def gain(theta: float) -> float:
        return float(np.interp(theta, angles, gains))

    return gain


# ---------------------------------------------------------------------------
# Plan fasstyrd array
# ---------------------------------------------------------------------------


def array_peak_gain_dbi(element_gain_dbi: float, nx: int, ny: int) -> float:
    """Toppförstärkning för en array: elementets + 10*log10(antal element).

    Koherent summering av N element ger 10*log10(N), inte 20*log10(N): det är
    effekt som adderas, inte amplitud. Fyra element ger alltså +6,0 dB, sexton
    ger +12,0 dB. Det är samma siffra som BEAMFORMING.md räknar fram.
    """
    if nx < 1 or ny < 1:
        raise ConfigError("array: nx och ny måste vara minst 1")
    return element_gain_dbi + 10.0 * math.log10(nx * ny)


def array_factor(
    nx: int,
    ny: int,
    spacing_lambda: float,
    u: float,
    v: float,
    u0: float,
    v0: float,
    phase_bits: int | None = None,
) -> float:
    """Normaliserad arrayfaktor |AF| i [0, 1] för en plan array i horisontalplanet.

    Element (m, n) sitter på (m*dx, n*dy) med dx = dy = spacing_lambda*våglängd.
    Mäter man avstånd i våglängder blir k*d = 2*pi*spacing_lambda, så våglängden
    behöver aldrig sättas in — modellen är bandoberoende, precis som resten.

    Styrningen mot (u0, v0) lägger på fasen

        phi_mn = -k(dx*m*u0 + dy*n*v0)

    och med `phase_bits` kvantiseras den fasen till 2^phase_bits nivåer. Det är
    vad en digital fasväxlare gör — MAPS-010144 är 4-bitars med 22,5 graders steg.
    Kvantiseringen fyller de ideala nollorna (från −240 dB till omkring −32 dB)
    men höjer inte toppsidoloben för en uniform array, eftersom belysningens egen
    sidolob ligger högre: −11,3 dB för 4×4 med d = 0,5λ, kontrollerat mot
    `|sin(N*pi*d*u)/(N*sin(pi*d*u))|`. Utan kvantisering ritas en ideal array, som
    är bättre än någon byggbar krets.

    Grating lobes uppstår när spacing_lambda > 0,5: då hamnar en extra huvudlob
    innanför den synliga delen av (u, v). Vid 0,5 finns bara en lob.
    """
    m = np.arange(nx, dtype=float)[:, None]
    n = np.arange(ny, dtype=float)[None, :]

    steer = -2.0 * math.pi * spacing_lambda * (m * u0 + n * v0)
    if phase_bits is not None:
        step = 2.0 * math.pi / float(2**phase_bits)
        steer = np.round(steer / step) * step

    phase = 2.0 * math.pi * spacing_lambda * (m * u + n * v) + steer
    # Absolutbeloppet ska ligga UTANFOR summeringen: |sum exp(j*phi)|. Skriver
    # man abs() innanför blir varje term 1 och arrayfaktorn alltid 1,0 — en bugg
    # som ser ut som en fungerande array men som aldrig ger sidolober.
    return float(np.abs(np.exp(1j * phase).sum()) / float(nx * ny))


@register_model("array")
def _array(cfg: AntennaConfig) -> Callable[[float], float]:
    """1D-vägen för arrayen — bara huvudlobens form.

    Motorn använder den inte (den går via `gain_dbi_2d`), men `AntennaPattern`
    kräver en 1D-funktion. Sidolober och grating lobes sitter i (u, v) och kan
    inte uttryckas som en funktion av en enda vinkel.
    """
    bw = cfg.beamwidth_3db_deg
    peak = cfg.peak_gain_dbi

    def gain(theta: float) -> float:
        if not bw or bw <= 0:
            return peak
        return peak - min(40.0, 12.0 * (theta / bw) ** 2)

    return gain


def _array_gain_2d(cfg: AntennaConfig) -> Callable[[float, float, float, float], float]:
    """Bygg arrayens (u, v)-mönster: elementmönster + arrayfaktor."""
    nx, ny = cfg.array_nx, cfg.array_ny
    if nx is None or ny is None:
        raise ConfigError("antenna: modellen 'array' kräver 'array_nx' och 'array_ny'")
    spacing = cfg.spacing_lambda
    if spacing is None:
        raise ConfigError("antenna: modellen 'array' kräver 'spacing_lambda'")

    # Elementets egen vinst räknas fram ur arrayens toppvinst, så att
    # peak_gain_dbi betyder samma sak för alla modeller: förstärkningen i
    # bredsidesriktningen.
    element_peak = cfg.peak_gain_dbi - 10.0 * math.log10(nx * ny)
    elem_bw = cfg.element_beamwidth_3db_deg or DEFAULT_ELEMENT_BEAMWIDTH_DEG

    # Återanvänd den gaussiska modellen för det enskilda elementet. Det är den
    # som gör arrayen svag mot horisonten: en horisontell array har sin bredsida
    # rakt upp, så ett element som sitter på 90 graders zenitvinkel är på sin
    # egen nollnivå. Det är fysikaliskt riktigt och gör jämförelsen med yagin ärlig.
    element_cfg = AntennaConfig(
        model="gaussian",
        peak_gain_dbi=element_peak,
        beamwidth_3db_deg=elem_bw,
        backlobe_db=cfg.backlobe_db,
    )
    element_gain = _gaussian(element_cfg)
    array_gain_db = 10.0 * math.log10(nx * ny)

    def gain_2d(u: float, v: float, u0: float, v0: float) -> float:
        # zenitvinkeln: sin(zeta) = sqrt(u^2 + v^2)
        sin_zeta = min(1.0, math.hypot(u, v))
        zeta = math.degrees(math.asin(sin_zeta))
        af = array_factor(nx, ny, spacing, u, v, u0, v0, cfg.phase_bits)
        return element_gain(zeta) + array_gain_db + 20.0 * math.log10(max(af, 1e-6))

    return gain_2d


def _array_beamwidth_deg(
    cfg: AntennaConfig, gain_2d: Callable[[float, float, float, float], float]
) -> float:
    """Strålbredd ur mönstret självt, inte ur en formel.

    Scenariofilen kan inte veta vilken strålbredd en 2x2-array med ett givet
    element mönster får — den beror på både arrayfaktorn och elementets lob. Att
    skatta den ur förstärkningen som för de andra modellerna skulle ge fel antal
    sveppositioner. Här söks -3 dB-punkten fram med bisektion i bredsidesplanet,
    vilket är deterministiskt och kostar några hundra utvärderingar en gång.
    """
    peak = gain_2d(0.0, 0.0, 0.0, 0.0)
    target = peak - 3.0
    lo, hi = 0.0, 90.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if gain_2d(math.sin(math.radians(mid)), 0.0, 0.0, 0.0) > target:
            lo = mid
        else:
            hi = mid
    # Bisektionen hittar **halva** bredden (punkten dar forstarkningen fallit
    # 3 dB fran toppen). De andra modellerna anger full bredd — 17,5 respektive
    # 48,4 grader — sa halvan maste dubbleras, annars blir straalbredden halv
    # och antalet sveppositioner fyra ganger for stort.
    return max(1.0, 2.0 * hi)


def _angle_between_uv(u1: float, v1: float, u2: float, v2: float) -> float:
    """Vinkeln mellan två riktningar givna som riktningscosinus (u, v).

    (u, v) är projektionen på horisontalplanet, så den tredje komponenten är
    w = sqrt(1 - u^2 - v^2). Skalärprodukten av två enhetsvektorer ger
    cos(vinkeln) — det är samma vinkel som geometry.pointing_error_deg räknar,
    bara uttryckt i projektionen i stället för i az/el.
    """
    w1 = math.sqrt(max(0.0, 1.0 - u1 * u1 - v1 * v1))
    w2 = math.sqrt(max(0.0, 1.0 - u2 * u2 - v2 * v2))
    c = u1 * u2 + v1 * v2 + w1 * w2
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


@register_model("hybrid")
def _hybrid(cfg: AntennaConfig) -> Callable[[float], float]:
    """1D-vägen för hybriden — bara mainlobens form.

    Motorn använder den inte (den går via `gain_towards`), men `AntennaPattern`
    kräver en 1D-funktion. Den riktiga fysiken ligger i `_hybrid_gain_2d`.
    """
    bw = cfg.element_beamwidth_3db_deg or DEFAULT_HYBRID_ELEMENT_BEAMWIDTH_DEG
    peak = cfg.peak_gain_dbi

    def gain(theta: float) -> float:
        return peak - min(40.0, 12.0 * (theta / bw) ** 2)

    return gain


def _hybrid_gain_2d(cfg: AntennaConfig) -> Callable[[float, float, float, float], float]:
    """Array **på** gimbal: gimbalen grovpekar, arrayen finjusterar elektroniskt.

    Det här är den arkitektur projektet ursprungligen planerade, och den skiljer
    sig från `"array"` på tre punkter som alla är avgörande:

    1. **Bredsidan är gimbalens riktning.** Arrayen sitter monterad på gimbalen,
       så dess bredsida pekar dit gimbalen pekar. Elementmönstret utvärderas
       därför vid **styrvinkeln** — avvikelsen mellan bredsidan och strålen —
       inte vid den absoluta vinkeln från en fast bredsida. Utan det här steget
       ärver hybriden array-only-modellens katastrof mot horisonten.
    2. **Styrningen är begränsad till ±max_scan_deg.** Utanför konen klämmer
       arrayen vid gränsen, och resten av felet kostar arrayfaktor. Det är
       gimbalens jobb att se till att den aldrig behöver klämma länge.
    3. **Scanförlusten är priset för den elektroniska styrningen.**
       Elementförstärkningen vid styrvinkeln theta är 12*(theta/65)^2 dB under
       toppen: 5,8 dB vid ±45 grader. Därför ska gimbalen följa så att
       styrvinkeln hålls liten — och därför är hybriden ingen gratis lunch.
    """
    nx, ny = cfg.array_nx, cfg.array_ny
    if nx is None or ny is None:
        raise ConfigError("antenna: modellen 'hybrid' kräver 'array_nx' och 'array_ny'")
    spacing = cfg.spacing_lambda
    if spacing is None:
        raise ConfigError("antenna: modellen 'hybrid' kräver 'spacing_lambda'")

    element_peak = cfg.element_gain_dbi if cfg.element_gain_dbi is not None else 8.0
    elem_bw = cfg.element_beamwidth_3db_deg or DEFAULT_HYBRID_ELEMENT_BEAMWIDTH_DEG
    max_scan = cfg.max_scan_deg if cfg.max_scan_deg is not None else 45.0
    array_gain_db = 10.0 * math.log10(nx * ny)

    element_cfg = AntennaConfig(
        model="gaussian",
        peak_gain_dbi=element_peak,
        beamwidth_3db_deg=elem_bw,
        backlobe_db=cfg.backlobe_db,
    )
    element_gain = _gaussian(element_cfg)

    def gain_2d(u: float, v: float, u0: float, v0: float) -> float:
        theta_abs = _angle_between_uv(u, v, u0, v0)
        theta_steer = min(theta_abs, max_scan)

        # Elementet ser styrvinkeln, inte den absoluta vinkeln.
        elem = element_gain(theta_steer)

        # Arrayfaktorn: styrd mot theta_steer, utvärderad vid theta_abs. Är
        # målet inom konen blir restfelet noll och AF = 1. Är det utanför blir
        # AF den dämpning som gimbalen ännu inte har hunnit ta bort.
        u_steer = math.sin(math.radians(theta_steer))
        u_targ = math.sin(math.radians(theta_abs))
        af = array_factor(nx, ny, spacing, u_targ, 0.0, u_steer, 0.0, cfg.phase_bits)
        return elem + array_gain_db + 20.0 * math.log10(max(af, 1e-6))

    return gain_2d


# Modeller vars mönster beror på **var** i (u, v) felet ligger, inte bara hur
# stort det är. Bara dessa behöver två riktningar; alla andra går via 1D-vägen.
_TWO_D_BUILDERS: dict[str, Callable[[AntennaConfig], Callable[..., float]]] = {
    "array": _array_gain_2d,
    "hybrid": _hybrid_gain_2d,
}


# ---------------------------------------------------------------------------
# Fabrik
# ---------------------------------------------------------------------------


def _require_beamwidth(cfg: AntennaConfig, model: str) -> float:
    if cfg.beamwidth_3db_deg is None:
        raise ConfigError(f"antenna: modellen '{model}' kräver 'beamwidth_3db_deg'")
    if cfg.beamwidth_3db_deg <= 0:
        raise ConfigError("antenna.beamwidth_3db_deg måste vara positiv")
    return cfg.beamwidth_3db_deg


def estimate_beamwidth_deg(gain_dbi: float) -> float:
    """Grov skattning av strålbredden ur förstärkningen.

    Rymdvinkeln är ungefär 4*pi/G, och för en någorlunda symmetrisk lob gäller
    Ω ≈ 1.27*θ². Används bara när scenariofilen saknar strålbredd — den riktiga
    siffran ska komma från antennens datablad eller en NEC-körning.
    """
    g = 10.0 ** (gain_dbi / 10.0)
    theta_rad = math.sqrt(4.0 * math.pi / (1.27 * max(g, 1.0)))
    return math.degrees(theta_rad)


def make_pattern(cfg: AntennaConfig) -> AntennaPattern:
    """Bygg ett mönster ur konfigurationen."""
    if cfg.model not in _MODELS:
        raise ConfigError(
            f"antenna.model: okänd '{cfg.model}'. Tillgängliga: {', '.join(available_models())}"
        )
    gain_fn = _MODELS[cfg.model](cfg)

    # Två modeller har en 2D-väg: array (fast bredsida) och hybrid (array på
    # gimbal). För alla andra är den None och gain_towards faller tillbaka på den
    # ursprungliga vinkelberäkningen.
    builder = _TWO_D_BUILDERS.get(cfg.model)
    gain_fn_2d = builder(cfg) if builder is not None else None

    bw = cfg.beamwidth_3db_deg
    if bw is None:
        bw = (
            _array_beamwidth_deg(cfg, gain_fn_2d)
            if gain_fn_2d is not None
            else estimate_beamwidth_deg(cfg.peak_gain_dbi)
        )
    return AntennaPattern(cfg, gain_fn, bw, gain_fn_2d=gain_fn_2d)
