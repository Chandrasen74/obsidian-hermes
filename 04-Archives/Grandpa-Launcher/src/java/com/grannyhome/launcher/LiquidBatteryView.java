/*
 * Liquid battery indicator for the Home launcher.
 *
 * Wave mechanism adapted from john990/WaveView (Apache License 2.0),
 * https://github.com/john990/WaveView, (c) 2014 john990.
 * Original: two Canvas sine waves y=A*sin(w*x+phi) with a per-frame phase
 * increment ticker. Adapted here into a single View shaped as a battery
 * tank: liquid fills bottom-up, state colors, percentage label, charge bolt.
 */
package com.grannyhome.launcher;

import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.PathEffect;
import android.view.View;

/**
 * A battery-shaped tank that fills with animated liquid from the bottom.
 * Mechanics (sine wave paths + per-frame offset ticker, now per original
 * 16 ms postDelayed loop) come from john990/WaveView.
 */
public class LiquidBatteryView extends View {

  private static final int LIQ_GOOD = 0xFF57A45B;    // >= 80%
  private static final int LIQ_MID = 0xFFE0A93C;     // 25..79%
  private static final int LIQ_LOW = 0xFFD96C5A;     // < 25%
  private static final int LIQ_CHARGE = 0xFF5FBF93;  // charging mint

  private static final int HOLE = 0xFFF5EEDF;
  private static final int OUTLINE = 0xFF26221D;
  private static final int HALO = 0xFFFBF6EC;

  private static final float WAVE_MULTIPLE = 1.5f;   // wave length = width * m
  private static final float HZ_CALM = 0.09f;        // rad per frame, original NORMAL
  private static final float HZ_SLOSH = 0.14f;       // charging: faster current

  private final Paint holePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint outlinePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint nubPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint frontWave = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint backWave = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint textFill = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint textHalo = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint boltFill = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final Paint boltHalo = new Paint(Paint.ANTI_ALIAS_FLAG);

  private final Path frontPath = new Path();
  private final Path backPath = new Path();
  private final Path clipPath = new Path();

  private int level = -1;
  private boolean charging;
  private float waveHz = HZ_CALM;
  private float waveHeight;
  private float waveLength;
  private float omega;
  private float surfaceY;
  private float clipL, clipR, clipT, clipB;
  private boolean geometryReady;

  /** phase offsets, original Wave fields: above starts 0, blow offset ahead */
  private float aboveOffset = 0f;
  private float blowOffset = 2.1f;

  private final Runnable refresher = new Runnable() {
    @Override
    public void run() {
      long start = android.os.SystemClock.uptimeMillis();
      // original Wave.getWaveOffset: both offsets advance by waveHz per frame
      aboveOffset += waveHz;
      blowOffset += waveHz;
      if (aboveOffset > 2f * (float) Math.PI) {
        aboveOffset -= 2f * (float) Math.PI;
        blowOffset -= 2f * (float) Math.PI;
      }
      computeWaves();
      invalidate();
      long gap = 16 - (android.os.SystemClock.uptimeMillis() - start);
      postDelayed(this, gap < 0 ? 0 : gap);
    }
  };

  public LiquidBatteryView(android.content.Context c) {
    super(c);
    float dens = c.getResources().getDisplayMetrics().density;
    waveHeight = 3.5f * dens;

    holePaint.setColor(HOLE);
    outlinePaint.setStyle(Paint.Style.STROKE);
    outlinePaint.setStrokeWidth(3f * dens);
    outlinePaint.setColor(OUTLINE);
    nubPaint.setColor(OUTLINE);
    frontWave.setStyle(Paint.Style.FILL);
    backWave.setStyle(Paint.Style.FILL);
    frontWave.setColor(LIQ_GOOD);
    backWave.setColor(LIQ_GOOD);

    textFill.setStyle(Paint.Style.FILL);
    textFill.setColor(OUTLINE);
    textFill.setTextAlign(Paint.Align.CENTER);
    textFill.setFakeBoldText(true);
    textHalo.setStyle(Paint.Style.STROKE);
    textHalo.setStrokeJoin(Paint.Join.ROUND);
    textHalo.setStrokeWidth(2.5f * dens);
    textHalo.setColor(HALO);
    textHalo.setTextAlign(Paint.Align.CENTER);
    textHalo.setFakeBoldText(true);
    boltFill.setStyle(Paint.Style.FILL);
    boltFill.setColor(OUTLINE);
    boltHalo.setStyle(Paint.Style.STROKE);
    boltHalo.setStrokeJoin(Paint.Join.ROUND);
    boltHalo.setStrokeWidth(2.5f * dens);
    boltHalo.setColor(HALO);
  }

