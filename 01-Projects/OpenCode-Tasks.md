---
name: OpenCode-Tasks
tags: ["#status/active", "#type/project", "#domain/productivity"]
---
# OpenCode Task Log & To-Do List

This note tracks our ongoing work on your Obsidian second brain vault. I'll update it after each session to maintain context.

## Completed Sessions
- [x] Initial vault setup with Worksheet X-A template- [x] Git repository initialized and connected to GitHub
- [x] MAQC-7 project extracted and organized
- [x] Created root and Worksheet README files
- [x] Added omniroute launcher and backup command
- [x] Configured obsidian-second-brain skill (already existed)
- [x] PARA folder structure implemented (Projects, Areas, Resources, Archives, Inbox)
- [x] MAQC Season 7 rewards processed and logged
- [x] AI Learning System (Learn) adapted, demoed, and archived to [[04-Archives/Learn/README|README]]
- [x] Obsidian graph view optimized with tags and wikilinks
- [x] Migrated the old agent setup to OpenCode (85 skills, memory consolidated into AGENTS.md rules)
- [x] Local AI / llama.cpp server project shipped, verified, then archived to [[04-Archives/Local AI/README|Local AI archive]]
- [x] Omniroute launcher retired to [[04-Archives/Omniroute/README|Omniroute archive]] (daily flow is OpenCode now)
- [x] Vault reorganised: PARA indexes cross-linked, all content git-versioned and pushed to GitHub

## Current Focus
- [ ] Task list maintenance (this note)
- [ ] Ready for next active project

*(VoiceStudio completed & archived 2026-10-26 → [[04-Archives/VoiceStudio/README|archive]]; install remains live at `C:\VoiceStudio`)*

## Next Steps / Ideas
- [ ] Explore Obsidian plugins for visualization (Dataview, Excalidraw, Calendar)
- [ ] Set up daily notes workflow
- [ ] Create template notes for common task types

## Session Notes

### Session: 2026-11-07 - Grandpa phone archives merged, stale grandma-launcher cleared

- Merged `04-Archives/Phone-Cleaner` + `04-Archives/Grandpa-Launcher` into one
  navigable archive: [[04-Archives/Grandpa-Phone-Setup/README|Grandpa-Phone-Setup]]
  (navigation table, quick how-to, phone note: Moto G35, Android 15, Ontim
  ROM). Both subfolders keep original names, so relative paths + how-to
  commands still work; the keystore gitignore line was repointed.
- Stale wikilinks fixed in both the tool READMEs, 01-Projects/README,
  OpenCode-Tasks, and AGENTS.md env facts. No content dropped.
