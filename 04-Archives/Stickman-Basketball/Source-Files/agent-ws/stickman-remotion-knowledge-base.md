# STICKMAN ANIMATION KNOWLEDGE BASE
## Complete Training Document for AI: Producing Buttery-Smooth Stickman Animation with Remotion + SVG

> **Purpose of this document:** This is a machine-consumable knowledge base. An AI that has ingested this file should be able to *design, code, and render* professional-grade stickman animation using **Remotion** (React-based programmatic video) and **SVG** (vector recreation of the stick figure). It expands a 3-pillar source framework — (1) the Principles of Animation, (2) the Alan Becker traditional methodology, (3) the modern AI-assisted pipeline — into an exact, code-level discipline.
>
> **Target stack:** Remotion v4.x, React 18+/19+, TypeScript, plain inline SVG inside Remotion compositions. No CSS transitions, no external animation libraries required.

---

# PART 0 — HOW AN AI SHOULD CONSUME THIS DOCUMENT

When asked to "animate a stickman doing X", follow this priority order:

1. **Golden rule:** Every visual value must be a pure function of `useCurrentFrame()`. Never use CSS transitions, `setTimeout`, `Date.now()`, or unseeded `Math.random()` — Remotion renders frames in parallel headless browsers and any non-determinism shows up as flicker.
2. Plan the motion as a **beat sheet** (§9.2) before writing code.
3. Build poses with the **rig spec and pose schema** (§3). Never hand-draw one-off SVG paths per frame — always parameterize through the rig so line weight and proportions stay uniform.
4. Use **move library keyframes** (§4) as starting data; tune by ±20%.
5. Apply **smoothness engineering** (§5): easing choice, anticipation, overshoot, arcs, ground-contact rules.
6. Add **FX** (§6) at impact frames: flash + hit-stop + shake + dust, layered.
7. Sync audio on exact frame boundaries (§2.5).
8. Run the **final checklist** (§5.6) before declaring done.

---

# PART 1 — ANIMATION THEORY (FOUNDATIONS)

## 1.1 The 12 Principles of Animation — translated for stickman + code

The source guide highlights Squash & Stretch, Anticipation, Staging, and Timing & Spacing. Here are all 12, each with its stickman-specific meaning and its Remotion/SVG implementation.

| # | Principle | Classic meaning | Stickman translation | Remotion/SVG implementation |
|---|-----------|-----------------|----------------------|------------------------------|
| 1 | **Squash & Stretch** | Mass deforms under force, volume preserved | Head becomes an ellipse on impact; torso compresses in a crouch; body elongates mid-launch | `squash` factor in the pose schema (§3.5). Scale bone *lengths* numerically in the FK solver — never scale the `<g>` transform, or stroke widths distort |
| 2 | **Anticipation** | A wind-up before the action | Deep crouch before a jump; arm pulls back before a punch | A keyframe 8–12 frames before the action key, moving ~12% of the main displacement in the *opposite* direction (formula §5.2) |
| 3 | **Staging** | Audience must instantly read the action | Keep the stickman ≥60% of frame height during action, centered or rule-of-thirds; far limbs rendered in lighter gray for depth | `<AbsoluteFill>` layers: background `zIndex: 0`, character `zIndex: 1`, FX `zIndex: 2`; camera transform wrapper (§7) |
| 4 | **Straight Ahead vs Pose-to-Pose** | Draw sequentially vs plan extremes | Always work **pose-to-pose**: define extreme poses as keyframes, let the engine in-between | Keyframe track system (§3.4) — poses keyed per frame, sampled with easing |
| 5 | **Follow-Through & Overlap** | Appendages lag behind the core | Arms and head lag 2–4 frames behind torso on stops and direction changes | Offset related param tracks: e.g. `head` eases toward its target with a 3-frame delayed ramp (§5.3) |
| 6 | **Slow In & Slow Out** | Movement accelerates/decelerates | Every keyframe transition uses easing, never linear (except machine-like motion or mid-flight) | `Easing.inOut(Easing.quad)` default; `ease-out` for rises, `ease-in` for falls (ballistics §5.2) |
| 7 | **Arcs** | Limbs travel in arcs, not lines | Fists and feet curve through space during swings | Swing limbs via *angle* interpolation in FK (angles naturally produce arcs at the extremity) — never lerp the hand's (x,y) directly unless planting on a target (then use IK §3.7) |
| 8 | **Secondary Action** | Extra motion supporting the main one | Coat-tail flaps → for stickman: head bob, arm counter-swing, dust at feet | Sinusoidal overlays added to base tracks: `torso += Math.sin(frame/9) * 1.5` at idle |
| 9 | **Timing** | Number of frames = perceived weight/speed | Heavy landing: slow. Snap punch: fast (see timing chart §1.2) | Frame budgeting table (§1.2); duplicate a keyframe to hold ("hit-stop") |
| 10 | **Exaggeration** | Push poses past realism | Crouch lower than anatomically needed; stretch the punch arm 1.3× | Bone-length multiplier passed through pose at the impact key only (e.g. `FA * 1.25` on the contact frame, reverting next key) |
| 11 | **Solid Drawing** | Form has volume | Consistent head radius, consistent bone lengths, no wobbling proportions | Single source of truth `RIG` constants (§3.2); solve positions mathematically — never eyeball per-frame SVG |
| 12 | **Appeal** | Character is watchable | Clean silhouette, rhythmic motion, personality via posture | Silhouette test: render pose in solid black — if the action reads, appeal holds (§5.6 checklist) |

## 1.2 Timing & Spacing — the animator's frame budget

Timing is *how many frames*; spacing is *how far between frames*. Together they are the texture of motion.

**Frame rates:** Animate at **60 fps** in Remotion for buttery output. Relation to classic animation:

| Classic term | Meaning | 60-fps equivalent |
|---|---|---|
| "On ones" | New drawing every frame (24fps) | New pose every frame — use for fast action |
| "On twos" | Hold each drawing 2 frames (classic standard) | Duplicate key values so a pose holds 2 frames — snappy, anime-like feel |
| "Hold" | Drawing frozen for N frames | Same key value repeated across keys |

