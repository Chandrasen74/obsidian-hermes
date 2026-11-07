package com.grannyhome.launcher;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Paint;
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
    String folderLabel = folder == null ? "Folder" : folder;

    ScrollView sv = new ScrollView(this);
    sv.setBackgroundColor(CREAM);
    sv.setFillViewport(true);

    LinearLayout root = new LinearLayout(this);
    root.setOrientation(LinearLayout.VERTICAL);
    int statusInset = 0;
    int insetId = getResources().getIdentifier("status_bar_height", "dimen", "android");
    if (insetId > 0) {
      statusInset = getResources().getDimensionPixelSize(insetId);
    }
    root.setPadding(dp(16), dp(14) + statusInset, dp(16), dp(22));
    sv.addView(root, new ViewGroup.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    TextView title = new TextView(this);
    title.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    title.setTextColor(INK);
    title.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(26));
    root.addView(title, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
    fitText(title, folderLabel, 26f, 18f, true);

    if (pkgs == null || pkgs.size() == 0) {
      TextView empty = new TextView(this);
      empty.setText("No apps here yet");
      empty.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(20));
      empty.setTextColor(MUTE);
      empty.setPadding(0, dp(24), 0, 0);
      empty.setMinHeight(textBlockHeightPx(
          Typeface.create("sans-serif", Typeface.NORMAL), 20f, 1));
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
    p.setMargins(0, dp(5), 0, dp(5));
    return p;
  }

  private View appRow(final String pkg, String label) {
    LinearLayout r = new LinearLayout(this);
    r.setOrientation(LinearLayout.HORIZONTAL);
    r.setGravity(Gravity.CENTER_VERTICAL);
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(WHITE);
    bg.setCornerRadius(dp(18));
    bg.setStroke(dp(1), 0xFFE8E0D2);
    r.setBackground(new android.graphics.drawable.RippleDrawable(
        android.content.res.ColorStateList.valueOf(0x223F3425), bg, null));
    r.setElevation(dp(3));
    Typeface nameTypeface = Typeface.create("sans-serif", Typeface.BOLD);
    int labelReserve = textBlockHeightPx(nameTypeface, 20f, 2);
    int rowMin = Math.max(dp(96), dp(10) + Math.max(dp(56), labelReserve) + dp(10));
    r.setMinimumHeight(rowMin);
    r.setPadding(dp(14), dp(10), dp(14), dp(10));

    ImageView iv = new ImageView(this);
    iv.setImageDrawable(icon(pkg));
    GradientDrawable thumb = new GradientDrawable();
    thumb.setColor(0xFFFFF8EB);
    thumb.setCornerRadius(dp(14));
    thumb.setStroke(dp(1), 0xFFEFE6D8);
    iv.setBackground(thumb);
    iv.setPadding(dp(4), dp(4), dp(4), dp(4));
    r.addView(iv, new LinearLayout.LayoutParams(dp(56), dp(56)));

    TextView tv = new TextView(this);
    tv.setText(label);
    tv.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(20));
    tv.setTypeface(nameTypeface);
    tv.setTextColor(INK);
    tv.setPadding(dp(14), 0, 0, 0);
    r.addView(tv, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
    fitText(tv, label, 20f, 16f, true);

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

  /** Fits text after layout using its real content width, preserving whole words. */
  private void fitText(final TextView tv, String text, float maxSp, float minSp,
      boolean allowTwoLines) {
    FitTextRule rule = tv.getTag() instanceof FitTextRule
        ? (FitTextRule) tv.getTag() : null;
    if (rule == null) {
      rule = new FitTextRule();
      tv.setTag(rule);
      final FitTextRule attachedRule = rule;
      tv.addOnLayoutChangeListener(new View.OnLayoutChangeListener() {
        @Override
        public void onLayoutChange(View view, int left, int top, int right, int bottom,
            int oldLeft, int oldTop, int oldRight, int oldBottom) {
          applyFitText(tv, attachedRule);
        }
      });
    }
    rule.text = text != null ? text : "";
    rule.maxSp = maxSp;
    rule.minSp = minSp;
    rule.allowTwoLines = allowTwoLines;
    tv.setSingleLine(false);
    tv.setMaxLines(allowTwoLines ? 2 : 1);
    tv.setEllipsize(null);
    if (!rule.text.equals(tv.getText().toString())) {
      tv.setText(rule.text);
    }
    final FitTextRule pendingRule = rule;
    tv.post(new Runnable() {
      @Override
      public void run() {
        applyFitText(tv, pendingRule);
      }
    });
  }

  private void applyFitText(TextView tv, FitTextRule rule) {
    if (tv.getWidth() <= 0) {
      return;
    }
    float width = tv.getWidth() - tv.getCompoundPaddingLeft() - tv.getCompoundPaddingRight();
    if (width <= 0f) {
      return;
    }

    Paint measure = new Paint(tv.getPaint());
    String text = rule.text;
    float size = largestSingleLineSize(measure, text, width, rule.maxSp, rule.minSp);
    if (size > 0f) {
      setFitText(tv, text, size, 1);
      return;
    }

    if (rule.allowTwoLines) {
      float wrapSize = rule.minSp;
      String wrapped = wrapAtBestWordBoundary(measure, text, width, wrapSize);
      while (wrapped == null && wrapSize > 8f) {
        wrapSize = Math.max(8f, wrapSize - 0.25f);
        wrapped = wrapAtBestWordBoundary(measure, text, width, wrapSize);
      }
      if (wrapped != null) {
        setFitText(tv, wrapped, wrapSize, wrapped.indexOf('\n') >= 0 ? 2 : 1);
        return;
      }
    }

    // A single long token has no legal word boundary; keep it whole and reduce only as needed.
    float fallbackSize = largestSingleLineSize(measure, text, width, rule.minSp, 8f);
    if (fallbackSize <= 0f) {
      float px = Math.max(1f, measure.measureText(text));
      fallbackSize = Math.max(1f, (rule.minSp * width / px) * 0.98f);
    }
    setFitText(tv, text, fallbackSize, 1);
  }

  private float largestSingleLineSize(Paint paint, String text, float width,
      float maxSp, float minSp) {
    for (float size = maxSp; size >= minSp - 0.001f; size -= 0.25f) {
      paint.setTextSize(size * getResources().getDisplayMetrics().scaledDensity);
      if (paint.measureText(text) <= width) {
        return size;
      }
    }
    return -1f;
  }

  private String wrapAtBestWordBoundary(Paint paint, String text, float width, float sizeSp) {
    String trimmed = text != null ? text.trim() : "";
    String[] words = trimmed.split("\\s+");
    if (words.length < 2) {
      return null;
    }
    paint.setTextSize(sizeSp * getResources().getDisplayMetrics().scaledDensity);
    String best = null;
    float bestLongest = Float.MAX_VALUE;
    float bestDifference = Float.MAX_VALUE;
    for (int split = 1; split < words.length; split++) {
      StringBuilder first = new StringBuilder();
      StringBuilder second = new StringBuilder();
      for (int i = 0; i < words.length; i++) {
        StringBuilder line = i < split ? first : second;
        if (line.length() > 0) {
          line.append(' ');
        }
        line.append(words[i]);
      }
      float firstWidth = paint.measureText(first.toString());
      float secondWidth = paint.measureText(second.toString());
      if (firstWidth <= width && secondWidth <= width) {
        float longest = Math.max(firstWidth, secondWidth);
        float difference = Math.abs(firstWidth - secondWidth);
        if (longest < bestLongest || (longest == bestLongest && difference < bestDifference)) {
          best = first.toString() + "\n" + second.toString();
          bestLongest = longest;
          bestDifference = difference;
        }
      }
    }
    return best;
  }

  private void setFitText(TextView tv, String text, float sizeSp, int maxLines) {
    float px = sizeSp * getResources().getDisplayMetrics().scaledDensity;
    if (Math.abs(tv.getTextSize() - px) > 0.5f) {
      tv.setTextSize(TypedValue.COMPLEX_UNIT_PX, px);
    }
    if (tv.getMaxLines() != maxLines) {
      tv.setMaxLines(maxLines);
    }
    if (!text.equals(tv.getText().toString())) {
      tv.setText(text);
    }
  }

  /** Metric-derived height of `lines` text lines at `sizeSp`, plus a 2dp bottom cushion. */
  private int textBlockHeightPx(Typeface typeface, float sizeSp, int lines) {
    Paint measure = new Paint(Paint.ANTI_ALIAS_FLAG);
    measure.setTypeface(typeface);
    measure.setTextSize(sizeSp * getResources().getDisplayMetrics().scaledDensity);
    Paint.FontMetrics fm = measure.getFontMetrics();
    float firstAndLastLine = fm.bottom - fm.top;
    float middleLine = fm.descent - fm.ascent;
    return (int) Math.ceil(firstAndLastLine + Math.max(0, lines - 1) * middleLine) + dp(2);
  }

  private static class FitTextRule {
    String text;
    float maxSp;
    float minSp;
    boolean allowTwoLines;
  }

  private int sp(float v) {
    return Math.round(v * getResources().getDisplayMetrics().scaledDensity);
  }

  private int dp(float v) {
    return Math.round(v * getResources().getDisplayMetrics().density);
  }
}

