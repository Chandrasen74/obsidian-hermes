# BUILD PROMPT: Stick Figure Windmill Slam Dunk (animation only)

You are building a 5-second hand-drawn style animation, animation and visuals ONLY.
There is NO audio in any form: no music, no sfx, no voice-over, no mixing. The
delivered video must contain no audio track at all (mux with `-an`, or PNG frames).

Do not read or copy any existing source for this piece; build from the spec below.
The spec is complete: every number you need is here.

---

## 0. Context: who wrote this prompt and why

- Authored 2026-10-24 by **OpenCode**, the open-source terminal coding agent, running the **GLM-5.3-Flash (free)** model from Z.ai (model id `glm-5.3-flash-free`). Its role for the owner: coding and animation agent inside the owner's Animate workspace (`01-Projects\projects\animate\` in the Obsidian vault).
- Division of labor on this piece: OpenCode does the frame analysis, code fixes, and numeric verification; the owner reviews and approves everything personally (and often relays vision feedback through another model).
- What OpenCode did on this piece so far: surfaced the animate harness at the project root, applied the plan's frame repairs, diagnosed the owner's "choppy" complaint as the harness's 2s pose clock and switched this piece to per-frame motion (`STYLE.ones = true`), rebuilt the court markings as a registered side-view half-court, made the ball's spin one continuous roll across all acts, reworked the dribble into the push-bounce-catch cycle, added ball speed cues (ghost rings, streaks, doubled trail), rekeyed camera/score to the 2.8s slam, re-ran all numeric gates (textcheck, tile determinism, review arc 3/3), and rebuilt `final.mp4` + `share.mp4`.
- The original harness and the knowledge base (`stickman-remotion-knowledge-base.md`, animate-harness edition) were produced earlier by the agent reading this prompt; every number in this spec is distilled from the resulting source (`src/scenes.js`, `src/bridges.js`, `piece.json`) so a rebuild lands on the reviewed choreography.
- Note: this prompt intentionally covers the ANIMATION layer only; the sound design stays out of scope by the owner's request.

### 0b. Vault and environment context (shared fully so the reviewing agent has the same picture)

- The working directory `C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode` is the owner's active **Obsidian Second Brain vault**, not a code repo. Layout is PAR: `00-Inbox\`, `01-Projects\`, `02-Areas\`, `03-Resources\`, `04-Archives\` plus `.obsidian\` config. Keep that structure intact when filing anything new.
- The Animate workspace lives at `01-Projects\projects\animate\` and carries the surfaced harness: `tools\`, `kit\`, `styles\`, `grammar\`, `templates\`, `examples\` (copied from the in-vault skill `plugins\animate\skills\animate\`, so versions stay in lockstep).
- This piece lives at `01-Projects\projects\animate\pieces\stickman-dunk\`: source in `src\` (scenes.js, bridges.js, head.html, score.js), built `index.html` (single file), `piece.json` (spec: 30fps, 120 BPM, 5.0s, 120px safe margins), `brief.md`, `LOG.md` (full change log), `plan.md` (task tracker; a duration decision, 5.0s strict vs 5.5-6.0s, is still open), `storyboard.png`, and still sheets + contact sheets in `review\`. Renders: `renders\final.mp4`, `renders\share.mp4`, `audio.wav`, `stem-music.wav`, `stem-sfx.wav` (the audio pipeline exists but is deliberately out of this rebuild's scope).
- Tooling verified on this machine: Node v24.21.0, ffmpeg 9.0 full build, Playwright Chromium (`chromium-1248`). Harness commands run from the animate workdir, e.g. `node tools/build.mjs pieces/stickman-dunk`, `node tools/review.mjs pieces/stickman-dunk`, `node tools/still.mjs <piece> <seconds> <out.png> --scale 0.5`.
- Shell is Windows PowerShell on win32; the vault sits on OneDrive.
- Vault git rules: commits use author `akulmach74`; never commit `thumbnails\` or `.obsidian\` workspace state as a side effect; as of today nothing from the stickman-dunk work is committed.
- Vault hard rules for any agent working here: do not background-scan or re-index the vault without asking directly (the owner keeps existing resource materials and will provide them on request); no em dashes in any outgoing message or draft; ready-to-send drafts get copied to the system clipboard via `clip.exe`.
- Hardware envelope (verified): no discrete NVIDIA GPU (Intel UHD iGPU only), one 16 GB DDR4-3200 stick (single channel, ~20 GB/s usable). Local LLM/image/video inference is CPU-bound and slow (~3 t/s for a 9B Q4 model; a working llama.cpp build lives archived at `04-Archives\Local AI (barebones)\`, revived via its `start.bat`). Vision/image analysis of frames runs at ~3 tokens/sec here, so use generous timeouts on any vision task.
- Owner's working style: visual-first outputs (diagrams and boards over text walls), spaced-repetition flashcards as `#card` inline tags when study notes are involved.

