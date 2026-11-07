import os, subprocess, csv
from datetime import datetime

PHOTO  = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
PLAY   = os.path.join(PHOTO, "playback")
THUMBS = os.path.join(PHOTO, "thumbs")
LOG    = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"
FF     = r"C:\Users\Kanchan Verma\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin\ffmpeg.exe"

VIDEOS = (".avi", ".mp4", ".mov", ".mts")

def log(action, src, dst, result):
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), action, src, dst, result])

def rel(p):
    return os.path.relpath(p, PHOTO).replace("\\", "/")

vids = []
for dirpath, dirs, files in os.walk(PHOTO):
    dirs[:] = [d for d in dirs if d.lower() not in ("thumbs", "playback", "__pycache__")]
    for fn in sorted(files):
        if os.path.splitext(fn)[1].lower() in VIDEOS:
            vids.append(os.path.join(dirpath, fn))
os.makedirs(PLAY, exist_ok=True)
os.makedirs(THUMBS, exist_ok=True)
print(f"videos found: {len(vids)}", flush=True)

t_ok = t_skip = t_fail = p_ok = p_skip = p_fail = 0
for src in vids:
    r = rel(src)
    ext = os.path.splitext(src)[1].lower()

    # ---- poster thumbnail (every video, incl. mp4) ----
    poster = os.path.join(THUMBS, r.replace("/", "__") + ".jpg")
    if os.path.exists(poster) and os.path.getsize(poster) > 0:
        p_skip += 1
    else:
        tmp = poster + ".tmp.jpg"
        cmd = [FF, "-y", "-ss", "1", "-i", src, "-frames:v", "1", "-vf", "scale=400:-2", "-q:v", "3", tmp]
        try:
            pr = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            pr = None
        if not (pr and pr.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0):
            # fallback: no seek (very short clips)
            cmd = [FF, "-y", "-i", src, "-frames:v", "1", "-vf", "scale=400:-2", "-q:v", "3", tmp]
            try:
                pr = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            except subprocess.TimeoutExpired:
                pr = None
        if pr and pr.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            os.replace(tmp, poster)
            p_ok += 1
        else:
            p_fail += 1
            err = (pr.stderr if pr else "timeout")[-200:]
            log("POSTER-FAIL", src, poster, err)
            print(f"  POSTER FAIL {r}: {err}", flush=True)

    # ---- playback transcode (browsers can't play avi/mov/mts; mp4 plays natively) ----
    if ext == ".mp4":
        continue
    out = os.path.join(PLAY, r.replace("/", "__") + ".mp4")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        t_skip += 1
        continue
    tmp = out + ".tmp.mp4"
    cmd = [FF, "-y", "-i", src, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", tmp]
    try:
        tr = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    except subprocess.TimeoutExpired:
        tr = None
    if tr and tr.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
        os.replace(tmp, out)
        t_ok += 1
        log("TRANSCODE", src, out, "OK (h264/aac copy for playback; original untouched)")
        print(f"  + {r}", flush=True)
    else:
        t_fail += 1
        err = (tr.stderr if tr else "timeout")[-200:]
        log("TRANSCODE-FAIL", src, out, err)
        print(f"  FAIL {r}: {err}", flush=True)

print(f"transcode: {t_ok} done, {t_skip} already present, {t_fail} failed", flush=True)
print(f"posters:   {p_ok} made, {p_skip} already present, {p_fail} failed", flush=True)
print("TRANSCODE DONE", flush=True)
