---
name: README
tags: ["#status/archived", "#type/index", "#domain/device-setup"]
---
# Grandpa Home Launcher — ARCHIVED 2026-10-26

Hand-built Android launcher APK for **grandpa's phone** (built and archived
same day, 2026-10-26, session 16:22-17:54).

> Naming note: owner says it is **for grandpa, not grandma**; the internal
> package name `com.grannyhome.launcher`, app name `Home`, keystore alias
> `granny` and folder drop name were kept as-built (renaming the package or
> key breaks the installed APK's update path: same package + same signature).

## What it is

- Pure-framework Android app: no Gradle, no AndroidX, no Play services.
- Built with `aapt2 + javac + d8 + zipalign + apksigner` via `build.ps1`
  (JDK17 + android-34 SDK from `%LOCALAPPDATA%\Android`).
- Big-text elderly-friendly home screen driven by `assets\config.json`:
  favorites (Phone, Messages, WhatsApp, YouTube, Google Pay, Country Delight)
  + folders (Shopping / Banking / Social / Media / AI / Tools + auto
  catch-all). Weather "skycon" cloud views (sun/snow/rain/fog/thunder),
  a "liquid battery" view, folder activity, app grid.

## Files

- `src\` — AndroidManifest.xml, `java\com\grannyhome\launcher\*.java`
  (13 sources), res\values\strings.xml, assets\config.json (EDITABLE
  favorites/folders; app reads it at runtime)
- `build\` — intermediate build outputs (classes, dex, res.zip, base.apk)
- `dist\Home.apk` + `.idsig` — the signed, installable APK (v1.0, 40 KB)
- `keys\granny.keystore` — signing key, alias `granny`,
  store/key password `grannyhome` (kept on disk + OneDrive, **git-ignored**)
- `build.ps1` — full build pipeline (`-Install` adb-installs,
  `-Install -SetRole` also sets it as default home via `cmd role`)
- `play_install.py` — uiautomator2 Play Store auto-installer for listed
  packages (banking/utility apps on the new phone)

## Stepwise creation timeline (file stamps, 2026-10-26)

| time | step |
|---|---|
| 15:20-16:32 | (sibling project) Phone Cleaner for the Moto G35 built first |
| 16:22 | src skeleton: manifest, strings, config.json, FolderActivity, HomeActivity, LiquidBatteryView |
| 16:25 | first build: `dist\Home.apk` + `keys\granny.keystore` created |
| 16:41-16:45 | LiquidBatteryView polished, FolderActivity updated |
| 17:13-17:16 | weather views added: Cloud family, Sun, Skycon (snow/rain/fog/thunder/cloud) |
| 17:27 | AndroidManifest updated |
| 17:49 | HomeActivity + config.json updated |
| 17:54 | final rebuild: build\ outputs + dist\Home.apk re-signed (current APK) |

## Rebuild / update path

1. Launch in this folder (run `.\build.ps1` from here; paths are relative).
2. Needs `%LOCALAPPDATA%\Android\{jdk17, sdk}` — unchanged machine setup.
3. Same package + same keystore = in-place app updates stay possible.
4. `python play_install.py <pkg>...` and `python pin_apps.py` (the latter in
   [[04-Archives/Phone-Cleaner/README|Phone-Cleaner]]) drive the phone over
   uiautomator2 after `uiautomator2 init` once.

## Phone-side state (live on the Moto G35 after this session, 2026-10-26)

All set over adb during the session; undocumented anywhere else, so listed here:

| setting | value |
|---|---|
| display density | `wm density 440` (was 400; revert: `wm density reset`) |
| font scale | `settings put system font_scale 1.55` (was 1.3) |
| screen timeout | 2 minutes (`screen_off_timeout 120000`) |
| theme | light mode on; Night Light warm tint OFF (`cmd uimode night no`) |
| default home | `com.grannyhome.launcher` holds the HOME role |
| USB debugging | left ON deliberately (future tweaks = one-cable job) |
| favorites config | final = Phone, Messages, WhatsApp, **YouTube** (Truecaller was swapped out to "All other apps" at the user's request; archived `src\assets\config.json` matches the phone) |
| system wallpaper | warm cream-to-sand gradient painted by the launcher (aimed at the Material You shade; also removed stale WeatherWall text from recents) |
| app inventory at handover | ~29-30 legit 3rd-party apps; PNB ONE + iMobile installed from Play; junk/system preloads wiped (see Phone-Cleaner) |

## Pending teardown (missed because the phone was unplugged; do next cable-in)

The session's plan promised these at handover but they never ran (user kept
asking for UI polish, then unplugged). Phone-side, ~30 s over adb:

1. **Play Protect / adb-install verification is still OFF**
   (`package_verifier_enable 0`, `verifier_verify_adb_installs 0`; disabled
   during `uiautomator2 init` because Play Protect blocked the helper APK).
   For an elderly phone this is a real risk; re-enable:
   `settings put global package_verifier_enable 1` +
   `settings put global verifier_verify_adb_installs 1`.
2. **uiautomator2 helper apps still installed** (`com.github.uiautomator`,
   `com.github.uiautomator.test`, its FastInput IME). Remove:
   `pm uninstall --user 0 com.github.uiautomator com.github.uiautomator.test`
   (keep USB debugging itself, which costs nothing and stays off unless asked).

See also: [[04-Archives/Phone-Cleaner/README|Phone-Cleaner]] (same-day
companion tool), [[01-Projects/README|01-Projects]] completed list,
[[01-Projects/OpenCode-Tasks|OpenCode-Tasks]].

---

*Archived: 2026-10-26 | APK v1.0 (versionCode 1) | min-sdk 29 / target 34*