**Standard stickman timings @60fps** (calibrate everything else against these):

| Action | Duration | Notes |
|---|---|---|
| Blink / head snap | 3–6 f | |
| Punch wind-up → contact | 7 f | Contact held 2 f (hit-stop) |
| Full walk cycle (2 steps) | 48 f | 1.25 steps/sec, casual |
| Full run cycle (2 steps) | 16 f | 3.75 steps/sec |
| Jump: crouch → land → recover | ~60 f | Ballistic middle |
| Impact flash | 1–2 f | Sub-perceptual but felt |
| Camera shake decay | 8–14 f | |
| Scene beat / dialogue line | 60–180 f | |

**Spacing rule:** For smooth perceived motion, spacing between consecutive frames must change *continuously*. An abrupt jump from 12px of travel to 2px of travel reads as a hitch. Easings exist to keep spacing continuous — keyframe velocity curves must meet at matched slopes (§5.1).

## 1.3 The Alan Becker traditional workflow — mapped to code

The source guide's traditional pipeline, translated into a Remotion pipeline:

| Traditional step | Purpose | Remotion equivalent |
|---|---|---|
| Storyboarding | Sketch shot sequence | Write the **beat sheet** (§9.2) — a JSON/Markdown table of shots |
| Animatic | Rough timed layout | Build a grey-box comp: stickman as a single line + title cards in `<Sequence>`s, validating pacing *before* detail |
| Keyframing | Draw extreme poses | Emit pose keyframes (§3.4 schema) at beat boundaries |
| In-betweening | Fill transitions | `samplePose()` interpolation with per-param easing — the machine is the in-betweener |
| Uniform line weight | Consistency | `RIG.STROKE` constant; never vary |
| Layer separation | Background vs character | Separate `<AbsoluteFill style={{zIndex}}>` layers; character layer is a pure function of frame |

**Becker-style quality bar:** readability over realism; impact frames are short and loud; fights have geography (establish positions, keep left/right consistent).

---

# PART 2 — REMOTION MASTERY

## 2.1 Setup

```bash
npm create video@latest        # scaffold (choose TypeScript template)
cd my-video
npx remotion studio            # live preview with timeline scrubbing
npx remotion render StickmanFight out/fight.mp4   # render
```

Minimal composition registration (`src/Root.tsx`):

```tsx
import {Composition} from 'remotion';
import {FightScene} from './FightScene';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="StickmanFight"
    component={FightScene}
    durationInFrames={600}   // 10s @ 60fps
    fps={60}
    width={1920}
    height={1080}
  />
);
```

## 2.2 Core API cheat sheet (v4.x)

| API | Signature | Use |
|---|---|---|
| `useCurrentFrame()` | `() => number` | The only time source. 0-indexed; **local** to the enclosing `<Sequence>` |
| `useVideoConfig()` | `() => {fps, width, height, durationInFrames}` | Composition constants |
| `interpolate` | `interpolate(x, [i0,i1,...], [o0,o1,...], {easing?, extrapolateLeft?, extrapolateRight?})` | Workhorse mapper. **Always** pass `extrapolateRight: 'clamp'` (and usually left) unless intentional looping |
| `Easing` | `Easing.linear / .quad / .cubic / .in(fn) / .out(fn) / .inOut(fn) / .bezier(x1,y1,x2,y2) / .back(...)` | Curve library for `interpolate` |
| `spring` | `spring({frame, fps, config?: {damping, stiffness, mass}, delay?, durationInFrames?})` | Physics 0→1 driver. `config: {damping: 200}` = smooth no-bounce; low damping = overshoot (great for follow-through & camera punch) |
| `measureSpring` | `measureSpring({fps, config})` | Frames a spring needs to settle — for budgeting durations |
| `random` | `random('seed-string')` | Deterministic 0–1. **Required** instead of `Math.random()`. Seed per frame for shake: `random(`sx${frame}`)` |
| `Sequence` | `<Sequence from={f} durationInFrames={n}>` | Timeline slice; children's frames restart at 0 relative to `from` |
| `AbsoluteFill` | `<AbsoluteFill style={...}>` | Full-frame absolutely-positioned layer |
| `Audio` | `<Audio src={staticFile('hit.mp3')} startFrom={frames} volume={0.8}/>` | Place inside a `<Sequence>` at the exact impact frame |
| `staticFile` | `staticFile('path/in/public')` | Asset URLs |
| `interpolateColors` | `interpolateColors(x, [i0,i1], ['#fff','#000'])` | Color ramps (impact flashes, day/night) |

## 2.3 The golden rendering rules (violations = flicker/broken renders)

1. **Every pixel is a pure function of frame.** No `useState`/`useEffect` for visuals, no CSS `transition`/`animation`, no Tailwind `animate-*`.
2. **Never `Math.random()`** — use Remotion's `random(seed)`.
3. **Clamp extrapolation** on every `interpolate` unless you deliberately want runaway values.
4. Prefer animating `transform`/`opacity` at the element level; avoid layout-triggering props (width/height/top/left) for 60fps hero motion.
5. Under SVG, remember `transform` on `<g>` is the attribute-style transform; percentage reference frames differ from CSS.
6. If you scale an SVG group, add `vector-effect="non-scaling-stroke"` to strokes — or better, don't scale groups at all (scale numbers in the solver, §3.5).

## 2.4 Sequencing pattern

```tsx
<AbsoluteFill>                             {/* master layer */}
  <Sequence from={0} durationInFrames={180}>
    <WalkIn />                             {/* frames 0..179 local */}
  </Sequence>
  <Sequence from={170} durationInFrames={10}>
    <FlashFrame />                         {/* 10-frame overlap = soft transition */}
  </Sequence>
  <Sequence from={180} durationInFrames={420}>
    <Fight />
  </Sequence>
</AbsoluteFill>
```

