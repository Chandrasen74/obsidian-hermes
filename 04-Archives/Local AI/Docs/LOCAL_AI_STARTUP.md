---
name: LOCAL_AI_STARTUP
tags: ["#status/archived", "#type/doc", "#domain/ai"]
---
# Local AI Startup Guide (llama.cpp + Qwen3.5-9B)

**Purpose:** Run local models with the barebones llama.cpp server, no LM Studio involved, plus your PySide6/QML GUI launcher

## Quick start

| Mode | How to start | What you get |
|---|---|---|
| Startup (everything) | Double-click `04-Archives\Local AI\start.bat` | Qwen3.5-9B served on `http://127.0.0.1:8080`, OpenAI-compatible API, built-in web chat UI (opens in your browser when ready) |
| GUI launcher (optional, not default) | From PowerShell: `& "...launcher\venv\Scripts\python.exe" server.py llm_launcher_config.json` | The old PySide6/QML window, still fully working |

`start.bat` runs everything in ONE window: it opens the browser chat tab, then runs the server in the foreground with the live llama.cpp log streamed below (also saved to `logs\llama_server.log`). Ready appears as llama.cpp's own `listening on http://127.0.0.1:8080` line (1-2 min on CPU for this 9B). Stop with Ctrl+C (then Y) or by closing the window.

## Endpoints (headless server)

- Web chat UI: `http://127.0.0.1:8080`
- OpenAI-compatible API: `http://127.0.0.1:8080/v1`
- Model id as seen by clients: `qwen3.5-9b` (set via `--alias`)

## OpenCode integration (archived, inactive)

The provider config was moved to `Docs\opencode.json`, so OpenCode no longer loads it. To revive: run `start.bat`, copy `Docs\opencode.json` back to the vault root, restart OpenCode, then pick `llama.cpp` → `qwen3.5-9b` in the model picker (`start.bat` sets the `--alias`, which is what the OpenCode model id matches).

## Files

- `start.bat` - THE single startup file; threads, port, context and model path are set at the top of the file
- `launcher\server.py`, `launcher\ui.qml`, `launcher\llm_launcher_config.json` - the optional GUI launcher and its model catalogue (models point at `.lmstudio` GGUFs)
- `llama.cpp\build\bin\Release\llama-server.exe` - your compiled server, build 11633, MSVC x64, CPU build (no CUDA, no Vulkan)
- Model: `%USERPROFILE%\.lmstudio\models\lmstudio-community\Qwen3.5-9B-GGUF\Qwen3.5-9B-Q4_K_M.gguf` (5.24 GB, kept outside OneDrive on purpose)

## Tuning knobs

| Knob | Default | Notes |
|---|---|---|
| `--threads` | 6 | Keeps all threads on the 6 P-cores (13620H). Bench 17-10-2026: generation 2.9 t/s at 6, 2.7 at 10, 2.6 at 16; prompt eval 34-36 t/s up to 10 threads but drops to 26 at 16. Never run 16 |
| `--ctx-size` | 8192 | KV cache RAM grows roughly linear; 16384 works too if other apps are closed |
| `--port` | 8080 | If you change it, also change `baseURL` in the archived `Docs\opencode.json` |
| `--flash-attn auto` | off by default | Optional; add in the GUI per model once the server boots fine without it |
| `--cache-type-k q8_0` + `--cache-type-v q8_0` | off by default | Halves KV cache RAM; requires flash attention; pair both with `--flash-attn auto` |

## Performance expectation

Roughly 3 to 4 tokens/sec generation on this machine; the hard ceiling is set by RAM bandwidth, not the CPU: one single 16 GB DDR4-3200 stick (single channel, ~20 GB/s) and 5.24 GB of weights per token. Measured 17-10-2026: 2.6-2.9 t/s generation, 34-36 t/s prompt processing. Prompt eval feels fast because it is compute-bound; generation is bandwidth-bound. The single biggest speed fix is a second matching DDR4-3200 SODIMM (~2x bandwidth, dual channel). A 4B-class model (~2.5 GB) would also roughly double t/s for lighter chat use.

## Troubleshooting

- **Port busy**: the bat offers to kill a stale `llama-server.exe`; manual: `taskkill /f /im llama-server.exe`
- **Window flashes and closes**: run it from PowerShell to see the error: `& "C:\Users\Kanchan Verma\OneDrive\Desktop\Hermes\04-Archives\Local AI\start.bat"`
- **Model not found**: check the `MODEL=` path at the top of the bat; it must exist outside OneDrive
- **Tail of the log**: `logs\llama_server.old.log` holds the previous run (rotated on each start)

## Notes

- The headless bat and the GUI launcher can run different servers at once if ports differ; default GUI args also use 8080, so stop one before starting the other on the same port
- `llm_launcher_config.json` in the launcher folder is the single source of truth; a stale empty copy at the vault root was removed on 2026-10-17

## See also

- [[OMNIROUTE_STARTUP]]
- [[Hermes-Tasks]]
