import os, json, csv, subprocess, sys, hashlib
from datetime import datetime
from PIL import Image

PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
LOG = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"
MANIFEST = os.path.join(PHOTO, "drive-folders.json")
KEEP_DIRS = {"camera", "screenshots", "whatsapp", "phone", "thumbs", "__pycache__"}

def log(action, src, dst, result):
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), action, src, dst, result])

# 0. safety: gdown must not be running
r = subprocess.run(["powershell", "-NoProfile", "-Command",
    "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object {$_.CommandLine -match 'gdown'} | Measure-Object | Select-Object -ExpandProperty Count"],
    capture_output=True, text=True)
if r.stdout.strip() not in ("0", ""):
    print("ABORT: gdown still running", flush=True); sys.exit(1)
print("gdown not running - safe to organize", flush=True)

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while True:
            b = f.read(1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

def exif_date(p):
    try:
        img = Image.open(p)
        exif = img._getexif()
        img.close()
        if exif:
            d = exif.get(36867) or exif.get(36868) or exif.get(306)
            if d:
                return datetime.strptime(str(d).strip(), "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None

# 1. record which top-level dirs came from Drive (everything except our own structure)
drive_dirs = sorted(d for d in os.listdir(PHOTO)
                    if os.path.isdir(os.path.join(PHOTO, d)) and d.lower() not in KEEP_DIRS)
json.dump(drive_dirs, open(MANIFEST, "w", encoding="utf-8"))
print(f"Drive folders recorded: {len(drive_dirs)} -> {drive_dirs}", flush=True)

def move_to(src, dest_dir, name=None):
    fn = name or os.path.basename(src)
    dest = os.path.join(dest_dir, fn)
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(dest):
        try:
            if md5(dest) == md5(src):
                log("SKIP-IDENTICAL", src, dest, "already present")
                os.remove(src)  # exact dup at root; keep organized copy only
                return "skip-identical"
        except Exception:
            pass
        base, ext = os.path.splitext(fn)
        dest = os.path.join(dest_dir, base + " (2)" + ext)
    os.rename(src, dest)
    log("MOVE", src, dest, "OK")
    return dest

moved = 0
for fn in sorted(os.listdir(PHOTO)):
    p = os.path.join(PHOTO, fn)
    if not os.path.isfile(p): continue
    if fn in ("photo-index.json", "gallery.html", "drive-folders.json", "descriptions.json"): continue
    low = fn.lower()
    ext = os.path.splitext(fn)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".avi", ".mp4", ".bmp", ".gif"): continue
    if fn.startswith("Screenshot"):
        move_to(p, os.path.join(PHOTO, "Screenshots"))
    elif fn.startswith("WhatsApp"):
        move_to(p, os.path.join(PHOTO, "WhatsApp"))
    elif fn.upper().startswith("DSCN") or ext == ".avi":
        dt = exif_date(p) if ext in (".jpg", ".jpeg") else datetime.fromtimestamp(os.path.getmtime(p))
        if dt is None: dt = datetime.fromtimestamp(os.path.getmtime(p))
        move_to(p, os.path.join(PHOTO, "Camera", dt.strftime("%Y-%m-%d")))
    elif fn[:4].isdigit() and (fn[4:5] == "-" or fn[4:6].isdigit()) or fn.startswith("Photo_"):
        # phone-generated names: 2025-12-26_171123.jpg, 20251104_210141.jpg, Photo_2025-...
        dt = exif_date(p) if ext in (".jpg", ".jpeg", ".png") else None
        if dt is None: dt = datetime.fromtimestamp(os.path.getmtime(p))
        move_to(p, os.path.join(PHOTO, "Phone", dt.strftime("%Y-%m-%d")))
    else:
        # unknown-origin loose files (Drive edits, one-off shots) -> Misc
        move_to(p, os.path.join(PHOTO, "Misc"))
    moved += 1

print(f"organizer pass done: {moved} root files processed", flush=True)
print("ORGANIZE DONE", flush=True)