- Overlapping sequences by 5–15 frames creates cross-dissolve windows.
- Because `useCurrentFrame()` is sequence-local, write each scene component assuming frame 0 = scene start.

## 2.5 Audio & beat sync

- Convert any timed event to frames: `frame = Math.round(seconds * fps)`.
- Drop SFX exactly on impact frames:

```tsx
<Sequence from={PUNCH_IMPACT}>
  <Audio src={staticFile('sfx/punch.mp3')} volume={0.9} />
</Sequence>
```

- For music-driven cuts: choose BPM-friendly frame multiples. At 120 BPM, a beat = 0.5 s = 30 frames @60fps. Keep cuts, launches and landings on multiples of the beat frame interval.
- Advanced: `getAudioData()` from `@remotion/media-utils` returns waveform/spectrum data (pair with `delayRender` or `calculateMetadata`) to drive shake intensity or pulse scale from actual audio energy.

---

# PART 3 — SVG STICKMAN ENGINEERING

## 3.1 Coordinate system: the y-flip wrapper

SVG y grows downward; animation intuition is y-up. Solve once, globally: render the character inside a flipped group. All rig math below is **y-up, +x = forward**, exactly like an animator's scene planning.

```tsx
const GROUND_Y = 960; // px from top of a 1080p comp; feet rest here
const STAGE_X = 960;  // default horizontal stage position

<g transform={`translate(${STAGE_X + pose.x}, ${GROUND_Y}) scale(1, -1)`}>
  <StickmanRig pose={pose} />
</g>
```

Inside the group: ground = y 0, pelvis rides at `rootY ∈ [0, ~200]`, limbs use intuitive angles. (Keep text outside flipped groups.)

## 3.2 The rig — fixed anatomy constants

```ts
export const RIG = {
  HEAD_R: 20,   // head radius
  HEAD_OFF: 26, // neck top -> head center distance
  TORSO: 54,    // pelvis -> neck
  UA: 32,       // upper arm
  FA: 30,       // forearm
  TH: 38,       // thigh
  SH: 38,       // shin
  STROKE: 9,    // uniform line weight — NEVER vary per frame
};
```

Total model height ≈ 174 units, big-head cartoon proportion. Scale the whole flipped group (`scale(1.4,-1.4)` + `vector-effect="non-scaling-stroke"`) or scale all constants to resize.

**Angle conventions (memorize exactly):**
- Limb angles are measured **clockwise from straight-down**: `0°` = hangs down, `+90°` = points forward (+x), `±180°` = straight up.
- `knee` = flexion amount, **positive bends backward** (natural knee). Computed as `shinAngle = hip - knee`.
- `elbow` = flexion amount, **positive curls forward** (natural elbow). `forearmAngle = shoulder + elbow`.
- `torso`/`head` measured from straight-up, `+` leans forward.

## 3.3 Forward-kinematics solver + component (complete, copy-pasteable)

```tsx
// rig.tsx
import React, {useMemo} from 'react';

export type Vec = [number, number];
const rad = (d: number) => (d * Math.PI) / 180;
const dd = (a: number, l: number): Vec => [Math.sin(rad(a)) * l, -Math.cos(rad(a)) * l]; // 0° = down
const du = (a: number, l: number): Vec => [Math.sin(rad(a)) * l,  Math.cos(rad(a)) * l]; // 0° = up
const add = (a: Vec, b: Vec): Vec => [a[0] + b[0], a[1] + b[1]];

export interface StickPose {
  x: number;      // forward travel (applied at wrapper)
  rootY: number;  // pelvis height above ground
  torso: number;  // lean, +fwd
  head: number;   // rel. to torso, +fwd
  lSh: number; lEl: number;   // left  = FAR arm (drawn dim, behind)
  rSh: number; rEl: number;   // right = NEAR arm
  lHip: number; lKnee: number;
  rHip: number; rKnee: number;
  squash: number; // 1 = neutral, <1 squashed, >1 stretched (§3.5)
}

export const IDLE: StickPose = {
  x: 0, rootY: 74, torso: 4, head: 2,
  lSh: 6, lEl: 14, rSh: -4, rEl: 16,
  lHip: -4, lKnee: 6, rHip: 6, rKnee: 6, squash: 1,
};

export function solve(p: StickPose) {
  const sq = p.squash;
  const hip: Vec = [0, p.rootY];
  const neck = add(hip, du(p.torso, RIG.TORSO * sq));
  const headC = add(neck, du(p.torso + p.head, RIG.HEAD_OFF * sq));
  const shoulder = add(hip, du(p.torso, (RIG.TORSO - 8) * sq));
  const lElbow = add(shoulder, dd(p.lSh, RIG.UA));
  const lHand = add(lElbow, dd(p.lSh + p.lEl, RIG.FA));
  const rElbow = add(shoulder, dd(p.rSh, RIG.UA));
  const rHand = add(rElbow, dd(p.rSh + p.rEl, RIG.FA));
  const lKnee = add(hip, dd(p.lHip, RIG.TH));
  const lFoot = add(lKnee, dd(p.lHip - p.lKnee, RIG.SH));   // knee flex positive = backward
  const rKnee = add(hip, dd(p.rHip, RIG.TH));
  const rFoot = add(rKnee, dd(p.rHip - p.rKnee, RIG.SH));
  return {hip, neck, headC, shoulder, lElbow, lHand, rElbow, rHand, lKnee, lFoot, rKnee, rFoot};
}

export const StickmanRig: React.FC<{
  pose: StickPose; color?: string; farColor?: string; opacity?: number;
}> = ({pose, color = '#111111', farColor = '#9aa0a6', opacity = 1}) => {
  const j = useMemo(() => solve(pose), [JSON.stringify(pose)]);
  const seg = (a: Vec, b: Vec, c: string) => (
    <line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={c}
          strokeWidth={RIG.STROKE} strokeLinecap="round" />
  );
  const headRx = RIG.HEAD_R * (1 + (1 - pose.squash) * 0.8);
  const headRy = RIG.HEAD_R * pose.squash;
  return (
    <g fill="none" opacity={opacity}>
      {seg(j.shoulder, j.lElbow, farColor)}{seg(j.lElbow, j.lHand, farColor)}
      {seg(j.hip, j.lKnee, farColor)}{seg(j.lKnee, j.lFoot, farColor)}
      {seg(j.hip, j.neck, color)}
      {seg(j.shoulder, j.rElbow, color)}{seg(j.rElbow, j.rHand, color)}
      {seg(j.hip, j.rKnee, color)}{seg(j.rKnee, j.rFoot, color)}
      <ellipse cx={j.headC[0]} cy={j.headC[1]} rx={headRx} ry={headRy}
               stroke={color} strokeWidth={RIG.STROKE} fill="white" />
    </g>
  );
};
```