- Deleted `01-Projects/grandma-launcher/` per owner call (verified untracked;
  contained only a stitch tool-state `.freebuff\` + an empty
  `stitch-variants\` folder, nothing else).

### Session: 2026-11-07 - closed + archived: Coolita TV attempt (CleanYourTV)

- Infinix TV runs **Coolita TV OS**, not Android: no browser, no APK install
  path, multiple attempt routes all blocked; the cleanyourtv ADB debloat method
  never applied (upstream's own rule: non-Android sets = stop).
- The workaround that was staged: `work\apks\` USB page ("Infinix Break-in")
  hosting `ActivityLauncher-2.4.1.apk`; failed with the above.
- Archived whole to [[04-Archives/Coolita-TV-Attempt/README|04-Archives/Coolita-TV-Attempt]]:
  `Project-Files\cleanyourtv` (upstream copy + break-in kit, APK committed per
  owner override) + `Git-Metadata\` (upstream clone's .git, merged in from the
  old `cleanyourtv-origin-clone` shell, now removed). Indexes refreshed
  ([[01-Projects/README|01-Projects]], [[04-Archives/README|04-Archives]]).

### Session: 2026-10-26 (late afternoon) — archived same-day builds: Phone Cleaner + Grandpa-Home launcher

Owner-built (with a parallel agent) device-setup pair for grandpa's Moto G35,
archived per owner request with stepwise creation timelines:
- `04-Archives/Phone-Cleaner/` - USB debloat GUI (PhoneCleaner.ps1 + bat +
  removed-apps.json + pin_apps.py uiautomator2 pinner), original README kept,
  index at [[04-Archives/Grandpa-Phone-Setup/Phone-Cleaner/Archive-README|Archive-README]]
  (merged into Grandpa-Phone-Setup 2026-11-07).
- `04-Archives/Grandpa-Launcher/` - no-Gradle Android launcher APK
  (com.grannyhome.launcher, build.ps1 aapt2+javac+d8 pipeline, config.json
  favorites/folders, skycon weather views, LiquidBatteryView, dist\Home.apk
  v1.0), stepwise timeline 16:22-17:54 in
  [[04-Archives/Grandpa-Phone-Setup/Grandpa-Launcher/README|README]]. Keystore kept on disk +
  OneDrive, git-ignored (signing keys never publish).
- Package naming note: internal name says "granny" (as built); owner
  clarified it is for grandpa; renaming the package/key would break the
  installed APK's update path, so kept.
- `01-Projects\` index updated; both folders moved whole (relative paths
  keep every script runnable from the archive location).

### Session: 2026-10-25/26 — COMPLETED: VoiceStudio install + first TTS test

**Setup & test (full process details in [[04-Archives/VoiceStudio/README|archive README]]):**
- New project `01-Projects/projects/voicestudio/` registered (plan + README).
- Installed VoiceStudio Electron 0.5.6; owner-approved location split:
  data/cache/engines at `C:\VoiceStudio\` via User env vars; 16.7 GB Python
  runtime left in AppData.
- Backend verified CPU-only (correct for this hardware); installed with
  consent: OmniVoice TTS 3.04 GB (CC-BY-NC weights) + faster-whisper-small
  0.45 GB into `C:\VoiceStudio\cache`.
- 503'd renders diagnosed as RAM starvation; fixed via closing fat apps +
  `OMNIVOICE_CPU_GENERATE_TIMEOUT_S=1800`; 4 takes rendered (2 spellings x
  2 designed voices) + finals trimmed/loudnorm-ed (ffmpeg).
- ASR verification pass run; English half clean in all takes; owner picked
  **female (Devanagari, take 3)** as best → `final_aap-kaise-ho_female.wav`.
- **Archived 2026-10-26** to [[04-Archives/VoiceStudio/README|04-Archives/VoiceStudio]]
  (README + Audio\Final + Audio\Takes + Documents + Payloads); project folder
  cleared; install stays live for future use.

### Session: 2026-10-25 (afternoon)

**VoiceStudio install + first TTS test (paused at render stage):**
- New project `01-Projects/projects/voicestudio/` registered ([[plan]] + [[README]]).
- Installed VoiceStudio Electron 0.5.6 (`VoiceStudio-Electron-0.5.6-win-x64.exe`,
  SHA256 ok). Data/cache/engines relocated to `C:\VoiceStudio\` via User env vars
  (`OMNIVOICE_DATA_DIR`, `OMNIVOICE_CACHE_DIR`, `OMNIVOICE_ENGINES_DIR`);
  16.7 GB Python runtime stays in AppData (owner-approved split).
- Backend verified: /health ok, device=cpu (correct: no NVIDIA GPU).
- Consent given -> installed OmniVoice TTS 3.04 GB (CC-BY-NC weights,
  personal use) + faster-whisper-small 0.45 GB into C:\VoiceStudio\cache.
- First generate 503'd at the 600 s CPU budget under RAM starvation
  (Chrome/Discord ate the RAM). VoiceStudio killed for the afternoon per
  owner; evening relaunch: app only, budget raised to 1800 s, rerun 4 renders.
- Owner heading out; PC stays on; OpenCode terminal closable.
- Evening: RAM freed (closed Chrome/Edge/webview/copilot/plarium ~4 GB),
  backend verified (hf cache on C:\VoiceStudio\cache), job 1r rendered
  HTTP 200 (romanized + "female, young adult, moderate pitch").
- Night: owner cut internet; renders stopped mid-job per owner; job 1r raw
  JSON saved to `output/gen_1r.json` (163 KB); VoiceStudio stopped; PC shut
  down. Tomorrow: extract WAV, rerun 2r/1d/2d, ASR-verify, findings note.


**AI Learning System (Learn) Adaptation, Demo & Archival:**
- Cloned and analyzed upstream repo `amosblomqvist/learn.git`.
- Ran SLOC code inspection via `pygount` (16 files, 1,784 SLOC code lines, 500 doc lines).
- Created the native `teach` skill with diagnostic probes, Socratic checkpoints, and strict user consent for vault files.
- Completed full interactive demonstration on "Git Internals (Blobs, Trees, Commits)".
- Created 6-tier system architecture vector diagram (`git-internals-architecture.svg`) and embedded Mermaid architecture flowcharts.
- Generated 11 Spaced Repetition flashcards (`#card` and cloze deletions) in lesson note.
- Formatted and organized full project archive in [[04-Archives/Learn/README|README]] following MAQC-7 standard with [[04-Archives/Learn/Project-Files/AGENTS|AGENTS]], `Project-Files/`, `Source-Files/`, `Lessons/`, and `Assets/`.
- Cleared active project folder `01-Projects/Learn/` and updated PARA indices.

### Session: 2026-09-29

**MAQC Season 7 Rewards Processing:**
- Read MAQC Season 7 announcement from [[00-Inbox/README|README]]
- Extracted reward data from PDF (66 pages, 1,467 teams)
- Found team @akulmach74: **2 wins, 4,158 A-Coins total (1,386 per player × 3 players)**
- Created `Season_7_Rewards_Log.md` in `01-Projects/MAQC-7/`
- Drafted gratitude/announcement message for team
- Copied source files to `04-Archives/MAQC-7-Source-Files/`
- Cleared [[00-Inbox/README|README]] after processing

**Reward Summary:**
- Total Distributed: 5,004,386 A-Coins
- Prize Pool: 5,000,000 A-Coins
- Participation Bonus: 100 A-Coins per player
- Match Bonus: 20 A-Coins per match

**Previous Sessions:**
- Explained how skills load automatically based on context
- Created/maintained this task log in vault root
- Confirmed all Git commits use "akulmach74" author
- Verified vault structure: Worksheet/, MAQC-7/, .obsidian/

**How the obsidian-second-brain skill works:**
This skill loads automatically when we discuss:
- Obsidian vault organization
- Second brain/PARA methodologies
- Note linking and graph view strategies
- Visualization techniques (Excalidraw, Mermaid, Dataview)
- Plugin recommendations for knowledge management
- Maintenance and review workflows

---

*Last updated: 2026-10-25 (VoiceStudio project registered)*

## See also
[[01-Projects/README|README]]
