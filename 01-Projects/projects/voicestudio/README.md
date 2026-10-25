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

## Evening resume (owner back ~evening 2026-10-25)

1. Launch VoiceStudio via the Start menu/desktop shortcut (Chrome + Discord
   closed: leave ~4-5 GB RAM free for the model).
2. Owner answers any first-run prompt; verify /health on port 3900.
3. Rerun the 4 renders (2 texts x 2 voices), budget now 1800 s;
   save WAVs to output/, then transcription-verify + owner listens.

---

*Last updated: 2026-10-25 (night: render 1r completed & raw JSON saved to
output/gen_1r.json, romanized text + designed female voice; remaining 3
renders stopped at owner request; PC shut down overnight. Tomorrow: boot with
internet, launch app, extract WAV from gen_1r.json, rerun 2r/1d/2d, run the
faster-whisper transcription check, then owner listens and picks.*)