Design notes: far limbs (left) are drawn first in light gray → free depth cue, same stroke width (uniform line weight rule). Head is an ellipse so squash can deform it without touching anything else.

## 3.4 Pose keyframe schema + sampling engine (the "in-betweener")

This is the contract between an AI planner and the renderer. Poses are pure data; the engine interpolates **each parameter on its own track** (a param only needs a key where it changes).

```ts
// engine.ts
export type EaseName = 'lin' | 'in' | 'out' | 'inOut' | 'snap' | 'backOut';
export const EASE: Record<EaseName, (t: number) => number> = {
  lin: t => t,
  in: t => t * t,                                   // accelerating (falls, wind-ups into contact)
  out: t => 1 - (1 - t) * (1 - t),                  // decelerating (rises, arrivals)
  inOut: t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2), // default
  snap: t => 1 - Math.pow(1 - t, 4),                // violent attack (punch extension)
  backOut: t => {                                    // overshoot & settle (follow-through)
    const c = 1.70158;
    return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2);
  },
};

export interface Key { f: number; pose: Partial<StickPose>; e?: EaseName } // e = easing INTO this key

const PARAMS: (keyof StickPose)[] = [
  'rootY', 'torso', 'head', 'lSh', 'lEl', 'rSh', 'rEl',
  'lHip', 'lKnee', 'rHip', 'rKnee', 'squash', 'x',
];

function sampleParam(keys: Key[], k: keyof StickPose, base: number, f: number): number {
  const pts = keys.filter(kk => kk.pose[k] !== undefined)
    .map(kk => ({f: kk.f, v: kk.pose[k] as number, e: kk.e ?? 'inOut'}))
    .sort((a, b) => a.f - b.f);
  if (pts.length === 0) return base;
  if (f <= pts[0].f) return pts[0].v;
  if (f >= pts[pts.length - 1].f) return pts[pts.length - 1].v;
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1];
    if (f >= a.f && f <= b.f) {
      const t = (f - a.f) / (b.f - a.f);
      return a.v + (b.v - a.v) * EASE[b.e](t);
    }
  }
  return base;
}

export function samplePose(keys: Key[], base: StickPose, f: number): StickPose {
  const out = {...base};
  for (const k of PARAMS) out[k] = sampleParam(keys, k, base[k], f);
  return out;
}
```

**JSON form an AI can emit** (validated against the same shape):

```json
{
  "base": "IDLE",
  "keys": [
    {"f": 0,  "pose": {"torso": 4}},
    {"f": 6,  "e": "in",   "pose": {"rootY": 48, "torso": 20, "rSh": -35, "rEl": 10}},
    {"f": 9,  "e": "snap", "pose": {"rootY": 76, "torso": 12, "rSh": 78, "rEl": 2}},
    {"f": 11, "e": "lin",  "pose": {"rootY": 76, "torso": 12, "rSh": 78, "rEl": 2}},
    {"f": 18, "e": "backOut","pose": {"torso": 5, "rSh": 12, "rEl": 28}}
  ]
}
```

(That is a complete punch, by the way: wind-up, snap, 2-frame hit-stop hold, overshoot settle.)

## 3.5 Squash & stretch without stroke distortion

The `squash` factor (pose field) is applied in the **solver arithmetic**, not in a transform:

- `rootY *= squash` implicitly via keyed values (you key the crouch yourself).
- `TORSO * squash` and `HEAD_OFF * squash` compress the upper body; legs stay planted via knee keys — feet never slide.
- Head: `rx = R·(1 + (1−sq)·0.8)`, `ry = R·sq` → near volume-preserving ellipse.
- Typical values: idle 1.0, landing crouch 0.8, launch stretch 1.12, impact frame 0.75 **for one frame only**.

## 3.6 Smears & bendy limbs (high-speed frames)

For swings faster than ~40 px of hand travel per frame, in-betweens look strobed. Classic fix: **smear frames**.

- **Triple-limb smear:** on the fastest 1–2 frames, additionally render the limb at its previous and next positions at 35%/20% opacity.
- **Curved smear:** draw the limb as a `path` with a quadratic curve through previous→current joint positions:

```tsx
<path d={`M ${prevSh[0]} ${prevSh[1]} Q ${midCtrl[0]} ${midCtrl[1]} ${curHand[0]} ${curHand[1]}`}
      stroke="#111" strokeWidth={RIG.STROKE} strokeLinecap="round" fill="none" opacity={0.5} />
```

Whichever you use, restrict smears to 1–3 consecutive frames or they read as blur mud. (Afterimages for whole-body speed: §6.5.)

## 3.7 Optional: two-bone IK (planting hands/feet on targets)

FK drives swings; IK drives *plants* (hand on a ledge, foot pinned on ground while the body shifts). Analytic two-bone IK:

```ts
export function ik2(S: Vec, T: Vec, a: number, b: number, bendForward: boolean): {E: Vec; T: Vec} {
  const dx = T[0] - S[0], dy = T[1] - S[1];
  let d = Math.hypot(dx, dy);
  d = Math.min(Math.max(d, Math.abs(a - b) + 0.001), a + b - 0.001);
  const baseAng = Math.atan2(dy, dx);
  const cosA = (a * a + d * d - b * b) / (2 * a * d);
  const off = Math.acos(Math.min(1, Math.max(-1, cosA))) * (bendForward ? 1 : -1);
  const E: Vec = [S[0] + Math.cos(baseAng + off) * a, S[1] + Math.sin(baseAng + off) * a];
  return {E, T};
}
```

