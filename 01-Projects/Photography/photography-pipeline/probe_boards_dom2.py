"""Deeper DOM probe of the logged-in boards page: case-insensitive links,
board-card structures, and embedded state JSON.
Usage: python probe_boards_dom2.py <port>
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
    time.sleep(10)

    js = r"""
    JSON.stringify({
      links: Array.from(new Set(
        Array.from(document.querySelectorAll('a[href]'))
          .map(a => a.getAttribute('href'))
          .filter(h => h && h.toLowerCase().includes('akulmach74') && !h.toLowerCase().includes('/pin'))
      )),
      boardCards: Array.from(document.querySelectorAll('[data-test-id]'))
        .map(e => e.getAttribute('data-test-id'))
        .filter(t => t && t.toLowerCase().includes('board'))
        .filter((v, i, a) => a.indexOf(v) === i)
        .slice(0, 20),
      cardTexts: Array.from(document.querySelectorAll('[data-test-id="board-card"], [data-test-id="boardCard"]'))
        .map(e => (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80))
        .slice(0, 20),
      pwsData: (function(){
        var el = document.getElementById('__PWS_DATA__');
        return el ? el.textContent.length : 0;
      })()
    })
    """
    ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate",
                        "params": {"expression": js, "returnByValue": True}}))
    msg = recv_until(ws, want_id=3, deadline_sec=30)
    if msg and "result" in msg:
        val = msg["result"].get("result", {}).get("value")
        if val:
            d = json.loads(val)
            print("links (case-insensitive):")
            for h in sorted(set(d.get("links", []))):
                print("  " + h)
            print("board data-test-ids:", d.get("boardCards"))
            print("board card texts:")
            for t in d.get("cardTexts", []):
                print("  " + t)
            print("__PWS_DATA__ size:", d.get("pwsData"))
        else:
            print("evaluate returned null")
    else:
        print("no evaluate response")
    ws.close()


if __name__ == "__main__":
    main()
