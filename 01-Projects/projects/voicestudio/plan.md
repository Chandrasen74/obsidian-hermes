---
name: plan
tags: ["#status/active", "#type/plan", "#domain/ai-voice"]
---
# VoiceStudio: Local ElevenLabs Alternative (Setup + First Test)

Created 2026-10-25. Source of truth for decisions; status tracked in [[README]].

## Goal

Install VoiceStudio (open-source, fully-local ElevenLabs alternative, AGPL-3.0)
on this PC, then generate one test clip with a **natural bundled voice**:

> `aap kaise ho, this is a test of ElevenLabs alternative`
> (first 3 words Hindi, rest English)

Pronunciation verified two ways: local ASR transcription diff + ears.

## Equipment facts (verified)

- Windows x64, Intel UHD iGPU, **no NVIDIA GPU** -> CPU-only mode (officially
  supported, slower; Windows PyTorch GPU support is NVIDIA-only anyway).
- 16 GB RAM, single channel DDR4-3200. Close RAM-heavy apps while generating.
- C: has ~428 GB free. Install needs ~10 GB total.

## Decisions (owner confirmed 2026-10-25)

| Decision | Choice |
|---|---|
| Heavy install location | Custom folder on C:, never the OneDrive vault |
| Hindi spelling | BOTH variants: romanized + Devanagari |
| Voice source | Bundled natural preset voices (no cloning) |
| Generation method | Local API (`POST /generate` on localhost:3900) |

## Install layout

- `C:\VoiceStudio\app\` — the Electron desktop app
- `C:\VoiceStudio\engines\` — engine sidecars (User env `OMNIVOICE_ENGINES_DIR`)
- `C:\VoiceStudio\data\` — voices, projects, models cache (User env `OMNIVOICE_DATA_DIR`)

The vault holds only notes + small output clips (`output/`).

## Steps

- [x] 1. `C:\VoiceStudio\` layout + User env vars (done, registry verified)
- [ ] 2. Install: `irm https://voicestudio.sh/install | iex` (downloads
      `VoiceStudio-Electron-*-win-x64.exe`, SHA256-verified, opens wizard)
- [ ] 3. MANUAL: owner clicks wizard; owner answers first-run analytics
      consent prompt (agent guide forbids doing this for them)
- [ ] 4. Backend check: `/health` at http://localhost:3900, `/openapi.json`
- [ ] 5. `GET /models`; if weights not installed -> report size + license,
      get consent, then `POST /models/install` + poll install status
- [ ] 6. Generate: OmniVoice engine (646 languages), 2 text variants
      (romanized + Devanagari) x 2-3 bundled voices, language `Auto`
- [ ] 7. Verify: transcribe each clip with local ASR, diff vs input; owner
      picks winner; save to `output/`
- [ ] 8. Report: version, engine, device (cpu), paths, reopen instructions

## Risks / fallbacks

- CPU render 10-50x slower than GPU; fine for a ~5 s clip (one-off).
- OmniVoice too heavy -> try OmniVoice GGUF or light CPU engines
  (KittenTTS / Supertonic-3 / PocketTTS) after checking Hindi support.
- Romanized Hindi pronunciation may be mangled -> Devanagari variant covers it.
- Weights may have licenses separate from the AGPL app; report before download.

## References

- Agent install guide: docs/install/agent.md (repo)
- Windows guide: docs/install/windows.md
- Engine catalog: docs/engines/README.md; performance: docs/performance.md
- Local API: docs/speech-platform.md
- [[OpenCode-Tasks]] session log
