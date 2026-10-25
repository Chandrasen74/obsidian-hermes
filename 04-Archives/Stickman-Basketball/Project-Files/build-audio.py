"""Build the SFX mixes for the two agent animations (dunk 5.0s, layup 6.0s).

Levels are set in explicit peak dBFS (one-shots) or RMS dBFS (beds), so each cue
lands where it was written instead of inheriting a sample's loudness.
Beats come from each piece's index.html (see the cue sheet printed at the end).
"""
import subprocess, wave
from pathlib import Path
import numpy as np

SR = 48000
SFX = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\sfx")
OUT = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\mix")
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(20261024)

_cache = {}
def snd(name):
    if name not in _cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SFX / f"{name}.mp3"),
                              "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                             capture_output=True).stdout
        _cache[name] = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return _cache[name].copy()

def db(v): return 10 ** (v / 20.0)
def norm(x):
    p = np.max(np.abs(x))
    return x / p if p > 0 else x
def peak_db(x):
    return 20 * np.log10(max(np.max(np.abs(x)), 1e-12))
def rms_db(x):
    return 20 * np.log10(max(np.sqrt(np.mean(x ** 2)), 1e-12))

# ---------------------------------------------------------------- primitives
def lpf_fft(x, fc, slope=2.0):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1.0 + (f / fc) ** (2 * slope)), len(x))

def hpf_fft(x, fc, slope=2.0):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * (1.0 - 1.0 / (1.0 + (f / fc) ** (2 * slope))), len(x))

def resample(x, ratio):
    n = max(2, int(len(x) / ratio))
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)

def trim(x, start, dur):
    a = int(start * SR)
    return x[a: min(len(x), a + int(dur * SR))]

def fade_ends(x, fin=0.004, fout=0.01):
    x = x.copy()
    a, b = int(fin * SR), int(fout * SR)
    if a: x[:a] *= np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)
    return x

def thump(dur=0.28, f0=130, f1=52, dec=0.10, click=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / dec)
    tick = hpf_fft(rng.standard_normal(n), 1200) * np.exp(-t / 0.006) * click
    return norm(body + 0.35 * tick)

def clank(dur=1.1):
    n = int(dur * SR); t = np.arange(n) / SR
    parts = [(188, 0.60, 1.00), (417, 0.44, 0.74), (731, 0.32, 0.56),
             (1163, 0.23, 0.42), (1691, 0.16, 0.30), (2450, 0.10, 0.20)]
    x = np.zeros(n)
    for f, d, a in parts:
        x += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / d)
    x += hpf_fft(rng.standard_normal(n), 800) * np.exp(-t / 0.009) * 0.9
    return norm(x)

def squeak(dur=0.17, f0=880, f1=1420, vib=26):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.linspace(f0, f1, n) + vib * np.sin(2 * np.pi * 31 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.22 * np.sin(3.02 * ph)
    x *= np.clip(t / 0.008, 0, 1) * np.exp(-t / (dur * 0.42))
    x += hpf_fft(rng.standard_normal(n), 2000) * np.exp(-t / 0.02) * 0.22
    return norm(x)

def scuff(dur=0.09, fc=2200, low=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    nz = lpf_fft(hpf_fft(rng.standard_normal(n), 900), fc)
    x = nz * np.exp(-t / (dur * 0.35))
    x += thump(dur, 95, 60, 0.05, click=0.2) * low
    return norm(x)

def bell(dur=0.9, f=1174):
    n = int(dur * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.30)
         + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / 0.19)
         + 0.25 * np.sin(2 * np.pi * f * 2.99 * t) * np.exp(-t / 0.11))
    return norm(x)

