---
name: README
tags: ["#status/active", "#type/index", "#domain/ai-voice"]
---
# VoiceStudio (local ElevenLabs alternative)

**Goal:** Fully-local voice generation (TTS) on this PC, replacing
ElevenLabs-style generation. Engine: **VoiceStudio (OmniVoice)** default,
646 languages, runs CPU-only on this hardware (no NVIDIA GPU).

**Status:** Setup in progress — see [[plan]] for decisions and checklist.

## Key facts

- App + models live OUTSIDE the vault (OneDrive must not sync ~10 GB):
  `C:\VoiceStudio\` — see [[plan]] for the exact layout.
- Generates on CPU (Intel UHD iGPU only); short clips are fine, expect slow
  first-time model download.
- Docs: https://github.com/debpalash/VoiceStudio (agent guide:
  `docs/install/agent.md`, local API: `docs/speech-platform.md`).
- Local API after launch: http://localhost:3900 (`/health`, `/openapi.json`).

## Test clip

`aap kaise ho, this is a test of ElevenLabs alternative`
(Hindi then English; both romanized + Devanagari variants; bundled voices.)

Outputs: `output/` (added below when generated).

## Notes for next AI/human

- First launch: analytics consent prompt is answered by the human.
- Model weight downloads need explicit consent after stating size + license.
- When the project completes, move to [[04-Archives/README|04-Archives]].

---

*Last updated: 2026-10-25*
