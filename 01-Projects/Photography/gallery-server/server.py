import json
import os
import secrets
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Request, Response, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import uploads as up

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
MAX_UPLOAD_MB = int(cfg.get("MAX_UPLOAD_MB", 500))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

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
    response = await call_next(request)
    # Cache headers: derived library assets are safe to cache (private, behind auth)
    if path.startswith("/photography-library/thumbs/") or path.startswith("/photography-library/converted/") or path.startswith("/photography-library/playback/"):
        response.headers.setdefault("Cache-Control", "private, max-age=604800")
    elif path.startswith("/photography-library/"):
        response.headers.setdefault("Cache-Control", "private, max-age=86400")
    elif path == "/":
        response.headers.setdefault("Cache-Control", "private, max-age=0, must-revalidate")
    return response


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
        "max_upload_mb": MAX_UPLOAD_MB,
        "phase": 2,
    }


UPLOAD_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Upload Photos</title>
<style>
:root{--bg:#111;--card:#1c1c1c;--line:#333;--txt:#eee;--dim:#aaa;--acc:#3b6fd8;--ok:#5fb37a;--warn:#d3a84a}
*{box-sizing:border-box} body{font-family:Segoe UI,system-ui,sans-serif;background:var(--bg);color:var(--txt);margin:0;padding:16px}
.wrap{max-width:760px;margin:0 auto}
a{color:var(--acc)} h1{font-size:20px;margin:0 0 6px} p{color:var(--dim);margin:0 0 14px;font-size:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
input[type=file]{width:100%;padding:10px;border:1px dashed var(--line);border-radius:8px;background:#111;color:var(--txt)}
button{background:var(--acc);color:#fff;border:none;border-radius:8px;padding:10px 14px;font-size:14px;cursor:pointer;margin-top:10px}
button:disabled{opacity:.6;cursor:default}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
#out{white-space:pre-wrap;font:13px/1.45 Consolas,monospace;background:#0b0b0b;border:1px solid var(--line);border-radius:8px;padding:10px;min-height:44px;color:var(--dim)}
.ok{color:var(--ok)} .warn{color:var(--warn)} .err{color:#e07a7a}
</style></head><body><div class="wrap">
  <h1>Upload Photos / Videos</h1>
  <p>Files are saved to staging, hashed (MD5), and checked for duplicates against the library index. Auto-processing (date organize, thumbnails, Gemini descriptions, gallery rebuild) is added in Phase 3. <a href="/">Back to gallery</a></p>
  <div class="card">
    <form id="f">
      <input id="files" type="file" name="files" multiple accept="image/*,video/*,.heic,.heif">
      <div class="row"><button id="btn" type="submit">Upload to staging</button><span id="st" style="color:var(--dim);font-size:13px"></span></div>
    </form>
  </div>
  <div class="card"><div id="out">Ready.</div></div>
</div>
<script>
const f=document.getElementById('f'), out=document.getElementById('out'), btn=document.getElementById('btn'), st=document.getElementById('st');
f.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const files=document.getElementById('files').files;
  if(!files.length){ out.textContent='Choose one or more files first.'; return; }
  btn.disabled=true; st.textContent='Uploading...'; out.textContent='';
  const fd=new FormData();
  for(const file of files) fd.append('files', file, file.name);
  try{
    const r=await fetch('/api/upload', {method:'POST', body:fd, credentials:'same-origin'});
    const data=await r.json().catch(()=>({error:'Invalid response', status:r.status}));
    if(!r.ok){ out.innerHTML='<span class="err">Upload failed: '+(data.error||r.status)+'</span>'; }
    else {
      const lines=[];
      (data.results||[]).forEach(x=>{
        if(!x.ok) lines.push('<span class="err">ERR</span> '+esc(x.filename)+': '+esc(x.error||'failed'));
        else if(x.duplicate_of) lines.push('<span class="warn">DUP</span> '+esc(x.filename)+' (md5 '+x.md5+') -> already in library: '+esc(x.duplicate_of)+' [staged: '+esc(x.stored_name)+']');
        else lines.push('<span class="ok">OK</span>  '+esc(x.filename)+' ('+fmt(x.size)+', md5 '+x.md5+') [staged: '+esc(x.stored_name)+']');
      });
      if(data.job_ids&&data.job_ids.length) lines.push('', 'Job IDs: '+data.job_ids.join(', '));
      out.innerHTML = lines.join('\\n') || JSON.stringify(data,null,2);
    }
  }catch(err){ out.innerHTML='<span class="err">Error: '+esc(String(err))+'</span>'; }
  btn.disabled=false; st.textContent='';
});
function esc(s){ return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
function fmt(n){ if(n>1048576) return (n/1048576).toFixed(1)+' MB'; if(n>1024) return (n/1024).toFixed(0)+' KB'; return n+' B'; }
</script></body></html>"""


@app.get("/upload")
async def upload_page():
    return HTMLResponse(UPLOAD_HTML)


@app.post("/api/upload")
async def api_upload(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    jobs_data = up.load_jobs(BASE_DIR)
    results = []
    job_ids = []
    for uf in files:
        rec = await up.save_upload_file(uf, STAGING_DIR, MAX_UPLOAD_BYTES)
        if not rec.get("ok"):
            results.append(rec)
            continue
        dup = up.find_existing_by_md5(LIB_ROOT, rec["md5"])
        rec["duplicate_of"] = dup
        job = up.make_job({
            "type": "upload",
            "filename": rec["filename"],
            "stored_name": rec["stored_name"],
            "staging_path": rec["staging_path"],
            "size": rec["size"],
            "md5": rec["md5"],
            "ext": rec["ext"],
            "duplicate_of": dup,
            "note": "Staged and deduped (Phase 2). Auto-processing runs in Phase 3 worker.",
        })
        jobs_data.setdefault("jobs", []).append(job)
        job_ids.append(job["id"])
        rec["job_id"] = job["id"]
        results.append(rec)
    up.save_jobs(BASE_DIR, jobs_data)
    ok_count = sum(1 for r in results if r.get("ok"))
    dup_count = sum(1 for r in results if r.get("ok") and r.get("duplicate_of"))
    return {
        "ok": True,
        "count": len(results),
        "staged": ok_count,
        "duplicates": dup_count,
        "results": results,
        "job_ids": job_ids,
    }


@app.get("/api/jobs")
async def api_jobs():
    data = up.load_jobs(BASE_DIR)
    jobs = data.get("jobs", [])
    # newest first, limit for sanity
    jobs = list(reversed(jobs))[:100]
    return {"ok": True, "count": len(data.get("jobs", [])), "jobs": jobs}


@app.get("/api/jobs/{job_id}")
async def api_job(job_id: str):
    data = up.load_jobs(BASE_DIR)
    for j in data.get("jobs", []):
        if j.get("id") == job_id:
            return {"ok": True, "job": j}
    raise HTTPException(status_code=404, detail="Job not found")


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
    print(f"Photography Gallery Server (Phase 2) listening on http://{HOST}:{PORT}")
    print(f"Library: {LIB_ROOT}")
    print(f"Gallery: {GALLERY_HTML}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
