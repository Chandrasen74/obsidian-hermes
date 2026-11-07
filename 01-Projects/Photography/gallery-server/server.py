import json
import os
import secrets
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
EXAMPLE_CONFIG_PATH = BASE_DIR / "config.example.json"
DEFAULT_TOKEN = "CHANGE-ME-generate-a-long-random-token"


def load_config() -> dict:
    path = CONFIG_PATH if CONFIG_PATH.exists() else EXAMPLE_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # Env overrides (useful for Task Scheduler / testing)
    for key in ("HOST", "PORT", "TOKEN", "REQUIRE_TOKEN", "LIB_ROOT", "GALLERY_HTML"):
        env = os.environ.get(f"PG_{key}")
        if env is not None:
            if key == "PORT":
                cfg[key] = int(env)
            elif key == "REQUIRE_TOKEN":
                cfg[key] = env.lower() in ("1", "true", "yes", "on")
            else:
                cfg[key] = env
    return cfg


cfg = load_config()


def resolve_path(p: str) -> Path:
    pp = Path(p)
    if not pp.is_absolute():
        pp = (BASE_DIR / pp).resolve()
    return pp


HOST = cfg.get("HOST", "0.0.0.0")
PORT = int(cfg.get("PORT", 8765))
TOKEN = str(cfg.get("TOKEN", ""))
REQUIRE_TOKEN = bool(cfg.get("REQUIRE_TOKEN", True))
LIB_ROOT = resolve_path(cfg.get("LIB_ROOT", "../photography-library"))
GALLERY_HTML = resolve_path(cfg.get("GALLERY_HTML", "../gallery.html"))
STAGING_DIR = resolve_path(cfg.get("STAGING_DIR", "../photography-staging"))

app = FastAPI(title="Photography Gallery Server", docs_url=None, redoc_url=None)


def token_ok(request: Request) -> bool:
    if not REQUIRE_TOKEN:
        return True
    if not TOKEN or TOKEN == DEFAULT_TOKEN:
        # Unsafe configuration: refuse unless explicitly local-only override
        if HOST not in ("127.0.0.1", "localhost"):
            return False
    supplied: Optional[str] = None
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        supplied = auth[7:].strip()
    if not supplied:
        supplied = request.cookies.get("pg_token")
    if not supplied:
        supplied = request.query_params.get("token")
    if not supplied:
        return False
    return secrets.compare_digest(supplied, TOKEN)


LOGIN_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gallery Login</title>
<style>
body{font-family:Segoe UI,system-ui,sans-serif;background:#111;color:#eee;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0}
form{background:#1c1c1c;border:1px solid #333;border-radius:12px;padding:20px;width:min(92vw,360px)}
h1{font-size:18px;margin:0 0 12px}
input,button{width:100%;box-sizing:border-box;padding:10px 12px;border-radius:8px;border:1px solid #333;font-size:14px}
input{background:#111;color:#eee;margin-bottom:10px}
button{background:#3b6fd8;color:#fff;border:none;cursor:pointer}
p{color:#aaa;font-size:13px;margin:10px 0 0}
</style></head><body>
<form method="post" action="/login">
  <h1>Photography Gallery</h1>
  <input type="password" name="token" placeholder="Access token" autocomplete="current-password" autofocus required>
  <input type="hidden" name="next" value="{next}">
  <button type="submit">Sign in</button>
  <p>Token is required for access.</p>
</form></body></html>"""


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path
    if path in ("/login", "/api/health"):
        return await call_next(request)

    # If a valid token is provided in the query string (bootstrap link), set a cookie
    # and redirect to strip the token from the URL so subresources (images) authenticate.
    qtoken = request.query_params.get("token")
    if qtoken and REQUIRE_TOKEN and TOKEN and secrets.compare_digest(qtoken, TOKEN):
        resp = RedirectResponse(url=request.url.path, status_code=302)
        resp.set_cookie("pg_token", TOKEN, httponly=True, samesite="lax", path="/")
        return resp

    if not token_ok(request):
        if path.startswith("/api/"):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        nxt = request.url.path
        if request.url.query:
            nxt += "?" + request.url.query
        return HTMLResponse(LOGIN_HTML.replace("{next}", nxt.replace('"', "&quot;")), status_code=401)
    return await call_next(request)


@app.get("/login")
async def login_get(next: str = "/"):
    return HTMLResponse(LOGIN_HTML.replace("{next}", next.replace('"', "&quot;")))


@app.post("/login")
async def login_post(request: Request):
    form = await request.form()
    supplied = str(form.get("token", ""))
    nxt = str(form.get("next", "/")) or "/"
    if not nxt.startswith("/"):
        nxt = "/"
    if REQUIRE_TOKEN and TOKEN and secrets.compare_digest(supplied, TOKEN):
        resp = RedirectResponse(url=nxt, status_code=302)
        resp.set_cookie("pg_token", TOKEN, httponly=True, samesite="lax", path="/")
        return resp
    return HTMLResponse(LOGIN_HTML.replace("{next}", nxt.replace('"', "&quot;")) + "<script>document.querySelector('p').textContent='Invalid token.';</script>", status_code=401)


@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "require_token": REQUIRE_TOKEN,
        "lib_exists": LIB_ROOT.exists(),
        "gallery_exists": GALLERY_HTML.exists(),
        "unsafe_token_default": (TOKEN == DEFAULT_TOKEN or not TOKEN) and HOST not in ("127.0.0.1", "localhost"),
    }


@app.get("/api/info")
async def info():
    # Non-sensitive config info for the UI
    return {
        "host": HOST,
        "port": PORT,
        "lib_root": str(LIB_ROOT),
        "gallery": str(GALLERY_HTML),
        "staging": str(STAGING_DIR),
        "phase": 1,
    }


@app.get("/")
async def root():
    if not GALLERY_HTML.exists():
        raise HTTPException(status_code=404, detail=f"Gallery file not found: {GALLERY_HTML}")
    return FileResponse(str(GALLERY_HTML), media_type="text/html")


# Serve the photography library (thumbs, playback, converted, originals) read-only.
# Mounted after explicit routes; StaticFiles is safe against path traversal.
if LIB_ROOT.exists():
    app.mount("/photography-library", StaticFiles(directory=str(LIB_ROOT)), name="photography-library")


def main():
    import uvicorn

    if REQUIRE_TOKEN and (not TOKEN or TOKEN == DEFAULT_TOKEN) and HOST not in ("127.0.0.1", "localhost"):
        raise SystemExit(
            "Refusing to start: TOKEN is still the default placeholder while HOST is not localhost. "
            "Set a strong TOKEN in gallery-server/config.json (copy from config.example.json)."
        )
    LIB_ROOT.mkdir(parents=True, exist_ok=True)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / cfg.get("LOG_DIR", "logs")).mkdir(parents=True, exist_ok=True)
    print(f"Photography Gallery Server (Phase 1) listening on http://{HOST}:{PORT}")
    print(f"Library: {LIB_ROOT}")
    print(f"Gallery: {GALLERY_HTML}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
