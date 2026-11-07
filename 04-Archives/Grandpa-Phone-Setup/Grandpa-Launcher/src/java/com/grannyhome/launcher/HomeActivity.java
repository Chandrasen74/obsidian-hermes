package com.grannyhome.launcher;

import android.app.Activity;
import android.app.WallpaperManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
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
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.Handler;
import android.os.Looper;
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
import java.util.function.Consumer;

public class HomeActivity extends Activity {

  static final String EXTRA_FOLDER = "folder";
  static final String EXTRA_PKGS = "pkgs";

  private static final int CREAM = 0xFFFBF6EC;
  private static final int INK = 0xFF26221D;
  private static final int MUTE = 0xFF8A8175;
  private static final int WHITE = 0xFFFFFFFF;
  private static final int TRACK = 0xFFEFE6D8;
  private static final int ORANGE = 0xFFE08A34;
  private static final int REQ_LOC = 101;
  private static final int[] ACCENTS = {
      0xFFE08A34, 0xFF2E9C8B, 0xFF7B5FC0, 0xFF5B9E4A,
      0xFF3E76C2, 0xFFC75B4A, 0xFF9C6B3F
  };
  private static final String[] HIDDEN = {
      "com.grannyhome.launcher",
      "com.github.uiautomator",
      "com.github.uiautomator.test",
      "com.motorola.launcher3",
      "com.android.launcher3",
      "com.ask.browser.ai",
      "com.safeweb.browser",
      "com.filebox.junkclean.filemanager",
      "app.blinkit.onboarding",
      "com.android.vending"
  };

  private PackageManager pm;
  private LiquidBatteryView battery;
  private TextView tempText;
  private TextView airText;
  private FrameLayout skyconBox;
  private int currentWxCode = Integer.MIN_VALUE;
  private boolean weatherBusy;
  private boolean askedLoc;
  private boolean freshLocationPending;
  private int freshLocationRequestId;
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
                new int[] {CREAM, 0xFFFAF0DA, 0xFFF4E5C8},
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
    resolveLocation();
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
  public void onRequestPermissionsResult(int requestCode, String[] permissions,
      int[] grantResults) {
    super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    if (requestCode == REQ_LOC && grantResults != null && grantResults.length > 0
        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
      resolveLocation();
      getSharedPreferences("home", MODE_PRIVATE).edit().putLong("wx_ts", 0L).apply();
      maybeFetchWeather();
    }
  }

  private void resolveLocation() {
    if (checkSelfPermission(android.Manifest.permission.ACCESS_COARSE_LOCATION)
        == PackageManager.PERMISSION_GRANTED) {
      try {
        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        if (lm == null) {
          return;
        }
        String[] providers = {
            LocationManager.NETWORK_PROVIDER,
            LocationManager.PASSIVE_PROVIDER,
            LocationManager.GPS_PROVIDER
        };
        Location fix = null;
        for (String provider : providers) {
          try {
            Location candidate = lm.getLastKnownLocation(provider);
            if (candidate != null) {
              double lat = candidate.getLatitude();
              double lon = candidate.getLongitude();
              if (lat >= -90.0 && lat <= 90.0 && lon >= -180.0 && lon <= 180.0
                  && (lat != 0.0 || lon != 0.0)) {
                fix = candidate;
                break;
              }
            }
          } catch (Throwable ignored) {
          }
        }
        if (fix == null) {
          requestFreshLocation(lm);
          return;
        }
        double lat = fix.getLatitude();
        double lon = fix.getLongitude();
        SharedPreferences sp = getSharedPreferences("home", MODE_PRIVATE);
        boolean hasCached = sp.contains("wx_lat") && sp.contains("wx_lon");
        float cachedLat = sp.getFloat("wx_lat", 28.46f);
        float cachedLon = sp.getFloat("wx_lon", 77.03f);
        double dx = (lon - cachedLon) * 111.0 * Math.cos(Math.toRadians(lat));
        double dy = (lat - cachedLat) * 111.0;
        if (!hasCached || Math.sqrt(dx * dx + dy * dy) > 15.0) {
          sp.edit().putFloat("wx_lat", (float) lat).putFloat("wx_lon", (float) lon)
              .putLong("wx_ts", 0L).apply();
        }
      } catch (Throwable ignored) {
      }
    } else if (!askedLoc) {
      askedLoc = true;
      requestPermissions(
          new String[] {android.Manifest.permission.ACCESS_COARSE_LOCATION}, REQ_LOC);
    }
  }

