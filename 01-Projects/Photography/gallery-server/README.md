# Gallery Server (Phase 1)

Read-only server for `gallery.html` + `photography-library/` (LAN/Tailscale ready).

## Setup
1. Run `..\start-gallery-server.bat` from `01-Projects\Photography\` (creates venv, installs deps, starts server).
2. On first run it creates `config.json` if missing. Set a strong `TOKEN` in `config.json` (a token may already be generated if created by tooling; keep it private).
3. Open `http://127.0.0.1:8765/` and sign in with the token.

## Config
Edit `config.json` (gitignored). Key fields:
- `HOST`: `0.0.0.0` for LAN/Tailscale, `127.0.0.1` for local only
- `PORT`: default `8765`
- `TOKEN`: required when `REQUIRE_TOKEN` is true
- `REQUIRE_TOKEN`: keep `true` on LAN/Tailscale

## Access
- PC: `http://127.0.0.1:8765/`
- LAN/Tailscale: `http://<pc-ip-or-100.123.127.127>:8765/?token=<TOKEN>` once to set cookie, or use the login page.
- Do not port-forward to the public internet.

## Phase 1 scope
Serves existing `gallery.html` and mounts `photography-library/` read-only. Uploads/auto-processing/PWA are Phase 2+.
