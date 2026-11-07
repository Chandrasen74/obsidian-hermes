import os, shutil, sys, csv, hashlib
from datetime import datetime

PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\photography"
STAGE = r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\drive_restore_staging"
LOG   = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"

def log(action, src, dst, result):
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), action, src, dst, result])

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while True:
            b = f.read(1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

files = []
for dirpath, dirs, names in os.walk(STAGE):
    for fn in sorted(names):
        files.append(os.path.join(dirpath, fn))
print(f"staging files: {len(files)}", flush=True)
tops = sorted({os.path.relpath(f, STAGE).split(os.sep)[0] for f in files})
print("top-level entries:", tops, flush=True)
if "--dry" in sys.argv:
    for f in files:
        print("  ", os.path.relpath(f, STAGE), flush=True)
    sys.exit(0)

copied = skipped = errs = 0
for s in files:
    rel = os.path.relpath(s, STAGE)
    d = os.path.join(PHOTO, rel)
    try:
        if os.path.exists(d):
            if md5(s) == md5(d):
                skipped += 1
                log("RESTORE-SKIP", s, d, "identical file already in place")
            else:
                base, ext = os.path.splitext(d)
                d2 = base + " (restored)" + ext
                shutil.copy2(s, d2)
                copied += 1
                log("RESTORE-COPY", s, d2, "name collision, different bytes -> (restored) suffix")
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            copied += 1
            log("RESTORE-COPY", s, d, "OK")
    except Exception as e:
        errs += 1
        log("RESTORE-ERROR", s, d, str(e))
print(f"copied: {copied} | already present (identical): {skipped} | errors: {errs}", flush=True)
print("RESTORE DONE", flush=True)
