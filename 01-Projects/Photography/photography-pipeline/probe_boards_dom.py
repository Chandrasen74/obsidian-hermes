"""Scrape the logged-in boards page of the automation Edge window via CDP.
Lists every /Akulmach74/<slug>/ link the rendered DOM contains (secret boards
appear for the owner). Never prints cookie values.
Usage: python probe_boards_dom.py <port>
"""
import json
import sys
import time
import urllib.request

import websocket


def http_json(url, method="GET"):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def recv_until(ws, want_id=None, want_method=None, deadline_sec=40):
    deadline = time.time() + deadline_sec
    while time.time() < deadline:
        try:
            msg = json.loads(ws.recv())
        except websocket.WebSocketTimeoutException:
            return None
        if want_id is not None and msg.get("id") == want_id:
            return msg
        if want_method is not None and msg.get("method") == want_method:
            return msg
    return None


def main():
    port = sys.argv[1]
    page = http_json(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
    ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60)
    ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
    recv_until(ws, want_id=1)
    ws.send(json.dumps({"id": 2, "method": "Page.navigate",
                        "params": {"url": "https://in.pinterest.com/Akulmach74/boards/"}}))
    recv_until(ws, want_id=2)
    recv_until(ws, want_method="Page.loadEventFired", deadline_sec=40)
    time.sleep(8)  # SPA render

    js = """
    JSON.stringify({
      links: Array.from(new Set(
        Array.from(document.querySelectorAll('a[href]'))
          .map(a => a.getAttribute('href'))
          .filter(h => h && h.includes('/Akulmach74/') && !h.includes('/pin/') && h !== '/Akulmach74/')
      )),
      titles: Array.from(new Set(
        Array.from(document.querySelectorAll('[data-test-id="board-title"], .boardCard h3, [title]'))
          .map(e => (e.getAttribute('title') || e.textContent || '').trim())
          .filter(t => t && t.length < 60)
      )).slice(0, 30)
    })
    """
    ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate",
                        "params": {"expression": js, "returnByValue": True}}))
    msg = recv_until(ws, want_id=3, deadline_sec=30)
    if msg and "result" in msg:
        val = msg["result"].get("result", {}).get("value")
        if val:
            d = json.loads(val)
            print("board-ish links:")
            for h in sorted(set(d.get("links", []))):
                print("  " + h)
            print("titles/texts:")
            for t in d.get("titles", []):
                print("  " + t)
        else:
            print("evaluate returned null")
    else:
        print("no evaluate response")
    ws.close()


if __name__ == "__main__":
    main()
