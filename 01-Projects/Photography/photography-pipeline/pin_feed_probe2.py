"""Replay gallery-dl's exact BoardFeedResource request and inspect pagination fields."""
import http.cookiejar
import json

import requests

jar = http.cookiejar.MozillaCookieJar(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\pinterest-cookies.txt")
jar.load(ignore_discard=True, ignore_expires=True)
s = requests.Session()
s.cookies.update(jar)
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
    "Accept": "application/json, text/javascript, */*, q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://in.pinterest.com/",
    "X-Pinterest-AppState": "active",
    "X-APP-VERSION": "4c8c1a6",
})

path = ("/resource/BoardFeedResource/get/?data=%7B%22options%22%3A%7B%22board_id%22%3A%22"
        "877498377336046688%22%2C%22field_set_key%22%3A%22react_grid_pin%22%2C%22prepend%22%3A"
        "false%2C%22bookmarks%22%3Anull%7D%7D&source_url=")
r = s.get("https://in.pinterest.com" + path, timeout=30)
print("status:", r.status_code, "bytes:", len(r.content))
if r.status_code != 200:
    print(r.text[:300])
    raise SystemExit
j = r.json()
res = j.get("resource_response", {})
data = res.get("data")
print("resource_response keys:", sorted(res.keys()))
if isinstance(data, list):
    print("pins in page:", len(data))
    if data:
        print("first pin id:", data[0].get("id"))
opts = j.get("resource", {}).get("options", {})
bm = opts.get("bookmarks")
print("resource.options.bookmarks:", "ABSENT" if "bookmarks" not in opts else f"type={type(bm).__name__} len={len(bm) if isinstance(bm, list) else '-'}")
if isinstance(bm, list) and bm:
    print("bookmark[0] preview:", str(bm[0])[:100])
ropts = res.get("options", {})
if ropts:
    print("resource_response.options keys:", sorted(ropts.keys()))
    if "bookmarks" in ropts:
        print("response bookmarks:", str(ropts["bookmarks"])[:150])
# scan whole JSON for any cursor-like fields
def scan(obj, pathstr=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ("bookmark", "bookmarks", "cursor", "next_cursor", "nextbookmark"):
                hits.append((pathstr + "/" + k, str(v)[:80]))
            hits += scan(v, pathstr + "/" + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:3]):
            hits += scan(v, pathstr + f"[{i}]")
    return hits
for h in scan(j)[:15]:
    print("cursor-ish:", h[0], "=", h[1])