  private void requestFreshLocation(LocationManager lm) {
    if (freshLocationPending) {
      return;
    }
    freshLocationPending = true;
    new FreshLocationRequest(lm, ++freshLocationRequestId).start();
  }

  private boolean isIndiaPlausibleFix(Location fix) {
    if (fix == null) {
      return false;
    }
    double lat = fix.getLatitude();
    double lon = fix.getLongitude();
    return (lat != 0.0 || lon != 0.0)
        && lat >= 6.0 && lat <= 38.0 && lon >= 68.0 && lon <= 98.0;
  }

  private final class FreshLocationRequest {
    private final LocationManager locationManager;
    private final int requestId;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final LocationListener[] listeners = new LocationListener[2];
    private final CancellationSignal[] cancellations = new CancellationSignal[2];
    private boolean timedOut;
    private boolean gpsStarted;

    private final Runnable fallback = new Runnable() {
      @Override
      public void run() {
        if (!timedOut && !gpsStarted) {
          requestProvider(1);
        }
      }
    };

    private final Runnable timeout = new Runnable() {
      @Override
      public void run() {
        timedOut = true;
        cleanup();
        if (freshLocationRequestId == requestId) {
          freshLocationPending = false;
        }
      }
    };

    FreshLocationRequest(LocationManager lm, int id) {
      locationManager = lm;
      requestId = id;
    }

    void start() {
      handler.postDelayed(timeout, 45000L);
      handler.postDelayed(fallback, 20000L);
      requestProvider(0);
    }

    private void requestProvider(final int attempt) {
      if (attempt == 1) {
        if (gpsStarted || timedOut) {
          return;
        }
        gpsStarted = true;
        handler.removeCallbacks(fallback);
      }
      final String provider = attempt == 0
          ? LocationManager.NETWORK_PROVIDER : LocationManager.GPS_PROVIDER;
      if (Build.VERSION.SDK_INT >= 30) {
        final CancellationSignal cancellation = new CancellationSignal();
        cancellations[attempt] = cancellation;
        try {
          locationManager.getCurrentLocation(provider, cancellation, getMainExecutor(),
              new Consumer<Location>() {
                @Override
                public void accept(Location fix) {
                  onFix(fix, attempt);
                }
              });
        } catch (Throwable ignored) {
          onFix(null, attempt);
        }
      } else {
        final boolean[] responded = {false};
        LocationListener listener = new LocationListener() {
          @Override
          public void onLocationChanged(Location fix) {
            if (responded[0]) {
              return;
            }
            responded[0] = true;
            onFix(fix, attempt);
          }

          @Override
          public void onStatusChanged(String name, int status, Bundle extras) {
            if (status == LocationProvider.OUT_OF_SERVICE && !responded[0]) {
              responded[0] = true;
              onFix(null, attempt);
            }
          }

          @Override
          public void onProviderEnabled(String name) {
          }

          @Override
          public void onProviderDisabled(String name) {
            if (!responded[0]) {
              responded[0] = true;
              onFix(null, attempt);
            }
          }
        };
        listeners[attempt] = listener;
        try {
          locationManager.requestSingleUpdate(provider, listener, Looper.getMainLooper());
        } catch (Throwable ignored) {
          onFix(null, attempt);
        }
      }
    }

    private void onFix(Location fix, int attempt) {
      if (isIndiaPlausibleFix(fix)) {
        cleanup();
        if (freshLocationRequestId == requestId) {
          freshLocationPending = false;
        }
        SharedPreferences sp = getSharedPreferences("home", MODE_PRIVATE);
        sp.edit().putFloat("wx_lat", (float) fix.getLatitude())
            .putFloat("wx_lon", (float) fix.getLongitude())
            .putLong("wx_ts", 0L).apply();
        runOnUiThread(new Runnable() {
          @Override
          public void run() {
            maybeFetchWeather();
          }
        });
      } else if (attempt == 0 && !timedOut && !gpsStarted) {
        requestProvider(1);
      } else if (attempt == 1 && !timedOut) {
        cleanup();
        if (freshLocationRequestId == requestId) {
          freshLocationPending = false;
        }
      }
    }