def air_swell(dur, fc=2600, hp=350):
    """Band-limited noise cloud, one breath, for the flight gap."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = lpf_fft(hpf_fft(rng.standard_normal(n), hp), fc)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.3
    x *= env
    return norm(x)

# ---------------------------------------------------------------- mixing
class Mix:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.L = np.zeros(self.n); self.R = np.zeros(self.n)
        self.cues = []

    def _place(self, x, t, gain_db, pan, name, level_txt):
        i = int(round(t * SR))
        if i >= self.n or len(x) == 0:
            return
        if i < 0:
            x, i = x[-i:], 0
        seg = x[: self.n - i]
        th = (np.clip(pan, -1, 1) + 1) * np.pi / 4
        g = db(gain_db)
        self.L[i:i + len(seg)] += seg * np.cos(th) * g * 1.4142
        self.R[i:i + len(seg)] += seg * np.sin(th) * g * 1.4142
        if name:
            self.cues.append((t, name, level_txt, pan))

    def addp(self, x, t, peak=-6.0, pan=0.0, name=""):
        """Place a one-shot so its own peak sits at `peak` dBFS."""
        self._place(x, t, peak - peak_db(x), pan, name, f"pk {peak:+.1f} dB")

    def addr(self, x, t, rms=-30.0, pan=0.0, name=""):
        """Place a bed so its RMS sits at `rms` dBFS."""
        self._place(x, t, rms - rms_db(x), pan, name, f"rms {rms:+.1f} dB")

    def reverb(self, wet=0.10, rt=0.9, predelay=0.012, fc=5200):
        n_ir = int(rt * SR); t = np.arange(n_ir) / SR
        ir = rng.standard_normal(n_ir) * np.exp(-t / (rt / 6.9))
        ir = lpf_fft(ir, fc)
        ir[: int(predelay * SR)] = 0
        ir = norm(ir) * 0.5
        nfft = 1 << int(np.ceil(np.log2(self.n + n_ir)))
        IR = np.fft.rfft(ir, nfft)
        for ch in ("L", "R"):
            x = getattr(self, ch)
            y = np.fft.irfft(np.fft.rfft(x, nfft) * IR, nfft)[: self.n]
            setattr(self, ch, x + wet * y)

    def write(self, path, ceiling=0.70):
        st = np.stack([self.L, self.R], axis=1)
        p = np.max(np.abs(st))
        if p > 0:
            st = st / p * ceiling
        with wave.open(str(path), "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(np.clip(st * 32767, -32768, 32767).astype("<i2").tobytes())

def ball_hit(ratio=1.0, body=True):
    x = fade_ends(trim(resample(snd("bounce-seq-2087"), ratio), 0, 0.42) * 0.6, 0.002, 0.03)
    if body:
        b = thump(0.26, 125, 50, 0.085, click=0.35)
        n = max(len(x), len(b))
        x = np.pad(x, (0, n - len(x))) + np.pad(b, (0, n - len(b))) * 1.0
    return norm(x)

# ================================================================ DUNK 5.0s
def build_dunk():
    m = Mix(5.0)
    N = m.n

    amb = lpf_fft(trim(snd("crowd-360"), 6.0, 5.0), 420)
    amb = fade_ends(amb * np.clip(np.arange(len(amb)) / (0.4 * SR), 0, 1), 0.01, 0.25)
    m.addr(amb, 0.0, -38, 0.0, "gym crowd murmur (bed)")
    m.addp(lpf_fft(rng.standard_normal(N), 160), 0.0, -34, 0.0, "room hum (bed)")

    # dribble contacts 0.20 / 0.60 / 1.00
    for t, pk, pan, r in [(0.20, -5.0, -0.42, 1.00), (0.60, -5.6, -0.14, 1.03),
                          (1.00, -6.2, 0.10, 0.97)]:
        m.addp(ball_hit(r), t, pk, pan, f"dribble {t:.2f}s")
        m.addp(squeak(0.09, 640, 780, 16), t + 0.01, -34, pan, "")

    for i, t in enumerate(np.arange(0.098, 1.48, 0.1963)):
        m.addp(scuff(), t, -20 + (1.5 if i % 2 else 0), -0.15, "" if i else "court steps")

    m.addp(trim(snd("catch-2081"), 0.0, 0.5), 1.42, -13, 0.22, "gather catch 1.42s")
    m.addp(squeak(0.20, 900, 1500, 30), 1.47, -14, 0.15, "push-off squeak 1.47s")
    wh = trim(resample(snd("whoosh-1491"), 1.0), 0.0, 0.62)
    m.addp(wh, 1.40, -15, 0.10, "takeoff whoosh 1.40s")

    # flight 1.5-2.8: keep air moving so the mix never drops out
    m.addr(air_swell(1.35, 2800, 320), 1.48, -25, 0.0, "flight air (bed)")
    m.addp(trim(resample(snd("whoosh-1492"), 0.95), 0.0, 1.20), 1.58, -17, 0.0, "windmill whoosh 1.58s")
    m.addp(resample(trim(wh, 0.0, 0.40), 1.25), 2.44, -21, 0.06, "pre-slam whip 2.44s")

    # SLAM 2.80
    m.addp(clank(1.1), 2.80, -2.5, 0.32, "rim clank 2.80s")
    m.addp(trim(snd("hit-2093"), 0.06, 0.38), 2.795, -9, 0.32, "rim hit layer")
    m.addp(thump(0.55, 100, 40, 0.16, 0.6), 2.80, -5.5, 0.28, "slam body")
    m.addp(trim(snd("net-2084"), 0.10, 0.58), 2.845, -6, 0.36, "net swish 2.85s")
    m.addp(trim(resample(snd("net-2084"), 1.18), 0.05, 0.38), 3.06, -17, 0.30, "net settle")
    m.addp(trim(resample(snd("net-2084"), 1.35), 0.05, 0.28), 3.34, -24, 0.28, "")

    cr = fade_ends(trim(snd("crowd-2111"), 0.0, 5.0), 0.05, 0.55)
    m.addr(cr, 2.86, -31, 0.0, "crowd ovation 2.86s")

    # release + landing 4.23
    m.addp(trim(snd("whoosh-1492"), 0.62, 0.50), 3.86, -28, 0.0, "release air")
    m.addp(thump(0.42, 115, 44, 0.15, 0.6), 4.23, -6.5, 0.05, "landing thump 4.23s")
    m.addp(scuff(0.12, 1800), 4.24, -17, 0.05, "landing scuff")
    m.addp(squeak(0.13, 700, 980, 20), 4.26, -27, 0.05, "")

    for t, pk, pan in [(4.175, -13, 0.42), (4.45, -12, 0.50), (4.725, -16, 0.56), (4.97, -20, 0.60)]:
        m.addp(ball_hit(1.02, body=False), t, pk, pan, "post-slam bounce" if t < 4.3 else "")
    m.addp(bell(0.85, 1174), 4.45, -26, 0.45, "score bell 4.45s")

    m.reverb(wet=0.11, rt=0.9)
    m.L = fade_ends(m.L, 0.02, 0.10); m.R = fade_ends(m.R, 0.02, 0.10)
    return m

# =============================================================== LAYUP 6.0s
def build_layup():
    m = Mix(6.0)

    amb = hpf_fft(trim(snd("forest-1231"), 1.0, 6.0), 110)
    amb = amb * np.clip(np.arange(len(amb)) / (0.5 * SR), 0, 1)
    amb[-int(0.35 * SR):] *= np.linspace(1, 0, int(0.35 * SR))
    m.addr(amb, 0.0, -34, 0.0, "park ambience (birds)")

    n = m.n; t = np.arange(n) / SR
    wind = lpf_fft(rng.standard_normal(n), 320) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.23 * t + 1.1))
    m.addr(wind, 0.0, -44, 0.0, "breeze")

    # dribble contacts (act 1 grid 0.068+0.42k, chase, gather)
    for t0, pk, pan in [(0.068, -5.0, 0.10), (0.488, -6.0, 0.04), (0.908, -5.4, -0.02),
                        (1.328, -6.2, -0.08), (1.775, -8.0, -0.12), (2.298, -9.0, -0.16),
                        (2.798, -7.0, -0.10)]:
        m.addp(ball_hit(0.96 + 0.05 * rng.random()), t0, pk, pan, f"dribble {t0:.2f}s")

    steps = list(np.arange(0.121, 1.80, 0.2417)) + list(np.arange(1.846, 2.79, 0.1848)) \
            + list(np.arange(5.128, 5.98, 0.2417))
    for i, t0 in enumerate(steps):
        m.addp(scuff(0.08, 2600), t0, -21 + (1.5 if i % 2 else 0), -0.05, "" if i else "court steps")

    m.addp(trim(snd("catch-2081"), 0.0, 0.42), 2.86, -14, -0.08, "gather 2.86s")
    m.addp(squeak(0.22, 620, 900, 22), 3.14, -14, -0.10, "plant squeak 3.14s")
    m.addp(scuff(0.14, 1500), 3.16, -19, -0.10, "")
    m.addp(trim(resample(snd("whoosh-1492"), 0.92), 0.05, 1.10), 3.44, -13, -0.05, "leap whoosh 3.44s")
    m.addp(squeak(0.16, 980, 1560, 34), 3.48, -16, -0.05, "push-off squeak")
    m.addp(resample(trim(snd("whoosh-1491"), 0.15, 0.40), 1.15), 3.98, -26, 0.0, "scoop air")

    m.addp(resample(trim(snd("hit-2093"), 0.05, 0.14), 1.30), 4.355, -23, -0.32, "rim tick 4.36s")
    m.addp(trim(snd("net-2084"), 0.08, 0.52), 4.375, -8, -0.32, "swish 4.38s")
    m.addp(trim(resample(snd("net-2084"), 1.12), 0.05, 0.38), 4.47, -17, -0.32, "net tail")

    m.addp(thump(0.36, 105, 48, 0.13, 0.5), 4.31, -5, -0.12, "landing 4.31s")
    m.addp(scuff(0.13, 2000), 4.32, -18, -0.12, "")

    for t0, pk, pan in [(4.98, -10, -0.25), (5.48, -12, -0.05), (5.72, -15, 0.06), (5.96, -18, 0.18)]:
        m.addp(ball_hit(0.98, body=False), t0, pk, pan, "bounce after net" if t0 < 5.0 else "")

    m.reverb(wet=0.05, rt=0.55)
    m.L = fade_ends(m.L, 0.02, 0.06); m.R = fade_ends(m.R, 0.02, 0.06)
    return m

if __name__ == "__main__":
    for name, fn in (("dunk", build_dunk), ("layup", build_layup)):
        m = fn(); p = OUT / f"{name}-mix.wav"; m.write(p)
        print(f"\n=== {name}: {m.n / SR:.2f}s  mix peak {peak_db(m.L):.1f} dBFS  rms {rms_db(m.L):.1f} dBFS -> {p}")
        for t, nm, lv, pan in m.cues:
            print(f"  {t:6.3f}s  {lv:11}  pan {pan:+.2f}  {nm}")
