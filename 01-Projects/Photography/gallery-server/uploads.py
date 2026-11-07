import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

ALLOWED_EXTS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heic", ".heif",
    ".mp4", ".mov", ".avi", ".mts", ".m4v", ".3gp",
}


def _jobs_path(base_dir: Path) -> Path:
    p = base_dir / "jobs.json"
    return p


def load_jobs(base_dir: Path) -> Dict[str, Any]:
    p = _jobs_path(base_dir)
    if not p.exists():
        return {"jobs": []}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"jobs": []}


def save_jobs(base_dir: Path, data: Dict[str, Any]) -> None:
    p = _jobs_path(base_dir)
    tmp = p.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)


def load_index_md5_set(lib_root: Path) -> set:
    idx_path = lib_root / "photo-index.json"
    if not idx_path.exists():
        return set()
    try:
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = json.load(f)
        items = idx.get("items", idx) if isinstance(idx, dict) else idx
        out = set()
        for it in items:
            m = it.get("md5") or it.get("hash")
            if m:
                out.add(str(m).lower())
        return out
    except Exception:
        return set()


def find_existing_by_md5(lib_root: Path, md5: str) -> Optional[str]:
    idx_path = lib_root / "photo-index.json"
    if not idx_path.exists():
        return None
    try:
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = json.load(f)
        items = idx.get("items", idx) if isinstance(idx, dict) else idx
        m = md5.lower()
        for it in items:
            im = str(it.get("md5") or it.get("hash") or "").lower()
            if im == m:
                return it.get("file")
        return None
    except Exception:
        return None


def safe_filename(name: str) -> str:
    name = os.path.basename(name or "upload")
    # keep simple chars; replace others
    cleaned = []
    for ch in name:
        if ch.isalnum() or ch in " ._-()":
            cleaned.append(ch)
        else:
            cleaned.append("_")
    out = "".join(cleaned).strip().strip(".") or "upload"
    return out[:180]


async def save_upload_file(upload, staging_dir: Path, max_bytes: int) -> Dict[str, Any]:
    staging_dir.mkdir(parents=True, exist_ok=True)
    original = safe_filename(getattr(upload, "filename", None) or "upload")
    ext = os.path.splitext(original)[1].lower()
    if ext not in ALLOWED_EXTS:
        return {"ok": False, "error": f"File type not allowed: {ext or '(none)'}", "filename": original}

    uid = uuid.uuid4().hex[:12]
    ts = time.strftime("%Y%m%d-%H%M%S")
    stored_name = f"{ts}-{uid}-{original}"
    dest = staging_dir / stored_name

    h = hashlib.md5()
    size = 0
    try:
        with open(dest, "wb") as f:
            while True:
                chunk = await upload.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    try:
                        f.close()
                    finally:
                        try:
                            dest.unlink(missing_ok=True)
                        except Exception:
                            pass
                    return {"ok": False, "error": f"File too large (limit {max_bytes} bytes)", "filename": original}
                h.update(chunk)
                f.write(chunk)
    finally:
        try:
            await upload.close()
        except Exception:
            pass

    return {
        "ok": True,
        "filename": original,
        "stored_name": stored_name,
        "staging_path": str(dest),
        "size": size,
        "md5": h.hexdigest(),
        "ext": ext,
    }


def make_job(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": uuid.uuid4().hex,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "staged",  # staged -> queued/processing -> done/failed (Phase 3 worker)
        **record,
    }
