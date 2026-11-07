import os, json, csv
from datetime import datetime
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # user's own photos; some are >100 MP

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

PHOTO  = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\Photography\photography-library"
GALLERY= r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\Photography\gallery.html"
INDEX  = os.path.join(PHOTO, "photo-index.json")
THUMBS = os.path.join(PHOTO, "thumbs")
CONV   = os.path.join(PHOTO, "converted")
DESCS  = os.path.join(PHOTO, "descriptions.json")
LOG    = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\Photography\photography-pipeline\undo-log-photography.csv"
KEY_FILE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\Photography\photography-pipeline\gemini_key.txt"

idx = json.load(open(INDEX, encoding="utf-8"))
items = idx["items"]

# merge descriptions if present
if os.path.exists(DESCS):
    descs = json.load(open(DESCS, encoding="utf-8"))
    for it in items:
        d = descs.get(it["file"])
        if d:
            it["desc"] = d.get("desc")
            it["tags"] = d.get("tags", [])
            it["ocr"] = d.get("ocr", "")

os.makedirs(THUMBS, exist_ok=True)

def thumb_name(rel):
    return rel.replace("/", "__") + ".jpg"

print("Generating thumbnails...", flush=True)
made = 0
for it in items:
    t = os.path.join(THUMBS, thumb_name(it["file"]))
    if it["ext"] in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heic"):
        if not os.path.exists(t):
            src = os.path.join(PHOTO, it["file"].replace("/", os.sep))
            try:
                img = Image.open(src)
                img = ImageOps.exif_transpose(img) if hasattr(ImageOps, "exif_transpose") else img
                img.thumbnail((400, 400), Image.LANCZOS)
                img.convert("RGB").save(t, "JPEG", quality=82)
                made += 1
            except Exception:
                pass
        it["thumb"] = "thumbs/" + thumb_name(it["file"])
    else:
        # video: poster thumbnails are made by transcode_videos.py; use when present
        it["thumb"] = ("thumbs/" + thumb_name(it["file"])
                       if os.path.exists(t) and os.path.getsize(t) > 0 else None)

print(f"thumbnails made now: {made}", flush=True)

# display copies for HEIC (browsers can't render HEIC; originals stay untouched)
os.makedirs(CONV, exist_ok=True)
converted = 0
for it in items:
    if it["ext"] == ".heic":
        c = os.path.join(CONV, thumb_name(it["file"]))
        if not os.path.exists(c):
            src = os.path.join(PHOTO, it["file"].replace("/", os.sep))
            try:
                img = Image.open(src)
                img = ImageOps.exif_transpose(img) if hasattr(ImageOps, "exif_transpose") else img
                img.thumbnail((2560, 2560), Image.LANCZOS)
                img.convert("RGB").save(c, "JPEG", quality=88)
                converted += 1
            except Exception:
                pass
        if os.path.exists(c) and os.path.getsize(c) > 0:
            it["disp"] = "converted/" + thumb_name(it["file"])
    it.setdefault("disp", it["file"])
print(f"HEIC display copies made now: {converted}", flush=True)

# orphan sweep: thumbs whose source file is no longer in the index
valid = {thumb_name(it["file"]) for it in items}
for folder in (THUMBS, CONV):
    orphans = [f for f in os.listdir(folder) if f.endswith(".jpg") and f not in valid]
    for f in orphans:
        try:
            os.remove(os.path.join(folder, f))
        except OSError:
            pass
    if orphans:
        with open(LOG, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), "THUMB-SWEEP",
                                    os.path.join(folder, "*"), f"{len(orphans)} orphan files removed",
                                    "derived cache only; source files no longer in index"])
    print(f"orphans removed in {os.path.basename(folder)}: {len(orphans)}", flush=True)

# ---- similarity groups: connected components over near-dup (same dhash, different bytes) ----
itemmap = {it["file"]: it for it in items}
parent = {it["file"]: it["file"] for it in items}

def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a

for it in items:
    for o in (it.get("near_of") or []):
        if o in parent:
            ra, rb = find(it["file"]), find(o)
            if ra != rb:
                parent[ra] = rb

clusters = {}
for k in parent:
    clusters.setdefault(find(k), []).append(k)

gid = 0
grouped = 0
for members in clusters.values():
    if len(members) < 2:
        continue
    gid += 1
    cams = [m for m in members if itemmap[m]["kind"] == "camera"]
    for m in members:
        itemmap[m]["grp"] = gid
        grouped += 1
        if len(cams) == 1:
            itemmap[m]["role"] = "raw" if m == cams[0] else "edit"
print(f"similarity groups: {gid} covering {grouped} items", flush=True)

# ---- build gallery html ----
data = []
for it in items:
    data.append({
        "f": it["file"], "t": it["thumb"], "k": it["kind"], "e": it["ext"],
        "disp": it.get("disp") or it["file"],
        "d": (it["date"] or "")[:10], "dt": it["date"] or "", "mt": it.get("mtime") or "",
        "c": it["camera"] or "",
        "w": it["w"], "h": it["h"], "s": it["size"],
        "desc": it.get("desc"), "tags": it.get("tags") or [], "ocr": it.get("ocr") or "",
        "dup": it.get("dup_of"), "near": it.get("near_of") or [],
        "exif": it.get("exif"), "dur": it.get("dur"),
        "grp": it.get("grp"), "role": it.get("role"),
    })

json_data = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

template = open(GALLERY, encoding="utf-8").read()

out = GALLERY
open(out, "w", encoding="utf-8").write(template.replace("__DATA__", json_data))
print(f"gallery.html written with {len(data)} items", flush=True)
print("GALLERY DONE", flush=True)
