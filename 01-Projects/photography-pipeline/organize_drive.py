import os, json, csv, hashlib, shutil, re, sys
from datetime import datetime
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PHOTO  = r"C:\Users\Kanchan Verma\OneDrive\Desktop\photography"
LOG    = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"
MANIFEST = os.path.join(PHOTO, "drive-folders.json")
INDEX  = os.path.join(PHOTO, "photo-index.json")
DESCS  = os.path.join(PHOTO, "descriptions.json")

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

def exif_date(p):
    """EXIF datetime, 'UNSET' for the 0000:00:00 unset-clock case, else None."""
    try:
        img = Image.open(p)
        exif = img._getexif()
        img.close()
        if exif:
            d = exif.get(36867) or exif.get(36868) or exif.get(306)
            if d:
                s = str(d).strip()
                if s.startswith("0000:00:00"):
                    return "UNSET"
                return datetime.strptime(s, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None

def exif_cam(p):
    """'MAKE MODEL' uppercased from EXIF, '' if unavailable."""
    try:
        img = Image.open(p)
        exif = img._getexif()
        img.close()
        if exif:
            return (str(exif.get(271, "")) + " " + str(exif.get(272, ""))).upper().strip()
    except Exception:
        pass
    return ""

MONTHS = {mn.lower(): i for i, mn in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"], 1)}

def folder_date(name):
    """Drive folders are user-named dates: M-D-YY[YY] or 'Month YYYY'."""
    m = re.match(r"^(\d{1,2})-(\d{1,2})-(\d{2,4})$", name.strip())
    if m:
        mo, da, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if yr < 100: yr += 2000
        try: return datetime(yr, mo, da)
        except ValueError: return None
    m = re.match(r"^([A-Za-z]+)\s+(\d{4})$", name.strip())
    if m:
        mo = MONTHS.get(m.group(1).lower())
        if mo:
            try: return datetime(int(m.group(2)), mo, 1)
            except ValueError: return None
    return None

def msg_date(fn):
    """YYYY-MM for WhatsApp/Screenshot style filenames, else None."""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", fn)
    if m: return m.group(1) + "-" + m.group(2)
    m = re.search(r"-(\d{4})(\d{2})(\d{2})-", fn)   # IMG-20240815-WA0033.jpg
    if m: return m.group(1) + "-" + m.group(2)
    m = re.search(r"_(\d{8})[_-]", fn)              # Screenshot_20260102-...
    if m: return m.group(1)[:4] + "-" + m.group(1)[4:6]
    return None

drive_folders = json.load(open(MANIFEST, encoding="utf-8"))
idx = json.load(open(INDEX, encoding="utf-8"))
lib = {}
for it in idx["items"]:
    # only trust index entries whose file still exists on disk
    # (stale entries for deleted files caused the self-match bug)
    if it.get("md5") and os.path.exists(os.path.join(PHOTO, it["file"].replace("/", os.sep))):
        lib.setdefault(it["md5"], []).append(it["file"])

descs = json.load(open(DESCS, encoding="utf-8")) if os.path.exists(DESCS) else {}
desc_moves = {}

stats = {"moved": 0, "skip_identical": 0, "errors": 0}
DRY = "--dry" in sys.argv
if DRY: print("DRY RUN - no files will be moved or removed", flush=True)

for folder in drive_folders:
    root = os.path.join(PHOTO, folder)
    if not os.path.isdir(root): continue
    fdate = folder_date(folder)
    for dirpath, dirs, files in os.walk(root):
        for fn in sorted(files):
            src = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            rel_old = os.path.relpath(src, PHOTO).replace("\\", "/")
            try:
                h = md5(src)
                matches = [p for p in lib.get(h, []) if p != rel_old]
                if matches:
                    if DRY:
                        print("DRY: discard dup", rel_old, "==", matches[0], flush=True)
                        stats["skip_identical"] += 1
                        continue
                    os.remove(src)
                    stats["skip_identical"] += 1
                    log("SKIP-DUPLICATE", src, matches[0], "byte-identical to OTHER library file, copy removed")
                    continue
                # route
                if fn.startswith("Screenshot"):
                    dest_dir = os.path.join(PHOTO, "Screenshots", msg_date(fn) or "")
                elif fn.startswith("WhatsApp") or re.match(r"^IMG-\d{8}-WA\d+", fn):
                    dest_dir = os.path.join(PHOTO, "WhatsApp", msg_date(fn) or "")
                elif fn.upper().startswith("DSCN") or "COOLPIX" in exif_cam(src):
                    dt = exif_date(src) if ext in (".jpg", ".jpeg") else None
                    unset = (dt == "UNSET")
                    if unset or dt is None: dt = fdate
                    if dt is None:
                        # unset camera clock with no folder date -> accepted 2016-01-01 bucket
                        dt = datetime(2016, 1, 1) if unset else datetime.fromtimestamp(os.path.getmtime(src))
                    dest_dir = os.path.join(PHOTO, "Camera", dt.strftime("%Y-%m-%d"))
                elif ((len(fn) >= 10 and fn[:10].isdigit() and ext in (".jpg", ".jpeg", ".png", ".heic"))
                      or fn.startswith("Photo_")
                      or re.match(r"^\d{8}_\d{6}", fn)          # Samsung: 20260302_191057.jpg
                      or re.match(r"^\d{4}-\d{2}-\d{2}_\d{6}", fn)):  # 2026-01-12_210839.jpg
                    dt = exif_date(src) if ext in (".jpg", ".jpeg", ".png") else None
                    if dt == "UNSET" or dt is None: dt = fdate
                    if dt == "UNSET" or dt is None: dt = datetime.fromtimestamp(os.path.getmtime(src))
                    dest_dir = os.path.join(PHOTO, "Phone", dt.strftime("%Y-%m-%d"))
                else:
                    dest_dir = os.path.join(PHOTO, "Misc")
                os.makedirs(dest_dir, exist_ok=True)
                dest = os.path.join(dest_dir, fn)
                if os.path.exists(dest):
                    if md5(dest) == h:
                        if DRY:
                            print("DRY: discard dup", rel_old, "==", os.path.relpath(dest, PHOTO), flush=True)
                            stats["skip_identical"] += 1
                            continue
                        os.remove(src)
                        stats["skip_identical"] += 1
                        log("SKIP-DUPLICATE", src, dest, "identical at destination, copy removed")
                        continue
                    base, e = os.path.splitext(fn)
                    dest = os.path.join(dest_dir, base + " (drive)" + e)
                if DRY:
                    print("DRY: move", rel_old, "->", os.path.relpath(dest, PHOTO).replace("\\", "/"), flush=True)
                    stats["moved"] += 1
                    continue
                shutil.move(src, dest)
                rel_new = os.path.relpath(dest, PHOTO).replace("\\", "/")
                log("MOVE", src, dest, "OK (drive dissolve)")
                if rel_old in descs:
                    desc_moves[rel_old] = rel_new
                lib.setdefault(h, []).append(rel_new)
                stats["moved"] += 1
            except Exception as e:
                stats["errors"] += 1
                log("DRIVE-DISSOLVE-ERROR", src, "", str(e))

# remove emptied drive folder trees, bottom-up
removed_dirs = 0
if not DRY:
    for folder in drive_folders:
        root = os.path.join(PHOTO, folder)
        if not os.path.isdir(root): continue
        for dirpath, dirs, files in os.walk(root, topdown=False):
            try:
                if not dirs and not files:
                    os.rmdir(dirpath)
                    removed_dirs += 1
            except OSError:
                log("RMDIR-FAIL", dirpath, "", "not empty or locked")
        # os.walk's parent dirs list is stale after child removals; catch the root itself
        try:
            if os.path.isdir(root) and not os.listdir(root):
                os.rmdir(root)
                removed_dirs += 1
        except OSError:
            log("RMDIR-FAIL", root, "", "not empty or locked")
    if os.path.isdir(root):
        print("NOT EMPTY (left in place):", folder, flush=True)
log("RMDIR", "drive folder trees", f"{removed_dirs} empty dirs removed", "OK")

# remap descriptions to new paths, then prune keys whose file is gone
for old, new in desc_moves.items():
    if old in descs:
        descs[new] = descs.pop(old)
pruned = []
if not DRY:
    pruned = [k for k in list(descs)
              if k.startswith("Screenshots/") or k.startswith("WhatsApp/")
              or not os.path.exists(os.path.join(PHOTO, k.replace("/", os.sep)))]
    for k in pruned:
        del descs[k]
    with open(DESCS, "w", encoding="utf-8") as f:
        json.dump(descs, f, indent=1, ensure_ascii=False)

print(f"moved: {stats['moved']} | identical dups discarded: {stats['skip_identical']} | "
      f"errors: {stats['errors']} | empty dirs removed: {removed_dirs} | "
      f"descriptions remapped: {len(desc_moves)} | desc keys pruned: {len(pruned)}", flush=True)
print("DRIVE DISSOLVE DONE", flush=True)
