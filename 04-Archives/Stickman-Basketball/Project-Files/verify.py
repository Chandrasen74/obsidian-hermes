import subprocess, json
from pathlib import Path
import numpy as np

OUT = Path(r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\animate\deliverables")
SRC = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\agent-ws")

def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                                   "-of", "json", str(p)], capture_output=True).stdout)
    return j

def audio(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a", "-ac", "1",
                          "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

def frame(p, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", str(p), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.uint8)
    return a.reshape(-1, 3) if a.size else None

for name, expect in (("stickman-dunk-sfx", [(2.80, "slam"), (0.20, "dribble1"), (1.00, "dribble3"), (4.23, "land")]),
                     ("stickman-layup-sfx", [(0.07, "dribble1"), (2.80, "gather"), (4.37, "swish"), (4.31, "land")])):
    p = OUT / f"{name}.mp4"
    j = probe(p)
    vs = [s for s in j["streams"] if s["codec_type"] == "video"][0]
    aud = [s for s in j["streams"] if s["codec_type"] == "audio"]
    print(f"\n=== {name}")
    print(f"  video {vs['codec_name']} {vs['width']}x{vs['height']} {vs['r_frame_rate']} "
          f"frames={vs.get('nb_frames')} pix={vs.get('pix_fmt')}")
    print(f"  audio {aud[0]['codec_name'] if aud else 'NONE'} {aud[0].get('sample_rate') if aud else ''} "
          f"{aud[0].get('channels') if aud else ''}ch  sr={aud[0].get('sample_rate') if aud else ''}")
    print(f"  duration {float(j['format']['duration']):.3f}s  size {int(j['format']['size'])/1e6:.2f} MB")

    x = audio(p)
    blk = 240  # 5 ms
    env = np.array([np.max(np.abs(x[i:i+blk])) for i in range(0, len(x) - blk, blk)])
    times = np.arange(len(env)) * blk / 48000
    print(f"  audio {len(x)/48000:.3f}s peak {20*np.log10(max(np.max(np.abs(x)),1e-9)):.1f} dBFS")
    # loudest 5ms block
    top = np.argsort(env)[-6:][::-1]
    print("  loudest transients: " + ", ".join(f"{times[i]:.3f}s" for i in top))
    for t, lbl in expect:
        i = int(t * 48000 / blk)
        w = env[max(0, i - 4): i + 12]
        print(f"    {lbl:9} @{t:.2f}s  local peak {20*np.log10(max(w.max(),1e-9)):6.1f} dBFS")
    # coverage: rms per 500ms
    rms = [np.sqrt(np.mean(x[i:i+24000]**2)) for i in range(0, len(x)-24000, 24000)]
    print("  500ms RMS dB: " + " ".join(f"{20*np.log10(max(r,1e-9)):.0f}" for r in rms))

    # grade check vs source
    for t in (1.0, 2.8):
        a = frame(p, t).astype(np.float32)
        b = frame(SRC / ("stickman-dunk" if "dunk" in name else "stickman-layup") / "final.mp4", t).astype(np.float32)
        def stats(z):
            mx, mn = z.max(axis=1), z.min(axis=1)
            sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
            return z.mean(), sat.mean()
        ma, sa = stats(a)
        mb, sb = stats(b)
        print(f"  frame {t:.1f}s: mean {ma:.1f} vs {mb:.1f}  sat {sa:.3f} vs {sb:.3f}")