---

## 1. Format and hard rules

| thing | value |
|---|---|
| canvas | 1920 x 1080 (16:9) |
| duration | 5.0s, 30fps, exactly 150 frames |
| safe margins | 120px on every side: nothing important (figure, ball, captions) may cross it |
| look | crosshatch ink sketch on warm paper: strokes of varying width, hatching for shading, slight jitter on every stroke |
| motion clock | EVERY FRAME animates (30 Hz). Do NOT pose on a coarse 2s clock; the owner rejected that as "choppy". |
| ink boil | stroke jitter re-rolls every 2 frames (jitter amplitude ~0.5-1.5px, rotation ~+/-0.6 deg). This is the hand-drawn feel and must stay. |
| determinism | fully deterministic: seeded PRNG only (no Math.random). Rendering the same frame twice must produce pixel-identical output. |
| captions | hand/marker font, left-anchored at x, baseline at y, small jitter, red-orange or ink color per section 8 |
| single file | one self-contained index.html with inline JS drawing on a canvas. No external assets, no http(s) URLs, no data URIs. |

Deliverables: `index.html` + all 150 rendered frames (PNG, 5 digits) + a silent mp4
(H.264, yuv420p, 1920x1080, 30fps, NO audio track).

## 2. Easing helpers (implement exactly)

- `lerp(a,b,u)` linear
- `easeOut2(u) = 1-(1-u)*(1-u)` (ease-out quad)
- `easeOut3(u) = 1-(1-u)^3` (ease-out cubic)
- `smoothstep(u) = u*u*(3-2*u)`
- `smooth(a,b,t)` = smoothstep of `clamp((t-a)/(b-a), 0, 1)`

## 3. World layout (static geometry)

- Paper background fill `#f5efe0`.
- Horizon/floor line at `y=760`, full width, ink `#2c221b`, width 3.5.
- Hardwood floor: y 760 to 1080 fill `#e7cfb0` with faint vertical wood grain (alpha ~0.35).
- Rafter banner belt: 6 washed boxes (176x116) from x=160 step 280 at y 60-170, fill `#dfd4be` at 0.25 alpha + one horizontal strap line each. The figure and ball must never enter this belt (they stay below y ~210).
- HOOP on the right:
  - Pole: x 1660-1692, y 220-760, dark `#24201d` crosshatched; two arm strokes from pole to board.
  - Backboard: x 1540-1556, y 270-480, `#fcf8ef` with bluish hatch; two small red target ticks at y 360/410 on the board face.
  - Rim: ellipse center (1512, 440), half-width 37, half-height 10, fill `#e03a1b`, contour; rim mount block on the board at rim height.
  - Net: 7 top points across the rim mouth; bottom row tapers to inner width 43, length 70, lattice + bottom loop, color `#3a342c`.
  - Net physics (always live): `netWave = sin((t-2.8)*22) * exp(-max(0,t-2.8)*4) * 18`; a lateral flare `sin((t-2.8)/0.45*pi)*22` active only 2.8-3.25s; vertical `netDeflect = sin(dt*26)*exp(-dt*5)*25` for dt = t-2.8 (0 before 2.8).
  - Rim vertical deflect: `rimDeflect = sin(dt*24)*exp(-dt*4.2)*28` for dt in [0, 1.4] counting from 2.8s (0 otherwise).

