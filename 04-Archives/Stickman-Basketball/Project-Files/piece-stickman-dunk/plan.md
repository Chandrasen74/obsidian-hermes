# stickman-dunk: Polish Plan

Written 2026-10-17 (end of session). Status update 2026-10-23 (overnight build): Stage 1 done, all Stage 2 repairs applied, build/textcheck/tile/review/export all pass numerically, renders rebuilt. Pending: visual sign-off (board + stills + contact sheets), board thumbs, duration decision. Start tomorrow by looking at `pieces/stickman-dunk/storyboard.png` and `review/morning-check.png`, then finish Section 4's review list with your own eyes.

## Where things are

- Piece: `01-Projects\projects\animate\pieces\stickman-dunk\` (workspace absorbed into the vault at commit 9e33393)
- Built already: complete `src/` (scenes.js, bridges.js, head.html, score.js), 150 rendered frames, `renders/final.mp4` + audio stems. Spec: 5.0s at 30fps, 1920x1080, crosshatch ink style, action-scene format.
- Harness NOW SURFACED at the project root (2026-10-23): `tools/`, `kit/`, `styles/`, `grammar/`, `templates/`, `examples/` copied from the in-vault skill `plugins\animate\skills\animate\`; `node tools/build.mjs pieces/stickman-dunk` works from the project dir.
- `brief.md` and `LOG.md` now exist in the piece dir (written 2026-10-23).
- AGENTS.md previously pointed at the dead path `C:\Users\Kanchan Verma\projects\animate`; pointer now updated to the vault location.

## Frame review findings (sampled f0000, f0030, f0060, f0090, f0120, f0148)

Verdict: individual frames are fine; the "awful together" feel comes from environment clutter, timing, and caption collisions:

1. **Stray 3-pt arc**: a huge curved line sweeps from the bottom-left up to head height through the runner (scenes.js, 3-Point Arc block, lines ~36-40). Reads as a wire through the scene.
2. **Floaty flight**: jump arc lasts 1.9s (1.5s to 3.4s) and apex is too high; head + ball overlap the rafter banner boxes (y 60-170) around f0045-f0060. Legs dangle instead of scissoring.
3. **Caption collisions**: `WINDMILL!` (placed at 1050,240) sits under the figure's arm/head at f0090; `10 / 10` (placed at 1400,300) is drawn on top of the backboard at f0148 (the final "0" gets swallowed). Both are `handText` calls in scenes.js.
4. **Rim-hang merge**: in act 3 the hanging figure straddles rim/net/pole and visually merges (f0120).
5. **Edge clipping**: speed lines are cut at the left frame edge at t=0; the ending ball rolls to ~x1880 and gets half-clipped in the corner (safe margin is 120px per piece.json).

## Stage 1: set the workspace straight (do first, ~15 min)

- [x] Harness surfaced into `01-Projects\projects\animate\`: copied `tools/`, `kit/`, `styles/`, `grammar/`, `templates/`, `examples/` from the in-vault skill (`plugins\animate\skills\animate\`), not an upstream clone, so versions stay in lockstep. `pieces/`, `docs/`, `node_modules` untouched.
- [x] Tooling verified 2026-10-23: Node v24.21.0, ffmpeg 9.0-full, Playwright Chromium installed.
- [x] `pieces/stickman-dunk/brief.md` written fresh; `LOG.md` created (2026-10-23 night build log).
- [x] Sanity check ran: `node tools/build.mjs pieces/stickman-dunk` OK; tile determinism across 11 boundary frames true (see LOG.md).

## Stage 2: frame repair (storyboard check-in with owner)

All edits in `pieces/stickman-dunk/src/scenes.js` (APPLIED 2026-10-23, details + continuity notes in LOG.md):

- [x] 3-pt arc: flattened onto the floor plane (ellipse at y >= 761, never crosses the flight zone).
- [x] Flight window: tightened 1.9s -> 1.3s (slam boundary moved to 2.8), crouch + ball gather added at 1.2-1.5s, apex capped (head max y ~210, ball clears the banner row by 90px+), scissor legs kept on the new base.
- [x] Captions: `WINDMILL!` -> (230,655) clear left hardwood zone; `10 / 10` -> (1180,300) fully left of the backboard; `SLAM!` nudged to (1280,250) to clear the pole corner. textcheck + review TEXT both PASS (0 violations).
- [x] Rim hang: body glides ~60px left of net/pole on contact (hands stay anchored on the rim).
- [x] t=0 speed lines gated past 0.15s + pushed inboard; final ball clamped to x 1780 (<= W-140).
- [x] `TIMELINE.board` filled with 5 key times (0.8/1.45/2.2/2.95/4.6) and rendered to `pieces/stickman-dunk/storyboard.png` - **owner thumbs up/down per panel STILL PENDING tomorrow** (gates further polish).

## Stage 3: polish loop

- [x] `node tools/build.mjs pieces/stickman-dunk` rebuilt through every edit (index.html 1836 lines, syntax ok).
- [~] `node tools/tile.mjs pieces/stickman-dunk pieces/stickman-dunk/tile-boundaries.png 2 42 46 81 83 84 86 90 97 117 138`: deterministic true; boundary tile rendered but NOT eyeballed tonight (in `tile-boundaries.png`).
- [~] `node tools/review.mjs pieces/stickman-dunk`: all sections pass (story arc 3/3, text 0 violations, dead beats 0, cuts on grid, -16.1 LUFS); contact sheets generated (`review/shot01-sheet.jpg`, `review/phone.jpg`) but the eyeball PASS table is TOMORROW's first job.
- [x] Export: `node tools/export.mjs pieces/stickman-dunk --share` -> `renders/final.mp4` + `renders/share.mp4` rebuilt with the final mix (delivered file is current).
- Morning check-in renders ready: `storyboard.png` (5 panels), `review/morning-check.png` (stills at 0.4/1.45/2.15/2.75/2.85/2.95/4.6 @ 0.5 scale), `tile-boundaries.png`, `review/phone.jpg`, `review/shot01-sheet.jpg`.

## Open decision (owner must answer before Stage 2 locks beats)

- Keep strict 5.0s, or extend to 5.5-6.0s so the four acts breathe? Recommendation: extend slightly; the floaty feel is mostly time pressure. Owner leaned "frames ok solo, awful together", which points to timing + collisions, not new scenes.

## Working rules

- Git author: `akulmach74`. Never commit `thumbnails/` or `.obsidian/` state as a side effect.
- Frame reviews: the agent reads PNGs directly with its own vision (GLM-5.3-Flash via the read tool); no local model needed.
- Skill non-negotiables apply: storyboard approved before animation work, measured checks over vibes, look at every contact sheet.
