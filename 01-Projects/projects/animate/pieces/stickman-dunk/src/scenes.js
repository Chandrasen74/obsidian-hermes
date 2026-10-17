// =====================================================================
//  SCENES — Stick Figure Windmill Slam Dunk (Crosshatch Ink Style)
// =====================================================================

function drawBasketballCourt() {
  // 1. Warm vintage paper background
  paperSheet('court_bg', { fill: '#f5efe0', ruled: false });

  // 2. Hardwood floor from y=760 to H+40
  const floorY = 760;
  woodSurface(-40, floorY, W + 40, H + 40, 'court_wood', {
    fill: '#e7cfb0',
    gw: 1.2,
    gal: 0.35
  });

  // Perspective floor line
  ink([[-40, floorY], [W + 40, floorY]], { w: 3.5, color: '#2c221b', key: 'baseline' });

  // Court markings in sketchy ink
  // Free-throw line at x = 850
  ink([[850, floorY], [850, floorY + 280]], { w: 3.0, color: '#3d3025', key: 'ft_line' });
  
  // Free-throw circle arc
  const ftPts = [];
  for (let a = -Math.PI / 2; a <= Math.PI / 2; a += 0.1) {
    ftPts.push([850 + Math.cos(a) * 160, floorY + 120 + Math.sin(a) * 70]);
  }
  ink(ftPts, { w: 2.5, color: '#4a3b2f', key: 'ft_circle' });

  // Key / Paint area markings
  ink([[850, floorY + 120], [1620, floorY + 120]], { w: 2.2, color: '#4a3b2f', key: 'key_top' });
  ink([[850, floorY + 240], [1620, floorY + 240]], { w: 2.2, color: '#4a3b2f', key: 'key_bot' });

  // 3-Point Arc
  const arcPts = [];
  for (let a = Math.PI * 0.55; a <= Math.PI * 1.15; a += 0.08) {
    arcPts.push([1600 + Math.cos(a) * 920, floorY - 60 + Math.sin(a) * 580]);
  }
  ink(arcPts, { w: 2.2, color: '#4a3b2f', key: 'three_pt_arc' });

  // Background stadium rafters & distant banners in faint crosshatch
  ctx.save();
  ctx.globalAlpha = 0.25;
  for (let i = 0; i < 6; i++) {
    const bx = 160 + i * 280;
    paint(box(bx, 60, 180, 110), {
      fill: '#dfd4be',
      key: 'banner' + i,
      w: 1.5,
      tex: [{ k: 'hatch', a: 0.6, gap: 8, al: 0.25 }]
    });
    ink([[bx + 30, 115], [bx + 150, 115]], { w: 2, color: '#2c221b', key: 'ban_str' + i });
  }
  ctx.restore();
}

