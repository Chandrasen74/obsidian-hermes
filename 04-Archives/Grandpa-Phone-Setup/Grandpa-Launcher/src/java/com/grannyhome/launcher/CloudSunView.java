package com.grannyhome.launcher;

/*
 * Vendored from torryharris/Skycons (public domain). Only the programmatic
 * 4-argument constructor is kept and the paint field is no longer static.
 */
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.PointF;
import android.view.MotionEvent;

public class CloudSunView extends SkyconView {

    private Paint paint;
    private int screenW, screenH;
    private float X, Y, XSun, YSun;
    private Path path, path1;
    private double count;
    Cloud cloud;

    public CloudSunView(Context context, boolean isStatic, boolean isAnimated,
                        int strokeColor, int backgroundColor) {
        super(context);

        this.isStatic = isStatic;
        this.isAnimated = isAnimated;
        this.strokeColor = strokeColor;
        this.bgColor = backgroundColor;

        init();
    }

    private void init() {

        // initialize default values
        count = 0;
        isAnimated = true;
        paint = new Paint();

        paint.setColor(strokeColor);
        paint.setStrokeWidth(10);
        paint.setAntiAlias(true);
        paint.setStrokeCap(Paint.Cap.ROUND);
        paint.setStrokeJoin(Paint.Join.ROUND);
        paint.setStyle(Paint.Style.STROKE);
        paint.setShadowLayer(0, 0, 0, Color.BLACK);

        cloud = new Cloud();
    }

    @Override
    public void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);

        screenW = w; //getting Screen Width
        screenH = h;// getting Screen Height

        // center point of Screen
        X = screenW / 2;
        Y = (screenH / 2);
    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        // set canvas background color
        canvas.drawColor(bgColor);
        // set stroke width
        paint.setStrokeWidth((float) (0.065 * screenW));

        // positioning Sun with respect to cloud
        PointF P5c1 = cloud.getP5c1(X, Y, screenW, count);
        if (XSun == 0) {
            // center point for Sun
            XSun = P5c1.x;
            YSun = P5c1.y + (int) (0.042 * screenW);
        }

        //incrementing counter for rotation
        count = count + 0.5;

        //comparison to check 360 degrees rotation
        int retval = Double.compare(count, 360.00);

        if (retval == 0) {
            //resetting counter on completion of a rotation
            count = 0;
        }

        // drawing sun core and rays above the cloud
        path = new Path();
        path1 = new Path();

        // drawing center circle
        path.addCircle(XSun, YSun, (int) (0.083 * screenW), Path.Direction.CW);

        // drawing arms of sun
        for (int i = 0; i < 360; i += 45) {
            path1.moveTo(XSun, YSun);
            float x1 = (float) ((int) (0.1146 * screenW) * Math.cos(Math.toRadians(i + count / 4)) + XSun);
            float y1 = (float) ((int) (0.1146 * screenW) * Math.sin(Math.toRadians(i + count / 4)) + YSun);
            float X2 = (float) ((int) (0.1563 * screenW) * Math.cos(Math.toRadians(i + count / 4)) + XSun);
            float Y2 = (float) ((int) (0.1563 * screenW) * Math.sin(Math.toRadians(i + count / 4)) + YSun);
            path1.moveTo(x1, y1);
            path1.lineTo(X2, Y2);
        }

        // drawing sun
        canvas.drawPath(path, paint);
        canvas.drawPath(path1, paint);

        // drawing cloud with fill
        paint.setColor(bgColor);
        paint.setStyle(Paint.Style.FILL);
        canvas.drawPath(cloud.getCloud(X, Y, screenW, count), paint);

        // drawing cloud with stroke
        paint.setColor(strokeColor);
        paint.setStyle(Paint.Style.STROKE);
        canvas.drawPath(cloud.getCloud(X, Y, screenW, count), paint);

        if (!isStatic || !isAnimated) {
            // invalidate if not static or not animating
            invalidate();
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                // nothing to do
                return true;
            case MotionEvent.ACTION_MOVE:
                // nothing to do
                break;
            case MotionEvent.ACTION_UP:
                // start animation if it is not animating
                if (isStatic && isAnimated) {
                    isAnimated = false;
                }
                break;
            default:
                return false;
        }

        // Schedules a repaint.
        if (!isAnimated) {
            invalidate();
        }
        return true;
    }
}
