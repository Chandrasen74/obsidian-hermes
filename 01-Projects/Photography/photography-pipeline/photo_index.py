import os, json, hashlib, subprocess
from datetime import datetime
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # user's own photos; some are >100 MP

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_OK = True
except Exception:
    HEIC_OK = False

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif") + (".heic",) if HEIC_OK else \
           (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif")

PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
OUT = os.path.join(PHOTO, "photo-index.json")
DRIVE_MANIFEST = os.path.join(PHOTO, "drive-folders.json")
CACHE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\index-cache.json"
FFPROBE = r"C:\Users\Kanchan Verma\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin\ffprobe.exe"

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while True:
            b = f.read(1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

def dhash(p):
    try:
        img = Image.open(p).convert("L").resize((9, 8), Image.LANCZOS)
        px = list(img.getdata())
        bits = 0
        for row in range(8):
            for col in range(8):
                if px[row*9+col] > px[row*9+col+1]:
                    bits |= 1 << (row*8+col)
        return "%016x" % bits
    except Exception:
        return None

def _ratio(v):
    try:
        return float(v)
    except Exception:
        return None

def exif_info(p):
    info = {"date": None, "camera": None, "w": None, "h": None, "exif": None}
    try:
        img = Image.open(p)
        info["w"], info["h"] = img.size
        exif = img._getexif()
        if exif:
            d = exif.get(36867) or exif.get(36868) or exif.get(306)
            if d:
                try:
                    info["date"] = datetime.strptime(str(d).strip(), "%Y:%m:%d %H:%M:%S").isoformat()
                except ValueError:
                    pass
            model = exif.get(272)  # Model
            make = exif.get(271)   # Make
            if model: info["camera"] = (str(make).strip() + " " if make else "") + str(model).strip()
            iso = exif.get(34679)
            fn = _ratio(exif.get(33437))   # FNumber
            et = _ratio(exif.get(33434))   # ExposureTime
            fl = _ratio(exif.get(37386))   # FocalLength
            if iso or fn or et or fl:
                ex = {}
                try:
                    if iso: ex["iso"] = int(float(iso))
                except Exception: pass
                if fn: ex["f"] = round(fn, 1)
                if et:
                    try:
                        ex["sh"] = ("1/" + str(round(1/et)) + " s") if et < 0.25 else (str(round(et, 1)) + " s")
                    except Exception: pass
                if fl: ex["fl"] = str(round(fl, 1)) + " mm"
                if ex: info["exif"] = ex
        img.close()
    except Exception:
        pass
    return info

def vid_info(p):
    out = {"dur": None, "w": None, "h": None}
    try:
        r = subprocess.run([FFPROBE, "-v", "error", "-print_format", "json",
                            "-show_format", "-show_streams", p],
                           capture_output=True, text=True, timeout=60)
        j = json.loads(r.stdout or "{}")
        v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), None)
        dur = float(j.get("format", {}).get("duration") or 0)
        out["dur"] = round(dur, 1) if dur else None
        if v:
            out["w"], out["h"] = v.get("width"), v.get("height")
    except Exception:
        pass
    return out

drive_folders = []
if os.path.exists(DRIVE_MANIFEST):
    drive_folders = json.load(open(DRIVE_MANIFEST, encoding="utf-8"))
drive_set = set(drive_folders)

# ---- incremental cache: reuse computed metadata for unchanged files ----
cache = {}
if os.path.exists(CACHE):
    try:
        cache = json.load(open(CACHE, encoding="utf-8"))
    except Exception:
        cache = {}

def path_of(rel):
    return os.path.join(PHOTO, rel.replace("/", os.sep))

print("Building index...", flush=True)
items = []
hashes = {}      # md5 -> [paths]
phashes = {}     # dhash -> [paths]
cache_hits = 0
computed = 0

for root, dirs, files in os.walk(PHOTO):
    dirs[:] = [d for d in dirs if d.lower() not in ("thumbs", "playback", "converted", "__pycache__")]
    rel_root = os.path.relpath(root, PHOTO)
    for fn in sorted(files):
        if fn in ("photo-index.json", "gallery.html", "drive-folders.json"): continue
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, PHOTO).replace("\\", "/")
        ext = os.path.splitext(fn)[1].lower()
        is_img = ext in IMG_EXTS
        is_vid = ext in (".avi", ".mp4", ".mov", ".mts")
        if not (is_img or is_vid): continue
        try:
            size = os.path.getsize(p)
            mtime = os.path.getmtime(p)
        except Exception:
            continue
        # classify by top-level folder
        top = rel.split("/")[0]
        if top == "Camera": kind = "camera"
        elif top == "Phone": kind = "phone"
        elif top == "Pinterest": kind = "pinterest"
        elif top == "Misc": kind = "misc"
        elif fn.startswith("Screenshot"): kind = "screenshot"
        elif fn.startswith("WhatsApp"): kind = "whatsapp"
        elif top in drive_set: kind = "drive"
        else: kind = "other"

        sig = [mtime, size]
        cached = cache.get(rel)
        if cached and cached.get("sig") == sig and cached["base"].get("date"):
            base = cached["base"]
            cache_hits += 1
        else:
            base = {"file": rel, "kind": kind, "ext": ext, "size": size,
                    "mtime": datetime.fromtimestamp(mtime).isoformat(),
                    "date": None, "camera": None, "w": None, "h": None,
                    "exif": None, "dur": None, "md5": None, "dhash": None}
            if is_img:
                ei = exif_info(p)
                base.update({k: ei[k] for k in ("date", "camera", "w", "h", "exif")})
                if not base["date"]:
                    base["date"] = base["mtime"]  # no EXIF: use file date (downloads, stripped copies)
            else:
                base["date"] = base["mtime"]
                base.update(vid_info(p))
            try:
                base["md5"] = md5(p)
            except Exception:
                pass
            if is_img:
                base["dhash"] = dhash(p)
            cache[rel] = {"sig": sig, "base": base}
            computed += 1

        it = dict(base)
        it["dup_of"] = None
        it["near_of"] = []
        it["desc"] = None
        it["tags"] = []
        items.append(it)
        if it["md5"]: hashes.setdefault(it["md5"], []).append(rel)
        if it["dhash"]: phashes.setdefault(it["dhash"], []).append(rel)

# exact duplicates: keep first (sorted order), mark others
for it in items:
    if it["md5"] and len(hashes[it["md5"]]) > 1:
        others = [x for x in hashes[it["md5"]] if x != it["file"]]
        it["dup_of"] = others[0]

# near duplicates: same dhash, different bytes
for it in items:
    if it["dhash"] and not it["dup_of"] and len(phashes[it["dhash"]]) > 1:
        for other in phashes[it["dhash"]]:
            if other != it["file"]:
                other_it = next((x for x in items if x["file"] == other), None)
                if other_it and other_it["md5"] != it["md5"]:
                    it["near_of"].append(other)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"built": datetime.now().isoformat(), "count": len(items), "items": items}, f, indent=1)
with open(CACHE, "w", encoding="utf-8") as f:
    json.dump(cache, f)

n_dup = sum(1 for i in items if i["dup_of"])
n_near = sum(1 for i in items if i["near_of"])
print(f"Indexed {len(items)} items | exact dups: {n_dup} | near-dups flagged: {n_near}", flush=True)
print(f"cache: {cache_hits} reused, {computed} computed fresh", flush=True)
print("INDEX DONE", flush=True)