function drawHoop(t, rimDeflect) {
  const poleX = 1660;
  const boardX = 1540;
  const boardY = 270;
  const rimX = 1475;
  const rimY = 440 + rimDeflect;
  const rimW = 75;

  // Sturdy Support Pole & Arm
  paint(box(poleX, 220, 32, 540), {
    fill: '#24201d',
    key: 'pole',
    w: 3,
    tex: [{ k: 'cross', c: '#151210', al: 0.4, gap: 4 }]
  });
  // Overhang arm
  ink([[poleX, 320], [boardX + 16, boardY + 110]], { w: 8, color: '#24201d', key: 'pole_arm' });
  ink([[poleX, 400], [boardX + 16, boardY + 140]], { w: 5, color: '#24201d', key: 'pole_arm_sub' });

  // Backboard (Glass with sturdy frame & target box)
  paint(box(boardX, boardY, 16, 210), {
    fill: '#fcf8ef',
    key: 'board_glass',
    w: 3.5,
    tex: [{ k: 'hatch', a: -0.7, gap: 6, al: 0.2, c: '#487294' }]
  });
  // Target square on backboard
  ink([[boardX, boardY + 90], [boardX + 8, boardY + 90]], { w: 4, color: '#c43319', key: 'board_sq1' });
  ink([[boardX, boardY + 140], [boardX + 8, boardY + 140]], { w: 4, color: '#c43319', key: 'board_sq2' });

  // Rim mount
  paint(box(boardX - 10, rimY - 8, 12, 16), { fill: '#b53014', key: 'rim_mount', w: 2 });

  // Rim (Classic Red-Orange with heavy ink contour)
  paint(ellipsePts(rimX + rimW / 2, rimY, rimW / 2, 10, 0, 32), {
    fill: '#e03a1b',
    key: 'rim_fill',
    w: 3.8,
    tex: [{ k: 'pencil', c: '#801a06', al: 0.5, per: 40 }]
  });

  // Net (Animated crosshatch strings with realistic vibration physics)
  const netLen = 70;
  const netWave = Math.sin((t - 3.4) * 22) * Math.exp(-Math.max(0, t - 3.4) * 4) * 18;
  const netFlare = t >= 3.4 && t <= 3.85 ? Math.sin((t - 3.4) / 0.45 * Math.PI) * 22 : 0;
  
  const netCols = 6;
  const topPts = [];
  const botPts = [];
  for (let c = 0; c <= netCols; c++) {
    const nx = rimX + (c / netCols) * rimW;
    const ny = rimY;
    topPts.push([nx, ny]);
    
    // Bottom points taper, swing with impact, and flare outward when ball passes through
    const bx = rimX + 16 + (c / netCols) * (rimW - 32) + netWave * 0.8 + (c > netCols / 2 ? netFlare : -netFlare);
    const by = rimY + netLen + netDeflect(t) * 0.5;
    botPts.push([bx, by]);
  }

  // Draw net diamond lattice
  for (let c = 0; c < netCols; c++) {
    ink([topPts[c], botPts[c + 1]], { w: 1.8, color: '#3a342c', key: 'net_x1_' + c });
    ink([topPts[c + 1], botPts[c]], { w: 1.8, color: '#3a342c', key: 'net_x2_' + c });
    ink([topPts[c], botPts[c]], { w: 1.4, color: '#3a342c', key: 'net_v_' + c });
  }
  // Bottom net rim loop
  ink(botPts, { w: 2.0, color: '#3a342c', key: 'net_bot' });
}

function netDeflect(t) {
  if (t < 3.4) return 0;
  const dt = t - 3.4;
  return Math.sin(dt * 26) * Math.exp(-dt * 5) * 25;
}

function drawBasketball(x, y, r, rot = 0, squash = 1) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.scale(1 / squash, squash);

  // Vibrant, authentic basketball orange with rich crosshatch ink shading
  paint(ellipsePts(0, 0, r, r, 0, 48), {
    fill: '#e86118',
    key: 'bball_body',
    w: 3.5,
    tex: [
      { k: 'pencil', c: '#ffa86b', al: 0.45, a: 0.4, per: 40 },
      { k: 'hatch', c: '#782603', al: 0.4, a: -0.7, gap: 4, dens: (px, py) => clamp((px + py + r * 0.4) / (r * 1.5)) },
      { k: 'cross', c: '#401200', al: 0.35, gap: 5, dens: (px, py) => clamp((px + py - r * 0.1) / (r * 1.2)) }
    ]
  });

  // Authentic curved black basketball seams
  // 1. Horizontal equator
  ink([[-r, 0], [r, 0]], { w: 2.6, color: '#1a110a', key: 'bb_eq' });

  // 2. Vertical meridian
  ink([[0, -r], [0, r]], { w: 2.6, color: '#1a110a', key: 'bb_mer' });

  // 3. Side curve seams (parabolas)
  const arcL = [], arcR = [];
  for (let a = -Math.PI / 2; a <= Math.PI / 2; a += 0.15) {
    arcL.push([-r * 0.45 + Math.cos(a) * (r * 0.45), Math.sin(a) * r * 0.88]);
    arcR.push([ r * 0.45 - Math.cos(a) * (r * 0.45), Math.sin(a) * r * 0.88]);
  }
  ink(arcL, { w: 2.2, color: '#1a110a', key: 'bb_arcL' });
  ink(arcR, { w: 2.2, color: '#1a110a', key: 'bb_arcR' });

  ctx.restore();
}