- COURT MARKINGS (all flat on the floor band, key/paint colors `#4a3b2f` / `#3d3025`):
  - Paint slab: quadrilateral from (852,770) to (1618,770) to (1672,982) to (796,982), filled `#ddbe95` with a light diagonal hatch (`#8a6a48`, ~0.15 alpha), outlined.
  - Near lane edge: line (796,982) to (1672,982).
  - Baseline: line (1618,770) to (1604,982) (recesses slightly left).
  - Free-throw line: line (852,770) to (826,982) (recession lean).
  - Top-of-the-key semicircle: ellipse arc centered (838,874), rx 135, ry 62, angles 0.55*pi to 1.45*pi (bulge toward half court / left).
  - 3-point arc: one big flattened ellipse arc centered (1512,878), rx 560, ry 102, angles 0.5*pi to 1.5*pi; it sprouts from both lane edges and bulges left past the FT line. Leftmost point approx (952,878).

## 4. Player (stick figure) anatomy

- Head radius 26, paper fill `#fbf5e6` with hatch shading; red-orange headband `#d6381a` with a flapping tail; single eye dot offset forward; ink limbs:
  spine width 7.5 `#15110d` (slight curve via `spineArch` px mid-control), right limbs 6-6.5, left limbs 5-5.5 at 0.85 alpha (background limbs).
- Floor shadow: ellipse under the mid-feet at y 775, alpha 0.35 -> 0.08 and width 65 -> 33 as the figure rises off the floor, hatch fill. Also a second airy ball shadow is NOT needed (skip).
- Draw order per frame: court, hoop+net, speed lines/ghost effects (behind figure), shadow, back limbs, spine, front limbs, head, THEN ball on top.

## 5. Ball anatomy

- Radius 28, fill `#e86118`, pencil highlight hatch `#ffa86b`, dark hatches `#782603`/`#401200`, contour width 3.5.
- Seams in `#1a110a`: horizontal equator stroke, vertical meridian, and two curved side arcs; the whole ball rotates by `ballRot` (so the seams spin).
- Squash: `scale(1/squash, squash)` with squash ~0.82 at floor contacts, ~1.15 at the net exit.
- `ballRot` is a single continuous monotonic-forward quantity across the whole 5s (no direction flips at act cuts). Chain (see acts): 3.0*t  ->  4.5 + (windmillAngle + 0.6*pi)*0.9  ->  10.44 + slamU*2.0  ->  12.44 + ballU*2.6.

## 6. Camera

Return (cx, cy, zoom); world is drawn translated by (960-cx, 540-cy) and scaled by zoom.

| t | cx | cy | zoom |
|---|---|---|---|
| 0 - 1.5 | lerp 600->960 by easeOut2(t/1.5) | 540 | 1.0 |
| 1.5 - 2.8 | lerp 960->1300 by smoothstep(u), u=(t-1.5)/1.3 | lerp 540->480 by sin(u*pi) | lerp 1.0->1.08 by sin(u*pi) |
| 2.8 - 3.9 | 1350 + shake | 490 + shake*0.7 | 1.06 |
| 3.9 - 5.0 | lerp 1350->1100 easeOut3 | lerp 490->540 easeOut2 | lerp 1.06->1.0 easeOut2 |

Slam shake: `shake = sin(st*45) * exp(-st*12) * 16`, st = t-2.8.

## 7. Choreography (exactly this, per act)

Baseline values: floorY = 760. `t` is seconds. Ball drawn last every frame.

### ACT 1: Drive and dribble, 0.0-1.5s
- `charX = lerp(180, 850, t/1.5)`.
- Run cycle: `stride = sin(t*16)`, `bob = |stride|*18`; right knee/foot lead `+stride*55/80 + 20/30`, left mirrored with `-stride`; feet clamp to floorY; step knee lift up to 55.
- Dribble cycle (0.4s period, locked so floor contacts land at t = 0.2, 0.6, 1.0):
  `phase = ((t-0.08)/0.4) mod 1`. Height profile h in [0..1] (0 = on floor, 1 = caught in hand):
  - phase < 0.3: `h = 1 - u1*u1`, u1 = phase/0.3 (accelerating free-fall push)
  - 0.3-0.4: h = 0 (contact hold on the floor)
  - 0.4-0.87: `h = 1-(1-u2)*(1-u2)`, u2 = (phase-0.4)/0.47 (fast launch easing into the catch)
  - 0.87-1.0: h = 1 (caught)
