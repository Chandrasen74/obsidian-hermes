"""Probe Pinterest BoardFeedResource with the extracted cookies; inspect pagination fields.
Never prints cookie values or full pin payloads.
"""
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
    "Referer": "https://in.pinterest.com/Akulmach74/-_~%2B/",
    "X-Pinterest-AppState": "active",
})

base = "https://in.pinterest.com"
data = json.dumps({"options": {"board_id": "877498377336046688", "field_set_key": "react_grid_pin", "prepend": False, "bookmarks": None}, "context": {}})
url = f"{base}/resource/BoardFeedResource/get/?data={requests.utils.quote(data)}&source_url=%2FAkulmach74%2F-_~%252B%2F"

r = s.get(url, timeout=30)
print("status:", r.status_code, "bytes:", len(r.content))
try:
    j = r.json()
except Exception as e:
    print("not JSON:", r.text[:200])
    raise SystemExit

print("top-level keys:", sorted(j.keys()))
res = j.get("resource_response", {})
print("resource_response keys:", sorted(res.keys()))
data_resp = res.get("data", {})
print("data type:", type(data_resp).__name__)
if isinstance(data_resp, dict):
    print("data keys:", sorted(data_resp.keys())[:20])
elif isinstance(data_resp, list):
    print("data list length:", len(data_resp))
    if data_resp:
        print("first item keys:", sorted(data_resp[0].keys())[:25])
        print("first item id:", data_resp[0].get("id"))

opts = j.get("resource", {}).get("options", {})
print("resource.options.bookmarks present:", "bookmarks" in opts, "| value type:", type(opts.get("bookmarks")).__name__)
if isinstance(opts.get("bookmarks"), list) and opts["bookmarks"]:
    b = str(opts["bookmarks"][0])
    print("bookmark[0] len:", len(b), "| preview:", b[:80])
print("response options bookmarks:", res.get("options", {}).get("bookmarks", "ABSENT"))