function drawStickFigure(pose) {
  // Pose object: head [x,y,r], neck [x,y], pelvis [x,y],
  // leftArm [sh, elb, wr], rightArm [sh, elb, wr],
  // leftLeg [hip, kn, ft], rightLeg [hip, kn, ft],
  // lean, headband, expression
  const { head, neck, pelvis, leftArm, rightArm, leftLeg, rightLeg, key = 'stick' } = pose;

  // 1. Shadow on floor
  const floorY = 760;
  const avgFootX = (leftLeg[2][0] + rightLeg[2][0]) / 2;
  const shadowDist = clamp((floorY - Math.min(leftLeg[2][1], rightLeg[2][1])) / 400);
  const shadowAlpha = lerp(0.35, 0.08, shadowDist);
  const shadowScale = lerp(1.0, 0.5, shadowDist);
  paint(ellipsePts(avgFootX, floorY + 15, 65 * shadowScale, 18 * shadowScale, 0, 32), {
    fill: `rgba(40,30,22,${shadowAlpha})`,
    line: false,
    key: key + '_sh',
    tex: [{ k: 'hatch', a: 0.1, gap: 4, al: shadowAlpha * 0.8 }]
  });

  // 2. Back limbs (Left Leg & Left Arm)
  ctx.save();
  ctx.globalAlpha = 0.85;
  ink([pelvis, leftLeg[1], leftLeg[2]], { w: 5.5, color: '#2a221a', key: key + '_lleg' });
  ink([neck, leftArm[1], leftArm[2]], { w: 5.0, color: '#2a221a', key: key + '_larm' });
  ctx.restore();

  // 3. Spine / Torso (Dynamic curved ink stroke)
  ink([neck, [(neck[0] + pelvis[0]) / 2 + (pose.spineArch || 0), (neck[1] + pelvis[1]) / 2], pelvis], {
    w: 7.5,
    color: '#15110d',
    key: key + '_torso'
  });

  // 4. Front limbs (Right Leg & Right Arm)
  ink([pelvis, rightLeg[1], rightLeg[2]], { w: 6.5, color: '#15110d', key: key + '_rleg' });
  ink([neck, rightArm[1], rightArm[2]], { w: 6.0, color: '#15110d', key: key + '_rarm' });

  // 5. Head (Hand-drawn ink circle with crosshatch shading inside)
  paint(ellipsePts(head[0], head[1], head[2], head[2], 0, 36), {
    fill: '#fbf5e6',
    key: key + '_head',
    w: 4.5,
    tex: [
      { k: 'pencil', c: '#dfd2b5', al: 0.5, per: 30 },
      { k: 'hatch', c: '#1f1812', al: 0.25, gap: 4, a: 0.8, dens: (x, y) => clamp((x - head[0] + y - head[1]) / (head[2] * 2)) }
    ]
  });

  // Stylish athletic headband in vibrant red-orange
  const hbY = head[1] - head[2] * 0.2;
  ink([[head[0] - head[2] * 0.95, hbY], [head[0] + head[2] * 0.95, hbY]], {
    w: 5.0,
    color: '#d6381a',
    key: key + '_headband'
  });
  // Headband tails flapping in the wind
  const tailWave = Math.sin(TT * 18) * 8;
  ink([[head[0] - head[2] * 0.9, hbY], [head[0] - head[2] * 1.6, hbY - 4 + tailWave], [head[0] - head[2] * 2.1, hbY + 6 - tailWave]], {
    w: 3.2,
    color: '#d6381a',
    key: key + '_hbtail'
  });

  // Eye / Expression (Focused game-face!)
  ctx.save();
  ctx.fillStyle = '#15110d';
  ctx.beginPath();
  ctx.arc(head[0] + head[2] * 0.45, head[1] - head[2] * 0.05, 3.2, 0, TAU);
  ctx.fill();
  ctx.restore();
}

