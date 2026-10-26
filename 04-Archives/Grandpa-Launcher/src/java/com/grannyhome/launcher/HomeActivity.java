package com.grannyhome.launcher;

import android.app.Activity;
import android.app.WallpaperManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Shader;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextClock;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class HomeActivity extends Activity {

  static final String EXTRA_FOLDER = "folder";
  static final String EXTRA_PKGS = "pkgs";

  private static final int CREAM = 0xFFFBF6EC;
  private static final int INK = 0xFF26221D;
  private static final int MUTE = 0xFF8A8175;
  private static final int WHITE = 0xFFFFFFFF;
  private static final int TRACK = 0xFFEFE6D8;
  private static final int ORANGE = 0xFFE08A34;
  private static final int[] ACCENTS = {
      0xFFE08A34, 0xFF2E9C8B, 0xFF7B5FC0, 0xFF5B9E4A,
      0xFF3E76C2, 0xFFC75B4A, 0xFF9C6B3F
  };
  private static final String[] HIDDEN = {
      "com.grannyhome.launcher",
      "com.github.uiautomator",
      "com.github.uiautomator.test",
      "com.motorola.launcher3",
      "com.android.launcher3"
  };

  private PackageManager pm;
  private LiquidBatteryView battery;
  private TextView tempText;
  private TextView airText;
  private FrameLayout skyconBox;
  private int currentWxCode = Integer.MIN_VALUE;
  private boolean weatherBusy;
  private final Map<String, Drawable> iconCache = new HashMap<String, Drawable>();
  private final List<AppRef> favorites = new ArrayList<AppRef>();
  private final List<FolderGroup> folders = new ArrayList<FolderGroup>();

  private static class AppRef {
    String pkg;
    String label;
    String special; // "dial" or "sms"
  }

  private static class FolderGroup {
    String name;
    boolean auto;
    final List<AppRef> apps = new ArrayList<AppRef>();
  }

  private final BroadcastReceiver batteryReceiver = new BroadcastReceiver() {
    @Override
    public void onReceive(Context c, Intent in) {
      updateBattery(in);
    }
  };

  @Override
  protected void onCreate(Bundle b) {
    super.onCreate(b);
    pm = getPackageManager();
    creamWindow();
    paintCleanWallpaper();
    paintWarmWallpaper();
    loadConfigAndBuildUi();
  }

  /**
   * One-time fix: the uninstalled WeatherWall companion left its weather
   * wallpaper in the system wallpaper slots; it keeps showing in the recents
   * view. Paint a plain cream wallpaper over both slots once.
   */
  private void paintCleanWallpaper() {
    try {
      SharedPreferences sp = getSharedPreferences("home", MODE_PRIVATE);
      if (sp.getBoolean("wp_fixed", false)) {
        return;
      }
      sp.edit().putBoolean("wp_fixed", true).apply();
      final Context self = this;
      new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            WallpaperManager wm = WallpaperManager.getInstance(self);
            Bitmap bmp = Bitmap.createBitmap(1080, 2400, Bitmap.Config.ARGB_8888);
            bmp.eraseColor(CREAM);
            try {
              wm.setBitmap(bmp, null, true, WallpaperManager.FLAG_SYSTEM);
            } catch (Throwable ignored) {
            }
            try {
              wm.setBitmap(bmp, null, true, WallpaperManager.FLAG_LOCK);
            } catch (Throwable ignored) {
            }
          } catch (Throwable ignored) {
          }
        }
      }, "wallpaper").start();
    } catch (Throwable ignored) {
    }
  }

  /**
   * Second one-time repaint: the plain cream wallpaper is so low-chroma that
   * Material You falls back to its default blue accent in the notification
   * shade. A soft warm gradient seeds warm sand/amber user palettes so the
   * shade and recents match the launcher instead of the factory blue.
   */
  private void paintWarmWallpaper() {
    try {
      SharedPreferences sp = getSharedPreferences("home", MODE_PRIVATE);
      if (sp.getBoolean("wp_warm", false)) {
        return;
      }
      sp.edit().putBoolean("wp_warm", true).apply();
      final Context self = this;
      new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            WallpaperManager wm = WallpaperManager.getInstance(self);
            Bitmap bmp = Bitmap.createBitmap(1080, 2400, Bitmap.Config.ARGB_8888);
            LinearGradient grad = new LinearGradient(0, 0, 0, bmp.getHeight(),
                new int[] {CREAM, 0xFFF9E9C4, 0xFFF0D69E},
                new float[] {0f, 0.55f, 1f}, Shader.TileMode.CLAMP);
            Paint wp = new Paint(Paint.ANTI_ALIAS_FLAG);
            wp.setShader(grad);
            new Canvas(bmp).drawRect(0, 0, bmp.getWidth(), bmp.getHeight(), wp);
            try {
              wm.setBitmap(bmp, null, true, WallpaperManager.FLAG_SYSTEM);
            } catch (Throwable ignored) {
            }
            try {
              wm.setBitmap(bmp, null, true, WallpaperManager.FLAG_LOCK);
            } catch (Throwable ignored) {
            }
          } catch (Throwable ignored) {
          }
        }
      }, "wallpaper").start();
    } catch (Throwable ignored) {
    }
  }

  @Override
  protected void onResume() {
    super.onResume();
    IntentFilter f = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
    Intent sticky;
    if (Build.VERSION.SDK_INT >= 33) {
      sticky = registerReceiver(batteryReceiver, f, Context.RECEIVER_NOT_EXPORTED);
    } else {
      sticky = registerReceiver(batteryReceiver, f);
    }
    if (sticky != null) {
      updateBattery(sticky);
    }
    maybeFetchWeather();
  }

  @Override
  protected void onPause() {
    try {
      unregisterReceiver(batteryReceiver);
    } catch (Throwable ignored) {
    }
    super.onPause();
  }

  @Override
  public void onBackPressed() {
    // no-op: back must never finish the home activity, the system relaunches
    // the home task and that reads as the page "reloading". Folders handle
    // their own back normally.
  }

  private void creamWindow() {
    // content flows under the transparent status bar; nav bar stays opaque cream
    getWindow().setStatusBarColor(Color.TRANSPARENT);
    getWindow().setNavigationBarColor(CREAM);
    getWindow().getDecorView().setSystemUiVisibility(
        View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
            | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
  }

  private int statusBarHeightPx() {
    try {
      int id = getResources().getIdentifier("status_bar_height", "dimen", "android");
      if (id > 0) {
        return getResources().getDimensionPixelSize(id);
      }
    } catch (Throwable ignored) {
    }
    return dp(28);
  }

  private void updateBattery(Intent in) {
    if (battery == null || in == null) {
      return;
    }
    int level = in.getIntExtra("level", -1);
    int scale = in.getIntExtra("scale", 100);
    boolean plugged = in.getIntExtra("plugged", 0) != 0;
    if (level >= 0 && scale > 0) {
      int pct = Math.round(level * 100f / scale);
      battery.setLevel(pct, plugged);
    }
  }

  // ------------------------------------------------------------- weather

  private void maybeFetchWeather() {
    if (weatherBusy) {
      return;
    }
    SharedPreferences sp = getSharedPreferences("home", MODE_PRIVATE);
    long ts = sp.getLong("wx_ts", 0L);
    if (ts > 0 && System.currentTimeMillis() - ts < 45L * 60L * 1000L) {
      return;
    }
    weatherBusy = true;
    new Thread(new Runnable() {
      @Override
      public void run() {
        final double[] temp = {Double.NaN};
        final int[] code = {-1};
        final int[] aqi = {-1};
        try {
          JSONObject o = fetchUrl("https://api.open-meteo.com/v1/forecast"
              + "?latitude=28.46&longitude=77.03"
              + "&current=temperature_2m,weather_code&timezone=Asia%2FKolkata");
          if (o != null) {
            JSONObject cur = o.getJSONObject("current");
            temp[0] = cur.optDouble("temperature_2m", Double.NaN);
            code[0] = cur.optInt("weather_code", -1);
          }
        } catch (Throwable ignored) {
        }
        try {
          JSONObject o = fetchUrl("https://air-quality-api.open-meteo.com"
              + "/v1/air-quality?latitude=28.46&longitude=77.03&current=us_aqi");
          if (o != null) {
            aqi[0] = o.getJSONObject("current").optInt("us_aqi", -1);
          }
        } catch (Throwable ignored) {
        }
        if (!Double.isNaN(temp[0])) {
          getSharedPreferences("home", MODE_PRIVATE).edit()
              .putLong("wx_ts", System.currentTimeMillis())
              .putFloat("wx_temp", (float) temp[0])
              .putInt("wx_code", code[0])
              .putInt("wx_aqi", aqi[0])
              .apply();
        }
        weatherBusy = false;
        runOnUiThread(new Runnable() {
          @Override
          public void run() {
            renderWeather();
          }
        });
      }
    }, "weather").start();
  }

  private static JSONObject fetchUrl(String spec) {
    HttpURLConnection conn = null;
    try {
      conn = (HttpURLConnection) new URL(spec).openConnection();
      conn.setConnectTimeout(12000);
      conn.setReadTimeout(16000);
      InputStream is = conn.getInputStream();
      StringBuilder sb = new StringBuilder();
      byte[] buf = new byte[4096];
      int n;
      while ((n = is.read(buf)) > 0) {
        sb.append(new String(buf, 0, n, "UTF-8"));
      }
      is.close();
      return new JSONObject(sb.toString());
    } catch (Throwable t) {
      return null;
    } finally {
      if (conn != null) {
        conn.disconnect();
      }
    }
  }

  private void renderWeather() {
    if (tempText == null || airText == null || skyconBox == null) {
      return;
    }
    SharedPreferences sp = getSharedPreferences("home", MODE_PRIVATE);
    if (sp.getLong("wx_ts", 0L) == 0L) {
      // never fetched yet: keep the card shape with a muted placeholder
      tempText.setText("Weather");
      tempText.setTextColor(MUTE);
      airText.setVisibility(View.GONE);
      return;
    }
    tempText.setTextColor(INK);
    int code = sp.getInt("wx_code", -1);
    double temp = sp.getFloat("wx_temp", Float.NaN);
    String word = condName(code);
    if (word.length() > 0 && !Double.isNaN(temp)) {
      tempText.setText(word + ", " + Math.round(temp) + "C");
    } else if (!Double.isNaN(temp)) {
      tempText.setText(Math.round(temp) + "C");
    } else if (word.length() > 0) {
      tempText.setText(word);
    } else {
      tempText.setText("Gurugram");
    }

    // weather only changes hourly, so swapping the animated skycon on code
    // change is enough
    if (code != currentWxCode) {
      currentWxCode = code;
      skyconBox.removeAllViews();
      skyconBox.addView(skyconFor(code), new FrameLayout.LayoutParams(
          ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
    }

    int aqi = sp.getInt("wx_aqi", -1);
    if (aqi < 0) {
      airText.setVisibility(View.GONE);
    } else {
      airText.setVisibility(View.VISIBLE);
      airText.setText("Air " + aqi);
      int bg = aqi <= 50 ? 0xFFDDF2E4
          : aqi <= 100 ? 0xFFFBEFD6
          : aqi <= 150 ? 0xFFFBE3DC
          : 0xFFF6D5CE;
      GradientDrawable g = new GradientDrawable();
      g.setCornerRadius(dp(14));
      g.setColor(bg);
      airText.setBackground(g);
      airText.setTextColor(aqi <= 100 ? INK : 0xFF9C3D2E);
    }
  }

  /** WMO weather code -> animated skycon, ink line-work on cream background. */
  private View skyconFor(int code) {
    if (code == 0) {
      return new SunView(this, false, true, INK, CREAM);
    }
    if (code == 1 || code == 2) {
      return new CloudSunView(this, false, true, INK, CREAM);
    }
    if (code == 45 || code == 48) {
      return new CloudFogView(this, false, true, INK, CREAM);
    }
    if (code >= 51 && code <= 57) {
      return new CloudRainView(this, false, true, INK, CREAM);
    }
    if ((code >= 61 && code <= 67) || (code >= 80 && code <= 82)) {
      return new CloudHvRainView(this, false, true, INK, CREAM);
    }
    if ((code >= 71 && code <= 77) || code == 85 || code == 86) {
      return new CloudSnowView(this, false, true, INK, CREAM);
    }
    if (code >= 95) {
      return new CloudThunderView(this, false, true, INK, CREAM);
    }
    return new CloudView(this, false, true, INK, CREAM);
  }

  /** WMO weather code -> short condition word for the text line. */
  private static String condName(int code) {
    if (code < 0) {
      return "";
    }
    if (code == 0) {
      return "Clear";
    }
    if (code <= 3) {
      return "Cloudy";
    }
    if (code == 45 || code == 48) {
      return "Fog";
    }
    if (code <= 57) {
      return "Drizzle";
    }
    if (code <= 67) {
      return "Rain";
    }
    if (code <= 77 || code == 85 || code == 86) {
      return "Snow";
    }
    if (code <= 82) {
      return "Rain";
    }
    if (code >= 95) {
      return "Storm";
    }
    return "";
  }

  private LinearLayout.LayoutParams halfCardParams() {
    // boxless halves: equal fixed height so both contents center on one line
    LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(0, dp(170), 1f);
    p.setMargins(dp(5), dp(10), dp(5), dp(6));
    return p;
  }

  private LinearLayout statusHalf() {
    // boxless half: content floats directly on the cream background
    LinearLayout half = new LinearLayout(this);
    half.setOrientation(LinearLayout.VERTICAL);
    half.setGravity(Gravity.CENTER);
    return half;
  }

  /** fixed-height slot row inside a status half; its content centers itself.
   * hDp arrives already density-scaled as pixels (callers pass dp() results). */
  private FrameLayout slotRow(float hPx, View content, int w, int h) {
    FrameLayout slot = new FrameLayout(this);
    slot.setLayoutParams(new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, Math.round(hPx)));
    if (content != null) {
      slot.addView(content, new FrameLayout.LayoutParams(w, h, Gravity.CENTER));
    }
    return slot;
  }

  private int dp(float v) {
    return Math.round(v * getResources().getDisplayMetrics().density);
  }

  private int sp(float v) {
    return Math.round(v * getResources().getDisplayMetrics().scaledDensity);
  }

  private String labelOf(String pkg) {
    try {
      return String.valueOf(pm.getApplicationLabel(pm.getApplicationInfo(pkg, 0)));
    } catch (Throwable t) {
      return pkg;
    }
  }

  private Drawable iconOf(String pkg) {
    Drawable d = iconCache.get(pkg);
    if (d == null) {
      try {
        d = pm.getApplicationIcon(pkg);
      } catch (Throwable t) {
        d = getResources().getDrawable(android.R.drawable.sym_def_app_icon);
      }
      iconCache.put(pkg, d);
    }
    return d;
  }

  private boolean launchable(String pkg) {
    try {
      return pkg != null && pkg.length() > 0 && pm.getLaunchIntentForPackage(pkg) != null;
    } catch (Throwable t) {
      return false;
    }
  }

  private String resolveDialerPkg() {
    try {
      android.telecom.TelecomManager tm = getSystemService(android.telecom.TelecomManager.class);
      String p = tm != null ? tm.getDefaultDialerPackage() : null;
      if (p != null && launchable(p)) {
        return p;
      }
    } catch (Throwable ignored) {
    }
    try {
      ResolveInfo r = pm.resolveActivity(new Intent(Intent.ACTION_DIAL), 0);
      if (r != null && r.activityInfo != null) {
        return r.activityInfo.packageName;
      }
    } catch (Throwable ignored) {
    }
    return null;
  }

  private String resolveSmsPkg() {
    try {
      String p = android.provider.Telephony.Sms.getDefaultSmsPackage(this);
      if (p != null && launchable(p)) {
        return p;
      }
    } catch (Throwable ignored) {
    }
    try {
      ResolveInfo r = pm.resolveActivity(new Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:")), 0);
      if (r != null && r.activityInfo != null) {
        return r.activityInfo.packageName;
      }
    } catch (Throwable ignored) {
    }
    return null;
  }

  private void loadConfigAndBuildUi() {
    Set<String> used = new HashSet<String>();
    try {
      InputStream is = getAssets().open("config.json");
      StringBuilder sb = new StringBuilder();
      byte[] buf = new byte[4096];
      int n;
      while ((n = is.read(buf)) > 0) {
        sb.append(new String(buf, 0, n, "UTF-8"));
      }
      is.close();
      JSONObject root = new JSONObject(sb.toString());

      JSONArray fa = root.optJSONArray("favorites");
      if (fa != null) {
        for (int i = 0; i < fa.length() && favorites.size() < 6; i++) {
          JSONObject o = fa.optJSONObject(i);
          if (o == null) {
            continue;
          }
          AppRef r = new AppRef();
          String p = o.optString("pkg", "");
          r.label = o.optString("label", null);
          if ("builtin:dialer".equals(p)) {
            r.special = "dial";
            r.pkg = resolveDialerPkg();
            if (r.label == null) {
              r.label = "Phone";
            }
          } else if ("builtin:sms".equals(p)) {
            r.special = "sms";
            r.pkg = resolveSmsPkg();
            if (r.label == null) {
              r.label = "Messages";
            }
          } else {
            r.pkg = p;
          }
          if (r.pkg == null || !launchable(r.pkg)) {
            continue;
          }
          favorites.add(r);
          used.add(r.pkg);
        }
      }

      JSONArray fo = root.optJSONArray("folders");
      if (fo != null) {
        for (int i = 0; i < fo.length(); i++) {
          JSONObject o = fo.optJSONObject(i);
          if (o == null) {
            continue;
          }
          FolderGroup g = new FolderGroup();
          g.name = o.optString("name", "Folder");
          if (o.optBoolean("auto", false)) {
            g.auto = true;
            folders.add(g);
            continue;
          }
          JSONArray apps = o.optJSONArray("apps");
          if (apps != null) {
            for (int j = 0; j < apps.length(); j++) {
              String p = apps.optString(j, "");
              if (p.length() == 0 || used.contains(p) || !launchable(p)) {
                continue;
              }
              AppRef r = new AppRef();
              r.pkg = p;
              g.apps.add(r);
              used.add(p);
            }
          }
          if (g.apps.size() > 0) {
            folders.add(g);
          }
        }
      }
    } catch (Throwable ignored) {
      // no usable config: everything falls through to "All other apps"
    }

    List<AppRef> rest = restOfApps(used);
    FolderGroup auto = null;
    for (FolderGroup g : folders) {
      if (g.auto) {
        auto = g;
        break;
      }
    }
    if (auto == null && rest.size() > 0) {
      auto = new FolderGroup();
      auto.name = "All other apps";
      auto.auto = true;
      folders.add(auto);
    }
    if (auto != null) {
      auto.apps.addAll(rest);
    }

    setContentView(buildRoot());
  }

  private List<AppRef> restOfApps(Set<String> used) {
    List<AppRef> out = new ArrayList<AppRef>();
    Intent main = new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER);
    try {
      List<ResolveInfo> rx = pm.queryIntentActivities(main, 0);
      if (rx != null) {
        for (ResolveInfo r : rx) {
          if (r == null || r.activityInfo == null) {
            continue;
          }
          String p = r.activityInfo.packageName;
          if (p == null || used.contains(p)) {
            continue;
          }
          boolean hidden = false;
          for (String h : HIDDEN) {
            if (h.equals(p)) {
              hidden = true;
              break;
            }
          }
          if (hidden || !launchable(p)) {
            continue;
          }
          AppRef a = new AppRef();
          a.pkg = p;
          out.add(a);
          used.add(p);
        }
      }
    } catch (Throwable ignored) {
    }
    java.util.Collections.sort(out, new java.util.Comparator<AppRef>() {
      @Override
      public int compare(AppRef a, AppRef b) {
        return labelOf(a.pkg).compareToIgnoreCase(labelOf(b.pkg));
      }
    });
    return out;
  }

  private View buildRoot() {
    ScrollView sv = new ScrollView(this);
    sv.setBackgroundColor(CREAM);
    sv.setFillViewport(true);
    sv.setVerticalScrollbarThumbDrawable(roundThumb());
    sv.setVerticalScrollbarTrackDrawable(roundTrack());
    sv.setScrollbarFadingEnabled(true);

    LinearLayout root = new LinearLayout(this);
    root.setOrientation(LinearLayout.VERTICAL);
    root.setPadding(dp(16), statusBarHeightPx() + dp(6), dp(16), dp(30));
    sv.addView(root, new ViewGroup.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    TextClock clock = new TextClock(this);
    clock.setFormat12Hour("h:mm");
    clock.setFormat24Hour("HH:mm");
    clock.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(46));
    clock.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    clock.setTextColor(INK);
    clock.setGravity(Gravity.CENTER);
    root.addView(clock, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    TextClock dateC = new TextClock(this);
    dateC.setFormat12Hour("EEE, dd MMM yyyy");
    dateC.setFormat24Hour("EEE, dd MMM yyyy");
    dateC.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(19));
    dateC.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    dateC.setTextColor(MUTE);
    dateC.setGravity(Gravity.CENTER);
    root.addView(dateC, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    // symmetric status band: two equal halves on a shared row grid
    LinearLayout status = new LinearLayout(this);
    status.setOrientation(LinearLayout.HORIZONTAL);

    // weather half: visual row, text row, chip row
    LinearLayout wxCard = statusHalf();
    skyconBox = new FrameLayout(this);
    wxCard.addView(slotRow(dp(86), skyconBox, dp(78), dp(78)));

    tempText = new TextView(this);
    tempText.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(18));
    tempText.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    tempText.setTextColor(INK);
    tempText.setGravity(Gravity.CENTER);
    tempText.setSingleLine(true);
    wxCard.addView(slotRow(dp(44), tempText,
        ViewGroup.LayoutParams.MATCH_PARENT, dp(40)));

    airText = new TextView(this);
    airText.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(13));
    airText.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    airText.setTextColor(INK);
    airText.setGravity(Gravity.CENTER);
    airText.setPadding(dp(8), dp(3), dp(8), dp(3));
    airText.setVisibility(View.GONE);
    wxCard.addView(slotRow(dp(40), airText,
        ViewGroup.LayoutParams.WRAP_CONTENT,
        ViewGroup.LayoutParams.WRAP_CONTENT));
    status.addView(wxCard, halfCardParams());

    // battery half: same three rows, last one intentionally blank
    LinearLayout btCard = statusHalf();
    battery = new LiquidBatteryView(this);
    btCard.addView(slotRow(dp(86), battery, dp(126), dp(64)));

    TextView cap = new TextView(this);
    cap.setText("Battery");
    cap.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(13));
    cap.setTextColor(MUTE);
    cap.setGravity(Gravity.CENTER);
    btCard.addView(slotRow(dp(44), cap,
        ViewGroup.LayoutParams.MATCH_PARENT, dp(40)));
    btCard.addView(slotRow(dp(40), null, 0, 0));
    status.addView(btCard, halfCardParams());

    root.addView(status, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    renderWeather();
    maybeFetchWeather();

    for (int i = 0; i < favorites.size(); i += 2) {
      LinearLayout row = new LinearLayout(this);
      row.setOrientation(LinearLayout.HORIZONTAL);
      row.addView(tile(favorites.get(i)), tileParams());
      if (i + 1 < favorites.size()) {
        row.addView(tile(favorites.get(i + 1)), tileParams());
      } else {
        View spacer = new View(this);
        spacer.setVisibility(View.INVISIBLE);
        row.addView(spacer, tileParams());
      }
      root.addView(row, new LinearLayout.LayoutParams(
          ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
    }

    int guide = 0;
    for (final FolderGroup g : folders) {
      if (g.apps.size() == 0) {
        continue;
      }
      root.addView(folderRow(g, ACCENTS[guide++ % ACCENTS.length]));
    }
    return sv;
  }

  private GradientDrawable roundThumb() {
    GradientDrawable g = new GradientDrawable();
    g.setColor(ORANGE);
    g.setCornerRadius(dp(7));
    return g;
  }

  private GradientDrawable roundTrack() {
    GradientDrawable g = new GradientDrawable();
    g.setColor(TRACK);
    g.setCornerRadius(dp(7));
    return g;
  }

  private LinearLayout.LayoutParams tileParams() {
    // fixed height for every tile: one-line and two-line labels live in equal boxes
    LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(0, dp(172), 1f);
    p.setMargins(dp(5), dp(10), dp(5), dp(6));
    return p;
  }

  private android.graphics.drawable.Drawable cardBg() {
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(WHITE);
    bg.setCornerRadius(dp(22));
    bg.setStroke(dp(3), 0xFFE8E0D2);
    // ripple so every tap gives visible feedback
    return new android.graphics.drawable.RippleDrawable(
        android.content.res.ColorStateList.valueOf(0x3326221D), bg, null);
  }

  private View tile(final AppRef ref) {
    LinearLayout t = new LinearLayout(this);
    t.setOrientation(LinearLayout.VERTICAL);
    t.setGravity(Gravity.CENTER);
    t.setBackground(cardBg());
    t.setElevation(dp(6));
    t.setPadding(dp(8), dp(14), dp(8), dp(12));

    ImageView iv = new ImageView(this);
    iv.setImageDrawable(iconOf(ref.pkg));
    LinearLayout.LayoutParams ilp = new LinearLayout.LayoutParams(dp(66), dp(66));
    ilp.gravity = Gravity.CENTER_HORIZONTAL;
    t.addView(iv, ilp);

    TextView lbl = new TextView(this);
    lbl.setText(ref.label != null ? ref.label : labelOf(ref.pkg));
    lbl.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(17));
    lbl.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    lbl.setTextColor(INK);
    lbl.setGravity(Gravity.CENTER);
    lbl.setMaxLines(2);
    LinearLayout.LayoutParams llp = new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    llp.topMargin = dp(8);
    t.addView(lbl, llp);

    t.setOnClickListener(new View.OnClickListener() {
      @Override
      public void onClick(View v) {
        openRef(ref);
      }
    });
    return t;
  }

  private void openRef(AppRef ref) {
    try {
      Intent i = null;
      if (ref.special != null) {
        String p = ref.pkg != null ? ref.pkg
            : ("dial".equals(ref.special) ? resolveDialerPkg() : resolveSmsPkg());
        if (p != null) {
          i = pm.getLaunchIntentForPackage(p);
        }
        if (i == null) {
          i = "dial".equals(ref.special)
              ? new Intent(Intent.ACTION_DIAL)
              : new Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:"));
        }
      } else {
        i = pm.getLaunchIntentForPackage(ref.pkg);
      }
      if (i != null) {
        startActivity(i);
      } else {
        Toast.makeText(this, "App not found", Toast.LENGTH_SHORT).show();
      }
    } catch (Throwable t) {
      Toast.makeText(this, "Could not open app", Toast.LENGTH_SHORT).show();
    }
  }

  private View folderRow(final FolderGroup g, int accent) {
    LinearLayout r = new LinearLayout(this);
    r.setOrientation(LinearLayout.HORIZONTAL);
    r.setGravity(Gravity.CENTER_VERTICAL);
    // same card language as the favorite tiles: white, bordered, soft shadow
    r.setBackground(cardBg());
    r.setElevation(dp(6));
    r.setPadding(dp(16), dp(10), dp(14), dp(10));

    LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, dp(120));
    rp.setMargins(0, dp(10), 0, dp(6));

    GradientDrawable dot = new GradientDrawable();
    dot.setShape(GradientDrawable.OVAL);
    dot.setColor(accent);
    ImageView dotIv = new ImageView(this);
    dotIv.setImageDrawable(dot);
    LinearLayout.LayoutParams dlp = new LinearLayout.LayoutParams(dp(16), dp(16));
    r.addView(dotIv, dlp);

    LinearLayout mid = new LinearLayout(this);
    mid.setOrientation(LinearLayout.VERTICAL);
    mid.setPadding(dp(12), 0, 0, 0);

    TextView name = new TextView(this);
    name.setText(g.name);
    name.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(21));
    name.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    name.setTextColor(INK);
    mid.addView(name, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    TextView count = new TextView(this);
    count.setText(g.apps.size() + (g.apps.size() == 1 ? " app" : " apps"));
    count.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(13));
    count.setTextColor(MUTE);
    mid.addView(count, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    r.addView(mid, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

    // peek strip: first three apps inside the folder
    int peek = Math.min(3, g.apps.size());
    for (int j = 0; j < peek; j++) {
      ImageView iv = new ImageView(this);
      iv.setImageDrawable(iconOf(g.apps.get(j).pkg));
      LinearLayout.LayoutParams ilp = new LinearLayout.LayoutParams(dp(36), dp(36));
      if (j > 0) {
        ilp.setMargins(-dp(9), 0, 0, 0);
      }
      r.addView(iv, ilp);
    }

    TextView chev = new TextView(this);
    chev.setText(">");
    chev.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(22));
    chev.setTextColor(MUTE);
    chev.setGravity(Gravity.CENTER);
    chev.setPadding(dp(6), 0, 0, 0);
    r.addView(chev, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    r.setOnClickListener(new View.OnClickListener() {
      @Override
      public void onClick(View v) {
        openFolder(g);
      }
    });
    return r;
  }

  private void openFolder(FolderGroup g) {
    Intent i = new Intent(this, FolderActivity.class);
    i.putExtra(EXTRA_FOLDER, g.name);
    ArrayList<String> arr = new ArrayList<String>();
    for (AppRef r : g.apps) {
      arr.add(r.pkg);
    }
    i.putStringArrayListExtra(EXTRA_PKGS, arr);
    startActivity(i);
  }
}

