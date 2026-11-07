"""Describe library videos via their poster frames so gallery search covers video content.

- Finds every indexed video, locates its poster (thumbs/<rel with / -> __>.jpg).
- Sends each poster to Gemini (single-image calls, model rotation on 429).
- Writes descriptions.json entries keyed by the VIDEO path; resumable (skips already-described).
- Rebuilds the gallery at the end.

Usage: python describe_videos.py
"""
import base64
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

PHOTO = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-library"
INDEX = os.path.join(PHOTO, "photo-index.json")
DESCS = os.path.join(PHOTO, "descriptions.json")
PIPELINE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline"
KEY_FILE = os.path.join(PIPELINE, "gemini_key.txt")
GALLERY = os.path.join(PIPELINE, "build_gallery.py")
VIDEO_EXTS = (".mp4", ".avi", ".mov", ".mts", ".m2ts", ".3gp", ".mkv", ".webm", ".wmv")
MODELS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite",
          "gemini-flash-lite-latest", "gemma-4-31b-it",
          "gemini-2.5-flash", "gemini-3.7-flash", "gemini-3.8-flash", "gemini-flash-latest"]

key = open(KEY_FILE, encoding="utf-8").read().strip()
HDRS = {"Content-Type": "application/json", "X-goog-api-key": key}


def url(m):
    return f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"


idx = json.load(open(INDEX, encoding="utf-8-sig"))
descs = json.load(open(DESCS, encoding="utf-8-sig")) if os.path.exists(DESCS) else {}

model_dead = {}


def poster_for(rel):
    return os.path.join(PHOTO, "thumbs", rel.replace("/", "__") + ".jpg")


def downscale_b64(path, maxpx=768):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((maxpx, maxpx), Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=80)
    return base64.standard_b64encode(buf.getvalue()).decode()


def save():
    with open(DESCS, "w", encoding="utf-8") as f:
        json.dump(descs, f, indent=1, ensure_ascii=False)


def kill(model, reason):
    if model not in model_dead:
        model_dead[model] = reason
        print(f"  >> {model} unavailable for rest of run: {reason}", flush=True)


def call_one(b64, prompt):
    parts = [{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": b64}}]
    while True:
        usable = [m for m in MODELS if m not in model_dead]
        if not usable:
            raise RuntimeError("all models unavailable (quota?)")
        m = usable[0]
        try:
            body = json.dumps({"contents": [{"parts": parts}],
                               "generationConfig": {"temperature": 0.2, "maxOutputTokens": 300}}).encode()
            req = urllib.request.Request(url(m), data=body, headers=HDRS)
            with urllib.request.urlopen(req, timeout=240) as r:
                out = json.loads(r.read().decode())
            txt = out["candidates"][0]["content"]["parts"][0]["text"].strip()
            txt = txt.strip("`")
            if txt.lower().startswith("json"):
                txt = txt[4:]
            return json.loads(txt.strip())
        except urllib.error.HTTPError as e:
            try:
                low = e.read().decode().lower()
            except Exception:
                low = ""
            if e.code == 429:
                if "per day" in low:
                    kill(m, "daily quota exhausted")
                    continue
                mm = re.search(r"retry in ([\d.]+)s", low)
                wait = min(int(float(mm.group(1))) + 5, 300) if mm else 60
                print(f"  {m}: rate-limited, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            if e.code == 503:
                print(f"  {m}: overloaded, waiting 45s", flush=True)
                time.sleep(45)
                continue
            kill(m, f"HTTP {e.code}")
        except Exception as e:
            if "timed out" in str(e).lower():
                kill(m, "timeout")
                continue
            raise


PROMPT = ('This is a poster frame from a video. Describe what the video likely shows in max 12 words, '
          'then give 3-5 short lowercase tags (subjects, place type, mood). Reply ONLY as JSON: '
          '{"desc":"...","tags":["..."]}, no other text.')

videos = [it for it in idx["items"] if it["ext"].lower() in VIDEO_EXTS]
todo = []
no_poster = []
for it in videos:
    if it["file"] in descs:
        continue
    p = poster_for(it["file"])
    if os.path.exists(p) and os.path.getsize(p) > 0:
        todo.append((it["file"], p))
    else:
        no_poster.append(it["file"])

print(f"videos in library: {len(videos)} | already described: {len(videos) - len(todo) - len(no_poster)} "
      f"| queue: {len(todo)} | no poster: {len(no_poster)}", flush=True)
for f in no_poster:
    print(f"  NO POSTER: {f}", flush=True)

done = 0
for n, (rel, p) in enumerate(todo, 1):
    try:
        b64 = downscale_b64(p)
        res = call_one(b64, PROMPT)
        if isinstance(res, dict) and res.get("desc"):
            descs[rel] = {"desc": str(res["desc"])[:120],
                          "tags": [str(t)[:24] for t in (res.get("tags") or [])][:5],
                          "via": "poster frame"}
            done += 1
            print(f"  + {rel}: {res['desc']}", flush=True)
        else:
            print(f"  ! empty response for {rel}", flush=True)
    except RuntimeError as e:
        print(f"STOPPED: {e}", flush=True)
        break
    except Exception as e:
        print(f"  ! failed {rel}: {str(e)[:90]}", flush=True)
    if n % 5 == 0:
        save()
    time.sleep(1)

save()
subprocess.run([sys.executable, GALLERY], capture_output=True)
print(f"QUEUE DONE: +{done} videos described, {len(descs)} description entries total", flush=True)
