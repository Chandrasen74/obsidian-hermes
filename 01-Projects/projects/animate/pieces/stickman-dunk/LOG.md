# LOG: stickman-dunk

## 2026-10-24 (owner feedback pass: smoothness + court + ball)

Owner's 5 complaints, each with the fix applied today (all in `src/scenes.js` except #1):

1. [x] **"Choppy and not smooth at all"** — mechanical cause found in the harness: scenes ran on the 2s pose clock (~12-15 poses/sec). `STYLE.ones = true` now set per-piece at the top of `src/bridges.js`: `kit/morph.js` reads it each frame, so motion advances every frame (30 Hz). The ink boil still ticks on `B = floor(F/2)` (2s), so the hand-drawn look is unchanged. Signal check: per-frame pixel motion rose 1.0 -> 1.3/1.4; all review gates still PASS.
2. [x] **Court markings (owner's first priority)** — the old jumble (vertical line + FT circle colliding with the runner + two floating lane lines + oversized arc) replaced with a registered side-view court: far lane edge under the runner's feet (y 770), paint slab (hatched trapezoid) hanging toward the viewer, baseline pin under the hoop receding to the near edge, FT line with a recession lean, top-of-the-key semicircle bulging toward half court, one big flattened 3-pt arc sprouting from both lane edges and bulging left past the FT line. Everything stays on the floor band (y 770-1044).
3. [x] **Ball spin consistency** — `ballRot` is now one continuous forward roll across all 4 acts (3.0/s dribble -> windmill-coupled 4.5 + sweep*0.9 -> slam 10.44 + slamU*2 -> landing 12.44 + ballU*2.6). No phase-reset flips at the act cuts.
4. [x] **Dribble naturalness** — asymmetric cycle locked to the Foley thuds (contacts exactly at 0.2/0.6/1.0s): free-fall push accelerating (h = 1 - u^2 over 0.12s), 0.04s squash hold on the floor, fast launch easing into the catch (EZ-out), palm dips on the push, lifts through the carry, drops to meet the catch; body dips 22px into every push (knee flex pulse).
5. [x] **Ball speed on the dunk** — ghost echo rings (3 orange rings fading at the angles the sweep just passed, gated to the windmill window), launch streaks peeling off the ball at takeoff, doubled windmill trail (wide sweep arc + inner echo), hot streaks above the ball during the net drop, all keyed after the ball itself (final alpha boosted after a 0.75-scale still check).
   - Also found and fixed during self-review: the ball's net-drop path dove onto the hanging figure's chest; rerouted through the net's right half (x 1500->1538, exponent 0.7 -> 1.3) and the rebound starts from 1538.

Verification (all on the final build): build OK (1925 lines) - textcheck PASS 0 violations - tile determinism TRUE over 11 frames (f6-f138, ~40-115ms/frame) - review: cuts on grid PASS, no flat frames, story arc PASS 3/3 (gift p90 -14.0 vs peak -15.9), TEXT PASS, loudest window 2.8s (-9.1 dBFS), -16.1 LUFS, peak -0.7 dBFS - export: final.mp4 + share.mp4 rebuilt.

Self-vision check notes (stills I eyeballed): court reads correctly on all 8 dribble-sheet panels; contacts land at 0.2/0.6/1.0s with visible squash; windmill sweep flows knee -> behind -> overhead; ghost rings visible from 0.75 scale; slam path separates ball from body cleanly (fixed in v2 of this pass).

Stills for the owner's personal confirmation:
- `review/v2-dribble-court.png` (8 panels: 0.1-1.45s, court + dribble cycle)
- `review/v2-windmill-slam.png` (6 panels: 1.95-4.6s, sweep + slam + landing)
- `review/v3-slam-path.png` (4 panels: 2.82-3.2s, slam path detail)
- `review/v2-speed-final.png` (4 panels: speed cues at 0.75 scale)
- `storyboard.png` (rebuilt)

## 2026-10-23 (overnight build, no-vision session)

### Stage 1 woke up

- [x] Harness surfaced into the project root: `tools/`, `kit/`, `styles/`, `grammar/`, `templates/`, `examples/` copied from the in-vault skill (`plugins/animate/skills/animate/`), not an upstream clone (no version drift; pieces/docs untouched).
- [x] Tooling verified: Node v24.21.0, ffmpeg 9.0-full, Playwright Chromium present (`chromium-1248`).
- [x] `brief.md` written fresh. (This LOG replaces the missing one.)
- [x] Sanity build: `node tools/build.mjs pieces/stickman-dunk` OK (syntax check, single file, no external assets).

### Stage 2 frame repair applied (from plan.md's review findings)

1. [x] 3-pt arc flattened onto the floor plane (ellipse arc at y >= 761; never crosses the flight zone).
2. [x] Flight 1.9s -> 1.3s: act-2 boundary moved to 2.8s; asymmetric arc (takeoff 790 -> apex ~617 -> hang 820) caps head/ball clear of the rafter banner row (y 60-170) by 90px+ of margin; scissor legs unchanged formulas, now on the 1.3s base.
3. [x] Crouch/gather anticipation added (t 1.2-1.5: hip +58px, lean deepens, ball gathers at the line; 0.1s rip-in at takeoff to kill the ball teleport).
4. [x] `WINDMILL!` moved (1050,240) -> (230,655) size 68->64, window 2.0-3.2 -> 1.75-2.75 (left hardwood zone, clear of figure/trail by geometry).
5. [x] `10 / 10` moved (1400,300) -> (1180,300), fully left of the backboard.
6. [x] `SLAM!` nudged (1380,220) -> (1280,250) to clear the pole corner (was not in plan's defect list, caught while re-measuring).
7. [x] Rim hang: body glides ~60px left of the net on contact (glide `EZ.o2` over first ~0.36s), hands stay anchored on the rim at x 1475/1500; elbows glide with the body.
8. [x] t=0 speed lines: gated past 0.15s + origin pushed inboard (>= 170px).
9. [x] Final ball x: 1880 -> clamp 1780 (<= W-140 safe margin).
10. [x] All rim/net/impact physics rekeyed 3.4 -> 2.8 (netWave, netFlare, netDeflect, rimDeflect bursts window now 2.8-4.2).
11. [x] Camera (bridges.js) retimed to the same boundaries; shake launches at 2.8s.
12. [x] Score retimed: slam clang/sub/swish at 2.80-2.85s; risers end at 2.75; riff compressed into flight; post-slam bass + bounce sfx re-anchored (3.35/4.05/4.5).
13. [x] `TIMELINE.cues`/`acts`/`board` updated: acts Drive 0-1.5 (build), Flight 1.5-2.8 (peak), Slam & Landing 2.8-5.0 (gift); board = 5 panels (0.8/1.45/2.2/2.95/4.6).

### Verification run (numeric only; no vision tonight per owner's order)

- build: OK (1836 lines, syntax ok, single file, no external assets)
- textcheck: PASS (0 cut-off / overlap / safe-zone violations on 26 sampled frames)
- tile determinism: PASS across 11 boundary frames (f2, f42, f46, f81, f83, f84, f86, f90, f97, f117, f138; ~30ms/frame)
- review (final render): CUTS on grid PASS - FLAT FRAMES none - LOOP diff 2.77 (info) - TEXT PASS - DEAD BEATS PASS (0 stretches) - STORY ARC PASS 3/3 (gift p90 -14.0 vs peak -15.9: the slam is the loudest moment, held 2.8-5.0) - SOUND: loudest 100ms window at 2.8s in the payoff act, -16.1 LUFS integrated, peak -0.7 dBFS (in the -16..-14 phone band)
- export: renders/final.mp4 + renders/share.mp4 + audio.wav + stems all rebuilt final (36ms/frame)
- Score iterations logged: fixed broken `sub()` velocity args (75/50/80 -> 0.08/0.85), thinned flight bus (pluck/sweep/riser), retimed bass to the 2.8 slam, dropped the busy 3.0s post-hit note, added a pad-drop pocket 2.6-2.95s so the clang lands in air (this took gift p90 from -11.2 FAIL to story arc PASS 3/3)

### Left open (for tomorrow's eyes and ears)

- `silence before payoff 0.5-4s at <= -40 dBFS`: the reviewer still measures 0.0s fully silent (the 2.6-2.95 pocket is quiet but not <= -40 dBFS). A full dry-send rewrite of the pre-slam bar is the next score move; the arc rules already PASS so this is a nicety, not a gate.
- Caption-hold rule: `DRIBBLE DRIVE` (0.7s) and `WINDMILL!` (1.0s) hold < 1.25s by design (fast interjections). Revisit only if the board look wants it.

### Pending tomorrow (needs eyes on it)

- Storyboard approval: look at `board.png` panels (P1-P5), thumbs up/down each (gates further polish).
- Look at `review/morning-check.png` (stills at the panel times + boundary frames 2.7/2.8/2.85/3.0).
- Look at the review contact sheets + cut/morph grids; write the per-shot PASS table here.
- Confirm the new caption zones read well (geometry says clear; eyes decide).
- Owner decision (from plan.md, still open): keep strict 5.0s or extend to 5.5-6.0s so the four acts breathe.
- Listen to the score: no silence-before-payoff act exists yet; candidate improvement for the next pass.

### Notes for the next session

- `handText` is left/left-baseline anchored (kit.js); widths at 60-84px handwriting are big, so the caption boxes in brief.md assume ~0.6-0.7 px size per char.
- Act-boundary continuity pairs measured in geometry: flight-end neck (1475,550) -> glide start (rim-40); handoff ball x 1640 at 3.9s; charY 820 -> hang pelvis ~695 via glide (do not hand-tune these pairs independently).
- Two captions still hold < 1.25s (`DRIBBLE DRIVE`, `WINDMILL!`): intended as fast interjections; revisit if the board look demands it.
