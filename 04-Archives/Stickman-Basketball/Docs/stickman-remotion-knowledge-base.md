# STICKMAN ANIMATION KNOWLEDGE BASE (v2: animate harness edition)

> **Remade 2026-10-23.** v1 taught Remotion; the actual project stack is the **animate skill harness** (`plugins/animate/skills/animate/`): one `<canvas>`, drawn and scored procedurally, deterministic frame by frame, rendered headless and mixed to MP4. There is no React, no Remotion, no CSS animation, no `interpolate()` API. This file is the machine-consumable remake: animation theory and smoothness discipline translated to the harness that actually renders the pieces.
>
> **Target stack:** Node 18+, Playwright Chromium, ffmpeg. Canvas 2D + the skill's `kit/`, rendered via `tools/build.mjs` + headless Chromium. Reference source docs (always authoritative, read on demand): `SKILL.md`, `craft.md`, `grammar/FRAME.md`, `styles/<name>/STYLE.md`.

## PART 0 — HOW TO CONSUME THIS DOCUMENT

When asked to animate a stickman (or fix one), in order:

1. **Golden rules** (non-negotiable, from `SKILL.md`):
   - No animating before the storyboard is approved.
   - Every pixel a pure function of the frame: seeded randomness only (`RNG(...)`), the boil index `B` for per-step variation. Never `Math.random()`, never wall-clock time. `tile.mjs` prints a determinism check and fails as `deterministic: false`.
   - Single built file: edit `src/` parts, never the built `index.html`.
   - Look at every contact sheet and test tile; "done" is measured by `review.mjs` numbers, never "looks good".
   - The text check beats the eye: `review.mjs` → TEXT finds crop/overlap the eye forgives.
2. Plan the story as a beat table (§6.1) and get approval before drawing.
3. Motion is data: schedule on `TT` with `ev(t, d)`, `popS(t)`, write-ons, springs (§3). Never hand-animate frame by frame.
4. Time on the beat grid: `onBeat(t)` (§3.2). Impacts land on the 8th grid.
5. FX stack at every impact: flash + hit-stop hold + shake + dust + SFX on the exact contact frame (§4.2).
6. Build, tile, review, fix, re-review (§5). Keep a `LOG.md` PASS table.
7. Deliver `renders/share.mp4`; report the check numbers and what is unverified.

---

# PART 1 — HARNESS REFERENCE

## 1.1 What the stack is

