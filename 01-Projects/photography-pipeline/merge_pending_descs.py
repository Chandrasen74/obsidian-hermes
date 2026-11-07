"""Merge pending-descs.json entries into descriptions.json by locating each
basename in the library (including '(drive)'-suffixed variants).
Logs DESC-MERGE rows to the undo log, then empties the pending file.
"""
import csv
import datetime
import json
import os

REORG = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline"
LIB = r"C:\Users\Kanchan Verma\OneDrive\Desktop\photography"
PENDING = os.path.join(REORG, "pending-descs.json")
DESCS = os.path.join(LIB, "descriptions.json")
UNDO = os.path.join(REORG, "undo-log-photography.csv")
SKIP_DIRS = {"thumbs", "playback", "converted"}

pending = json.load(open(PENDING, encoding="utf-8-sig"))
descs = json.load(open(DESCS, encoding="utf-8-sig"))

# index library files by basename (and '(drive)' variants)
by_name = {}
for root, dirs, files in os.walk(LIB):
    dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
    for fn in files:
        by_name.setdefault(fn, []).append(os.path.relpath(os.path.join(root, fn), LIB).replace("\\", "/"))

def undo_log(action, frm, to, result):
    new = not os.path.exists(UNDO)
    with open(UNDO, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["Timestamp", "Action", "From", "To", "Result"])
        w.writerow([datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), action, frm, to, result])

merged, missing, kept = [], [], []
for base, entry in pending.items():
    stem, ext = os.path.splitext(base)
    candidates = by_name.get(base, []) + by_name.get(f"{stem} (drive){ext}", [])
    if not candidates:
        missing.append(base)
        undo_log("DESC-MERGE", base, "(not found)", "FAILED - no library file")
        continue
    if len(candidates) > 1:
        # prefer exact basename match, then (drive) variant
        candidates.sort(key=lambda p: (not p.endswith("/" + base), "(drive)" not in p))
    rel = candidates[0]
    if rel in descs:
        kept.append((base, rel))
        undo_log("DESC-MERGE", base, rel, "SKIPPED - description already present")
        continue
    descs[rel] = {"desc": entry["desc"], "tags": entry["tags"]}
    merged.append((base, rel))
    undo_log("DESC-MERGE", base, rel, "OK")

with open(DESCS, "w", encoding="utf-8") as f:
    json.dump(descs, f, ensure_ascii=False, indent=1)

if not missing:
    with open(PENDING, "w", encoding="utf-8") as f:
        json.dump({}, f)

print(f"merged: {len(merged)} | already-had-desc: {len(kept)} | missing: {len(missing)}")
for base, rel in merged:
    print(f"  {base} -> {rel}")
for base in missing:
    print(f"  MISSING: {base}")
print("descriptions.json entries now:", len(descs))