Usage: when a foot must stay nailed to `(fx, 0)` while `rootY` sinks (landing absorb), solve `ik2(hip, footTarget, TH, SH, true)` for knee and draw those segments instead of FK legs for those frames. Blend FK→IK at a contact key and back at lift-off.

---

# PART 4 — MOVE LIBRARY (ready key data @60fps)

All tables use the pose schema keys. Values are calibrated starting points — nudge ±20% for personality. Easings: default `inOut`; noted otherwise.

## 4.1 Idle breathing (loop 120f)

Overlay, don't key, for perfect smoothness:

```ts
const breathe = Math.sin(frame / 19) * 1.4;
const pose = {...IDLE, torso: IDLE.torso + breathe * 0.6, head: IDLE.head - breathe * 0.5,
              rootY: IDLE.rootY + Math.sin(frame / 19) * 0.7};
```

Add a 6f blink-equivalent (head tilts +3°) every ~150f for life.

## 4.2 Walk cycle — 24f half-cycle, mirrored for steps 2 (loop 48f)

| f | rootY | torso | rHip | rKnee | lHip | lKnee | rSh | rEl | lSh | lEl |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 (R contact) | 70.5 | 6 | 26 | 4 | −22 | 14 | −22 | 18 | 24 | 14 |
| 6 (down) | 69 | 5 | 12 | 16 | −8 | 42 | −12 | 22 | 10 | 20 |
| 12 (passing) | 76 | 7 | −6 | 8 | 14 | 62 | 10 | 26 | −8 | 26 |
| 18 (up) | 74 | 6 | −18 | 6 | 26 | 18 | 18 | 18 | −18 | 18 |
| 24 = f0 mirrored | | | | | | | | | | |

```ts
const mirror = (p: StickPose): StickPose => ({...p,
  lSh: p.rSh, rSh: p.lSh, lEl: p.rEl, rEl: p.lEl,
  lHip: p.rHip, rHip: p.lHip, lKnee: p.rKnee, rKnee: p.lKnee});

const local = frame % 48;
const pose = local < 24 ? samplePose(WALK_KEYS, IDLE, local)
                        : mirror(samplePose(WALK_KEYS, IDLE, local - 24));
```

**Foot-skate rule:** forward scroll speed must match stride. Stride per 24f ≈ `2·(TH+SH)·sin(26°)` ≈ 67 units → `speed ≈ 2.8 u/frame`. Scroll the stage (`x`) at exactly that, or feet slide.

## 4.3 Run cycle — 16f loop (8f mirrored), with flight phase

| f | rootY | torso | rHip | rKnee | lHip | lKnee | rSh | rEl | lSh | lEl |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 (R contact) | 72 | 14 | 34 | 12 | −26 | 34 | −34 | 60 | 30 | 65 |
| 4 (flight) | 84 | 15 | 12 | 40 | 2 | 60 | −12 | 58 | 8 | 62 |
| 8 (pass) | 76 | 15 | −8 | 30 | 26 | 55 | 12 | 60 | −16 | 64 |
| 12 (flight 2) | 82 | 14 | −24 | 45 | 34 | 18 | 26 | 62 | −28 | 60 |
| 16 = mirror of f0 | | | | | | | | | | |

Run DNA: both feet off ground on frames 4–6 and 12–14 (`rootY` peaks there), torso pinned forward, elbows at ~60° pumping.

## 4.4 Jump (single shot, 60f)

| f | e (into key) | rootY | torso | rHip | rKnee | lHip | lKnee | rSh | rEl | lSh | lEl | squash |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | – | 74 | 4 | 6 | 6 | −4 | 6 | −4 | 16 | 6 | 14 | 1 |
| 8 | in | 46 | 18 | 22 | 55 | 22 | 55 | −30 | 10 | −30 | 10 | 0.85 |
| 12 | snap | 84 | −6 | −8 | 2 | −8 | 2 | 165 | 8 | 160 | 8 | 1.12 |
| 20 | lin | 150 | 10 | −20 | 80 | −20 | 80 | 120 | 15 | 115 | 15 | 1 |
| 28 | out | 168 | 8 | −25 | 85 | −25 | 85 | 90 | 20 | 85 | 20 | 1 |
| 36 | in | 120 | 8 | 15 | 25 | 15 | 25 | 60 | 25 | 55 | 25 | 1 |
| 42 | snap | 62 | 22 | 30 | 45 | 30 | 45 | 35 | 20 | 30 | 20 | 0.9 |
| 50 | inOut | 52 | 16 | 34 | 60 | 34 | 60 | −15 | 25 | −18 | 25 | 0.82 |
| 60 | backOut | 74 | 4 | 6 | 6 | −4 | 6 | −4 | 16 | 6 | 14 | 1 |

Ballistics built from easing: rise decelerates (`out` into apex f28), fall accelerates (`in` into contact f42). Crouch = anticipation (f8), landing crouch + settle = follow-through (f50–60).

## 4.5 Punch (22f) — the reference impact

Already given as JSON in §3.4. Keys: f0 idle → f6 wind-up (opposite direction −) → f9 contact (snap in, arm exaggeration: render forearm at `FA·1.25` this frame) → f9–11 **hit-stop hold** → f18 backOut settle → f22 idle. FX stack fires at f9 (§6).

## 4.6 Kick (20f)

f0 idle → f4 chamber: `rHip 55, rKnee 95, torso −12, lHip −6, lKnee 12` (support flex) → **f7 snap extend**: `rHip 65, rKnee 4, torso −18, rSh −40, lSh 45` (balance arms), impact FX → f9 hold → f14 rechamber (`rKnee 70`) → f20 idle via backOut.

