"""Library integrity check: re-hash every indexed file and compare against the index.

- MISSING: indexed file no longer on disk
- SIZE-CHANGED / HASH-CHANGED: file differs from the index snapshot (sync corruption, edits)
- NEW: file on disk that the index does not know about

Derived dirs (thumbs, playback, converted) are skipped. Writes integrity-report.csv
in the pipeline folder when anything is wrong; prints a summary either way.

Usage: python verify_library.py [--quick]   (--quick = size-only, no hashing)
"""
import csv
import hashlib
import json
import os
import sys

PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
INDEX = os.path.join(PHOTO, "photo-index.json")
PIPELINE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline"
REPORT = os.path.join(PIPELINE, "integrity-report.csv")
SKIP_DIRS = {"thumbs", "playback", "converted", "__pycache__", "_duplicates"}
ROOT_FILES = {"photo-index.json", "descriptions.json", "gallery.html"}


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


quick = "--quick" in sys.argv
idx = json.load(open(INDEX, encoding="utf-8-sig"))
items = idx["items"]
print(f"verifying {len(items)} indexed files{' (quick mode)' if quick else ''}...", flush=True)

problems = []  # (status, rel, detail)
ok = 0
for n, it in enumerate(items, 1):
    rel = it["file"]
    p = os.path.join(PHOTO, rel.replace("/", os.sep))
    if not os.path.exists(p):
        problems.append(("MISSING", rel, "indexed but not on disk"))
        continue
    sz = os.path.getsize(p)
    if it.get("size") and sz != it["size"]:
        problems.append(("SIZE-CHANGED", rel, f"index={it['size']} disk={sz}"))
        continue
    if not quick and it.get("md5"):
        h = md5(p)
        if h != it["md5"]:
            problems.append(("HASH-CHANGED", rel, f"index={it['md5']} disk={h}"))
            continue
    ok += 1
    if n % 300 == 0:
        print(f"  ...{n}/{len(items)}", flush=True)

indexed = {it["file"] for it in items}
new_files = []
for root, dirs, files in os.walk(PHOTO):
    dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
    for fn in files:
        if fn.lower() in ("thumbs.db", "desktop.ini") or fn.endswith(".tmp"):
            continue
        rel = os.path.relpath(os.path.join(root, fn), PHOTO).replace("\\", "/")
        if rel in indexed or rel in ROOT_FILES:
            continue
        new_files.append(rel)

print(f"OK: {ok} | problems: {len(problems)} | new-on-disk: {len(new_files)}", flush=True)
for status, rel, detail in problems:
    print(f"  {status}: {rel}  {detail}", flush=True)
for rel in new_files[:40]:
    print(f"  NEW: {rel}", flush=True)
if len(new_files) > 40:
    print(f"  ...and {len(new_files) - 40} more new files", flush=True)

if problems or new_files:
    with open(REPORT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Status", "File", "Detail"])
        for row in problems:
            w.writerow(row)
        for rel in new_files:
            w.writerow(("NEW", rel, "on disk, not in index"))
    print(f"report written: {REPORT}", flush=True)
else:
    if os.path.exists(REPORT):
        os.remove(REPORT)
        print("old report removed (all clean)", flush=True)
print("VERIFY DONE", flush=True)
