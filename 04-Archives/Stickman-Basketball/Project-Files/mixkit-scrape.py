import re, json, sys, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
cats = sys.argv[1:] or ["basketball"]
out = {}
for cat in cats:
    url = f"https://mixkit.co/free-sound-effects/{cat}/"
    try:
        req = urllib.request.Request(url, headers=UA)
        html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"FAIL {cat}: {e}")
        continue
    n0 = len(out)
    blocks = html.split('class="item-grid__item"')[1:]
    for b in blocks:
        t = re.search(r'<h2 class="item-grid-card__title">\s*(?:<a[^>]*>)?\s*(.*?)\s*(?:</a>)?\s*</h2>', b, re.S)
        u = re.search(r'data-audio-player-preview-url-value="([^"]+)"', b)
        if t and u:
            title = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t.group(1))).strip()
            out[title] = u.group(1)
    print(f"{cat}: +{len(out)-n0} cards={len(blocks)} (total {len(out)})")

Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\mixkit-index.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for k, v in out.items():
    print(f"{k}  ->  {v}")
