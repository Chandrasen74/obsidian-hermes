"""Download all pins from all accessible boards of the logged-in session.

- Extracts full board feed via BoardFeedResource pagination (real session cookies).
- Downloads largest available image per pin, idempotent by pin id.
- Logs every download to pinterest-download-log.csv.

Usage: python pin_download.py
"""
import csv
import datetime
import http.cookiejar
import json
import os
import time

import requests

COOKIE_FILE = r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\pinterest-cookies.txt"
BASE = "https://in.pinterest.com"
USER = "Akulmach74"
OUT_ROOT = r"C:\Users\Kanchan Verma\Pictures\pinterest\pinterest\Akulmach74"
LOG_FILE = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\pinterest-download-log.csv"

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


def paginate(resource, options, source_url="", max_pages=60, sleep=0.8):
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
        if not key or key == "-end-" or key.startswith("Y2JOb25lO") or key in seen_bookmarks:
            return results, "end"
        seen_bookmarks.add(key)
        options = dict(options)
        options["bookmarks"] = bm
        time.sleep(sleep)
    return results, "maxpages"


def log_row(action, detail, status):
    new = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["Timestamp", "Action", "Detail", "Status"])
        w.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action, detail, status])


def best_image(pin):
    imgs = pin.get("images") or {}
    if not isinstance(imgs, dict):
        return None
    if isinstance(imgs.get("orig"), dict) and imgs["orig"].get("url"):
        return imgs["orig"]["url"]
    for size in ("736x", "474x", "236x"):
        u = imgs.get(size, {})
        if isinstance(u, dict) and u.get("url"):
            return u["url"]
    return None


def download_board(board_name, board_id, source_url):
    out_dir = os.path.join(OUT_ROOT, board_name)
    os.makedirs(out_dir, exist_ok=True)
    print(f"board {board_name!r} ({board_id}): fetching feed...")
    pins, how = paginate("BoardFeed", {
        "board_id": board_id, "field_set_key": "react_grid_pin",
        "prepend": False, "bookmarks": None,
    }, source_url=source_url)
    uniq = {}
    for p in pins:
        if isinstance(p, dict) and p.get("id"):
            uniq[str(p["id"])] = p
    print(f"  {len(uniq)} unique pins (stop={how})")
    ok = skip = fail = 0
    for i, (pid, p) in enumerate(sorted(uniq.items()), 1):
        url = best_image(p)
        if not url:
            log_row("download", f"pin {pid}", "no-media-url")
            fail += 1
            continue
        ext = os.path.splitext(url.split("?")[0])[1].lower() or ".jpg"
        dest = os.path.join(out_dir, f"pin_{pid}{ext}")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skip += 1
            continue
        try:
            r = s.get(url, timeout=60)
            if r.status_code == 200 and r.content:
                with open(dest, "wb") as f:
                    f.write(r.content)
                log_row("download", f"pin {pid} <- {url}", f"ok {len(r.content)} B")
                ok += 1
            else:
                log_row("download", f"pin {pid} <- {url}", f"HTTP {r.status_code}")
                fail += 1
        except Exception as e:
            log_row("download", f"pin {pid} <- {url}", f"error {e}")
            fail += 1
        if i % 10 == 0:
            print(f"  ...{i}/{len(uniq)}")
        time.sleep(0.3)
    print(f"  downloaded={ok} skipped={skip} failed={fail}")
    return len(uniq), ok, skip, fail


def main():
    # who is logged in
    j = call("UserSettings", {"field_set_key": "detailed"})
    if isinstance(j, dict):
        d = j.get("resource_response", {}).get("data", {})
        for k in ("username", "full_name", "email"):
            if isinstance(d, dict) and d.get(k):
                print(f"logged in as: {k}={d[k]!r}")

    # board diagnostics: show the nameless entry's keys
    boards, _ = paginate("Boards", {
        "sort": "last_pinned_to", "field_set_key": "profile_grid_item",
        "filter_stories": False, "username": USER, "page_size": 25,
        "include_archived": True,
    })
    targets = []
    for b in boards:
        if not isinstance(b, dict) or not b.get("id"):
            continue
        if b.get("url") and b.get("name"):
            slug = b["url"].rstrip("/")
            board_slug = slug.rsplit("/", 1)[-1]
            targets.append((b["name"], str(b["id"]), board_slug, b.get("pin_count")))
        else:
            print("nameless board entry keys:", sorted(b.keys()))
            print("  id:", b.get("id"), "type:", b.get("type"), "privacy:", b.get("privacy"))

    total_pins = total_ok = total_skip = total_fail = 0
    for name, bid, slug, cnt in targets:
        n, ok, skip, fail = download_board(name, bid, f"/{USER}/{slug}/")
        total_pins += n
        total_ok += ok
        total_skip += skip
        total_fail += fail
    print(f"TOTAL: pins={total_pins} downloaded={total_ok} skipped={total_skip} failed={total_fail}")
    log_row("summary", f"pins={total_pins} ok={total_ok} skip={total_skip} fail={total_fail}", "done")


if __name__ == "__main__":
    main()
