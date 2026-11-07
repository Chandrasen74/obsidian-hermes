"""Move the Pinterest download tree into the photography library.

- Source: Pictures\\pinterest\\pinterest\\Akulmach74\\('-_~+')\\  (176 pin_*.jpg + older gallery-dl files)
- Destination: <library>\\Pinterest\\<YYYY-MM-DD\\  (subfolder per file mtime date, library convention)
- Older gallery-dl files that are byte-identical to a pin_ file are discarded
  (standing authorization: byte-identical MD5 duplicates) and logged SKIP-DUPLICATE.
- Unique gallery-dl files move in under their own names.
- Every move/discard is logged to undo-log-photography.csv.
- Emptied source tree is removed at the end.

Usage: python pinterest_into_library.py
"""
import csv
import datetime
import hashlib
import os

SRC = r"C:\Users\Kanchan Verma\Pictures\pinterest\pinterest\Akulmach74\('-_~+')"
LIB = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
OUT_BASE = os.path.join(LIB, "Pinterest")
PIPELINE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline"
LOG = os.path.join(PIPELINE, "undo-log-photography.csv")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def log(action, frm, to, result):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["Timestamp", "Action", "From", "To", "Result"])
        w.writerow([datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), action, frm, to, result])


files = [f for f in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, f))]
pins = [f for f in files if f.startswith("pin_")]
others = [f for f in files if not f.startswith("pin_")]
print(f"source files: {len(files)} (pin_: {len(pins)}, older gallery-dl: {len(others)})", flush=True)

# md5 map of pin files (for overlap detection)
pin_hashes = {}
for f in pins:
    pin_hashes[md5(os.path.join(SRC, f))] = f

moved = discarded = 0
date_dirs = {}

def dest_for(fname):
    mtime = os.path.getmtime(os.path.join(SRC, fname))
    day = datetime.date.fromtimestamp(mtime).isoformat()
    date_dirs.setdefault(day, 0)
    date_dirs[day] += 1
    d = os.path.join(OUT_BASE, day)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, fname)

# 1. unique gallery-dl files first (so pin/id collisions by name are impossible)
seen_other_hashes = {}
for f in others:
    h = md5(os.path.join(SRC, f))
    if h in pin_hashes:
        os.remove(os.path.join(SRC, f))
        discarded += 1
        log("SKIP-DUPLICATE", os.path.join(SRC, f), f"Pinterest/{pin_hashes[h]}", "byte-identical to new pin download, copy removed")
        continue
    if h in seen_other_hashes:
        os.remove(os.path.join(SRC, f))
        discarded += 1
        log("SKIP-DUPLICATE", os.path.join(SRC, f), f"Pinterest/{seen_other_hashes[h]}", "byte-identical to another gallery-dl file, copy removed")
        continue
    seen_other_hashes[h] = f
    dst = dest_for(f)
    os.rename(os.path.join(SRC, f), dst)
    moved += 1
    log("MOVE", os.path.join(SRC, f), dst, "ok")

# 2. all pin files
for f in pins:
    dst = dest_for(f)
    os.rename(os.path.join(SRC, f), dst)
    moved += 1
    log("MOVE", os.path.join(SRC, f), dst, "ok")

print(f"moved: {moved} | discarded byte-identical: {discarded}", flush=True)
print("destination date folders:", flush=True)
for day in sorted(date_dirs):
    print(f"  Pinterest/{day}/: {date_dirs[day]} files", flush=True)

# 3. remove emptied source tree
removed = 0
for root, dirs, fnames in os.walk(SRC, topdown=False):
    if not os.listdir(root):
        os.rmdir(root)
        removed += 1
parent = os.path.dirname(SRC)
while parent.lower() != r"c:\users\kanchan verma\pictures" and os.path.isdir(parent) and not os.listdir(parent):
    os.rmdir(parent)
    removed += 1
    parent = os.path.dirname(parent)
log("CLEANUP", SRC, "(removed)", f"emptied source tree, {removed} dirs removed")
print(f"empty source dirs removed: {removed}", flush=True)
print("PINTEREST MOVE DONE", flush=True)
