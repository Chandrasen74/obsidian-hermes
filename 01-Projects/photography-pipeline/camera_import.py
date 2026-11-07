import os, sys, json, csv, hashlib, shutil
from datetime import datetime
from PIL import Image
from PIL import ExifTags

CARD = r"D:\DCIM"
PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\photography"
CAM = os.path.join(PHOTO, "Camera")
LOG = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"
SUMMARY = r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\import-summary.json"

def log(action, src, dst, result):
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([datetime.now().isoformat(timespec="seconds"), action, src, dst, result])

def md5(path, bufsize=1024*1024):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b: break
            h.update(b)
    return h.hexdigest()

def exif_date(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if exif:
            for tag in (36867, 36868, 306):  # DateTimeOriginal, DateTimeDigitized, DateTime
                if tag in exif:
                    d = str(exif[tag]).strip()
                    try:
                        return datetime.strptime(d, "%Y:%m:%d %H:%M:%S")
                    except ValueError:
                        pass
        img.close()
    except Exception:
        pass
    return None

# 1. hash existing photography files (all current files, any depth)
print("Hashing existing photography files...", flush=True)
existing = {}
for root, dirs, files in os.walk(PHOTO):
    if "thumbs" in root.lower(): continue
    for fn in files:
        p = os.path.join(root, fn)
        try:
            if os.path.getsize(p) < 200*1024*1024:
                existing.setdefault(md5(p), []).append(p)
        except Exception:
            pass
print(f"  {len(existing)} unique hashes from existing files", flush=True)

# 2. walk the card
card_files = []
for sub in sorted(os.listdir(CARD)):
    d = os.path.join(CARD, sub)
    if not os.path.isdir(d): continue
    for fn in sorted(os.listdir(d)):
        card_files.append(os.path.join(d, fn))
print(f"Card files: {len(card_files)}", flush=True)

stats = {"copied": 0, "skipped_identical": 0, "verify_failed": 0, "errors": 0, "bytes_copied": 0}
details = []

for i, src in enumerate(card_files, 1):
    fn = os.path.basename(src)
    try:
        size = os.path.getsize(src)
        h = md5(src)
        if h in existing:
            stats["skipped_identical"] += 1
            details.append({"file": fn, "action": "skip-identical", "match": existing[h][0]})
            if stats["skipped_identical"] % 25 == 0:
                print(f"[{i}/{len(card_files)}] skip-identical so far: {stats['skipped_identical']}", flush=True)
            continue
        # destination date
        dt = exif_date(src)
        if dt is None:
            mtime = os.path.getmtime(src)
            dt = datetime.fromtimestamp(mtime)
        datestr = dt.strftime("%Y-%m-%d")
        dest_dir = os.path.join(CAM, datestr)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, fn)
        if os.path.exists(dest):
            # name collision on disk: compare hash
            if md5(dest) == h:
                stats["skipped_identical"] += 1
                existing.setdefault(h, []).append(dest)
                details.append({"file": fn, "action": "skip-dest-identical", "dest": dest})
                continue
            base, ext = os.path.splitext(fn)
            dest = os.path.join(dest_dir, base + " (from card)" + ext)
        shutil.copy2(src, dest)
        h2 = md5(dest)
        if h2 != h:
            os.remove(dest)
            stats["verify_failed"] += 1
            details.append({"file": fn, "action": "VERIFY-FAILED", "error": "copy hash mismatch"})
            log("COPY-VERIFY-FAIL", src, dest, "hash mismatch, copy removed")
            continue
        stats["copied"] += 1
        stats["bytes_copied"] += size
        existing.setdefault(h, []).append(dest)
        log("COPY", src, dest, "OK md5-verified")
        details.append({"file": fn, "action": "copied", "dest": dest, "date": datestr})
        if stats["copied"] % 25 == 0:
            print(f"[{i}/{len(card_files)}] copied so far: {stats['copied']} ({stats['bytes_copied']/1e9:.2f} GB)", flush=True)
    except Exception as e:
        stats["errors"] += 1
        details.append({"file": fn, "action": "ERROR", "error": str(e)})
        log("COPY-ERROR", src, "", str(e))

with open(SUMMARY, "w", encoding="utf-8") as f:
    json.dump({"stats": stats, "details": details}, f, indent=1)

print(json.dumps(stats, indent=2), flush=True)
print("IMPORT DONE", flush=True)
