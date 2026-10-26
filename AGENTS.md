---
name: AGENTS
tags: ["#status/active", "#type/doc", "#domain/productivity"]
---
# OpenCode Vault — Project Instructions

Personal user preferences and rules consolidated from the retired agent's memory
store (USER.md + SOUL.md notes) during the migration to OpenCode (2026-10-17).

## Identity & Workspace

- This directory (`C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode`) is the active **Obsidian Second Brain vault**. Treat it as a knowledge vault, not a typical code repo.
- Vault layout: `00-Inbox\`, `01-Projects\`, `02-Areas\`, `03-Resources\`, `04-Archives\`, plus `.obsidian\` config. Keep the PARAType structure intact when filing notes.
- Git commits in this vault use author `Chandrasen74` with email `107239606+Chandrasen74@users.noreply.github.com` (GitHub noreply, so commits link to the profile and show its avatar).

## Hard Rules

- **Do not autonomously background-scan or re-index vault files.** Ask directly whether the user has existing resource materials; only explore specific paths on request.
- **No em dashes (—) in any Discord message, draft, or outgoing text** (they look AI-generated). Use commas, periods, colons, or parentheses instead.
- Drafts the user intends to send must be **ready-to-send and copied to the system clipboard via `clip.exe`**.
- Don't commit or modify `thumbnails\` or `.obsidian\` workspace state as a side effect of other work.

## Learning & Output Style

- The user prefers **visual-first learning**: rich flowcharts and diagrams over dense text walls.
- Generate **spaced-repetition flashcards** as `#card` inline tags in study notes.
- Match reply length to the weight of the request: one-line questions get one-line answers; finished work gets a short report of what changed, what's verified, and what's left. No filler, no restating the request, no narrating tool calls. State uncertainty plainly. Depth is earned, not default.

## Environment Facts

- Local AI project (llama.cpp Qwen3.5-9B server) COMPLETED and archived 2026-10-17 at `04-Archives\Local AI (barebones)\`; revive by double-clicking `start.bat`. Model stays outside the vault in `.lmstudio`. Operational guide: `04-Archives\Local AI (barebones)\Docs\LOCAL_AI_STARTUP.md`.
- Hardware (verified 2026-10-17): no discrete NVIDIA GPU (Intel UHD iGPU only, no nvidia-smi); RAM is ONE 16 GB DDR4-3200 stick = single channel (~20 GB/s usable). llama.cpp CPU build 11633 lives inside the Local AI archive. Local LLM generation ceiling: ~3 t/s for a 9B Q4 (bandwidth-bound, math in the archive README).

- Vision/image analysis token generation on this machine runs at ~3 tokens/sec; set generous timeouts on vision tasks.
- Project `stickman-dunk` (5s crosshatch ink basketball dunk animation) finished; the whole animate workspace was archived 2026-10-25 at `04-Archives\Stickman-Basketball\` (dev piece = `Project-Files\piece-stickman-dunk`, harness = `Source-Files\animate-harness`). The sign-off gate lives in the piece's `LOG.md`. Nothing animate remains under `01-Projects`.
- Project `VoiceStudio` (local ElevenLabs-alternative TTS, Electron 0.5.6): installed and live at `C:\VoiceStudio\` (User env vars `OMNIVOICE_DATA_DIR`/`OMNIVOICE_CACHE_DIR`/`OMNIVOICE_ENGINES_DIR`; 16.7 GB Python runtime in AppData\Roaming). Project archived 2026-10-26 at `04-Archives\VoiceStudio\`; winner: `final_aap-kaise-ho_female.wav` (Devanagari + designed female voice). OmniVoice weights are CC-BY-NC (personal use only). CPU renders need fat apps closed + `OMNIVOICE_CPU_GENERATE_TIMEOUT_S=1800` (set User-scope).
- Grandpa's Moto G35 setup tools (built + archived 2026-10-26): `04-Archives\Phone-Cleaner\` (USB debloat GUI; run `Launch Phone Cleaner.bat`, needs adb) and `04-Archives\Grandpa-Launcher\` (no-Gradle Android home launcher APK `com.grannyhome.launcher`, rebuild with its `build.ps1`, keystore on disk + git-ignored, package name stays "granny" as built - owner says: for grandpa). Both folders run in place; stepwise timelines in their READMEs.
- Repo facts for the `maqc 7` GitHub project: player count does not affect reward calculation; only final-week IDs receive rewards; solo/1v1-with-bot matches work. (A match was scheduled for 9:30 PM IST on Sat, Sep 26, 2026.)

## Skills Anchored Here

- `stitch` is defined at `.opencode\skills\stitch\` (migrated from `.agents\skills\stitch`). It routes design work through the `stitch` CLI; run `stitch status --flow=design --json` when repo/dev-server state matters.
- `DESIGN.md` at the vault root is the Stitch design-system spec for this vault.
