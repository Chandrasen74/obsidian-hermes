---
name: README
tags: ["#status/archived", "#type/index", "#domain/animation"]
---
# Stickman-Basketball Archive

**Status:** COMPLETED
**Date Archived:** 2026-10-25
**Project Type:** Animation production (two finished cuts with SFX and colour grade)

---

## Summary

Two shareable 1920x1080/30fps shorts made from the reviewing agent's stickman basketball
animations: `stickman-dunk-sfx.mp4` (5.0 s, gym) and `stickman-layup-sfx.mp4` (6.0 s, park).
The agent's animations arrived silent; this project added the full sound design (Mixkit
samples + synthesised layers), the colour grade, and a layup hoop revision (pole planted
mid-court, base pad, net rebuilt to match the dunk's lattice with live physics).

The finished videos live in `Assets/deliverables/` (moved there from the animate workspace
on archive day). Build inputs and intermediates are copied verbatim from the temp workspace.
Later the same day the entire animate workspace left `01-Projects`: the dev piece moved to
`Project-Files/piece-stickman-dunk/` and the harness to `Source-Files/animate-harness/`;
`01-Projects/projects/animate` no longer exists.

---

## Archive Contents

```
Stickman-Basketball/
├── README.md                          # this note
├── Assets/deliverables/               # MOVED 2026-10-25 from 01-Projects/projects/animate
│   ├── stickman-dunk-sfx.mp4          # 5.0 s cut, audio -16.8 LUFS / -2.8 dBTP
│   ├── stickman-layup-sfx.mp4         # 6.0 s cut (v2 hoop), -16.4 LUFS / -2.6 dBTP
│   ├── audio/dunk-master.wav, layup-master.wav
│   ├── stills/layup-reach-3.8s.png, layup-make-4.4s.png
│   └── README.md                      # grade recipe + full cue sheets
├── Source-Files/
│   ├── animate-harness/               # the animate workspace itself, MOVED 2026-10-25:
│   │                                  # kit, tools, plugins, styles, grammar, templates,
│   │                                  # docs, examples (node_modules stays git-ignored)
│   ├── agent-ws/                      # reviewing agent's returned workspace, verbatim
│   │   ├── stickman-dunk/             # delivered dunk: index.html + frames/final outputs
│   │   ├── stickman-layup/            # layup source incl. det/ scratch dir
│   │   ├── ref/, uploads/, tools-bin/, .fonts/
│   ├── workspace-01a16ceb-…e2.zip     # 65.7 MB: the reviewer's return zip, verbatim
│   └── workspace-01a08917-…92.zip     # 9.6 MB: the video workspace generated with
│                                      #  another agent, saved earlier by the owner
├── Project-Files/
│   ├── build-audio.py                 # SFX mix builder (cue lists per video)
│   ├── master-mux.py                  # gain, limiter, grade, mux (dual-video driver)
│   ├── master-layup-v2.py             # v2 hoop rebuild: frames -> grade -> mux
│   ├── verify.py                      # stream/cue/loudness verifier
│   ├── grade-test.py, render-layup.mjs, preview-grid.py
│   ├── sfx-analyze.py, mixkit-scrape.py, mixkit-index.json
│   ├── clip-frame.ps1                 # clipboard still-frame helper used during sign-off
│   └── piece-stickman-dunk/           # crosshatch dunk dev piece, MOVED from 01-Projects (201 MB):
│       ├── src/ (scenes.js, bridges.js, head.html, score.js)
│       ├── frames/ (150 rendered), renders/, review/
│       └── brief.md, plan.md, LOG.md (has the keep-BOTH-dunks owner note),
│          index.html, piece.json, storyboard.png, tile pngs
├── Working-Data/
│   ├── layup-frames-v2/               # 180 rendered v2 frames (the delivered layup picture)
│   ├── hoop-test/, hoop-test2/ + contact sheets (hoop-test-sheet.png, hoop-test2-sheet.png)
│   ├── mix/ (intermediate mixes), sfx/ (16 Mixkit samples)
│   ├── ref-frames/ (42 extracted reference frames) + ref-grid*.py, ref-preview.py/png
└── Docs/
    ├── reference-frames.pdf           # 29-frame reference laid out for matching
    ├── reference.mp4                  # the agent's layup reference video
    └── stickman-remotion-knowledge-base.md
```

---

## Quick Links to Core Artifacts

- **Final videos:** [[04-Archives/Stickman-Basketball/Assets/deliverables/README|deliverables README]] (with cue sheets and the grade recipe)
- **Dev history of the dunk piece:** [[04-Archives/Stickman-Basketball/Project-Files/piece-stickman-dunk/plan|piece plan]] and [[04-Archives/Stickman-Basketball/Project-Files/piece-stickman-dunk/LOG|LOG]]

---

## Key Facts

- Spec: 1920x1080, 30 fps, H.264 High, yuv420p, +faststart; audio AAC 48 kHz stereo 192 kbps.
- Grade strings live in `master-mux.py` (GRADE dict) and `master-layup-v2.py`.
- Layup v2 hoop: rim y 420 -> 520, pole down to y 938 with base pad on the court, net rebuilt
  to the dunk lattice (7 strands, taper 78 -> 44, length 70, wave/deflect/flare/rim-deflect
  18/25/22/28), leap shortened 300 -> 210 so the man still reaches the rim.
- Audio pipeline: Mixkit samples (free licence) + synthesised layers; masters at
  -16 LUFS target, alimiter ceiling 0.72 linear.

---

## Notes for Next AI/Human

- The animate workspace no longer lives under `01-Projects` (moved here in full 2026-10-25):
  harness at `Source-Files/animate-harness/`, dev piece at `Project-Files/piece-stickman-dunk/`.
  The dev piece stays gated by its visual sign-off list (see its LOG.md); nothing else moved.
- To re-cut: copy `Project-Files` scripts + `Working-Data` inputs to a scratch dir and run
  `build-audio.py` then `master-mux.py` / `master-layup-v2.py` (see deliverables README).
- The original zip files are byte-identical copies from `Downloads`.
- The live address book story: the videos people share should come from
  `Assets/deliverables/` here, since that folder moved into the archive.

---

*Last Updated: 2026-10-25*

## See also
[[04-Archives/README|README]]
