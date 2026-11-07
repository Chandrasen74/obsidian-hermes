import os, json, csv
from datetime import datetime

PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
DESCS = os.path.join(PHOTO, "descriptions.json")
PENDING = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\pending-descs.json"
LOG = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"

def log(action, src, dst, result):
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), action, src, dst, result])

descs = json.load(open(DESCS, encoding="utf-8"))

# All 9 still-missing files (gdown rate-limited twice).
# The 3 DSCN "twins" in Camera are same-name different-bytes (raws vs deleted edits),
# so descriptions must NOT be remapped to them; park everything by basename instead.
AT_RISK = {"DSCN1325.jpg", "DSCN1326.jpg", "DSCN1328.jpg",
           "20260302_191057.jpg", "20260302_191114 (2).jpg", "20260304_112211.jpg",
           "20260304_112253.jpg", "20260304_112314.jpg", "20260304_112319.jpg"}

pending = {}
for k in list(descs):
    if os.path.basename(k) in AT_RISK:
        pending[os.path.basename(k)] = descs[k]
json.dump(pending, open(PENDING, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k in pending:
    log("DESC-PARK", k, PENDING, "desc parked until gdown re-download succeeds")
print(f"pending descs parked: {len(pending)} of 9 -> {PENDING}", flush=True)
print("PRESERVE DESCS DONE", flush=True)
