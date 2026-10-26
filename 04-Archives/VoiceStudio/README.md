---
name: README
tags: ["#status/archived", "#type/index", "#domain/ai-voice"]
---
# VoiceStudio (local ElevenLabs alternative) — ARCHIVED 2026-10-26

Fully-local TTS install + first Hindi↔English generation test, completed and
archived one session after it started (2026-10-25 setup → 2026-10-26 applied).

**Chosen deliverable:** `Audio\Final\final_aap-kaise-ho_female.wav`
(take 3: Devanagari `आप कैसे हो` + designed "female, young adult" voice).
Runner-up: `Audio\Final\final_aap-kaise-ho_male.wav` (take 2, romanized).
Original line: `aap kaise ho, this is a test of ElevenLabs alternative.`
(Hindi first 3 words, English rest.)

## What was set up (still installed, NOT removed)

| location | content |
|---|---|
| `C:\VoiceStudio\app` → actually `AppData\Local\Programs\VoiceStudio` | VoiceStudio Electron 0.5.6 (`VoiceStudio-Electron-0.5.6-win-x64.exe`, SHA256-verified) |
| `C:\VoiceStudio\engines` | engine sidecars (User env `OMNIVOICE_ENGINES_DIR`) |
| `C:\VoiceStudio\data` | voices, projects, DB, prefs, logs (User env `OMNIVOICE_DATA_DIR`) |
| `C:\VoiceStudio\cache` | model weights: k2-fsa/OmniVoice TTS 3.04 GB + Systran/faster-whisper-small 0.45 GB (User env `OMNIVOICE_CACHE_DIR`) |
| `AppData\Roaming\VoiceStudio\runtime` | 16.7 GB bundled Python env (one-time, owner chose to leave it in AppData) |

Revive = launch VoiceStudio from the Start menu/desktop shortcut, click
"start the local engine" on first screen; backend answers on
http://localhost:3900 (`/health`, `/openapi.json`).

**License note:** app = AGPL-3.0; OmniVoice model weights = CC-BY-NC
(non-commercial) + tokenizer notice — fine for personal use, not cleared for
commercial outputs (see VoiceStudio docs/licensing/model-inventory.md).

## Process info found along the way (lessons, 2026-10-25/26)

- **CPU-only rendering is the whole ballgame on this machine** (no NVIDIA
  GPU; Windows PyTorch is CUDA-only). A ~50-character / ~3.3 s OmniVoice
  render costs roughly 13-30 min of synthesis on 16 GB single-channel RAM.
- **RAM starvation is the #1 failure mode**: first render died at the 600 s
  default CPU budget with 0.6-1.2 GB free (Chrome/Discord + model collision),
  HTTP 503 "abandoned". Fixes that worked: close the fat apps, raise
  `OMNIVOICE_CPU_GENERATE_TIMEOUT_S` to 1800 (User env, set), leave ~5 GB
  free, and let renders run sequentially.
- A timed-out render can't be killed from outside; restart the backend to
  drop it. The app's own "abandoned job" text confirms this behavior.
- **`POST /generate` returns raw WAV bytes** (audio/wav), not a JSON
  envelope — point curl's `-o` at a `.wav` file.
- **Multipart field trick that kept Devanagari intact:** `-F "text=< <file>"`
  (angle-bracket file read) — passing Unicode text through PowerShell argv
  mangles it, file payloads don't.
- `POST /v1/audio/transcriptions` (OpenAI-style, field `file=`) is the check
  endpoint; but **must run after renders finish**, concurrent with a render
  it 504s (one CPU worker).
- Voice Design API: `instruct="female, young adult, moderate pitch"`
  (taxonomy: gender/age/pitch/style/accent/dialect), no reference audio
  needed. Vocabulary is strict (OmniVoice tags; see docs/voice-design.md).
- **ASR-small is a noisy judge for Hindi:** whatever whisper-small "heard"
  ("App Case Ho" etc.) is partly its own Hindi weakness. English segments
  decoded perfectly in ALL takes → the English half is solid regardless.
- **Devanagari payload vs romanized:** both roughly equal per the noisy ASR;
  owner's ear chose the Devanagari + female take as best.
- Freeing RAM after a churn: `POST /system/flush-memory?unload_model=true`
  (takes the model out of RAM; next render pays ~8 s lazy reload). Chrome
  reabsorbs the freed RAM instantly, which is the desired trade.
- Engine quirks seen: engine probes/"A previous engine check failed" noise on
  optional engines is harmless; only omnivoice (active) matters here.
  KittenTTS is English-only → useless for this test.

## Files in this archive

- `Audio\Final\` — 2 polished finals (trim + loudnorm, 24 kHz mono)
- `Audio\Takes\` — all 4 raw renders (also the reproducible raw outputs)
- `Documents\plan.md` — the full build plan/process checklist as executed
- `Documents\Findings.md` — test-clip verdict table + fix-up options
- `Documents\asr_take*.json` — raw transcription responses (the audit trail)
- `Payloads\text_*.txt` — exact text payloads (re-render recipes)

See also: [[01-Projects/README|01-Projects]] (completed list),
[[01-Projects/OpenCode-Tasks|OpenCode-Tasks]] session log.

---

*Archived: 2026-10-26 | Engine 0.5.6 cpu | Install verified working*
