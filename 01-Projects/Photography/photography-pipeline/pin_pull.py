"""Custom Pinterest board scraper using the user's real session cookies.

Read-only probe mode: enumerates boards, paginates board feeds, reports counts.
Never prints cookie values.

Usage: python pin_pull.py
"""
import http.cookiejar
import json
import sys
import time

import requests

COOKIE_FILE = r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\pinterest-cookies.txt"
BASE = "https://in.pinterest.com"
USER = "Akulmach74"

jar = http.cookiejar.MozillaCookieJar(COOKIE_FILE)
jar.load(ignore_discard=True, ignore_expires=True)

s = requests.Session()
s.cookies.update(jar)
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
    "Accept": "application/json, text/javascript, */*, q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "X-APP-VERSION": "a89153f",
    "X-Pinterest-AppState": "active",
    "X-Pinterest-PWS-Handler": "www/[username].js",
    "Alt-Used": "in.pinterest.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
})


def call(resource, options, source_url=""):
    payload = json.dumps({"options": options}, separators=(",", ":"))
    url = f"{BASE}/resource/{resource}Resource/get/"
    r = s.get(url, params={"data": payload, "source_url": source_url}, timeout=30)
    if r.status_code != 200:
        return ("HTTP", r.status_code, r.text[:120])
    return r.json()


def paginate(resource, options, source_url="", max_pages=40, sleep=1.0):
    seen_bookmarks = set()
    results = []
    for page in range(max_pages):
        j = call(resource, options, source_url)
        if isinstance(j, tuple):
            print(f"  page {page}: ERROR {j}")
            return results, "error"
        res = j.get("resource_response", {})
        data = res.get("data")
        if isinstance(data, dict):
            data = data.get("results", [])
        batch = data if isinstance(data, list) else []
        results.extend(batch)
        bm = j.get("resource", {}).get("options", {}).get("bookmarks") or []
        key = bm[0] if bm else ""
        print(f"  page {page}: +{len(batch)} pins (total {len(results)}), bookmark={'END' if not key or key=='-end-' or key.startswith('Y2JOb25lO') else key[:24]+'...'}")
        if not key or key == "-end-" or key.startswith("Y2JOb25lO") or key in seen_bookmarks:
            return results, "end"
        seen_bookmarks.add(key)
        options = dict(options)
        options["bookmarks"] = bm
        time.sleep(sleep)
    return results, "maxpages"


def main():
    # 1. session validation: own-profile signal
    j = call("UserSettings", {"field_set_key": "detailed"})
    if isinstance(j, tuple):
        print("UserSettings probe:", j)
    else:
        d = j.get("resource_response", {}).get("data", {})
        print("UserSettings: keys =", sorted(d.keys())[:12] if isinstance(d, dict) else type(d).__name__)

    # 2. enumerate boards
    print("boards:")
    boards, how = paginate("Boards", {
        "sort": "last_pinned_to", "field_set_key": "profile_grid_item",
        "filter_stories": False, "username": USER, "page_size": 25,
        "include_archived": True,
    })
    for b in boards:
        if isinstance(b, dict) and b.get("id"):
            print(f"  board: {b.get('name')!r} slug={b.get('url')} pins={b.get('pin_count')} id={b.get('id')} privacy={b.get('privacy')}")

    # 3. paginate the known board
    print("board feed ('-_~+'):")
    pins, how = paginate("BoardFeed", {
        "board_id": "877498377336046688", "field_set_key": "react_grid_pin",
        "prepend": False, "bookmarks": None,
    }, source_url=f"/{USER}/-_~%2B/")
    print(f"board feed result: {len(pins)} pins, stop={how}")
    ids = [p.get("id") for p in pins if isinstance(p, dict)]
    print("unique pin ids:", len(set(ids)))
    # media types
    kinds = {}
    for p in pins:
        if not isinstance(p, dict):
            continue
        if p.get("videos"):
            kinds["video"] = kinds.get("video", 0) + 1
        elif p.get("is_video") or p.get("video_list"):
            kinds["video2"] = kinds.get("video2", 0) + 1
        else:
            kinds["image"] = kinds.get("image", 0) + 1
    print("media kinds:", kinds)
    # sample image url shapes
    for p in pins[:2]:
        if isinstance(p, dict):
            imgs = p.get("images", {})
            print("  sample images keys:", sorted(imgs.keys()) if isinstance(imgs, dict) else type(imgs).__name__)


if __name__ == "__main__":
    main()