## 4.7 Getting hit (18f) — sells your opponent's punch

f0 idle → f2: `head −25, torso −12, rootY 76` (snap *back*, `in` ease) → f5: `rootY 68, torso −18, rSh 40, lSh −40` (flail, snap) → f9: `rootY 60, torso −8` (stagger low) → f14: `torso 6, backOut` → f18 idle. Knockdown: extend f9 → rotate whole rig −80° around the foot contact point over 12f, dust on touchdown.

## 4.8 Backflip recipe (36f)

Rotate the *whole flipped rig group* around the hip:

```ts
const rot = interpolate(frame, [4, 26], [0, -360], {easing: Easing.inOut(Easing.cubic), extrapolateRight: 'clamp', extrapolateLeft: 'clamp'});
// rootY keys: f0 74 → f4 50 (crouch) → f14 190 (apex, tuck knee 100) → f26 58 (land) → f34 74 (recover)
<g transform={`translate(${STAGE_X}, ${GROUND_Y}) scale(1,-1) rotate(${rot}, 0, ${pose.rootY})`}>
```

Alternate rotation pivot = center of mass for realism; keep pivot *in motion space* (it flips with the group).

## 4.9 Custom moves

Compose from the same grammar: anticipation key (10–15% frames, opposite sign, `in`), action key (1–3f, `snap`), impact hold (2f duplicated), settle (`backOut`), return (`inOut`). If you can write it as {f, pose, e}, you can animate it.

---

# PART 5 — SMOOTHNESS ENGINEERING

## 5.1 Easing selection = spacing selection

| Feel | Ease | Use for |
|---|---|---|
| Robotic / constant scroll | `lin` | Camera pans, looped treadmills |
| Natural default | `inOut` | 80% of keys |
| Arrival / deceleration | `out` | Rises into apex, hand reaching target |
| Departure / acceleration | `in` | Falls, wind-ups entering the snap |
| Violent attack | `snap` (quart-out) | Punch/kick extension, body hits |
| Elastic settle | `backOut` | Return-to-idle after overshoot, follow-through |

**Velocity-continuity rule:** where two segments meet at a key, avoid ending one at high speed while the next starts at zero. Chained `inOut` segments each come to rest at their key — perfect for walk-cycle turning points, wrong for continuous falls (use one long `in` segment instead).

## 5.2 Anticipation & overshoot formulas

- **Anticipation key** at `T − 0.15·T` frames before action of duration T: displacement `= −0.12·D` where D is the action's total displacement, easing `in` (accelerates *out* of the crouch).
- **Overshoot** on arrival: `+0.06 → 0.10·D`, decaying over `0.25·T` via `backOut`.
- **Ballistic y:** apex key timed at `√`-symmetry — time up ≈ time down, easings `out` up / `in` down.

## 5.3 Follow-through implementation

Delay a *child* param's approach by re-keying it 2–4 f later at its previous value, then easing to target. E.g. torso snaps on f9, `head` holds old value until f11 then `backOut` to target by f16 — the head visibly lags and catches up. Mass order of lag: torso (0) < head (+3f) < arms (+2f) < loose props.

## 5.4 Ground contact law

- At any *contact* key, the planted foot's solved y must equal 0 (within 1 unit). Compute backward: given `rootY` and hip angle, solve knee so foot lands exactly — or use IK (§3.7) for those frames.
- While planted, foot (x) must be **constant in world space** until lift. If the stage scrolls at `s` u/f, animate `x` so planted-foot world-x doesn't drift.
- Violating either = foot-skate, the #1 giveaway of amateur animation.

## 5.5 Snappiness dial (the anime trick)

At 60fps, deliberately duplicate key values so extreme poses hold 2 frames ("on twos") while transitions happen in 1–3 frames. Smooth ≠ more interpolation — smooth is *controlled timing*. Eric-animator-style fights are snappy-hold-snap; idle conversations are long `inOut` drifts.

## 5.6 Pre-render checklist

- [ ] All values from `useCurrentFrame()`; `random()` seeded; no `Date.now()`.
- [ ] 60 fps composition; every `interpolate` clamped.
- [ ] Planted feet: y = 0, world-x constant during stance.
- [ ] Stroke width identical in every frame (browser-zoom the preview to check).
- [ ] Every impact has: anticipation before, 2f hold at contact, flash/shake/dust at contact, settle after.
- [ ] Ballistic arcs use out/in easings, not inOut.
- [ ] Silhouette test: fill everything black — action still readable?
- [ ] Character ≥60% of frame height in action shots; consistent screen-direction (hero moves left→right, villain right→left).
- [ ] Scroll speed matches stride (walk 2.8 u/f, run ~8 u/f).
- [ ] SFX lands on the exact contact frame.

---

# PART 6 — FX TOOLKIT (code recipes)

All FX are components driven by local sequence frames; fire them by placing `<Sequence from={IMPACT_FRAME} durationInFrames={…}><FX/></Sequence>`.

## 6.1 Impact flash (1–2 f)

```tsx
const opacity = interpolate(frame, [0, 2], [0.85, 0], {extrapolateRight: 'clamp'});
return <AbsoluteFill style={{backgroundColor: 'white', opacity, zIndex: 9}} />;
```
Variant (impact frames technique): 1 frame of *inverted* colors (black figure on white) — pure style points.

## 6.2 Hit-stop

Not an FX component — a *data* technique: duplicate the contact pose in two consecutive keys (f9 & f11 in the punch). Everything freezes 2 frames; the audience's eye catches up and perceives force.

## 6.3 Camera shake

```tsx
const mag = interpolate(frame, [0, 12], [14, 0], {extrapolateRight: 'clamp'});
const dx = (random(`sx${frame}`) * 2 - 1) * mag;
const dy = (random(`sy${frame}`) * 2 - 1) * mag;
return <AbsoluteFill style={{transform: `translate(${dx}px, ${dy}px)`}}>{children}</AbsoluteFill>;
```

## 6.4 Camera punch (spring zoom)

