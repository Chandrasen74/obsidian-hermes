# Brief: stickman-dunk

**Title:** Stick Figure Windmill Slam Dunk

## Spec

- 5.0s @ 30fps, 1920x1080 (16:9), 150 frames, 120 BPM cut grid.
- Style: crosshatch ink (`styles/crosshatch`). Safe margins: 120px on all sides (`piece.json review.safe`).
- storyFormat: action-scene (single continuous shot, hard-cut-free; acts inside one era, no morph bridges: `BRIDGES = []`).
- Everything drawn in code from kit primitives (`ink`, `paint` with hatch/cross/pencil textures, `handText`), deterministic (`RNG` seeds + boil `B`; no `Math.random`).

## Story beats (post-repair timeline)

| t0-t1 | act | beat | sound's role |
|---|---|---|---|
| 0.0-1.5 | Drive & Gather (build) | sprint down the court with dribble bounces; from 1.2s crouch and gather the ball at the line | dribble thuds + shoe squeaks; riser starts ~1.2s |
| 1.5-2.8 | Flight & Windmill (peak) | takeoff from the line, capped asymmetric arc, 378-degree windmill sweep finishing hand-on-rim | whoosh sweep + riser peak |
| 2.8-3.9 | Slam & Landing (gift) | contact slam at 2.8s: rim clang, ball through the net, glide into a rim hang (body 60px left of the net), release at 3.9s | the single loudest moment (metallic clang + sub) lands on 2.8s, nothing busier after |
| 3.9-5.0 | Descent & finish | deep squat absorb, rise into the finish pose, ball bays to the right and clamps inside the safe margin | landing stomp + decaying bounces, score caption beats |

## Captions

- `DRIBBLE DRIVE` (0.4-1.1s) at (320,340) top-left court, 52px.
- `WINDMILL!` (1.75-2.75s) at (230,655) clear left hardwood zone, 64px. Moved from (1050,240) which sat under the figure's arm/head.
- `SLAM!` (2.8-3.9s) at (1280,250) left of the backboard, 84px. Nudged from (1380,220) to clear the pole corner.
- `10 / 10` (from 4.4s) at (1180,300), 60px. Moved from (1400,300) which sat on the backboard.

All caption anchors are left/baseline (`handText` contract); overlap/crop must pass `tools/textcheck.mjs` and `review.mjs` TEXT.

## Sound plan (src/score.js)

- Music bus: D-minor funk pad + bassline, riff plucks compressed into the 1.7-2.7s flight window.
- Payoff: metallic rim clang (1550/2900 Hz bandpass) + 50 Hz sub + net swish at 2.80-2.85s, the piece's loudest moment; post-slam bass and bounces decay.
- Foley anchors: dribbles 0.2/0.6/1.0, squeaks 0.4/0.8/1.45, takeoff sweep 1.5-2.75, bounces 3.35/4.05/4.5, landing stomp 4.18.
- No silence-before-payoff act is built yet (candidate improvement, LOG.md).

## Claims & sources

None: fictional action piece, no factual claims on screen.

## Known deviations from the original draft (all deliberate, per plan.md 2026-10-17 review)

1. 3-pt arc flattened onto the floor plane (was sweeping through the runner).
2. Flight tightened 1.9s -> 1.3s (act slam boundary moved 3.4 -> 2.8); apex capped so head/ball clear the rafter banner row (y 60-170).
3. Rim-hang figure glides ~60px left on contact so only hands touch the rim.
4. t=0 speed lines gated past 0.15s and pushed inboard; final ball x clamped to 1780 (<= W-140).
5. Ball gather added at 1.2-1.5s and a 0.1s rip-in at takeoff to remove the takeoff teleport.
6. Motion runs every frame (`STYLE.ones = true` in bridges.js; harness default is a 2s pose clock). Ink boil unchanged (still ticks on the 2s clock).
7. Court markings redesigned as a registered side-view half-court (paint slab under the hoop, far/near lane edges, baseline pin, FT line + top-of-key bulge, flattened 3-pt arc).
8. `ballRot` continuous across all acts (no spin flips at cuts); dribble is an asymmetric push-bounce-catch cycle synced to the Foley thuds; ball speed cues = ghost echo rings + launch/net streaks + doubled windmill trail.
