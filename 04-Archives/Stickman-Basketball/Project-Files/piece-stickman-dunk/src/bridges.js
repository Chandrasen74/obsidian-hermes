// =====================================================================
//  ERAS, CAMERAS, BRIDGES — Stick Figure Dunk
// =====================================================================
// Smoothness fix (owner: "choppy and not smooth at all"): run this piece's
// motion on every frame (30 Hz) instead of the harness's 2s pose clock.
// kit/morph.js reads STYLE.ones each renderFrame (TT = F/FPS); the ink boil
// still ticks on B = floor(F/2), so the hand-drawn boil look is unchanged.
STYLE.ones = true;

const ERA_BG = ['#f5efe0'];

function pieceCam(era, t) {
  // Cinematic camera tracking: follow motion, zoom slightly during flight, punch on slam!
  let cx = 960, cy = 540, zoom = 1.0;
  
  if (t < 1.5) {
    // Follow the dribble drive across court
    const u = t / 1.5;
    cx = lerp(600, 960, EZ.o2(u));
    cy = 540;
    zoom = 1.0;
  } else if (t < 2.8) {
    // Flight & windmill: rise with jump (flight tightened to 1.3s)
    const u = (t - 1.5) / 1.3;
    cx = lerp(960, 1300, EZ.io(u));
    cy = lerp(540, 480, Math.sin(u * Math.PI));
    zoom = lerp(1.0, 1.08, Math.sin(u * Math.PI));
  } else if (t < 3.9) {
    // Slam dunk impact: screen shake & hold (slam now at 2.8)
    const st = t - 2.8;
    const shake = Math.sin(st * 45) * Math.exp(-st * 12) * 16;
    cx = 1350 + shake;
    cy = 490 + shake * 0.7;
    zoom = 1.06;
  } else {
    // Settle to final wide composition for graceful landing
    const u = (t - 3.9) / 1.1;
    cx = lerp(1350, 1100, EZ.o3(u));
    cy = lerp(490, 540, EZ.o2(u));
    zoom = lerp(1.06, 1.0, EZ.o2(u));
  }
  
  return { p: [cx, cy], z: zoom };
}

const BRIDGES = [];