```tsx
const s = spring({frame, fps, config: {stiffness: 180, damping: 12}});
const scale = 1 + 0.08 * (1 - s); // starts zoomed-in, settles with wobble
<AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '50% 60%'}}>
```

## 6.5 Afterimages (whole-body motion blur)

Inside an action shot, render the rig at sampled past poses:

```tsx
const pNow = samplePose(KEYS, IDLE, frame);
const p3 = samplePose(KEYS, IDLE, Math.max(0, frame - 3));
const p6 = samplePose(KEYS, IDLE, Math.max(0, frame - 6));
// render p6 at opacity .08, p3 at .16, pNow at 1 — same group, sequential siblings
```

## 6.6 Speedlines

```tsx
const lines = Array.from({length: 10}, (_, i) => random(`l${i}`));
{lines.map((r, i) => {
  const y = r * 1080;
  const off = interpolate(frame, [0, 8], [1920 * (0.5 + r), -400], {extrapolateRight: 'clamp'});
  return <line key={i} x1={off} y1={y} x2={off + 180} y2={y} stroke="#000"
               strokeWidth={3} opacity={0.35} />;
})}
```
Radial variant: rotate each line by `i * (360/N)°` around the impact point.

## 6.7 Dust puff (landings, foot plants)

```tsx
{[0, 1, 2, 3].map(i => {
  const a = random(`da${i}`) * Math.PI - Math.PI / 2;          // fan upward
  const f = Math.max(0, frame - i * 2);                         // stagger
  const r = interpolate(f, [0, 14], [3, 20], {extrapolateRight: 'clamp'});
  const o = interpolate(f, [0, 14], [0.5, 0], {extrapolateRight: 'clamp'});
  const d = interpolate(f, [0, 14], [0, 46], {extrapolateRight: 'clamp'});
  return <circle key={i} cx={Math.cos(a) * d} cy={-Math.abs(Math.sin(a)) * d}
                 r={r} fill="#8d8d8d" opacity={o} />;
})}
```

---

# PART 7 — CAMERA & STAGING

- **Layer stack:** `zIndex 0` background parallax → `1` ground line → `2` characters → `3` FX/flashes.
- **Push-in** (tension/dialogue): scale 1→1.08 over 120f, `inOut`.
- **Snap zoom** on impact: combine 6.4.
- **Tracking shot:** keep character fixed at STAGE_X; scroll background at stride-matched speed instead of moving the rig — walk-cycle feet then plant trivially.
- **Whip pan** transition: translateX ±1920 over 6f `snap`, cut at the midpoint frame.
- Screen direction is sacred: establish left/right allegiance per character and never cross the line mid-fight without a cut.

---

# PART 8 — FULL WORKING EXAMPLES

## 8.1 Walking loop component (complete)

```tsx
// WalkCycle.tsx
import React from 'react';
import {useCurrentFrame, AbsoluteFill} from 'remotion';
import {IDLE, StickmanRig, StickPose} from './rig';
import {samplePose, Key, mirror as _unused} from './engine'; // see below

const GROUND_Y = 960, STAGE_X = 660;

const WALK: Key[] = [
  {f: 0,  pose: {rootY: 70.5, torso: 6, rHip: 26, rKnee: 4,  lHip: -22, lKnee: 14, rSh: -22, rEl: 18, lSh: 24, lEl: 14}},
  {f: 6,  pose: {rootY: 69,   torso: 5, rHip: 12, rKnee: 16, lHip: -8,  lKnee: 42, rSh: -12, rEl: 22, lSh: 10, lEl: 20}},
  {f: 12, pose: {rootY: 76,   torso: 7, rHip: -6, rKnee: 8,  lHip: 14,  lKnee: 62, rSh: 10,  rEl: 26, lSh: -8, lEl: 26}},
  {f: 18, pose: {rootY: 74,   torso: 6, rHip: -18,rKnee: 6,  lHip: 26,  lKnee: 18, rSh: 18,  rEl: 18, lSh: -18,lEl: 18}},
];

const mirror = (p: StickPose): StickPose => ({...p,
  lSh: p.rSh, rSh: p.lSh, lEl: p.rEl, rEl: p.lEl,
  lHip: p.rHip, rHip: p.lHip, lKnee: p.rKnee, rKnee: p.lKnee});

export const WalkCycle: React.FC = () => {
  const frame = useCurrentFrame();
  const local = frame % 48;
  const pose = local < 24 ? samplePose(WALK, IDLE, local) : mirror(samplePose(WALK, IDLE, local - 24));
  return (
    <AbsoluteFill style={{backgroundColor: '#f4f4f4'}}>
      <line x1={0} y1={GROUND_Y} x2={1920} y2={GROUND_Y} stroke="#ccc" strokeWidth={4} />
      <g transform={`translate(${STAGE_X}, ${GROUND_Y}) scale(1,-1)`}>
        <StickmanRig pose={pose} />
      </g>
    </AbsoluteFill>
  );
};
```

## 8.2 Fight beat (assembly pattern)

```tsx
// FightScene.tsx skeleton
<AbsoluteFill>
  <Background />                                            {/* zIndex 0 */}
  <Sequence from={0} durationInFrames={60}>
    <StanceIdle who="hero" />                               {/* sizing up */}
  </Sequence>
  <Sequence from={60} durationInFrames={22}>
    <Punch who="hero" />                                    {/* §3.4 JSON data */}
  </Sequence>
  <Sequence from={60 + 9} durationInFrames={18}>            {/* impact lands on punch f9 */}
    <>
      <FlashFrame />                                        {/* 6.1 */}
      <ShakeWrapper><GetHit who="villain" /></ShakeWrapper> {/* 4.7 + 6.3 */}
      <DustAt feet="villain" />
      <Audio src={staticFile('sfx/punch.mp3')} />
    </>
  </Sequence>
  <CameraPunch from={60 + 9} />                             {/* 6.4 wrapper */}
</AbsoluteFill>
```

