"""OCR pass: extract visible text from screenshots, WhatsApp, Misc and Phone images.

- Adds an "ocr" field to descriptions.json entries (verbatim text found in the image).
- Makes text inside screenshots searchable in the gallery (build_gallery includes it in search).
- Resumable: images whose entry already has an "ocr" key are skipped ("" = checked, no text).
- Rebuilds the gallery at the end.

Usage: python ocr_pass.py
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
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
TARGET_PREFIXES = ("Screenshots/", "WhatsApp/", "Misc/", "Phone/")
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


def downscale_b64(path, maxpx=1024):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((maxpx, maxpx), Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=85)
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
                               "generationConfig": {"temperature": 0.1, "maxOutputTokens": 800}}).encode()
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


PROMPT = ('Extract ALL visible text in this image verbatim (signs, screens, documents, chat messages, '
          'captions, labels, handwriting). Keep the original language. Use \\n between lines. '
          'If there is no readable text, reply {"text": ""}. Reply ONLY as JSON, no other text.')

targets = [it for it in idx["items"]
           if it["ext"].lower() in IMG_EXTS
           and any(it["file"].startswith(p) for p in TARGET_PREFIXES)]
todo = [it for it in targets if "ocr" not in descs.get(it["file"], {})]

per_src = {}
for it in targets:
    src = it["file"].split("/")[0]
    per_src[src] = per_src.get(src, 0) + 1
print(f"OCR targets: {len(targets)} ({', '.join(f'{k} {v}' for k, v in sorted(per_src.items()))})", flush=True)
print(f"queue: {len(todo)} (rest already OCR-checked)", flush=True)
if not todo:
    print("OCR DONE: nothing to do", flush=True)
    sys.exit(0)

done = has_text = 0
for n, it in enumerate(todo, 1):
    p = os.path.join(PHOTO, it["file"].replace("/", os.sep))
    try:
        b64 = downscale_b64(p)
        res = call_one(b64, PROMPT)
        text = ""
        if isinstance(res, dict):
            text = str(res.get("text") or "").strip()[:600]
        entry = descs.setdefault(it["file"], {})
        entry["ocr"] = text
        done += 1
        if text:
            has_text += 1
            print(f"  + {it['file']}: {text[:70].replace(chr(10), ' / ')}", flush=True)
        if n % 5 == 0:
            save()
    except RuntimeError as e:
        print(f"STOPPED: {e}", flush=True)
        break
    except Exception as e:
        print(f"  ! failed {it['file']}: {str(e)[:90]}", flush=True)
        descs.setdefault(it["file"], {})["ocr"] = ""
    time.sleep(0.5)

save()
subprocess.run([sys.executable, GALLERY], capture_output=True)
print(f"OCR DONE: {done} checked this run, {has_text} with text, {len(descs)} description entries total", flush=True)