  /** level 0..100; plugged switches on mint liquid and the charge bolt */
  public void setLevel(int pct, boolean plugged) {
    level = pct > 100 ? 100 : pct;
    charging = plugged;
    int liq = plugged ? LIQ_CHARGE
        : level < 25 ? LIQ_LOW : level < 80 ? LIQ_MID : LIQ_GOOD;
    // original paint pattern: same hue, back wave lighter (alpha instead of the
    // original 30/alpha stacking since this fill must read as solid liquid)
    frontWave.setColor(liq);
    backWave.setColor((liq & 0x00FFFFFF) | 0x8A000000);
    waveHz = plugged ? HZ_SLOSH : HZ_CALM;
    invalidate();
  }

  @Override
  protected void onSizeChanged(int w, int h, int ow, int oh) {
    super.onSizeChanged(w, h, ow, oh);
    if (w <= 0 || h <= 0) {
      geometryReady = false;
      return;
    }
    float dens = getResources().getDisplayMetrics().density;
    float stroke = 3f * dens;
    float nubW = 5f * dens;
    float gap = 2f * dens;

    // battery body (pill) leaves room for the nub on the right
    clipL = stroke / 2f;
    clipT = stroke / 2f;
    clipR = w - nubW - gap - stroke / 2f;
    clipB = h - stroke / 2f;
    float bodyR = (clipB - clipT) / 2f;

    clipPath.reset();
    clipPath.addRoundRect(clipL + stroke / 2f, clipT + stroke / 2f,
        clipR - stroke / 2f, clipB - stroke / 2f,
        bodyR, bodyR, Path.Direction.CCW);

    // original Wave.startWave: omega = 2*PI / (width * multiple)
    waveLength = (clipR - clipL) * WAVE_MULTIPLE;
    omega = 2f * (float) Math.PI / waveLength;
    geometryReady = true;
  }

  private void computeWaves() {
    if (!geometryReady) {
      return;
    }
    float step = Math.max(6f, waveLength / 48f);
    buildWave(backPath, clipL, blowOffset, step);
    buildWave(frontPath, clipL, aboveOffset, step);
  }

  /** liquid region between the sine surface and the tank bottom */
  private void buildWave(Path p, float x0, float phase, float step) {
    p.reset();
    p.moveTo(x0, clipB);
    for (float x = x0; x <= clipR; x += step) {
      p.lineTo(x, surfaceY + waveHeight
          * (float) Math.sin(omega * x + phase));
    }
    p.lineTo(clipR, clipB);
    p.close();
  }

