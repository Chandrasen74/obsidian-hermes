  // SCORE BODY — Stick Figure Windmill Slam Dunk (inside buildScore(); see kit/score-head.js)
  const T = TIMELINE, cu = T.cues;
  
  // MUSIC BUS (to = 'm') — rhythmic hip-hop / funk groove backing track
  to = 'm';
  pad(0.0, 5.1, ['D2', 'A2', 'D3'], 0.04, { type: 'triangle', cut: 800, att: 0.1, rel: 0.3 });
  
  // Energetic bassline
  const bassNotes = [
    [0.0, 'D2'], [0.5, 'D2'], [1.0, 'F2'], [1.5, 'G2'],
    [2.0, 'A2'], [2.5, 'C3'], [3.0, 'D3'],
    [3.4, 'D1'], [3.8, 'D2'], [4.2, 'A2'], [4.6, 'D2']
  ];
  bassNotes.forEach(([t, n]) => {
    bass(t, nz(n), 0.35, 0.08, 0.4);
  });

  // Melodic riff during windmill flight
  [['D4', 1.8], ['F4', 2.1], ['A4', 2.4], ['D5', 2.7], ['E5', 3.0]].forEach(([n, t]) => {
    pluck(t, nz(n), 0.25, 0.05, 0.5, 2800, 0.3);
  });

  // SFX BUS (to = 's') — realistic basketball & dunk Foley
  to = 's';

  // 1. Dribble thuds (mellow bass thump + court tap)
  [0.2, 0.6, 1.0].forEach((t) => {
    noiseHit(t, 0.05, 'lowpass', 200, 2, 0.08, 0);
    sub(t, 75, 0.08, 0.1);
  });

  // 2. Shoe squeaks on hardwood
  [0.4, 0.8, 1.45].forEach((t) => {
    blip(t, 2200, 1600, 0.03, 0.04);
  });

  // 3. Takeoff & Windmill Whoosh Riser
  sweep(1.5, 3.3, 0.02, 160, 2200, 0);
  riser(2.2, 3.35, 0.06, 100, 750);

  // 4. THE SLAM DUNK IMPACT (t = 3.4s) — explosive peak payoff!
  // Metallic Rim Clang
  noiseHit(3.4, 0.45, 'bandpass', 1550, 8, 0.55, 0.1);
  noiseHit(3.4, 0.3, 'bandpass', 2900, 10, 0.4, -0.1);
  // Heavy sub bass impact
  sub(3.4, 50, 0.5, 0.75);
  // Net swish sound (hissing white noise burst)
  noiseHit(3.45, 0.2, 'highpass', 4500, 1.5, 0.3, 0.2);

  // 5. Post-dunk ball bounces
  [3.65, 4.15, 4.55].forEach((t, i) => {
    const vol = 0.12 * Math.pow(0.6, i);
    noiseHit(t, 0.05, 'lowpass', 220, 2, vol, 0.2);
    sub(t, 80, 0.06, vol);
  });

  // 6. Landing shoe stomp
  noiseHit(4.18, 0.08, 'lowpass', 300, 2, 0.1, 0);
