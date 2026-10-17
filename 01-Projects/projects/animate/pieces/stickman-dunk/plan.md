# stickman-dunk: Polish Plan

Written 2026-10-17 (end of session). Status: frames reviewed, scope agreed, execution pending. Start here next session.

## Where things are

- Piece: `01-Projects\projects\animate\pieces\stickman-dunk\` (workspace absorbed into the vault at commit 9e33393)
- Built already: complete `src/` (scenes.js, bridges.js, head.html, score.js), 150 rendered frames, `renders/final.mp4` + audio stems. Spec: 5.0s at 30fps, 1920x1080, crosshatch ink style, action-scene format.
- Missing: `brief.md`, `LOG.md`, and the workspace harness (`tools/`, `kit/`, `styles/`, `grammar/`, `templates/` are NOT in `01-Projects\projects\animate\`; only `.claude-plugin`, `docs`, `node_modules`, `pieces`, `plugins\`)
- AGENTS.md previously pointed at the dead path `C:\Users\Kanchan Verma\projects\animate`; pointer now updated to the vault location.

## Frame review findings (sampled f0000, f0030, f0060, f0090, f0120, f0148)

Verdict: individual frames are fine; the "awful together" feel comes from environment clutter, timing, and caption collisions:

1. **Stray 3-pt arc**: a huge curved line sweeps from the bottom-left up to head height through the runner (scenes.js, 3-Point Arc block, lines ~36-40). Reads as a wire through the scene.
2. **Floaty flight**: jump arc lasts 1.9s (1.5s to 3.4s) and apex is too high; head + ball overlap the rafter banner boxes (y 60-170) around f0045-f0060. Legs dangle instead of scissoring.
3. **Caption collisions**: `WINDMILL!` (placed at 1050,240) sits under the figure's arm/head at f0090; `10 / 10` (placed at 1400,300) is drawn on top of the backboard at f0148 (the final "0" gets swallowed). Both are `handText` calls in scenes.js.
4. **Rim-hang merge**: in act 3 the hanging figure straddles rim/net/pole and visually merges (f0120).
5. **Edge clipping**: speed lines are cut at the left frame edge at t=0; the ending ball rolls to ~x1880 and gets half-clipped in the corner (safe margin is 120px per piece.json).

## Stage 1: set the workspace straight (do first, ~15 min)

- [ ] Restore harness from upstream https://github.com/cth9191/animate into `01-Projects\projects\animate\`: copy `tools/`, `kit/`, `styles/`, `grammar/`, `templates/` (and `examples/`). Do NOT overwrite `pieces/`, `docs/`, or anything already there; `node_modules` is already present.
- [ ] Verify tooling: Node 18+, Playwright Chromium (`npx playwright install chromium`), ffmpeg on PATH. If any is missing, stop and tell the user the install command.
- [ ] Write `pieces/stickman-dunk/brief.md` (spec, style, beats, sound plan) and `LOG.md` fresh.
- [ ] Sanity check: `node tools/build.mjs pieces/stickman-dunk`, then `node tools/still.mjs pieces/stickman-dunk 0,30,60,90,120,148 still-check.png --scale 0.5` and confirm the current frames still reproduce.

## Stage 2: frame repair (storyboard check-in with owner)

All edits in `pieces/stickman-dunk/src/scenes.js`:

- [ ] 3-pt arc: keep it on the floor plane (flatten the y span below floorY=760, shrink radius) or heavily dim; it must never cross the flight zone.
- [ ] Flight window: tighten the arc from 1.9s to about 1.2-1.3s by moving the act boundary (e.g. bake at ~2.8), add a crouch/anticipation dip right before takeoff, cap the apex so the head stays below about y=180 (clear of banner row), give the legs a real scissor (bigger legCycle amplitude, knee lead).
- [ ] Captions: `WINDMILL!` to a clear zone left of the figure (target roughly x=700-850, y=600-650; verify against payload). `10 / 10` fully left of the backboard (x < 1440, y around 300). Everything must clear the 120px safe margin; confirm with `node tools/textcheck.mjs pieces/stickman-dunk` (or review's text section).
- [ ] Rim hang: shift the hanging figure about 60px left so only the hands touch the rim; body clear of net and pole.
- [ ] t=0: start speed lines inside the frame or fade them in from 0.15s. End: clamp final ball x to <= W-140.
- [ ] Fill `TIMELINE.board` with one key time per beat, render the board, and get thumbs up/down per panel from the owner BEFORE polishing further.

## Stage 3: polish loop

- [ ] `node tools/build.mjs pieces/stickman-dunk`, then `node tools/tile.mjs pieces/stickman-dunk tile.png` across the three cut points (1.5s, 2.8s, 3.4s, 3.9s depending on new boundaries).
- [ ] `node tools/review.mjs pieces/stickman-dunk`: fix everything it flags (text cutoff/overlap, arc, sound loudest moment), record a per-shot PASS table in `LOG.md`.
- [ ] Export: `node tools/export.mjs pieces/stickman-dunk --share`, deliver `renders/share.mp4`.

## Open decision (owner must answer before Stage 2 locks beats)

- Keep strict 5.0s, or extend to 5.5-6.0s so the four acts breathe? Recommendation: extend slightly; the floaty feel is mostly time pressure. Owner leaned "frames ok solo, awful together", which points to timing + collisions, not new scenes.

## Working rules

- Git author: `akulmach74`. Never commit `thumbnails/` or `.obsidian/` state as a side effect.
- Frame reviews: the agent reads PNGs directly with its own vision (GLM-5.3-Flash via the read tool); no local model needed.
- Skill non-negotiables apply: storyboard approved before animation work, measured checks over vibes, look at every contact sheet.