- `ballY = floorY - 28 - h*172`; `ballX = neckX + 69` (directly under the palm); squash 0.82 while h < 0.02.
- `ballRot = t*3.0`.
- Hand: `rHandY = neckY + 125 - handAct*58` with `handAct = smooth(0.5,0.7,phase) * (1 - smooth(0.85,1.0,phase))` (dips on the push, lifts through the carry, drops to meet the catch). Palm x = neckX + 75. Left arm counter-pumps the stride.
- Body: `hipY = floorY - 170 + bob + crouch*58 + (1-h)*22` (the knee flex pulse dips into every push); crouch = smooth(1.2, 1.5, t) adds +58px hip drop and a deepening forward lean (head +25px forward).
- Spine lean: headX = charX + 50 (+25 in the crouch), neckX = charX + 35, pelvisX = charX.
- Gather: over 1.2-1.5s blend the ball to exactly (905, 733) so the flight act can take it from there (use the smooth() of the same window).
- Speed lines behind the runner (radial dashes, back-left direction) only when t >= 0.15, anchored at max(charX-80, 170).
- Caption (see section 8): DRIBBLE DRIVE.

### ACT 2: Takeoff, flight, windmill, 1.5-2.8s
- `u = (t-1.5)/1.3`.
- Body: `charX = lerp(850, 1490, u)`; `charY = floorY + 30 - 190*sin(u*pi) + 30*u` (takeoff 790, capped apex ~617, ends near 820). hip = charY-140, neck = hip-130, head = neck-45. Torso lean interpolates 25 -> -15. Legs scissor via `legCycle = sin(u*pi*2.5)`. Left arm trails low-out for balance.
- WINDMILL: `angle = lerp(-0.6*pi, 1.5*pi, smoothstep(u))` (a 378-degree sweep: starts up-left, over the top, down past the knees, behind the spine, overhead into the rim). Shoulder = (neckX+15, neckY+20); palm = shoulder + (cos,sin) of angle at 123.5 (armLen 95 * 1.3); elbow at 0.7 armLen slightly trailing (angle - 0.3).
- Ball rides the palm (offset 22 outward along the same angle) but RIPS in from the gather point over the first 0.1s: `rip = easeOut2(min(1, u/0.077))`, `ballX = lerp(905, palmX, rip)`, `ballY = lerp(733, palmY, rip)`.
- `ballRot = 4.5 + (angle + 0.6*pi)*0.9` (carry-over from act 1, monotonic).
- Speed cues (the owner wants VISIBLE ball speed):
  - Windmill trail: bold arc `#e86118` width 3.5 from angle-1.9 to angle at radius 1.35*armLen, plus an inner echo at 1.1*armLen, width 2.4, orange at 0.4 alpha, from angle-1.2 to angle.
  - Ghost rings: while 0.12 < smoothstep-gate active (fade in u 0.12-0.3, out u 0.8-0.95): 3 orange rings behind the sweep at angle-g*0.5 (g=1..3), radius 28-6g, at palm radius +24, stroke alpha (0.5/0.37/0.24)*gate.
  - Launch streaks: 3 short dashes trailing back-left off the ball while u < 0.35, orange 0.45 alpha.
- Ground takeoff speed lines from (850, 760) angled 0.75*pi while u < 0.4.
- Caption: WINDMILL! (window 1.75-2.75).

### ACT 3: Slam and rim hang, 2.8-3.9s
- `su = (t-2.8)/1.1`.
- Contact instant is EXACTLY t=2.8 (frame 84). rimY = 440 + rimDeflect(t).
- Hang pose: hands pinned on the rim at x 1475 and 1500, y rimY+5/+8. Body GLIDES ~65px left over the first ~0.36s (`glide = easeOut2(clamp(su*2.2))`): neck = rimMountX(1515) - 40 - 65*glide + swing*0.6, neckY = rimY + 110; head +18/-42; pelvis = neckX-35+swing, pelvisY = neckY+145; elbows glide out with the body; knees tuck and swing (`swing = sin(su*pi*1.6)*35`). Only the hands touch the rim; the body stays clear of net and pole.
- Ball: while su < 0.27 it drops through the net's RIGHT HALF clear of the body: `netU = su/0.27`, ballX lerp 1500->1538, ballY = lerp(rimY+20, 730, netU^1.3), squash 1.0->1.15. After that it rebounds to the right: `bounceU = clamp((t-3.097)/0.803)`, ballX lerp 1538->1640, ballY = 730 - sin(bounceU*pi*1.5)*150*(1-bounceU*0.5).
- `ballRot = 10.44 + su*2.0`.
- Impact burst at (1515, 440): 16 radial spokes between r 56 and 90-150, `#c43319`, only while su < 0.3.
- Net-drop speed streaks: 4 short vertical dashes trailing above the ball while su < 0.24, orange 0.6 alpha.
- Caption: SLAM! (whole act).

