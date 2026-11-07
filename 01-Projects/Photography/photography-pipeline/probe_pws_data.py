"""Extract __PWS_DATA__ from the logged-in boards page and list all board objects.
Usage: python probe_pws_data.py <port>
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


def walk_boards(node, out):
    if isinstance(node, dict):
        if node.get("type") == "board" or ("pin_count" in node and "url" in node and node.get("url", "").startswith("/Akulmach74/") is False and "name" in node):
            pass
        # generic: any dict that looks like a board
        if isinstance(node.get("name"), str) and isinstance(node.get("id"), (int, str)) and ("pin_count" in node or node.get("type") == "board"):
            key = str(node.get("id"))
            if key not in out:
                out[key] = {
                    "name": node.get("name"),
                    "url": node.get("url"),
                    "pin_count": node.get("pin_count"),
                    "privacy": node.get("privacy"),
                    "type": node.get("type"),
                    "id": node.get("id"),
                }
        for v in node.values():
            walk_boards(v, out)
    elif isinstance(node, list):
        for v in node:
            walk_boards(v, out)


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
    time.sleep(8)
    ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate",
                        "params": {"expression": "document.getElementById('__PWS_DATA__').textContent",
                                   "returnByValue": True}}))
    msg = recv_until(ws, want_id=3, deadline_sec=30)
    ws.close()
    if not (msg and "result" in msg):
        print("no data")
        return
    raw = msg["result"].get("result", {}).get("value")
    if not raw:
        print("empty __PWS_DATA__")
        return
    data = json.loads(raw)
    out = {}
    walk_boards(data, out)
    print(f"board-like objects: {len(out)}")
    for bid, b in out.items():
        print(f"  id={b['id']} name={b['name']!r} url={b['url']} pins={b['pin_count']} privacy={b['privacy']} type={b['type']}")


if __name__ == "__main__":
    main()