  @Override
  protected void onDraw(Canvas canvas) {
    super.onDraw(canvas);
    if (!geometryReady) {
      return;
    }
    float w = getWidth();
    float h = getHeight();
    float dens = getResources().getDisplayMetrics().density;

    // empty glass interior
    float cx = (clipL + clipR) / 2f;
    float cy = (clipT + clipB) / 2f;
    int shown = level < 0 ? 0 : level;
    surfaceY = clipT + (clipB - clipT) * (1f - shown / 100f);

    canvas.save();
    canvas.clipPath(clipPath);
    canvas.drawRect(clipL, clipT, clipR, clipB, holePaint);
    computeWaves();
    if (level >= 0) {
      canvas.drawPath(backPath, backWave);
      canvas.drawPath(frontPath, frontWave);
    }
    canvas.restore();

    // body outline + nub, drawn unclipped on top
    Path body = new Path();
    body.addRoundRect(clipL, clipT, clipR, clipB,
        (clipB - clipT) / 2f, (clipB - clipT) / 2f, Path.Direction.CCW);
    canvas.drawPath(body, outlinePaint);
    float nubH = h * 0.42f;
    canvas.drawRoundRect(w - 5f * dens, (h - nubH) / 2f, w - 0.5f * dens,
        (h + nubH) / 2f, 2f * dens, 2f * dens, nubPaint);

    // percent label centered in the body, fitted for the widest battery label
    String label = level < 0 ? "--%" : (level + "%");
    float innerH = clipB - clipT;
    float bodyW = clipR - clipL;
    float padW = 6f * dens;
    float maxTs = innerH * 0.46f;
    textFill.setTextSize(1f);
    float widestLabelAtOne = textFill.measureText("100%");
    float lowTs = 0f;
    float highTs = maxTs;
    float boltGap = 6f * dens;
    float minBoltOutlineGap = outlinePaint.getStrokeWidth() / 2f + dens;
    for (int i = 0; i < 24; i++) {
      float candidate = (lowTs + highTs) / 2f;
      float haloStroke = Math.max(2f * dens, candidate * 0.14f);
      float labelW = widestLabelAtOne * candidate;
      float requiredW = labelW + haloStroke;
      boolean fits = requiredW <= bodyW - padW;
      if (charging) {
        float boltW = candidate * 0.70f * 0.62f;
        requiredW += boltW + boltGap;
        float leftClearance = (bodyW - labelW - haloStroke) / 2f
            - boltW - boltGap;
        fits = fits && requiredW <= bodyW - padW
            && leftClearance >= minBoltOutlineGap;
      }
      if (fits) {
        lowTs = candidate;
      } else {
        highTs = candidate;
      }
    }
    float ts = lowTs;
    textFill.setTextSize(ts);
    textHalo.setTextSize(ts);
    textHalo.setStrokeWidth(Math.max(2f * dens, ts * 0.14f));
    boltHalo.setStrokeWidth(Math.max(2f * dens, ts * 0.14f));
    Paint.FontMetrics fm = textFill.getFontMetrics();
    float textY = cy - (fm.ascent + fm.descent) / 2f;
    float textW = textFill.measureText(label);
    canvas.drawText(label, cx, textY, textHalo);
    canvas.drawText(label, cx, textY, textFill);

    if (charging) {
      // small bolt drawn as a path (no font dependency), left of the label
      float kH = textFill.getTextSize() * 0.70f;
      float kW = kH * 0.62f;
      float bx = cx - textW / 2f - kW - boltGap;
      float by = cy - kH / 2f;
      float sx = kW / 0.94f; // polygon spans x 0.10..0.94
      Path bolt = new Path();
      bolt.moveTo(bx + 0.62f * sx, by);
      bolt.lineTo(bx + 0.10f * sx, by + 0.60f * kH);
      bolt.lineTo(bx + 0.44f * sx, by + 0.60f * kH);
      bolt.lineTo(bx + 0.34f * sx, by + kH);
      bolt.lineTo(bx + 0.94f * sx, by + 0.40f * kH);
      bolt.lineTo(bx + 0.58f * sx, by + 0.40f * kH);
      bolt.lineTo(bx + 0.86f * sx, by);
      bolt.close();
      canvas.drawPath(bolt, boltHalo);
      canvas.drawPath(bolt, boltFill);
    }
  }

  // original Wave lifecycle: ticker only runs while attached and visible
  @Override
  protected void onAttachedToWindow() {
    super.onAttachedToWindow();
    startTicker();
  }

  @Override
  protected void onDetachedFromWindow() {
    removeCallbacks(refresher);
    super.onDetachedFromWindow();
  }

  @Override
  protected void onWindowVisibilityChanged(int visibility) {
    super.onWindowVisibilityChanged(visibility);
    if (visibility == VISIBLE) {
      startTicker();
    } else {
      removeCallbacks(refresher);
    }
  }

  private void startTicker() {
    removeCallbacks(refresher);
    postDelayed(refresher, 16);
  }
}
