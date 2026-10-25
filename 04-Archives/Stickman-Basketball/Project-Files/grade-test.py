import subprocess
import numpy as np
from pathlib import Path

SRC = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\agent-ws")
variants = [
    ("none", "null"),
    ("eq only", "eq=contrast=1.05:saturation=1.08:brightness=0.004"),
    ("vig PI/5", "eq=contrast=1.05:saturation=1.08:brightness=0.004,vignette=angle=PI/5"),
    ("vig PI/4.5", "eq=contrast=1.05:saturation=1.08:brightness=0.004,vignette=angle=PI/4.5"),
    ("vig PI/4", "eq=contrast=1.05:saturation=1.08:brightness=0.004,vignette=angle=PI/4"),
    ("vig PI/3.5", "eq=contrast=1.05:saturation=1.08:brightness=0.004,vignette=angle=PI/3.5"),
    ("curve+eq", "eq=saturation=1.10:contrast=1.04:brightness=0.006,curves=master='0/0 0.5/0.52 1/1'"),
]

def stats(path, t, vf):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1",
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.float32)
    mx, mn = a.max(axis=1), a.min(axis=1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    luma = 0.2126 * a[:, 0] + 0.7152 * a[:, 1] + 0.0722 * a[:, 2]
    return a.mean(), luma.mean(), sat.mean()

for piece, t in (("stickman-dunk", 2.8), ("stickman-layup", 1.0)):
    p = SRC / piece / "final.mp4"
    base = stats(p, t, "null")
    print(f"\n=== {piece} @ {t}s  base mean RGB {base[0]:.1f} luma {base[1]:.1f} sat {base[2]:.3f}")
    for label, vf in variants:
        s = stats(p, t, vf)
        print(f"  {label:12} mean {s[0]:6.1f} ({100*(s[0]/base[0]-1):+5.1f}%)  "
              f"luma {s[1]:6.1f} ({100*(s[1]/base[1]-1):+5.1f}%)  sat {s[2]:.3f} ({100*(s[2]/base[2]-1):+5.1f}%)")
