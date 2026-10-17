---
name: README
tags: ["#status/archived", "#type/index", "#domain/ai"]
---
# Local AI Archive

**Status:** COMPLETED
**Date Archived:** 2026-10-17
**Project Type:** Local LLM Server (barebones llama.cpp, CPU, Windows)

---

## To Run (the whole project in one double-click)

1. Double-click `start.bat` (top of this folder)
2. Browser opens `http://127.0.0.1:8080` with the built-in chat UI; the tab may show a load error until the model finishes loading
3. Ready appears as llama.cpp's own `listening on http://127.0.0.1:8080` line in the same window (live log also streams there)
4. OpenAI-compatible API: `http://127.0.0.1:8080/v1`, model id `qwen3.5-9b`
5. Stop: Ctrl+C (then Y), or just close the window

Everything is self-contained: `start.bat` resolves paths relative to its own folder, and the 5.24 GB model lives outside the vault at `%USERPROFILE%\.lmstudio\models\lmstudio-community\Qwen3.5-9B-GGUF\Qwen3.5-9B-Q4_K_M.gguf`. Verified to run from this archived location on 2026-10-17.

---

## Summary

A barebones llama.cpp server for Qwen3.5-9B on Windows, built on the user's own llama.cpp compile (build 11633, MSVC x64, CPU) plus the PySide6/QML GUI launcher written earlier in the project. Final形态: one startup file (`start.bat`) running the server in the foreground with live output teed to `logs\llama_server.log`, browser auto-open, port-conflict recovery and log rotation. Work included wiring the launcher config (executable + clean args + `--alias`), end-to-end endpoint verification, a llama-bench tuning pass, and an OpenCode provider config (archived inert after the decision to skip OpenCode usage). The GUI launcher remains fully optional and functional; a TUI launcher idea was dropped before implementation.

---

## Archive Contents

```
Local AI/
├── start.bat                     ← the single startup file (revive the project)
├── README.md                     ← this index
├── Docs/
│   ├── LOCAL_AI_STARTUP.md       ← full operating guide (paths updated to archive)
│   └── opencode.json             ← archived OpenCode provider config (inactive)
├── launcher/
│   ├── server.py, ui.qml         ← optional PySide6/QML GUI launcher
│   ├── llm_launcher_config.json  ← model catalogue (points at .lmstudio GGUFs)
│   ├── scan_models.py
│   ├── venv/                     (Python 3.14 + PySide6)
│   └── logs/
├── llama.cpp/                    ← full source clone + compiled build 11633 (CPU, no CUDA/Vulkan)
└── logs/                         ← server logs (rotated on each start)
```

---

## To-Do List

**Completed:**
- [x] llama.cpp clone compiled and verified (smoke test, build 11633)
- [x] Launcher config wired: default executables, clean default args, per-model `--alias qwen3.5-9b`
- [x] Single startup file `start.bat`: one window, tee logging, browser auto-open, stale-port recovery
- [x] End-to-end verified: `/health`, `/v1/models`, real chat completion (latency 3 s cold start)
- [x] OpenCode provider configured, then archived inert (OpenCode usage skipped by decision)
- [x] llama-bench thread sweep and performance ceiling documented
- [x] Cleanup: RUN bats consolidated, stale root config deleted, textual dependency removed

**Future Tasks:**
- [ ] Optional hardware upgrade: second DDR4-3200 SODIMM for dual channel (roughly 2x generation speed)
- [ ] Optional: 4B-class model (~2.5 GB) for roughly 8 t/s chat
- [ ] Optional: copy `Docs\opencode.json` back to the vault root to use the model inside OpenCode

---

## Key Information

**Measured 2026-10-17 (llama-bench, single repeat):**

| threads | prompt eval (pp128) | generation (tg96) |
|---|---|---|
| 6 | 33.8 t/s | 2.9 t/s |
| 10 | 35.8 t/s | 2.7 t/s |
| 16 | 25.9 t/s | 2.6 t/s |

**Why the ceiling exists:** one single 16 GB DDR4-3200 stick (single channel, ~20 GB/s usable) must stream 5.24 GB of weights per generated token, so ~3.8 t/s theoretical max, measured 2.6-2.9. Generation is RAM-bandwidth-bound; prompt processing is compute-bound (34-36 t/s). Machine: i7-13620H (6 P + 4 E cores, threads pinned to 6 P-cores), Intel UHD iGPU only, no discrete NVIDIA GPU.

---

## Notes for Next AI/Human

- `start.bat` only needs its sibling `llama.cpp\build\bin\Release\llama-server.exe` plus the model in `.lmstudio`; no registry, service or PATH dependencies
- Thinking mode (Qwen3.5 template with `--jinja`) is ON by default: answers first emit reasoning not shown in `content`. Per request off: `chat_template_kwargs: {"enable_thinking": false}`, or the web UI toggle
- GUI launcher manual start: `launcher\venv\Scripts\python.exe server.py llm_launcher_config.json`
- `Docs\LOCAL_AI_STARTUP.md` has the tuning knobs, troubleshooting steps and the full operational guide
- Archives are read-only for reference; reviving is simply running `start.bat`

---

*Last Updated: 2026-10-17*

## See also

[[04-Archives/README|README]]
[[OMNIROUTE_STARTUP]]
