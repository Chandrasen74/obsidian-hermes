import os, json, csv

PHOTO   = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
BACKUP  = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\gallery-0932-backup.html"
LIVE    = os.path.join(PHOTO, "gallery.html")
DESCS   = os.path.join(PHOTO, "descriptions.json")
LOG     = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"

# prefer the 09:32 backup (contains ALL descriptions incl. the 52 deleted files)
GALLERY = BACKUP if os.path.exists(BACKUP) else LIVE

# 1) the 52 files deleted by the self-match bug (log window 2026-11-07T10:22)
deleted = []
with open(LOG, encoding="utf-8") as f:
    for row in csv.reader(f):
        if len(row) >= 5 and row[1] == "SKIP-DUPLICATE" and row[0].startswith("2026-11-07T10:22"):
            deleted.append(os.path.relpath(row[2], PHOTO).replace("\\", "/"))
deleted = sorted(set(deleted))
print(f"deleted files to recover: {len(deleted)}", flush=True)

# 2) parse the baked DATA array out of the gallery build
src = open(GALLERY, encoding="utf-8").read()
marker = "const DATA = "
i = src.index(marker) + len(marker)
data, _ = json.JSONDecoder().raw_decode(src[i:].lstrip())
by_f = {it["f"]: it for it in data}
print(f"gallery source: {GALLERY}")
print(f"gallery DATA items: {len(data)}", flush=True)

# 3) inject descriptions under the OLD drive-relative paths
#    (organize_drive.py remaps old->new when it moves the restored files)
descs = json.load(open(DESCS, encoding="utf-8"))
added = already = 0
for rel in deleted:
    it = by_f.get(rel)
    if not it:
        continue
    if it.get("desc") or it.get("tags"):
        if rel in descs:
            already += 1
        descs[rel] = {"desc": it.get("desc"), "tags": it.get("tags") or []}
        added += 1
with open(DESCS, "w", encoding="utf-8") as f:
    json.dump(descs, f, indent=1, ensure_ascii=False)

missing = [r for r in deleted if r not in by_f]
print(f"descriptions recovered: {added} ({already} were already present); not found in gallery: {len(missing)}", flush=True)
for m in missing:
    print("  MISSING:", m, flush=True)
print("RECOVER DESCS DONE", flush=True)
