import os, json, base64, io, time, sys, subprocess, re
import urllib.request, urllib.error
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

PHOTO  = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
INDEX  = os.path.join(PHOTO, "photo-index.json")
DESCS  = os.path.join(PHOTO, "descriptions.json")
KEY_FILE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\gemini_key.txt"
GALLERY = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\build_gallery.py"
MODELS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite",
          "gemini-flash-lite-latest", "gemma-4-31b-it",
          "gemini-2.5-flash", "gemini-3.7-flash", "gemini-3.8-flash", "gemini-flash-latest"]
THINK = {}  # model -> supports thinkingConfig; models 400-ing on it get retried without
BATCH  = 15
SLEEP  = 5

key  = open(KEY_FILE, encoding="utf-8").read().strip()
HDRS = {"Content-Type": "application/json", "X-goog-api-key": key}
def url(m): return f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"

idx   = json.load(open(INDEX, encoding="utf-8"))
descs = json.load(open(DESCS, encoding="utf-8")) if os.path.exists(DESCS) else {}

todo = [it for it in idx["items"]
        if it["ext"] in (".jpg", ".jpeg", ".png", ".webp", ".bmp")
        and it["file"] not in descs]
print(f"queue: {len(todo)} images undescribed", flush=True)
if not todo:
    subprocess.run([sys.executable, GALLERY], capture_output=True)
    print("QUEUE DONE: nothing to do", flush=True); sys.exit(0)

model_dead = {}   # model -> reason (per-run state; fresh runs re-test)
done = 0

def downscale_b64(path, maxpx=768):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((maxpx, maxpx), Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=80)
    return base64.standard_b64encode(buf.getvalue()).decode()

def call_batch(b64s, model):
    n = len(b64s)
    prompt = (f"You are given {n} photos, in order (image 1 to image {n}). For EACH photo give: "
              '"desc": what it shows in max 12 words; "tags": 3-5 short lowercase tags '
              "(subjects, place type, mood). Reply ONLY as a JSON array of exactly "
              f'{n} objects in order, like [{{"i":1,"desc":"...","tags":["..."]}}, ...], no other text.')
    parts = [{"text": prompt}]
    for b in b64s:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b}})
    def send(use_think):
        gc = {"temperature": 0.2, "maxOutputTokens": 2000}
        if use_think: gc["thinkingConfig"] = {"thinkingBudget": 0}
        body = json.dumps({"contents": [{"parts": parts}], "generationConfig": gc}).encode()
        req = urllib.request.Request(url(model), data=body, headers=HDRS)
        with urllib.request.urlopen(req, timeout=240) as r:
            return json.loads(r.read().decode())
    try:
        out = send(THINK.get(model, True))
    except urllib.error.HTTPError as e:
        if e.code == 400 and THINK.get(model, True):
            e.read()
            THINK[model] = False
            print(f"  {model}: no thinkingConfig support, retrying without", flush=True)
            out = send(False)
        else:
            raise
    try:
        txt = out["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        raise ValueError("empty response")
    txt = txt.strip("`")
    if txt.lower().startswith("json"): txt = txt[4:]
    return json.loads(txt.strip())

def parse_results(arr, n):
    out = {}
    if isinstance(arr, list):
        for obj in arr:
            if not isinstance(obj, dict): continue
            try: i = int(obj.get("i"))
            except (TypeError, ValueError): continue
            if 1 <= i <= n and obj.get("desc"):
                out[i] = {"desc": str(obj["desc"])[:120],
                          "tags": [str(t)[:24] for t in (obj.get("tags") or [])][:5]}
    return out

def save():
    with open(DESCS, "w", encoding="utf-8") as f:
        json.dump(descs, f, indent=1, ensure_ascii=False)

def kill(model, reason):
    if model not in model_dead:
        model_dead[model] = reason
        print(f"  >> {model} unavailable for rest of run: {reason}", flush=True)

def _pb(valid, b64s, attempts=0):
    """Process one batch. Returns True when fully resolved, False when out of quota."""
    global done
    n = len(valid)
    if n == 0: return True
    timeouts = 0
    while True:
        attempts += 1
        if attempts > 14:
            print(f"  batch stuck ({n} imgs) - deferring to next run", flush=True)
            return True  # treat as resolved-for-now; undescribed files retry next run
        usable = [m for m in MODELS if m not in model_dead]
        if not usable:
            return False
        m = usable[0]
        try:
            arr = call_batch(b64s, m)
            timeouts = 0
            res = parse_results(arr, n)
            if len(res) == n:
                for i, it in enumerate(valid, 1):
                    descs[it["file"]] = res[i]
                done += n
                save()
                for i, it in enumerate(valid, 1):
                    print(f"  + {it['file']}: {res[i]['desc']}", flush=True)
                return True
            raise ValueError(f"got {len(res)}/{n} descriptions")
        except urllib.error.HTTPError as e:
            try: body = e.read().decode()
            except Exception: body = ""
            low = body.lower()
            if e.code == 429:
                if "per day" in low:
                    kill(m, "daily quota exhausted")
                    continue
                wait = 60
                mm = re.search(r"retry in ([\d.]+)s", body)
                if mm: wait = min(int(float(mm.group(1))) + 5, 300)
                print(f"  {m}: rate-limited, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            if e.code == 503:
                print(f"  {m}: overloaded (503), waiting 45s", flush=True)
                time.sleep(45)
                continue
            kill(m, f"HTTP {e.code}")
            continue
        except Exception as e:
            if type(e).__name__ == "TimeoutError" or "timed out" in str(e).lower():
                timeouts += 1
                if timeouts >= 3:
                    kill(m, "repeated timeouts")
                    continue
                print(f"  {m}: timeout ({timeouts}/3), retrying", flush=True)
                time.sleep(10)
                continue
            # parse or network error: retry a little, then split the batch
            if attempts >= 3 or n == 1:
                if n == 1:
                    print(f"  ! giving up for now: {valid[0]['file']} ({str(e)[:90]})", flush=True)
                    return True
                half = n // 2
                print(f"  splitting batch {n} -> {half}+{n-half}", flush=True)
                if not _pb(valid[:half], b64s[:half], attempts):
                    return False
                return _pb(valid[half:], b64s[half:], attempts)
            time.sleep(8)

def process_batch(batch):
    valid, b64s = [], []
    for it in batch:
        try:
            b64s.append(downscale_b64(os.path.join(PHOTO, it["file"].replace("/", os.sep))))
            valid.append(it)
        except Exception as e:
            print(f"  SKIP unreadable: {it['file']} ({str(e)[:80]})", flush=True)
    return _pb(valid, b64s)

batches = [todo[i:i+BATCH] for i in range(0, len(todo), BATCH)]
print(f"{len(batches)} batches of up to {BATCH}", flush=True)
stopped = None
for bi, batch in enumerate(batches, 1):
    print(f"[batch {bi}/{len(batches)}]", flush=True)
    if not process_batch(batch):
        stopped = "out of quota (all models day-capped) - rerun after reset"
        break
    time.sleep(SLEEP)

subprocess.run([sys.executable, GALLERY], capture_output=True)
print(f"QUEUE DONE: +{done} described this run, {len(descs)} total", flush=True)
if stopped: print("STOPPED EARLY:", stopped, flush=True)
