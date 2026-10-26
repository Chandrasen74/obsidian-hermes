package com.grannyhome.launcher;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class FolderActivity extends Activity {

  private static final int CREAM = 0xFFFBF6EC;
  private static final int INK = 0xFF26221D;
  private static final int MUTE = 0xFF8A8175;
  private static final int WHITE = 0xFFFFFFFF;

  @Override
  protected void onCreate(Bundle b) {
    super.onCreate(b);
    getWindow().setStatusBarColor(CREAM);
    getWindow().setNavigationBarColor(CREAM);
    getWindow().getDecorView().setSystemUiVisibility(
        android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
            | android.view.View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);

    String folder = getIntent().getStringExtra(HomeActivity.EXTRA_FOLDER);
    ArrayList<String> pkgs = getIntent().getStringArrayListExtra(HomeActivity.EXTRA_PKGS);

    ScrollView sv = new ScrollView(this);
    sv.setBackgroundColor(CREAM);
    sv.setFillViewport(true);

    LinearLayout root = new LinearLayout(this);
    root.setOrientation(LinearLayout.VERTICAL);
    root.setPadding(dp(16), dp(18), dp(16), dp(30));
    sv.addView(root, new ViewGroup.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    TextView title = new TextView(this);
    title.setText(folder == null ? "Folder" : folder);
    title.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(26));
    title.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    title.setTextColor(INK);
    root.addView(title, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
    root.setPadding(dp(16), dp(18), dp(16), dp(30));

    if (pkgs == null || pkgs.size() == 0) {
      TextView empty = new TextView(this);
      empty.setText("No apps here yet");
      empty.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(20));
      empty.setTextColor(MUTE);
      empty.setPadding(0, dp(24), 0, 0);
      root.addView(empty, new LinearLayout.LayoutParams(
          ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
    } else {
      for (final String p : pkgs) {
        if (!launchable(p)) {
          continue;
        }
        root.addView(appRow(p, titleSafeLabel(p)), rowParams());
      }
    }

    setContentView(sv);
  }

  private String titleSafeLabel(String pkg) {
    try {
      android.content.pm.PackageManager pm = getPackageManager();
      return String.valueOf(pm.getApplicationLabel(pm.getApplicationInfo(pkg, 0)));
    } catch (Throwable t) {
      return pkg;
    }
  }

  private LinearLayout.LayoutParams rowParams() {
    LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    p.setMargins(0, dp(6), 0, dp(6));
    return p;
  }

  private View appRow(final String pkg, String label) {
    LinearLayout r = new LinearLayout(this);
    r.setOrientation(LinearLayout.HORIZONTAL);
    r.setGravity(Gravity.CENTER_VERTICAL);
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(WHITE);
    bg.setCornerRadius(dp(22));
    bg.setStroke(dp(3), 0xFFE8E0D2);
    r.setBackground(new android.graphics.drawable.RippleDrawable(
        android.content.res.ColorStateList.valueOf(0x3326221D), bg, null));
    r.setElevation(dp(5));
    r.setMinimumHeight(dp(88));
    r.setPadding(dp(12), dp(8), dp(12), dp(8));

    ImageView iv = new ImageView(this);
    iv.setImageDrawable(icon(pkg));
    r.addView(iv, new LinearLayout.LayoutParams(dp(52), dp(52)));

    TextView tv = new TextView(this);
    tv.setText(label);
    tv.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(20));
    tv.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    tv.setTextColor(INK);
    tv.setPadding(dp(14), 0, 0, 0);
    r.addView(tv, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

    TextView chev = new TextView(this);
    chev.setText(">");
    chev.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(22));
    chev.setTextColor(MUTE);
    r.addView(chev, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    r.setOnClickListener(new android.view.View.OnClickListener() {
      @Override
      public void onClick(android.view.View v) {
        try {
          Intent i = getPackageManager().getLaunchIntentForPackage(pkg);
          if (i != null) {
            startActivity(i);
            finish();
          } else {
            Toast.makeText(FolderActivity.this, "App not found", Toast.LENGTH_SHORT).show();
          }
        } catch (Throwable t) {
          Toast.makeText(FolderActivity.this, "Could not open app", Toast.LENGTH_SHORT).show();
        }
      }
    });
    return r;
  }

  private Drawable icon(String pkg) {
    try {
      android.content.pm.PackageManager pm = getPackageManager();
      return pm.getApplicationIcon(pkg);
    } catch (Throwable t) {
      return getResources().getDrawable(android.R.drawable.sym_def_app_icon);
    }
  }

  private boolean launchable(String pkg) {
    try {
      return pkg != null && getPackageManager().getLaunchIntentForPackage(pkg) != null;
    } catch (Throwable t) {
      return false;
    }
  }

  private int sp(float v) {
    return Math.round(v * getResources().getDisplayMetrics().scaledDensity);
  }

  private int dp(float v) {
    return Math.round(v * getResources().getDisplayMetrics().density);
  }
}

