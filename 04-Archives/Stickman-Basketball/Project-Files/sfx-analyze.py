import subprocess, numpy as np, wave, io, sys
from pathlib import Path

D = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\sfx")

def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", "44100",
                          "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

rows = []
for p in sorted(D.glob("*.mp3")):
    x = load(p)
    sr = 44100
    if x.size == 0:
        print(p.name, "EMPTY"); continue
    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x ** 2)))
    db = lambda v: 20 * np.log10(max(v, 1e-9))
    # onset: first 5ms block within 20 dB of peak
    blk = int(0.005 * sr)
    env = np.array([np.sqrt(np.mean(x[i:i+blk] ** 2)) for i in range(0, len(x) - blk, blk)])
    thr = env.max() * 0.1
    onset = (np.argmax(env > thr) * blk) / sr
    pk_i = int(np.argmax(np.abs(x)))
    # centroid over active part
    seg = x[pk_i: pk_i + int(0.4 * sr)]
    if seg.size < 512:
        seg = x
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    cen = float((S * f).sum() / max(S.sum(), 1e-9))
    lo = float(S[f < 300].sum() / max(S.sum(), 1e-9))
    hi = float(S[f > 3000].sum() / max(S.sum(), 1e-9))
    # decay: time from peak to -20 dB of peak envelope
    env_pk = env.max()
    below = np.where(env[pk_i // blk:] < env_pk * 0.1)[0]
    decay = (below[0] * blk) / sr if below.size else len(x) / sr
    rows.append((p.stem, len(x) / sr, db(peak), db(rms), onset, decay, cen, lo, hi))

print(f"{'name':16} {'dur':>6} {'peak':>6} {'rms':>6} {'onset':>6} {'dec20':>6} {'cent':>7} {'<300':>5} {'>3k':>5}")
for r in rows:
    print(f"{r[0]:16} {r[1]:6.2f} {r[2]:6.1f} {r[3]:6.1f} {r[4]:6.3f} {r[5]:6.2f} {r[6]:7.0f} {r[7]:5.2f} {r[8]:5.2f}")
