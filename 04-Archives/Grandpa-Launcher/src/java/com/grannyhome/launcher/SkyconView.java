package com.grannyhome.launcher;

/*
 * Vendored from torryharris/Skycons (https://github.com/torryharris/Skycons),
 * public domain, Java port of Dark Sky's Skycons by the Skycons team.
 * Trimmed for this app: the XML AttributeSet constructor and the styleable
 * lookup were removed; views are built programmatically only.
 */
import android.content.Context;
import android.graphics.Color;
import android.view.View;

public class SkyconView extends View {
    protected boolean isStatic = false;
    boolean isAnimated = false;
    int strokeColor = Color.parseColor("#000000");
    int bgColor = Color.parseColor("#ffffff");

    public SkyconView(Context context) {
        super(context);
    }

    public boolean isStatic() {
        return isStatic;
    }

    public void setIsStatic(boolean isStatic) {
        this.isStatic = isStatic;
    }

    public boolean isAnimated() {
        return isAnimated;
    }

    public void setIsAnimated(boolean isAnimated) {
        this.isAnimated = isAnimated;
    }

    public int getStrokeColor() {
        return strokeColor;
    }

    public void setStrokeColor(int strokeColor) {
        this.strokeColor = strokeColor;
    }

    public int getBgColor() {
        return bgColor;
    }

    public void setBgColor(int bgColor) {
        this.bgColor = bgColor;
    }
}
