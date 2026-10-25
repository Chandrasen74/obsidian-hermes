  // SCORE BODY — Stick Figure Windmill Slam Dunk (inside buildScore(); see kit/score-head.js)
  const T = TIMELINE, cu = T.cues;
  
  // MUSIC BUS (to = 'm') — rhythmic hip-hop / funk groove backing track
  // The pad drops out 2.6-2.95: a pocket of near-silence before the payoff clang lands in air.
  to = 'm';
  pad(0.0, 2.6, ['D2', 'A2', 'D3'], 0.04, { type: 'triangle', cut: 800, att: 0.1, rel: 0.3 });
  pad(2.95, 5.1, ['D2', 'A2', 'D3'], 0.04, { type: 'triangle', cut: 800, att: 0.01, rel: 0.3 });
  
  // Energetic bassline (flight act thinned pre-slam; nothing busy lands right after the 2.8 hit)
  const bassNotes = [
    [0.0, 'D2', 0.35], [0.5, 'D2', 0.35], [1.0, 'F2', 0.35], [1.5, 'G2', 0.22],
    [2.0, 'A2', 0.22], [2.5, 'C3', 0.22],
    [2.8, 'D1', 0.45], [3.3, 'D2', 0.35], [3.8, 'A2', 0.35], [4.4, 'D2', 0.35]
  ];
  bassNotes.forEach(([t, n, v]) => {
    bass(t, nz(n), v);
  });

  // Melodic riff during windmill flight
  // Melodic riff during windmill flight (thinned: the slam must out-score this act)
  [['D4', 1.7], ['F4', 1.95], ['A4', 2.2], ['D5', 2.45], ['E5', 2.6]].forEach(([n, t]) => {
    pluck(t, nz(n), 0.11, 0.05, 0.5, 2800, 0.3);
  });

  // SFX BUS (to = 's') — realistic basketball & dunk Foley
  to = 's';

  // 1. Dribble thuds (mellow bass thump + court tap)
  [0.2, 0.6, 1.0].forEach((t) => {
    noiseHit(t, 0.05, 'lowpass', 200, 2, 0.08, 0);
    sub(t, 0.08);
  });

  // 2. Shoe squeaks on hardwood
  [0.4, 0.8, 1.45].forEach((t) => {
    blip(t, 2200, 1600, 0.03, 0.04);
  });

  // 3. Takeoff & Windmill Whoosh Riser (sweep tops out at the 2.8 slam)
  sweep(1.5, 2.68, 0.008, 160, 2200, 0);
  riser(2.1, 2.68, 0.02, 100, 750);

  // 4. THE SLAM DUNK IMPACT (t = 2.8s) — explosive peak payoff!
  // Metallic Rim Clang
  noiseHit(2.8, 0.45, 'bandpass', 1550, 8, 0.62, 0.1);
  noiseHit(2.8, 0.3, 'bandpass', 2900, 10, 0.45, -0.1);
  // Heavy sub bass impact
  sub(2.8, 0.85);
  // Net swish sound (hissing white noise burst)
  noiseHit(2.85, 0.2, 'highpass', 4500, 1.5, 0.3, 0.2);

  // 5. Post-dunk ball bounces
  [3.35, 4.05, 4.5].forEach((t, i) => {
    const vol = 0.12 * Math.pow(0.6, i);
    noiseHit(t, 0.05, 'lowpass', 220, 2, vol, 0.2);
    sub(t, vol);
  });

  // 6. Landing shoe stomp
  noiseHit(4.18, 0.08, 'lowpass', 300, 2, 0.1, 0);