### ACT 4: Release and landing, 3.9-5.0s
- `lu = (t-3.9)/1.1`.
- Body: drop phase (lu<0.3): from y 580 to the floor with quadratic fall; absorb phase (0.3-0.65): deep squat, kneeBend 35+45*sin(absorbU*pi), arms sweep wide 80+30; stand phase (0.65-1): rise to kneeBend 12, arms in, upright (`easeOut3` on all three).
- Ball: `ballX = lerp(1640, 1780, lu)`; bounces `ballY = 732 - |sin(lu*4*pi)| * 100*exp(-lu*2.5)` (decaying); `ballRot = 12.44 + lu*2.6`; final x 1780 is inside the safe margin.
- Dust puffs: 6 blurred ellipses near the feet while 0.28 < lu < 0.55.
- Caption: 10 / 10 (from lu > 0.5).

## 8. Captions (all windowed exactly)

| text | window (s) | x | y (baseline) | size | color | weight |
|---|---|---|---|---|---|---|
| DRIBBLE DRIVE | 0.4 - 1.1 | 320 | 340 | 52 | #2c221b | 700 |
| WINDMILL! | 1.75 - 2.75 | 230 | 655 | 64 | #c43319 | 800 |
| SLAM! | 2.8 - 3.9 | 1280 | 250 | 84 | #d6381a | 800 |
| 10 / 10 | 4.4 - 5.0 | 1180 | 300 | 60 | #2c221b | 800 |

Each caption appears/disappears on-window only (no hard pop outside the window is an option
if you have a fade system, but cropped or off-margin text is a fail; verify every frame
the text is drawn).

## 9. Expressive extras (keep these)

- Headband tail flaps: `sin(t*18)*8` wave.
- Login stick shadow scales/fades with height (section 4).
- Windmill trail is orange (matches the ball) so the sweep reads as the ball's arc, not just the arm's.
- Everything sketchy: every stroke gets the seeded jitter; textures are hatches/crosses, never flat fills.

## 10. Continuity checklist (self-verify before delivering)

1. Frame 84 (t=2.800) is the slam contact: rim deflect starts, burst draws, SLAM! shows. Reaching the rim happens at the end of act 2, not after.
2. Ball positions at act boundaries: 1.5s: (905, 733) -> act 2 starts the rip from exactly there; 2.8s: at the rim mouth (1500, rimY+20); 3.9s: (1640, near floor). `ballRot` values at boundaries: 4.5 / 10.44 / 12.44. No visual teleport, no rotation flip anywhere.
3. No stroke, figure part, ball, or caption text crosses the 120px safe margins; the head and ball stay below the banner belt (y max ~210).
4. Adjacent frames always differ (motion every frame); the ink boil must still be visible.
5. Deterministic: render frame 100 twice (in any order), outputs must be identical.
6. Net is visibly animated after the slam (wave + flare + deflect) and could plausibly still be settling at 4.2s.
7. Loop-friendliness: the last frame must read as a settle, not a freeze; a first/last pixel match is not required.
8. The dribble contacts plot at 0.2 / 0.6 / 1.0s (ball lowest + squashed), takeoff at 1.5s, windmill sweep at 1.5-2.8s, hands on rim at 2.8s, release at 3.9s, landing squat at ~4.25s, finish pose at 5.0s.

## 11. What NOT to build

- No audio of any kind (no music stem, no sfx, no voice track, no mixing, no silence track).
- No title cards, logos, watermarks, credits, progress bars, or UI chrome.
- No extra scenes, annotations, subtitles, or captions beyond section 8.
- No camera cuts: it is one continuous shot with the camera moves in section 6 only.
- Do not change any timing, coordinate, or color given above without a strong reason; the whole point of this spec is to reproduce the reviewed animation.
