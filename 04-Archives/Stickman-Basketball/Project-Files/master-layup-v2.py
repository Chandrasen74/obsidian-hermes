"""Rebuild stickman-layup-sfx.mp4 from the v2 rendered frames (hoop revision).

Audio is untouched: the same layup-master.wav (cue times unchanged is the constraint).
Picture: PNG image sequence -> same grade string as before -> fade -> x264 CRF18 (lossless
source this time, so no double compression like the old final.mp4 -> grade chain).
"""
import subprocess, re, sys
from pathlib import Path

TMP = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode")
FRAMES = TMP / "layup-frames-v2"
MIX = TMP / "mix" / "layup-master.wav"
OUT = Path(r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\animate\deliverables")
PASS = OUT / "stickman-layup-sfx.mp4"

# identical to master-mux.py GRADE["layup"] + fades (6.0 s cut, out from 5.78)
VF = ("eq=contrast=1.04:saturation=1.14:brightness=0.005,vignette=angle=PI/14,"
      "fade=t=in:st=0:d=0.10,fade=t=out:st=5.78:d=0.22,format=yuv420p")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode:
        print(r.stderr[-3000:]); sys.exit(1)
    return r.stdout + r.stderr

def loudness(p):
    o = run(["ffmpeg", "-v", "info", "-nostats", "-i", str(p), "-map", "0:a",
             "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"])
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o)[-1])
    return i, tp

run(["ffmpeg", "-y", "-v", "error",
     "-framerate", "30", "-start_number", "0", "-i", str(FRAMES / "f%05d.png"),
     "-i", str(MIX),
     "-filter_complex", f"[0:v]{VF}[v]", "-map", "[v]", "-map", "1:a",
     "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
     "-movflags", "+faststart", str(PASS)])

li, ltp = loudness(PASS)
probe = run(["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_name,width,height,nb_frames,avg_frame_rate,pix_fmt:format=duration",
             "-of", "default=nw=1", str(PASS)])
print(probe)
print(f"mp4 audio: {li:.1f} LUFS, true peak {ltp:.1f} dBFS -> {PASS.name} "
      f"({PASS.stat().st_size/1e6:.2f} MB)")