    private void cleanup() {
      handler.removeCallbacks(fallback);
      handler.removeCallbacks(timeout);
      for (CancellationSignal cancellation : cancellations) {
        if (cancellation != null) {
          try {
            cancellation.cancel();
          } catch (Throwable ignored) {
          }
        }
      }
      for (LocationListener listener : listeners) {
        if (listener != null) {
          try {
            locationManager.removeUpdates(listener);
          } catch (Throwable ignored) {
          }
        }
      }
    }
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
        // Share one cached device fix across both weather indexes.
        SharedPreferences wxPrefs = getSharedPreferences("home", MODE_PRIVATE);
        float lat = wxPrefs.getFloat("wx_lat", 28.46f);
        float lon = wxPrefs.getFloat("wx_lon", 77.03f);
        String location = "?latitude=" + String.valueOf(lat)
            + "&longitude=" + String.valueOf(lon);
        try {
          JSONObject o = fetchUrl("https://api.open-meteo.com/v1/forecast"
              + location
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
              + "/v1/air-quality" + location + "&current=us_aqi");
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
      fitText(tempText, "Weather", 20f, 14f, true);
      tempText.setTextColor(MUTE);
      airText.setVisibility(View.GONE);
      return;
    }
    tempText.setTextColor(INK);
    int code = sp.getInt("wx_code", -1);
    double temp = sp.getFloat("wx_temp", Float.NaN);
    String word = condName(code);
    String weatherLine;
    if (word.length() > 0 && !Double.isNaN(temp)) {
      weatherLine = word + ", " + Math.round(temp) + "C";
    } else if (!Double.isNaN(temp)) {
      weatherLine = Math.round(temp) + "C";
    } else if (word.length() > 0) {
      weatherLine = word;
    } else {
      weatherLine = "Gurugram";
    }
    fitText(tempText, weatherLine, 20f, 14f, true);

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
      airText.setText("AQI " + aqi);
      int bg = aqi <= 50 ? 0xFF4A9B62
          : aqi <= 100 ? 0xFFE3AD36
          : aqi <= 150 ? 0xFFDF762B
          : aqi <= 200 ? 0xFFC94335
          : 0xFF812B2B;
      GradientDrawable g = new GradientDrawable();
      g.setCornerRadius(dp(14));
      g.setColor(bg);
      airText.setBackground(g);
      airText.setTextColor(aqi <= 150 ? INK : WHITE);
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
    LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(0, dp(180), 1f);
    p.setMargins(dp(5), dp(8), dp(5), dp(8));
    return p;
  }

