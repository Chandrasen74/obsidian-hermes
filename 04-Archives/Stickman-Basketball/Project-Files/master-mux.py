"""Master each mix to -16 LUFS with a codec-safe ceiling, then mux with the graded picture."""
import subprocess, re, sys
from pathlib import Path

MIX = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\mix")
WS = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\agent-ws")
OUT = Path(r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\animate\deliverables")
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "audio").mkdir(exist_ok=True)

GRADE = {
    "dunk": ("eq=contrast=1.05:saturation=1.08:brightness=0.005,"
             "curves=master='0/0 0.5/0.515 1/1',unsharp=5:5:0.28:5:5:0,vignette=angle=PI/14"),
    "layup": "eq=contrast=1.04:saturation=1.14:brightness=0.005,vignette=angle=PI/14",
}
CEIL = {"dunk": 0.72, "layup": 0.72}       # linear amplitude, tuned so AAC stays under -0.5 dBFS

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
    return r.stdout + r.stderr

def loudness(p):
    o = run(["ffmpeg", "-v", "info", "-nostats", "-i", str(p), "-af",
             "ebur128=peak=true:framelog=quiet", "-f", "null", "-"])
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o)[-1])
    return i, tp

for name, dur in (("dunk", 5.0), ("layup", 6.0)):
    mix, master = MIX / f"{name}-mix.wav", MIX / f"{name}-master.wav"
    i0, pk0 = loudness(mix)
    gain = -16.0 - i0
    run(["ffmpeg", "-y", "-v", "error", "-i", str(mix), "-af",
         f"highpass=f=28,volume={gain:.2f}dB,alimiter=limit={CEIL[name]}:attack=4:release=60:level=disabled",
         "-ar", "48000", "-ac", "2", str(master)])
    i1, tp1 = loudness(master)
    print(f"{name}: mix {i0:.1f} LUFS / {pk0:.1f} dBTP -> gain {gain:+.1f} dB -> "
          f"master {i1:.1f} LUFS / {tp1:.1f} dBTP")

    fade_out = dur - 0.22
    vf = (f"{GRADE[name]},fade=t=in:st=0:d=0.10,"
          f"fade=t=out:st={fade_out:.2f}:d=0.22,format=yuv420p")
    dst = OUT / f"stickman-{name}-sfx.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WS / f"stickman-{name}" / "final.mp4"),
         "-i", str(master), "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "1:a",
         "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
         "-movflags", "+faststart", str(dst)])
    # measure what actually comes out of the container
    o = run(["ffmpeg", "-v", "info", "-nostats", "-i", str(dst), "-map", "0:a", "-af",
             "ebur128=peak=true:framelog=quiet", "-f", "null", "-"])
    di = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
    dtp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o)[-1])
    print(f"   mp4 audio: {di:.1f} LUFS, true peak {dtp:.1f} dBFS  -> {dst.name} "
          f"({dst.stat().st_size/1e6:.2f} MB)")
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    f"Copy-Item '{master}' '{OUT / 'audio' / (name + '-master.wav')}' -Force"])