Pattern to internalize: **impact frame is the synchronization anchor** — flash, hit victim pose, shake, SFX and camera all keyed off `PUNCH_START + 9`.

---

# PART 9 — THE AI GENERATION CONTRACT

## 9.1 The 10-step procedure (follow exactly when asked for an animation)

1. **Parse intent** → move list (from Part 4) + mood (snappy vs floaty → §5.5 dial).
2. **Write the beat sheet** (below) before any code.
3. Choose fps 60 and comp duration = sum of beats + tails.
4. Emit pose keyframes (JSON schema §3.4) — reuse library data, don't reinvent angles.
5. Wire `<Sequence>`s per beat; overlaps of 8–12f for transitions.
6. Mark every impact frame; attach full FX stack (flash + hold + shake + dust + SFX).
7. Add camera moves only after body motion reads correctly.
8. Run checklist §5.6.
9. Render: `npx remotion render <CompId> out/<name>.mp4`.
10. QA: re-read frames at impacts; verify foot contact and stroke width; iterate keys ±20%.

## 9.2 Beat sheet schema (planning artifact)

```json
[
  {"shot": 1, "from": 0,   "dur": 90,  "action": "hero walks in from left", "move": "walk@48f", "camera": "tracking",  "fx": [], "audio": "footsteps loop"},
  {"shot": 2, "from": 82,  "dur": 22,  "action": "hero punches villain",    "move": "punch@22f","camera": "static+punch@+9", "fx": ["flash@+9","shake@+9","dust@+9"], "audio": "whoosh@+3, hit@+9"},
  {"shot": 3, "from": 100, "dur": 18,  "action": "villain reels, falls",    "move": "gethit@18f","camera": "hold", "fx": ["dust@+14"], "audio": "thud@+14"}
]
```

Rules: every `fx`/`audio` offset is relative to its shot's `from`; overlaps between shots default 8f; cut on action (mid-motion frames hide cuts).

## 9.3 Modern AI-assisted pipeline (source guide) → Remotion edition

| Source-guide phase | Generic approach | Remotion approach (deterministic upgrade) |
|---|---|---|
| Scripting & beat sheets | LLM dialogue + timing cues | LLM emits §9.2 beat sheet JSON directly |
| Visual asset generation | Image-model pose extraction (inconsistent!) | LLM emits §3.4 pose JSON — mathematically uniform line weight, zero drift |
| Temporal video synthesis | Video diffusion morph between key poses | `samplePose()` interpolation — exact, reviewable, editable per frame |
| Timeline assembly | CapCut manual sync | Native `<Sequence>` + `<Audio>`, frame-perfect by construction |

Net result: the probabilistic middle steps of the AI pipeline are replaced by deterministic code — the LLM's creativity goes into *poses, timing and staging* (data), while physics of smoothness (interpolation, easing, contacts) is guaranteed by the engine.

---

# PART 10 — COMMON MISTAKES & FIXES

| Symptom | Cause | Fix |
|---|---|---|
| Render flickers / differs between runs | CSS animations, `Math.random()`, `Date.now()` | Frame-driven values only; `random(seed)` |
| Values overshoot past the last keyframe | Missing clamp | `extrapolateRight: 'clamp'` everywhere |
| Feet slide on the ground | rootY/x not matched to stride; planted foot not pinned | §5.4: solve contact, pin world-x, match scroll speed |
| Limbs look rubbery at the ends | Lerping hand/foot coordinates instead of angles | FK angle tracks (arcs come free) |
| Motion feels floaty/robotic | All-linear or all-inOut timing | Match easing table §5.1; add hit-stop holds for snap |
| Line weight wobbles | Scaling groups with transforms | Scale values in solver, or `vector-effect="non-scaling-stroke"` |
| Head/or text upside down | Content placed inside the y-flip group | Render it outside the flipped `<g>` |
| Impacts feel weak | Missing FX layers at contact frame | Flash (1–2f) + 2f pose hold + shake ±14px + punch zoom + SFX on exact frame |
| Strobing on fast swings | >40px/frame travel on a thin limb | 1–2f smear frames or afterimages (§3.6/6.5) |
| Composition jitters in preview | Huge SVG node counts / giant blur filters | Keep rig ≤ ~50 nodes; ghost copies instead of blur filters |
| Cuts feel abrupt | Hard cuts on static frames | Cut on action; 8–12f sequence overlaps |

---

# PART 11 — GLOSSARY

- **Pose / keyframe:** complete-ish body description at a frame; intervening frames are interpolated per-parameter.
- **FK (forward kinematics):** joints computed from cascading angles — swings, gestures.
- **IK (inverse kinematics):** joint angles solved so an extremity hits a target point — planted hands/feet.
- **Hit-stop:** freezing the contact pose 2 frames to amplify impact.
- **Smear:** a 1–2 frame elongated/multiplied drawing replacing a too-fast in-between.
- **Afterimage:** low-opacity past poses trailing the live pose (deterministic motion blur).
- **On twos:** holding each pose 2 frames — the classic 12-drawings-per-second feel (2f @60 here).
- **Spacing:** frame-to-frame distance traveled; its *derivative* is what easing controls.
- **Staging/silhouette:** composing so the pose reads in solid black.
- **Beat sheet:** timed shot list — the single planning artifact every generation starts from.
- **Rig:** the parameterized stickman skeleton (constants + solver + renderer), single source of truth for anatomy.

---

# PART 12 — REFERENCE & VERSION NOTES

- Remotion v4.x docs: remotion.dev — `useCurrentFrame`, `interpolate`, `spring`, `Easing`, `Sequence`, `Audio`, `random`, `getAudioData` (@remotion/media-utils). Single-value `interpolate` ranges supported since v4.0.469.
- Foundations adapted from the attached *Comprehensive Guide to Stickman Animation* (12 Principles subset, Alan Becker methodology, modern AI-assisted pipeline) and expanded into code-level form.
- Everything in this document is deterministic and reproducible: same code + same frame ⇒ same pixel. That property, not any single technique, is what makes Remotion stickman animation *smooth*.