function drawSpeedLines(origin, angle, count, length, key) {
  for (let i = 0; i < count; i++) {
    const R = RNG('spd', key, i, B);
    const a = angle + R.n(0.18);
    const len = length * R.r(0.6, 1.3);
    const rad = R.r(30, 90);
    const x0 = origin[0] + Math.cos(a) * rad + R.n(15);
    const y0 = origin[1] + Math.sin(a) * rad + R.n(15);
    const x1 = x0 + Math.cos(a) * len;
    const y1 = y0 + Math.sin(a) * len;
    ink([[x0, y0], [x1, y1]], {
      w: R.r(1.5, 3.5),
      color: 'rgba(35,26,18,0.5)',
      key: key + '_line_' + i
    });
  }
}

function drawImpactBurst(cx, cy, radius, key) {
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * TAU;
    const r1 = radius * 0.4;
    const r2 = radius * (0.8 + ((i * 3) % 4) * 0.2);
    ink([
      [cx + Math.cos(a) * r1, cy + Math.sin(a) * r1],
      [cx + Math.cos(a) * r2, cy + Math.sin(a) * r2]
    ], { w: 3.0, color: '#c43319', key: key + '_burst_' + i });
  }
}

// =====================================================================
//  MAIN SCENE ANIMATION LOGIC (5.0 seconds total)
// =====================================================================
function sceneDunk() {
  const t = TT; // Current time in seconds (0.0 to 5.0)
  
  // Calculate rim physics
  let rimDeflect = 0;
  if (t >= 3.4 && t < 4.8) {
    const dt = t - 3.4;
    rimDeflect = Math.sin(dt * 24) * Math.exp(-dt * 4.2) * 28;
  }

  // 1. Draw Court & Environment
  drawBasketballCourt();
  drawHoop(t, rimDeflect);

  // Animation Variables
  let charX = 200;
  let charY = 760;
  let ballX = 240;
  let ballY = 680;
  let ballRot = t * 12;
  let ballSquash = 1.0;
  let pose = null;

  const floorY = 760;

  // -------------------------------------------------------------------
  // ACT 1: DRIBBLE DRIVE ACROSS COURT (0.0s - 1.5s)
  // -------------------------------------------------------------------
  if (t < 1.5) {
    const u = t / 1.5; // 0 to 1
    charX = lerp(180, 850, u);
    
    // Sprint stride oscillation (running cycle)
    const runFreq = 16.0;
    const stride = Math.sin(t * runFreq);
    const strideCos = Math.cos(t * runFreq);
    const bob = Math.abs(stride) * 18;
    
    const hipY = floorY - 170 + bob;
    const neckY = hipY - 140;
    const headY = neckY - 45;
    
    // Forward athletic driving lean
    const headX = charX + 50;
    const neckX = charX + 35;
    const pelvisX = charX;
    
    // Leg IK / Forward running strides
    const rKnee = [pelvisX + stride * 55 + 20, hipY + 80 - Math.max(0, strideCos) * 45];
    const rFoot = [pelvisX + stride * 80 + 30, Math.min(floorY, hipY + 165 - Math.max(0, strideCos) * 55)];

    const lKnee = [pelvisX - stride * 55 + 20, hipY + 80 - Math.max(0, -strideCos) * 45];
    const lFoot = [pelvisX - stride * 80 + 30, Math.min(floorY, hipY + 165 - Math.max(0, -strideCos) * 55)];

    // Left arm pumping for sprint balance
    const lElbow = [neckX - stride * 45 - 20, neckY + 60];
    const lHand = [neckX - stride * 60 - 35, neckY + 40 - strideCos * 30];

    // Right arm dribbling the ball
    const dribblePhase = (t * 2.5) % 1.0;
    const rElbow = [neckX + 45, neckY + 55];
    const rHandY = neckY + 85 + Math.sin(dribblePhase * Math.PI) * 40;
    const rHand = [neckX + 75, rHandY];

    // Basketball bounce physics
    ballX = charX + 85;
    const bounceHeight = 160;
    const bounceSin = Math.sin(dribblePhase * Math.PI);
    ballY = floorY - 28 - (1 - Math.abs(Math.cos(dribblePhase * Math.PI))) * bounceHeight;
    
    if (ballY > floorY - 40) {
      ballSquash = 0.82; // Squash on impact with floor
    }

    pose = {
      head: [headX, headY, 26],
      neck: [neckX, neckY],
      pelvis: [pelvisX, hipY],
      leftArm: [[neckX, neckY], lElbow, lHand],
      rightArm: [[neckX, neckY], rElbow, rHand],
      leftLeg: [[pelvisX, hipY], lKnee, lFoot],
      rightLeg: [[pelvisX, hipY], rKnee, rFoot],
      spineArch: 12
    };

    // Action speed lines behind runner
    drawSpeedLines([charX - 80, hipY], Math.PI, 6, 90, 'run_spd');

    // Comic dribble caption
    if (t > 0.4 && t < 1.1) {
      handText('DRIBBLE DRIVE', 320, 340, 52, '#2c221b', { key: 'drib_txt', weight: 700 });
    }
  }

  // -------------------------------------------------------------------
  // ACT 2: TAKEOFF & FLIGHT / WINDMILL ROTATION (1.5s - 3.4s)
  // -------------------------------------------------------------------
  else if (t < 3.4) {
    const flightU = (t - 1.5) / 1.9; // 0 to 1
    
    // Parabolic trajectory from Free-Throw Line (850, 760) to Dunk Point (1490, 420)
    charX = lerp(850, 1490, flightU);
    const apexHeight = 440;
    const jumpArc = Math.sin(flightU * Math.PI);
    charY = floorY - jumpArc * apexHeight;

    const hipY = charY - 140;
    const neckY = hipY - 130;
    const headY = neckY - 45;

    // Body arch / extension during flight
    const torsoLean = lerp(25, -15, flightU);
    const neckX = charX + torsoLean;
    const headX = neckX + 22;
    const pelvisX = charX - torsoLean * 0.5;

    // Legs scissor / bicycle kick in mid-air
    const legCycle = Math.sin(flightU * Math.PI * 2.5);
    const lKnee = [pelvisX - 40 + legCycle * 35, hipY + 80 + Math.abs(legCycle) * 25];
    const lFoot = [pelvisX - 70 + legCycle * 50, hipY + 160];

    const rKnee = [pelvisX + 20 - legCycle * 35, hipY + 95 - Math.abs(legCycle) * 20];
    const rFoot = [pelvisX + 45 - legCycle * 50, hipY + 175];

    // Left arm extended out for balance / flight silhouette
    const lElbow = [neckX - 70, neckY + 20];
    const lHand = [neckX - 110, neckY - 10];

    // -----------------------------------------------------------------
    // THE WINDMILL 360-DEGREE ROTATION
    // Sweeps down past knees -> back behind spine -> up overhead -> smash down!
    // -----------------------------------------------------------------
    const windmillAngle = lerp(-Math.PI * 0.6, Math.PI * 1.5, EZ.io(flightU));
    const armLen = 95;
    const shoulderX = neckX + 15;
    const shoulderY = neckY + 20;

    const rHandX = shoulderX + Math.cos(windmillAngle) * armLen * 1.3;
    const rHandY = shoulderY + Math.sin(windmillAngle) * armLen * 1.3;
    const rElbowX = shoulderX + Math.cos(windmillAngle - 0.3) * armLen * 0.7;
    const rElbowY = shoulderY + Math.sin(windmillAngle - 0.3) * armLen * 0.7;

    // Basketball firmly in right hand
    ballX = rHandX + Math.cos(windmillAngle) * 22;
    ballY = rHandY + Math.sin(windmillAngle) * 22;
    ballRot = windmillAngle * 1.5;

    pose = {
      head: [headX, headY, 26],
      neck: [neckX, neckY],
      pelvis: [pelvisX, hipY],
      leftArm: [[neckX, neckY], [lElbow[0], lElbow[1]], [lHand[0], lHand[1]]],
      rightArm: [[neckX, neckY], [rElbowX, rElbowY], [rHandX, rHandY]],
      leftLeg: [[pelvisX, hipY], lKnee, lFoot],
      rightLeg: [[pelvisX, hipY], rKnee, rFoot],
      spineArch: -18 * Math.sin(flightU * Math.PI)
    };

    // Windmill circular motion trail lines in ink
    const trailPts = [];
    for (let a = windmillAngle - 1.2; a <= windmillAngle; a += 0.2) {
      trailPts.push([shoulderX + Math.cos(a) * armLen * 1.35, shoulderY + Math.sin(a) * armLen * 1.35]);
    }
    if (trailPts.length >= 2) {
      ink(trailPts, { w: 3.5, color: '#e86118', key: 'windmill_trail' });
    }

    // Speed lines radiating from takeoff point
    if (flightU < 0.4) {
      drawSpeedLines([850, floorY], Math.PI * 0.75, 10, 140, 'takeoff_spd');
    }

    // Dramatic caption badge
    if (t > 2.0 && t < 3.2) {
      handText('WINDMILL!', 1050, 240, 68, '#c43319', { key: 'wm_txt', weight: 800 });
    }
  }

  // -------------------------------------------------------------------
  // ACT 3: THE SLAM DUNK IMPACT & RIM HANG (3.4s - 3.9s)
  // -------------------------------------------------------------------
  else if (t < 3.9) {
    const slamU = (t - 3.4) / 0.5; // 0 to 1
    const rimMountX = 1515;
    const rimMountY = 440 + rimDeflect;

    // Stick figure hanging onto the rim!
    const rHand = [rimMountX, rimMountY + 5];
    const lHand = [rimMountX - 25, rimMountY + 8];

    // Dynamic swing momentum forward
    const swing = Math.sin(slamU * Math.PI * 0.8) * 35;
    
    const neckX = rimMountX - 45 + swing * 0.6;
    const neckY = rimMountY + 110;
    const headX = neckX + 18;
    const headY = neckY - 42;
    const pelvisX = neckX - 35 + swing;
    const pelvisY = neckY + 145;

    // Arms holding rim
    const rElbow = [rimMountX - 10, rimMountY + 55];
    const lElbow = [rimMountX - 35, rimMountY + 60];

    // Tucked / swinging knees
    const rKnee = [pelvisX + 45 + swing * 0.4, pelvisY + 55];
    const rFoot = [pelvisX + 30 + swing * 0.5, pelvisY + 140];

    const lKnee = [pelvisX + 25 + swing * 0.3, pelvisY + 65];
    const lFoot = [pelvisX + 10 + swing * 0.4, pelvisY + 155];

    pose = {
      head: [headX, headY, 26],
      neck: [neckX, neckY],
      pelvis: [pelvisX, pelvisY],
      leftArm: [[neckX, neckY], lElbow, lHand],
      rightArm: [[neckX, neckY], rElbow, rHand],
      leftLeg: [[pelvisX, pelvisY], lKnee, lFoot],
      rightLeg: [[pelvisX, pelvisY], rKnee, rFoot],
      spineArch: 15
    };

    // Basketball shoots down through the net and bounces
    const ballDownU = (t - 3.4) / 0.5;
    if (ballDownU < 0.5) {
      // Passing through net
      ballX = 1515;
      ballY = lerp(440, floorY - 30, ballDownU * 2);
      ballSquash = 1.15;
    } else {
      // Bouncing upward off floor
      const bounceU = (ballDownU - 0.5) * 2;
      ballX = lerp(1515, 1640, bounceU);
      ballY = floorY - 30 - Math.sin(bounceU * Math.PI) * 160;
    }

    // Massive Slam impact burst lines & comic text
    drawImpactBurst(1515, 440, 140, 'slam_impact');
    handText('SLAM!', 1380, 220, 84, '#d6381a', { key: 'slam_txt', weight: 800 });
  }

  // -------------------------------------------------------------------
  // ACT 4: RELEASE, DESCENT & GRACEFUL LANDING (3.9s - 5.0s)
  // -------------------------------------------------------------------
  else {
    const landU = (t - 3.9) / 1.1; // 0 to 1
    charX = lerp(1480, 1420, EZ.o2(landU));

    let charYVal, kneeBend, armSpread, bodyLean;

    if (landU < 0.3) {
      // Dropping from rim to floor
      const dropU = landU / 0.3;
      charYVal = lerp(580, floorY, dropU * dropU);
      kneeBend = 20;
      armSpread = 50;
      bodyLean = 5;
    } else if (landU < 0.65) {
      // Impact compression cushion (deep athletic squat absorption)
      const absorbU = (landU - 0.3) / 0.35;
      const squat = Math.sin(absorbU * Math.PI);
      charYVal = floorY;
      kneeBend = 35 + squat * 45; // Deep knee bend
      armSpread = 80 + squat * 30; // Arms sweeping wide for balance
      bodyLean = 15 + squat * 10;
    } else {
      // Rise into confident, graceful finishing pose
      const standU = (landU - 0.65) / 0.35;
      charYVal = floorY;
      kneeBend = lerp(35, 12, EZ.o3(standU));
      armSpread = lerp(80, 45, EZ.o3(standU));
      bodyLean = lerp(15, 0, EZ.o3(standU));
    }

    const hipY = charYVal - 165 + (kneeBend - 12) * 0.8;
    const neckY = hipY - 135;
    const headY = neckY - 45;

    const neckX = charX - bodyLean;
    const headX = neckX + 15;
    const pelvisX = charX - bodyLean * 0.5;

    // Feet planted firmly on court
    const rFoot = [charX + 45, floorY];
    const lFoot = [charX - 45, floorY];

    const rKnee = [charX + 35 + kneeBend * 0.4, (hipY + floorY) / 2 + kneeBend * 0.3];
    const lKnee = [charX - 35 - kneeBend * 0.4, (hipY + floorY) / 2 + kneeBend * 0.3];

    // Arms graceful balance / celebration pose
    const rElbow = [neckX + armSpread * 0.6, neckY + 40];
    const rHand = [neckX + armSpread, neckY - (landU > 0.6 ? 40 : -30)];

    const lElbow = [neckX - armSpread * 0.6, neckY + 40];
    const lHand = [neckX - armSpread, neckY - (landU > 0.6 ? 40 : -30)];

    pose = {
      head: [headX, headY, 26],
      neck: [neckX, neckY],
      pelvis: [pelvisX, hipY],
      leftArm: [[neckX, neckY], lElbow, lHand],
      rightArm: [[neckX, neckY], rElbow, rHand],
      leftLeg: [[pelvisX, hipY], lKnee, lFoot],
      rightLeg: [[pelvisX, hipY], rKnee, rFoot],
      spineArch: bodyLean * 0.8
    };

    // Basketball continues decaying bounces off to right
    const ballU = (t - 3.9) / 1.1;
    ballX = lerp(1640, 1880, ballU);
    const bPhase = ballU * 4;
    ballY = floorY - 28 - Math.abs(Math.sin(bPhase * Math.PI)) * (100 * Math.exp(-ballU * 2.5));

    // Dust puffs at landing
    if (landU >= 0.28 && landU <= 0.55) {
      for (let i = 0; i < 6; i++) {
        const R = RNG('dust', i);
        paint(ellipsePts(charX + R.n(60), floorY + 5, R.r(12, 28), R.r(6, 14), 0, 16), {
          fill: 'rgba(180,160,130,0.35)',
          line: false,
          key: 'land_dust_' + i
        });
      }
    }

    if (landU > 0.5) {
      handText('10 / 10', 1400, 300, 60, '#2c221b', { key: 'score_txt', weight: 800 });
    }
  }

  // Draw Stick Figure
  if (pose) {
    drawStickFigure(pose);
  }

  // Draw Basketball (Rendered on top for crispness & right color)
  drawBasketball(ballX, ballY, 28, ballRot, ballSquash);
}