- Pieces live at `pieces/<name>/` in the project dir (`01-Projects/projects/animate/`). A piece is: `piece.json`, `src/head.html` (timeline + page), `src/scenes.js`, `src/bridges.js`, `src/score.js`, optional `brief.md`, `LOG.md`, `review/`, `renders/`, `frames/`.
- `node tools/build.mjs pieces/<name>` concatenates `src/` + the style's `kit.js` + `kit/core.js` + `kit/morph.js` + `kit/score-*.js` into one `index.html`. All paths below are relative to the skill base: `plugins/animate/skills/animate/`.
- Preview: open `index.html`; `?t=2.5` freezes a frame; `?format=16:9` re-lays out. Rendering: `tools/export.mjs` screenshots every frame headless and runs ffmpeg.
- One style per piece, picked by `piece.json` `"style"`; the renderer calls only the style's `STYLE` hooks (`styles/<name>/STYLE.md` documents its kit API).
- `storyFormat` in `piece.json` declares the narrative engine ("F2 morph chain", "F4 mission", "beat-cut", a piece may declare its own, e.g. stickman-dunk's "action-scene": hard cuts on the beat, no morph bridges).

## 1.2 `piece.json` schema

```json
{
  "name": "stickman-dunk",
  "title": "Stick Figure Windmill Slam Dunk",
  "format": { "width": 1920, "height": 1080, "fps": 30, "bpm": 120, "duration": 5.0, "frames": 150 },
  "storyFormat": "action-scene",
  "style": "crosshatch",
  "review": { "safe": { "top": 120, "bottom": 120, "right": 120, "left": 120 }, "refs": {} }
}
```

- `fps` is per piece. Harness default is 24 (60 BPM grid is frame-perfect there); stickman-dunk runs **30 fps @ 120 BPM** (8th = 0.25 s = 7.5 frames, so snap cues with `onBeat()` and let the renderer round to the nearest frame).
- `review.safe` is every shot's hard margin in px: nothing intentional within it; `review.mjs` → TEXT flags anything crossing it.

## 1.3 `src/head.html` contract (what the page defines)

```js
const FORMATS = { '9:16': [1080,1920], '4:5': [1080,1350], '1:1': [1080,1080], '16:9': [1920,1080] };
const FPS = 30, [W, H] = FORMATS[FORMAT];
const BPM = 120, GRID0 = 0;                    // or from BEATS (a supplied track via tools/beats.mjs)
const BEAT = 60/BPM, E8 = BEAT/2, E16 = BEAT/4; // 0.5 / 0.25 / 0.125 s
const SAFE = { ... };  const CX = (W - SAFE.right) / 2;   // caption centre
const onBeat = (t) => nearest 8th of the grid;            // every cut, morph and big cue goes on it
const ERA_LIST = [[t0, t1, () => sceneA()], ...];         // eras: time ranges + scene functions
const SHOTS   = [[key, era, t0, t1, title], ...];
const TIMELINE = {
  width, height, fps, bpm, gridOffset, duration, frames, loop, safe, aspect,
  format: 'action-scene',
  shots, cuts: [s, ...],         // hard cut times (seconds, on the 8th grid)
  morphs: [...],                 // bridge centres (seconds), [] for cut-only pieces
  cues: { name: t, ... },        // every named event time scenes schedule against
  acts: [ { name, role, t0, t1 }, ...],   // roles: build | journey | peak | silence | gift | goodbye
  board: [ { t, title, sound, next }, ...],   // storyboard: ONE key frame per beat (rendered by storyboard.mjs)
  narration: [],
};
```

Rules: boundaries with a morph `BRIDGE` or declared `cuts` carry the timing; scenes read `TIMELINE.cues`, never hardcoded seconds (:: verify each cue exists in the head). `reviews` read `TIMELINE.acts[].role` for the story-arc check.

## 1.4 `src/scenes.js` contract

- One function per era/shot: full-bleed world, hero acting, background life, tag/caption.
- Layout with `LX(frac)`, `LY(frac)`, size with `UNIT` (1 at 1080 on the short side); branch on `PORTRAIT` / `WIDE` when a shape needs a different arrangement. Channels with per-shot variation for multi-format pieces.
- Animate with `TT` / `ev(t, d)` / `popS(t)` only (§3.2). Schedule against `TIMELINE.cues`.
- Draw with the style's kit; the drawn world must start from a clean sheet each frame (the renderer clears the era layer to `STYLE.paper`; `tile.mjs` catches carryover as `deterministic: false`).
- A shot is complete on its first frame: the thing defining it is fully drawn at `E0`; write-ons start a few frames early.

## 1.5 `src/bridges.js` (morph-joined pieces; empty `BRIDGES = []` for cut-only)

```js
const ERA_BG = ['#26315f', '#a9d9c6'];          // dominant colour per era (fade through STYLE.paper)
function pieceCam(era, t) { return push(...) / bump(...) / null; }
const BRIDGES = [
  { tc: TIMELINE.morphs[0], A: () => ({P: ellipsePts(...), c: '#f6ecc8'}), B: () => ({P: ..., c: PAL_YELLOW}) },
];
```

- Bridge budget: each costs ~1.2 s by default (0.4 s of it blank paper), shorten with `{ tc, d: 0.4, ... }` (0.8 s). Under 30 s use 3 or fewer. Bridge object ≥ 200 px at the boundary, **must be in frame at the boundary** (pull push-ins back first). Bridge on `STYLE.paper`, never a blend of two wall colours. Max one hard cut in a morph piece: the payoff slam.

## 1.6 Command cheat sheet (run from the project dir, skill tools by relative path)

| command | what |
|---|---|
| `node plugins/animate/skills/animate/tools/build.mjs pieces/<name>` | build `index.html` (run after every `src/` change) |
| `... tools/still.mjs pieces/<name> 0,1.25,2.5 look.png --scale 0.5` [--format 16:9] | full-res stills at given times |
| `... tools/tile.mjs pieces/<name> tile.png <times...>` | grid of frames + determinism check; tile across every cut/morph |
| `... tools/storyboard.mjs pieces/<name> board.png` | renders `TIMELINE.board` as the approval board |
| `... tools/textcheck.mjs pieces/<name>` | text-only: cutoff, overlap, safe margins |
| `... tools/review.mjs pieces/<name>` [--format 16:9] | full QA: per-shot contact sheets, cut/morph grids, STORY ARC, ANCHOR, TEXT, SOUND (loudest moment, silence before it, LUFS), DEAD BEATS |
| `... tools/export.mjs pieces/<name> --share` | frames + audio.wav + stems + `renders/final.mp4` + `renders/share.mp4` |
| `... tools/export.mjs pieces/<name> --only-audio` | re-render the score and remux (~4x faster; mix iteration) |
| `... tools/export.mjs pieces/<name> --formats 9:16,1:1,16:9 --share` | one piece, several shapes (never crop; re-lay out) |
| `... tools/export.mjs pieces/<name> --blur 4` | motion blur (4 sub-frames averaged) |
| `... tools/beats.mjs <track.wav> pieces/<name> --start 12 --dur <len>` [--bpm 128] | beat map of a supplied track → injected as `BEATS` (`onBeat` snaps to the song) |
| `... tools/framehash.mjs` / `tools/compare.mjs` | pixel-identity check; reference vs frame compare sheet |
| `... tools/gallery.mjs <out.png> [<styles>]` | style gallery for the look check-in |
| `... tools/measure/refs.mjs` / `shotlog.py` | measure a reference (proportions / cut log with real fps) |
| `... tools/voice.mjs pieces/<name>` [--scratch] | voice-over line/word timing (faster-whisper); injects `VOICE`, `VL(id)`, `VW(id, word, n)` |
| `... tools/capture.mjs <url> pieces/<name>/assets/x.png [--selector css] [--full]` | screenshot the user's own site (assets embedded by build; `drawAsset('x.png', x, y, w, h)`) |

---

# PART 2 — KIT API (draw with these, never raw canvas except `ctx.save/translate/scale`)

## 2.1 `kit/core.js` geometry + medium

- Points arrays are the universal currency: `ellipsePts(cx, cy, rx, ry, rot?, n?): P`, `rrectPts(x, y, w, h, r?): P`, `arcPts(cx, cy, r, a0, a1, n?, sy?): P`, `xform(P, tx, ty, rot?, sx?, sy?): P`, `bbox(P, pad?)`, `resample(P, closed, step)`, `subPath(P, frac)`, `pointAt(P, frac)`.
- `trace(P, closed)` rounds corners through midpoints; give it dense points (`resample(P, true, 30)`) for boxes that must reach the frame edges.
- `wobble(P, closed, amt, key, step?)`: the hand-drawn line; `key` reseeds it per boil step so held shapes still boil.
- `ink(P, { w, color, amt, key, frac, double })`: the line itself (default for crosshatch); `frac` writes it on 0..1.
- `paint(P, { fill, w, line, tex: [...] })`: fill with textures clipped inside, then outline. Texture objects: `{ k: 'hatch', a, gap, dash?, al?, dens: (x,y) => 0..1 }`, `'cross'`, `{ k: 'pencil', c, al, per }`, `'stipple'`. Shade with a density function, light top-left; never flat fills except paper.
- `grain(o)`: paper grain over every frame (style `STYLE.post`).
- Text: `monoText(str, x, y, size, color, { count })` (typing), `monoW(size)`, `handwrite(str, x, y, size, o)`.
- Construction: `construct(cx, cy, r, o)`, `cline`, `ruler`, `sparkBurst`, `burst`, `star4`, `rainbow`, `hexGrid`, `irisRim`, `irisHole` (iris in/out into a dark world).
- Camera: `camera(cx, cy, zoom, rot, sx, sy)` matrix; `screen()` / `toScreen(x, y)` / `fillAll(color)` after it; `ctx.setTransform` via `screen()` to draw UI/captions outside the camera.
- Crosshatch style kit extras (`styles/crosshatch/kit.js`): `paperSheet`, `woodSurface`, `darkWorld`, `stripedCloth`, `toolPill('Read', 'file.md')`, `planInk`, `dotHero(x, y, r, { dark, mood })`, `inkCard`, `inkTag`, `inkCaption`, `handText(str, x, y, size, o)`, `handW(size, str)`, `box`.
- Assets: `asset(name)`, `drawAsset(name, x, y, w, h, { fit: 'cover'|'contain', r, alpha })`. Real product UI only.
- Layout: `LX(f) = f*W`, `LY(f) = f*H`, `UNIT = min(W,H)/1080`, `PORTRAIT = H > W*1.2`, `WIDE = W > H*1.2`.

## 2.2 Time state (set by the renderer each frame)

- `F` absolute frame 0..NFRAMES-1. `TT` = absolute time **on the motion step**: styles on 2s move on `TT = B * 2 / FPS` where `B = Math.floor(t * 12)`... in practice: `B = floor(F / 2)` at 24 fps (12 steps/s); the boil, camera and every move share `B`. `STYLE.ones` styles (math, isometric) step every frame.
- `E0` = current era/shot start time. Scene-local scheduling: `TT - E0`.
- `ev(t, d = 0.25)` = clamped 0..1 progress of an event at absolute time `t` over `d` seconds.
- `popS(t)` = back-eased pop-in scale 0..1 over 0.25 s.
- `DEFER` overlay queue: captions drawn after the camera transforms; set by the renderer.

## 2.3 Springs (the default mover, closed-form and deterministic)

```js
const SPRING = {
  snappy:  { k: 320, d: 30 },   // UI, buttons, leading edges
  smooth:  { k: 170, d: 26 },   // cards, containers, the camera
  heavy:   { k: 90,  d: 19 },   // big type, logos, large objects
  playful: { k: 260, d: 14 },   // mascots, stickers: visible overshoot
};
springEase(t, k = 170, d = 26)          // 0 -> 1 over t seconds (underdamped = hair of overshoot)
springMove(t0, a, b, p = SPRING.smooth) // a value travelling a -> b starting at t0
springTrack([[t, v], ...], p)           // a value with many targets: one spring per change, summed,
                                        // so a mid-move retarget stays continuous (never restart an ease)
```

Raw `EZ` easings exist (`EZ.o2/o3/i2/i3/io/back`) and `seg`, but **springs over easing curves** for anything with mass. A value with many targets gets `springTrack`, never a restarted ease. On-2s styles step the springs every 2 frames, as they should.

## 2.4 Score API (`src/score.js`, scheduled in seconds; synth in `kit/score-head.js`)

`pluck(t, f, vel, pan?, dur?, bright?, send?)`, `noiseHit(t, dur, type, freq, q, vel, pan?, send?, sweepTo?)`, `sub(t, vel)`, `sweep(t0, t1, vel, f0, f1)`, `riser(t0, t1, vel)`, `chime(t, freqs, vel, pan?)`, `bass(t, f, vel)`, `blip(t, f0, f1, dur, vel)`, `pad(t0, t1, notes, peak, o?)`, `drone(t0, t1, f, peak, o?)`. Parts `to: 's'` are sfx (kept when a supplied track replaces the music bus). `kit/score-tail.js` = loudness stage (RMS to -17 dBFS, limiter at -1 dBFS; stems share mix gain so they sum back; export normalises to -14 LUFS and ducks under voice).

---

# PART 3 — MOTION SYSTEM (the in-betweener)

## 3.1 The clock is the law

- One motion step per boil step `B`: on-2s at 24 fps = 12 moves/s; at 30 fps step every 2 frames = 15 moves/s. Every executor of "smooth" is `TT`-derived, and `TT` derives from `B * 2 / FPS`.
- Never recompute time twice in one scene. Every animated quantity is `f(TT)`; a pose that must hold is `ev(t) >= 1`.

## 3.2 Beat grid timing

| term | value |
|---|---|
| beat | 0.5 s @ 120 BPM (15 f @ 30 fps, 12 f @ 24 fps) |
| 8th (`E8`) | 0.25 s (7.5 f @ 30 fps, 6 f @ 24 fps) |
| 16th | 0.125 s (3 f @ 24 fps) |
| hits | `onBeat(t)` snaps any time to the 8th grid; cuts and morph centres are proven by `review.mjs`, not by eye |

Walk/run/jump cycle lengths (fps-independent, with frame counts at 24/30 fps):

| action | classical reference | seconds | f @ 24 | f @ 30 |
|---|---|---|---|---|
| blink / head snap | 3-6 f @ 60 | 0.05-0.10 | 1-2 (use 2) |
| punch wind-up to contact | 7 f @ 60 | ~0.12 | 3 | 3-4 |
| walk cycle, 2 steps | 48 f @ 60 | 0.80 | 19 | 24 |
| run cycle, 2 steps | 16 f @ 60 | 0.27 | 6-7 | 8 |
| jump crouch -> land -> recover | 60 f @ 60 | 1.0 | 24 | 30 |
| hit-stop | 2 f @ 60 | 0.033-0.067 | 1-2 | 1-2 (hold the pose 2 f) |
| impact flash | 1-2 f @ 60 | 0.017-0.033 | 1 | 1 |
| shake decay | 8-14 f @ 60 | 0.13-0.23 | 4-6 | 6-8 |

Caption law: each caption on screen >= 1.25 s; <= 3.5 words/s. "Something new every 2-4 s" (a move, reveal, cut, reaction); `review.mjs` DEAD BEATS flags longer still stretches (silence acts exempt; `review.deadMax`).

## 3.3 The 12 principles, harness idiom

| # | principle | harness translation |
|---|---|---|
| 1 | Squash & stretch | deform in the **point math** (numerically scale head rx/ry or limb lengths); never `ctx.scale` on the stroke layer, or line weight wobbles |
| 2 | Anticipation | an event `0.9*T`, or a spring to `-0.12*D` for `0.15*T` before the main move; crouch key before launch |
| 3 | Staging | hero >= 60% of frame height in action (16:9: >= 500 px of 1080); `ctx.save(); camera(...)` layers background z0, character z1, FX z3; captions outside camera (deferred) |
| 4 | pose-to-pose | extremes as keyed times, `TT`-helpers fill the middles; never hand-draw per-frame |
| 5 | follow-through | delay a child track 2-4 frames: `head` ease lags `torso` (springTrack with a later key time) |
| 6 | slow in/out | `springMove` defaults; falls/rises that must be ballistic get `ev` with an authored easing curve, apex split (`EZ.o3` up / `EZ.i3` down), **not** one smooth segment |
| 7 | arcs | swing limbs via angles (radians), FK-compose joints from radians; never lerp hand (x, y) directly except IK contact |
| 8 | secondary action | idle overlays: `torso += Math.sin(TT * w) * amp`, blink every ~6 s, arm counter-swing; idle life is free and mandatory in held shots |
| 9 | timing | frame budget above; a duplicate key = hit-stop |
| 10 | exaggeration | push the extreme pose past anatomy (arm stretch 1.25x on the contact frame only, revert next key) |
| 11 | solid drawing | one source of truth for anatomy constants (§3.5 RIG); solve positions mathematically |
| 12 | appeal | silhouette test: fill black mentally, the action must read; cleanest shapes carry the story |

## 3.4 The stickman rig pattern (canvas edition, drop-in)

There is no shipped stickman kit; a piece defines its own rig in `src/scenes.js` from kit primitives. Contract the harness gives you: `wobble(..., key)` reseeds per boil step, so a limb drawn via `ink(P, { key: 'armR' })` boils automatically while the pose data stays global and poseable.

```js
// ---- rig constants (one source of truth; 1920x1080 reference) ----
const RIG = {
  HEAD_R: 34, NECK: 26, TORSO: 96, UA: 58, FA: 54, TH: 70, SH: 70,
  GROUND: 960,           // y of the floor line
  INKW: 10,              // uniform stroke; NEVER vary per frame
};
const rad = d => d * Math.PI / 180;

// pose: pure data (radians, 0 = straight down for limbs, 0 = up for torso; +x forward)
function solve(p, sq = 1) {                  // sq: squash <1 crouch, >1 stretch
  const J = {};                              // joints, y-up math, flipped at draw time
  J.hip    = [p.x, p.rootY * sq];
  J.neck   = [p.x + Math.sin(rad(p.torso)) * RIG.TORSO * sq, p.rootY * sq + Math.cos(rad(p.torso)) * RIG.TORSO * sq];
  J.head   = add(J.neck, [Math.sin(rad(p.torso + p.head)) * RIG.NECK * sq, Math.cos(rad(p.torso + p.head)) * RIG.NECK * sq]);
  J.sh     = lerpPt(J.hip, J.neck, (RIG.TORSO - 14) / RIG.TORSO);
  J.el     = add(J.sh, arm(p.armL, RIG.UA)); J.hand = add(J.el, arm(p.armL + p.elbowL, RIG.FA));
  // same for the far arm, legs: knee = hip + thigh(hipAng); foot = knee + shin(hipAng - kneeFlex)
  return J;
}
// draw: flip once at the wrapper, draw full-res points
function drawStickman(J) {
  const flip = ([x, y]) => [x, RIG.GROUND - y];               // world -> canvas (y-down)
  ink([flip(J.hip), flip(J.neck)], { w: RIG.INKW, key: 'torso' });
  ink([flip(J.sh), flip(J.el), flip(J.hand)], { w: RIG.INKW, key: 'armR' });  // near arm
  ink([flip(J.hip), flip(J.knee), flip(J.foot)], { w: RIG.INKW, key: 'legR' });
  // far limbs: lighter colour, same stroke width = free depth
  ink([flip(J.sh), flip(J.elF), flip(J.handF)], { w: RIG.INKW, key: 'armL', color: '#9a8f80' });
  const [hx, hy] = flip(J.head);
  paint(ellipsePts(hx, hy, RIG.HEAD_R * squashRx, RIG.HEAD_R * squashRy, rad(p.torso + p.head), 24),
        { fill: '#ffffff', w: RIG.INKW, key: 'head' });
}
```

- Angles: radians, measured from straight down for limbs, straight up for torso/head. Knee flex positive bends backward naturally; elbow positive curls forward.
- **IK for pins only** (foot planted on the ground, hand gripping the rim): solve the two-bone triangulation for the knee/elbow given the target; blend FK for swings. Contact law: while planted, the foot's world position is constant until lift-off (scroll `x` to compensate). Violation = foot-skate = the #1 amateur tell.
- Ballistics: time up ≈ time down; `EZ.o3` into the apex, `EZ.i3` into contact; never one inOut for a jump.
- Squash: values idle 1.0, landing crouch 0.8, launch stretch 1.12; head becomes an ellipse `rx = R*(1 + (1-sq)*0.8)`, `ry = R*sq`.

## 3.5 Move grammar (frame data -> harness schedule)

Compose every custom move from: **anticipation** (10-15% of the move, opposite direction, `EZ.i3`), **action** (1-3 frames, `EZ.o3` or spring `playful`), **impact hold** (2 frames duplicate: hit-stop), **settle** (`back` or `springTrack` target), **return** (`springMove(..., SPRING.smooth)`).

- Walk cycle (0.8 s/2 steps, at 30 fps 24 f): contact -> down -> passing -> up, mirrored half; stride per half-cycle ≈ `2 * (TH + SH) * sin(26°)` ≈ 55 units with the v1 rig values; drive x at exactly `stride / halfCycleSeconds` so feet do not skate, and scroll the stage, not the rig, when holding a tracking shot (feet then plant trivially).
- Run: 0.27 s/2 steps, both feet off the ground on the flight frames (`rootY` peaks there), torso pinned forward ~14°, elbows ~60° pumping, stride scroll ~2.7x walk.
- Jump/dunk beats at 30 fps: crouch (`in`, ~6 f) -> launch (`EZ.o3`, apex ~7 f after) -> tuck/rotate (8-12 f) -> lunge fill -> contact hand at rim (`snap`) -> hang (2-3 f) -> drop and land crouch (`EZ.i3`, ~6 f) -> recover (`springMove`, ~6 f).
- Smears: hand travel > 40 px/frame on a thin limb reads strobed; draw the limb at previous and next position at 35%/20% alpha for 1-2 frames max (this is exactly what ink doubling and hand-drawn smears imitate).
- Multi-target rule: any *new* target mid-move must retarget via `springTrack`, never restart `springMove`.

---

# PART 4 — FX AND SOUND AT THE IMPACT

## 4.1 The impact is the synchronisation anchor

The frame of contact keys off one time: `T_IMPACT = TIMELINE.cues.slam`. Everything lands on it:

| layer | technique |
|---|---|
| impact flash | 1 frame `fillAll('white')` at alpha 0.85 then gone (or inverted colours for style points) |
| hit-stop | duplicate the contact pose 2 frames (hold keys) |
| camera shake | ±14 px decaying 8-14 f; deterministic: `RNG('sx' + B).r(-1, 1) * mag` |
| shake wrapper | camera transform with `sx`, `sy` set |
| dust | 4 seeded circles puffed from the foot: `RNG('dust' + B)`; alpha fade via `ctx.globalAlpha` before `ink`/`paint` |
| speed lines | 8-10 `RNG`-seeded streaks (`cline`), radial from the impact point |
| burst FX | `sparkBurst(cx, cy, r)`, `burst(cx, cy, r0, r1)` |
| SFX | `noiseHit(T_IMPACT, ..., 's')` in `score.js` + a sub on the hit; landed on the exact frame |
| camera punch | zoom bump centred on the hero: `camOf({ z: 1 + amt * exp(-d * 7), p: [heroX, heroY] })` |

- `paint()`/`hatch()`/`pencil()` reset `globalAlpha`: to hide or fade, skip drawing (or set alpha on `ctx` before the call for your own primitives and restore after).
- Silence before payoff, loudest on the payoff (§6.3).

## 4.2 Sound rules that constrain the picture

- Score improves with the story: thin early, fullest at peak. Motifs carry characters (a rising fifth = the spark/hero).
- Payoff recipe: short chord stab (~0.4 s) + sub on the hit, *flat* after, nothing busy on top (a held chord or busy section outscores the hit).
- Silence needs a hard stop: dry sends in the preceding beat, every event ends before it, faint room tone at most.
- **You cannot hear the score.** Measure it: `review.mjs` SOUND section (loudest 100 ms window, the silence before it, LUFS), and tell the user to listen.

---

# PART 5 — WORKFLOW GATES (what must pass)

1. **Intake + look check**: build `gallery.mjs`, pick/reference the style; when matching user references: `measure/refs.mjs` first, the piece's style frames *are* the check-in.
2. **Story check** (text, fast): format, style, length, BPM from `TIMELINE.acts`; numbered beat table (time, what happens, bridge into the next beat, sound's role). Approve / change / different angle, repeat until approved.
3. **Storyboard check**: `TIMELINE.board` filled (one key time per beat), `storyboard.mjs`, per-panel thumbs up/down from the owner. **No animating before this passes.**
4. **Build loop**: animate scenes from cues -> `build.mjs` -> tile across every cut/morph and READ THE TILES -> score -> `export.mjs --share` -> `review.mjs` -> fix flagged items, re-run -> per-shot PASS table in `LOG.md`, name the weakest shot and its fix.
5. **Every frame checked against** `grammar/FRAME.md`: one constant the eye can hold (a hero with a face/mood); colour reserved for the story's one thing; the medium visible at phone size; the idea acted out not labelled; something happening (idle life in held shots); text in the world (>= 50 px at 1080 wide, >= ~100 px things that matter); scale varies with >= 1 extreme close-up; a recurring thread across frames; phone-safe (9:16: x 60-940, y 250-1500).

---

# PART 6 — STICKMAN-DUNK LEDGER (cold-start facts)

Path: `pieces/stickman-dunk/`. Spec: `piece.json` (16:9, 1920x1080, **30 fps**, 120 BPM, 5.0 s, 150 frames, crosshatch, storyFormat "action-scene", safe margins 120 px all sides). Built: `src/` (scenes.js, bridges.js, head.html, score.js), `renders/final.mp4` + stems. Missing: `brief.md`, `LOG.md`. Active work plan: `pieces/stickman-dunk/plan.md` (read it; it owns the fix list).

Recorded defects (from the 2026-10-17 frame review):

1. Stray 3-pt arc sweeping through the runner (scenes.js, 3-Point Arc block); must stay on the floor plane or read as a wire.
2. Flight window too long (`1.9 s`: 1.5 s -> 3.4 s) with a too-high apex: head/ball collide with the rafter banner row (y 60-170) around f45-f60; legs dangle instead of scissor.
3. Caption collisions: `WINDMILL!` at 1050,240 sits under the figure's arm/head at f90; `10 / 10` at 1400,300 sits on the backboard at f148 (final glyph swallowed). Both are `handText` calls; textcheck over the eye.
4. Act-3 rim hang: figure straddles rim/net/pole and merges visually (f120); shift ~60 px left so only the hands touch the rim.
5. Edge crossings: speed lines cut at the left edge at t=0; ending ball rolls to ~x1880 (half-clipped; safe margin 120 px, clamp to <= W-140).

Stages: (1) restore the workspace harness from upstream `cth9191/animate` (`tools/`, `kit/`, `styles/`, `grammar/`, `templates/` sit inside this skill dir already at `plugins/animate/skills/animate/`; the project root may just need them surfaced, do not overwrite `pieces/`), write `brief.md` + `LOG.md`, sanity stills f0/30/60/90/120/148. (2) Frame repair with a storyboard check-in before locking beats. (3) tile across cuts (1.5/2.8/3.4/3.9 s region), `review.mjs` fixes + PASS table, `export.mjs --share`. Open owner decision: keep strict 5.0 s vs extend ~5.5-6.0 s (recommendation: extend; the floaty feel is time pressure).

Working rules: git author `akulmach74`; never commit `thumbnails/` or `.obsidian/` as a side effect; the agent reviews PNGs with its own vision.

---

# PART 7 — COMMON MISTAKES IN THIS STACK

| symptom | cause | fix |
|---|---|---|
| `deterministic: false` in tile | trying to read a previous frame's content / off-book randomness | clean-sheet drawing; `RNG(...)` seeds only |
| page shows stale visuals after src edits | edited the built `index.html` | always edit `src/` parts, rebuild |
| frozen preview / wrong frame | using real frame numbers where `TT` (seconds) is expected | read §2.2; helpers take seconds |
| jerk after every stop | restarts of `springMove` per target | `springTrack` for multi-target values |
| feet skate | walk scroll speed <> stride, or planted foot drifting | §3.4 contact law |
| limbs rubbery | lerping hand/foot (x, y) instead of joint angles | FK angles (§3.4) |
| line weight wobbles | `ctx.scale` on the stroke layer | deform point math, not the transform |
| captions upside-down/camera-warped | drawn under the camera transform | captions after `DEFER`/`screen()` reset |
| impacts feel weak | FX not stacked at the frame | §4.1: flash + 2 f hold + shake + dust + SFX all keyed to `T_IMPACT` |
| text cut at a shot edge | eye-tested | `textcheck.mjs` + `review.mjs` -> TEXT; deliberate crowding goes in `review.textIgnore` with a reason |
| eras identical on contact sheets | eras differ only in motion | give each era a still-visible signature |
| jitters/long renders | giant blur filters, huge node counts | ghost copies not blurs; canvas stays lean |
| flat look | no texture clipping in fills, no boil | crosshatch frame checklist (`STYLE.md`): every filled shape textured, the line boils |
| cuts feel abrupt | hard cuts on static frames | cut on action; hard cuts land on finished/active frames only |

## Glossary (short)

Beat = 1/2 s @ 120 BPM. **8th/16th** = grid cuts land on (0.25/0.125 s). **Boil** = hand-drawn shimmer; reseeded per 2-frame step (`B`). **On 2s** = motion steps every 2 frames. **Hit-stop** = 2-frame hold of the contact pose. **Write-on** = ink/hand text drawn on partially (`frac`). **Era** = a shot/scene function's time range; **bridge** = its morph window; **cut** = hard boundary. **TT/E0** = scene-relative motion clock and era start. **Board** = `TIMELINE.board`, the approval storyboard. **Pass table** = per-shot PASS report written into `LOG.md`.

---

*Sources (authoritative): `plugins/animate/skills/animate/SKILL.md`, `craft.md`, `grammar/FORMATS.md`, `grammar/STORY.md`, `grammar/FRAME.md`, `kit/core.js`, `kit/morph.js`, `kit/score-*.js`, `templates/piece/*`, `styles/<name>/STYLE.md` + `kit.js`; piece state: `pieces/stickman-dunk/plan.md`, `piece.json`, `src/*`. Same code + same frame == same pixel: that property, and the measured review gates, are what make the output smooth.*