  private LinearLayout statusHalf() {
    LinearLayout half = new LinearLayout(this);
    half.setOrientation(LinearLayout.VERTICAL);
    half.setGravity(Gravity.CENTER);
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(0xFFFFFBF4);
    bg.setCornerRadius(dp(18));
    bg.setStroke(dp(1), 0xFFE8E0D2);
    half.setBackground(bg);
    half.setElevation(dp(2));
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

  private static class FitTextRule {
    String text;
    float maxSp;
    float minSp;
    boolean allowTwoLines;
  }

  private static class TileLayoutMetrics {
    int tileHeightPx;
    int paddingTopPx;
    int paddingBottomPx;
    int iconSizePx;
    int labelGapPx;
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
    root.setPadding(dp(14), statusBarHeightPx() + dp(8), dp(14), dp(22));
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
    dateC.setPadding(0, 0, 0, dp(8));
    root.addView(dateC, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    // Single borderless status strip beneath the clock.
    LinearLayout status = new LinearLayout(this);
    status.setOrientation(LinearLayout.HORIZONTAL);
    status.setGravity(Gravity.CENTER_VERTICAL);
    status.setPadding(dp(4), dp(3), dp(4), dp(9));
    skyconBox = new FrameLayout(this);
    status.addView(skyconBox, new LinearLayout.LayoutParams(dp(44), dp(44)));

    tempText = new TextView(this);
    tempText.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(20));
    tempText.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    tempText.setTextColor(INK);
    tempText.setGravity(Gravity.CENTER_VERTICAL);
    tempText.setIncludeFontPadding(true);
    tempText.setMaxLines(2);
    tempText.setMinHeight(dp(44));
    tempText.setPadding(dp(8), 0, dp(8), 0);
    status.addView(tempText, new LinearLayout.LayoutParams(
        0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

    airText = new TextView(this);
    airText.setTextSize(TypedValue.COMPLEX_UNIT_PX, sp(20));
    airText.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
    airText.setIncludeFontPadding(true);
    airText.setTextColor(INK);
    airText.setGravity(Gravity.CENTER);
    airText.setPadding(dp(8), dp(4), dp(8), dp(4));
    airText.setVisibility(View.GONE);
    status.addView(airText, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    battery = new LiquidBatteryView(this);
    LinearLayout.LayoutParams blp = new LinearLayout.LayoutParams(dp(88), dp(42));
    blp.leftMargin = dp(12);
    status.addView(battery, blp);

    root.addView(status, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

    renderWeather();
    resolveLocation();
    maybeFetchWeather();

    final TileLayoutMetrics tileMetrics = favoriteTileMetrics();
    for (int i = 0; i < favorites.size(); i += 2) {
      LinearLayout row = new LinearLayout(this);
      row.setOrientation(LinearLayout.HORIZONTAL);
      for (int column = 0; column < 2; column++) {
        int favoriteIndex = i + column;
        if (favoriteIndex < favorites.size()) {
          row.addView(tile(favorites.get(favoriteIndex), tileMetrics),
              tileParams(tileMetrics.tileHeightPx));
        } else {
          View spacer = new View(this);
          spacer.setVisibility(View.INVISIBLE);
          row.addView(spacer, tileParams(tileMetrics.tileHeightPx));
        }
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
    g.setCornerRadius(dp(10));
    g.setStroke(dp(1), 0x66FFFFFF);
    return g;
  }

  private GradientDrawable roundTrack() {
    GradientDrawable g = new GradientDrawable();
    g.setColor(TRACK);
    g.setCornerRadius(dp(7));
    return g;
  }

  private LinearLayout.LayoutParams tileParams(int tileHeightPx) {
    // Equal weights split row width after 4dp outer and 8dp inter-tile margins.
    // One shared, metric-derived height keeps every tile in every row balanced.
    LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(0, tileHeightPx, 1f);
    p.setMargins(dp(4), dp(7), dp(4), dp(5));
    return p;
  }

  /** Reserves the actual font-metric height for a wrapped label, including a small safety edge. */
  private int textBlockHeightPx(Typeface typeface, float sizeSp, int lines) {
    Paint measure = new Paint(Paint.ANTI_ALIAS_FLAG);
    measure.setTypeface(typeface);
    measure.setTextSize(sizeSp * getResources().getDisplayMetrics().scaledDensity);
    Paint.FontMetrics fm = measure.getFontMetrics();
    float firstAndLastLine = fm.bottom - fm.top;
    float middleLine = fm.descent - fm.ascent;
    return (int) Math.ceil(firstAndLastLine + Math.max(0, lines - 1) * middleLine)
        + dp(2);
  }

  private TileLayoutMetrics favoriteTileMetrics() {
    TileLayoutMetrics metrics = new TileLayoutMetrics();
    metrics.paddingTopPx = dp(10);
    metrics.paddingBottomPx = dp(10); // >= the required 6dp bottom cushion
    metrics.iconSizePx = dp(60);
    metrics.labelGapPx = dp(6);

    Typeface labelTypeface = Typeface.create("sans-serif", Typeface.BOLD);
    int requiredLabelHeightPx = textBlockHeightPx(labelTypeface, 22f, 2);
    int tileContentHeightPx = metrics.paddingTopPx + metrics.iconSizePx
        + metrics.labelGapPx + requiredLabelHeightPx + metrics.paddingBottomPx;
    metrics.tileHeightPx = Math.max(dp(160), tileContentHeightPx);
    return metrics;
  }

  private android.graphics.drawable.Drawable cardBg() {
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(WHITE);
    bg.setCornerRadius(dp(18));
    bg.setStroke(dp(1), 0xFFE8E0D2);
    // ripple so every tap gives visible feedback
    return new android.graphics.drawable.RippleDrawable(
        android.content.res.ColorStateList.valueOf(0x223F3425), bg, null);
  }

  private View tile(final AppRef ref, TileLayoutMetrics metrics) {
    Typeface labelTypeface = Typeface.create("sans-serif", Typeface.BOLD);

    LinearLayout t = new LinearLayout(this);
    t.setOrientation(LinearLayout.VERTICAL);
    t.setGravity(Gravity.CENTER);
    t.setBackground(cardBg());
    t.setElevation(dp(3));
    t.setPadding(dp(8), metrics.paddingTopPx, dp(8), metrics.paddingBottomPx);

    ImageView iv = new ImageView(this);
    iv.setImageDrawable(iconOf(ref.pkg));
    GradientDrawable thumb = new GradientDrawable();
    thumb.setColor(0xFFFFF8EB);
    thumb.setCornerRadius(dp(17));
    thumb.setStroke(dp(1), 0xFFEFE6D8);
    iv.setBackground(thumb);
    iv.setPadding(dp(5), dp(5), dp(5), dp(5));
    LinearLayout.LayoutParams ilp = new LinearLayout.LayoutParams(
        metrics.iconSizePx, metrics.iconSizePx);
    ilp.gravity = Gravity.CENTER_HORIZONTAL;
    t.addView(iv, ilp);

    TextView lbl = new TextView(this);
    String label = ref.label != null ? ref.label : labelOf(ref.pkg);
    lbl.setTypeface(labelTypeface);
    lbl.setTextColor(INK);
    lbl.setGravity(Gravity.CENTER_HORIZONTAL | Gravity.TOP);
    lbl.setIncludeFontPadding(true);
    lbl.setPadding(0, 0, 0, dp(2));
    lbl.setMaxLines(2);
    LinearLayout.LayoutParams llp = new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    llp.topMargin = metrics.labelGapPx;
    t.addView(lbl, llp);
    fitText(lbl, label, 22f, 16f, true);

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
    r.setElevation(dp(3));
    r.setPadding(dp(12), dp(6), dp(10), dp(6));
    r.setMinimumHeight(dp(88));

    LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    rp.setMargins(0, dp(8), 0, dp(5));

    GradientDrawable dot = new GradientDrawable();
    dot.setCornerRadius(dp(4));
    dot.setColor(accent);
    ImageView dotIv = new ImageView(this);
    dotIv.setImageDrawable(dot);
    LinearLayout.LayoutParams dlp = new LinearLayout.LayoutParams(dp(8), dp(54));
    r.addView(dotIv, dlp);

    LinearLayout mid = new LinearLayout(this);
    mid.setOrientation(LinearLayout.VERTICAL);
    mid.setPadding(dp(9), 0, 0, 0);

    TextView name = new TextView(this);
    Typeface nameTypeface = Typeface.create("sans-serif", Typeface.BOLD);
    name.setTypeface(nameTypeface);
    name.setTextColor(INK);
    name.setIncludeFontPadding(true);
    name.setPadding(0, 0, 0, dp(2));
    name.setMinHeight(textBlockHeightPx(nameTypeface, 20f, 1));
    mid.addView(name, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
    fitText(name, g.name, 20f, 16f, true);

    TextView count = new TextView(this);
    String countLabel = g.apps.size() + (g.apps.size() == 1 ? " app" : " apps");
    Typeface countTypeface = Typeface.create("sans-serif", Typeface.NORMAL);
    count.setTypeface(countTypeface);
    count.setTextColor(MUTE);
    count.setIncludeFontPadding(true);
    count.setPadding(0, 0, 0, dp(2));
    count.setMinHeight(textBlockHeightPx(countTypeface, 18f, 1));
    mid.addView(count, new LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
    fitText(count, countLabel, 18f, 14f, false);

    r.addView(mid, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

    // Peek strip: first four apps inside the folder.
    int peek = Math.min(4, g.apps.size());
    for (int j = 0; j < peek; j++) {
      ImageView iv = new ImageView(this);
      iv.setImageDrawable(iconOf(g.apps.get(j).pkg));
      GradientDrawable preview = new GradientDrawable();
      preview.setColor(0xFFFFF8EB);
      preview.setCornerRadius(dp(8));
      preview.setStroke(dp(1), 0xFFEFE6D8);
      iv.setBackground(preview);
      iv.setPadding(dp(2), dp(2), dp(2), dp(2));
      LinearLayout.LayoutParams ilp = new LinearLayout.LayoutParams(dp(32), dp(32));
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

