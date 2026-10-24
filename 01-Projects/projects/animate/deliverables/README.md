# Stickman basketball: finished cuts (SFX + grade)

Two shareable cuts made from the reviewing agent's animations. Both were silent when
they arrived; everything here adds the sound design and the colour grade on top.

| file | length | picture | audio |
|---|---|---|---|
| `stickman-dunk-sfx.mp4` | 5.00 s | 1920x1080, 30 fps, 150 frames, H.264 High, yuv420p | AAC-LC 48 kHz stereo, 192 kbps, -16.8 LUFS, -2.8 dBTP |
| `stickman-layup-sfx.mp4` | 6.00 s | 1920x1080, 30 fps, 180 frames | AAC-LC 48 kHz stereo, 192 kbps, -16.4 LUFS, -2.6 dBTP |
| `audio/dunk-master.wav` | 5.00 s |  | 48 kHz 16-bit stereo master |
| `audio/layup-master.wav` | 6.00 s |  | 48 kHz 16-bit stereo master |

Both are `+faststart`, so they stream/preview instantly in chat and on the web.

## Source

- Zip: `workspace-01a16ceb-b795-7460-a5a0-545ccd85b3e2.zip` (the reviewing agent's return)
- Pictures used as-is: `stickman-dunk/final.mp4` (spec rebuild, with captions) and
  `stickman-layup/final.mp4` (reference-style flat cartoon). No frame was re-rendered,
  no timing was touched: the grade and fades are the only picture changes.
- Audio is built from scratch. Nothing from the source clips was kept (they had no audio track).

## Colour grade

Applied with ffmpeg, then cut to the same length.

- **Dunk** (ink-on-paper): contrast 1.05, saturation 1.08, gamma lift 0.005, a gentle
  master S-curve (`0/0 0.5/0.515 1/1`), unsharp 0.28 on the 5x5 luma so the pen strokes
  read at 1080p, vignette `PI/14` (very light).
  Net effect measured at the slam frame: luma -2.7%, saturation +11%.
- **Layup** (flat cartoon): contrast 1.04, saturation 1.14, gamma lift 0.005, vignette `PI/14`.
  Net effect: luma -5.1%, saturation +9.7%.
- Both: 0.10 s fade in from black, 0.22 s fade out (dunk from 4.78 s, layup from 5.78 s).

A stronger vignette was tested and rejected: ffmpeg's default `PI/5` costs 24 to 28% of
average brightness, which turns the flat art muddy.

## Sound design

Cues are placed from the beats read out of each piece's `index.html`, not by ear-guessing.
One-shots are levelled by peak, beds by RMS, so the slam stays a hit and the ambience stays under it.

### Dunk (indoor gym)

| time | sound |
|---|---|
| 0.00 | gym crowd murmur bed (RMS -38) + room hum |
| 0.20 / 0.60 / 1.00 | dribble contacts (leather + floor thump), panned with the ball |
| 0.10 to 1.47 | 8 court steps |
| 1.40 / 1.42 / 1.47 | takeoff whoosh, gather catch, push-off sneaker squeak |
| 1.48 | flight air bed rising through the windmill |
| 1.58 / 2.44 | windmill whoosh, pre-slam whip |
| 2.795 / 2.80 | rim hit + synthesised rim clank, slam body thump |
| 2.845 / 3.06 / 3.34 | net swish, then two settling rustles |
| 2.86 | crowd ovation swelling out to the end |
| 3.86 | release air |
| 4.175 / 4.45 / 4.725 / 4.97 | ball bouncing away after the net |
| 4.23 / 4.24 / 4.26 | landing thump, scuff, knee squeak |
| 4.45 | soft score bell under "10 / 10" |

### Layup (outdoor park)

| time | sound |
|---|---|
| 0.00 | park ambience (birds) + breeze bed |
| 0.068 / 0.488 / 0.908 / 1.328 | dribble drive contacts |
| 1.775 / 2.298 / 2.798 | loose chase bounces |
| 0.12 to 2.79, 5.13 to 5.98 | court steps on both run cycles |
| 2.86 / 3.14 / 3.16 | gather, plant squeak, scuff |
| 3.44 / 3.48 / 3.98 | leap whoosh, push-off squeak, scoop air |
| 4.31 / 4.32 | landing thump, scuff |
| 4.355 / 4.375 / 4.47 | rim tick, swish, net tail |
| 4.98 / 5.48 / 5.72 / 5.96 | ball falling out of the net and bouncing away |

Synthesised elements (no sample): floor thumps, rim clank, sneaker squeaks, court scuffs,
the score bell, the flight air bed. The gym reverb is a convolution with a synthetic 0.9 s IR
at 11% wet; the park gets 5% at 0.55 s to keep it outdoors.

## Sample sources

Mixkit free sound effects (free licence, no attribution required):
`basketball ball hitting the net`, `basketball ball bouncing`, `catching a basketball ball`,
`basketball ball hard hit`, `air woosh`, `cinematic whoosh fast transition`,
`small crowd ovation`, `crowd at the stadium`, `walking in the forest with birds`.
Everything is mixed, pitched, trimmed and re-levelled.

## Rebuild

The build scripts live in `%LOCALAPPDATA%\Temp\opencode\`:
`build-audio.py` (mix), `master-mux.py` (gain, limit, grade, mux), `verify.py` (stream and
cue checks), `preview-grid.py` (contact sheet). Re-running them reproduces exactly these files.
