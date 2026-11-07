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

## 2026-10-28 UI refresh v2 + emulator verification (in progress)

Codex CLI visual polish session (Commit pending):

- Restyled `HomeActivity.java` (63 lines) + `FolderActivity.java` (26 lines):
  softer wallpaper gradient, weather/battery cards, bigger tiles and folder
  cards, all text >= 17sp. Behavior zones verified untouched via git diff
  (HIDDEN, extras, openRef/openFolder, config parsing, weather/battery).
- Rebuilt: `dist\Home.apk` 41,428 bytes, signed 22:01:25 (v3 verified).
- Emulator end-to-end test rig installed: emulator 37.2.12 +
  `system-images;android-34;google_apis;x86_64` under `%LOCALAPPDATA%\Android\Sdk`,
  platform-tools now also inside Sdk root, AVD `granny` (Pixel 5 profile).
  Accel: WHPX usable. NOTE: relaunch needs `ANDROID_SDK_ROOT` = the Sdk root,
  else "Cannot find AVD system path" fatal.
- Verified in emulator (`emulator -avd granny -gpu swiftshader_indirect`):
  APK installs, HomeActivity renders correctly: live weather card (Cloudy
  22C + Air 182 pill), liquid battery 100%, big favorite tiles (emulator
  only shows locally installed apps), accent-dot folder cards.
  Screenshots: `test-shots\emu_home.png` (+ bottom crop for tap mapping).
- Remaining next session: tap Media card (coords from the bottom crop),
  screenshot FolderActivity, then real device install
  (`powershell -ExecutionPolicy Bypass -File .\build.ps1 -Install`), then
  commit everything incl. Phone Cleaner UI change in the same vault repo.

## 2026-10-29 restyle rounds 2 + 3 (Codex CLI, commit pending)

Two more Codex rounds (`gpt-6-luna`; round 2 at effort `low`, round 3 at
`xhigh`, sandbox `danger-full-access`), building on the 2026-10-28 v2 look:

- Round 2: replaced the weather + battery cards with ONE borderless status
  strip under the clock (skycon ~44dp, temp, severity-tinted Air pill keeping
  the raw AQI number, slim liquid battery); favorites now 3-per-row (two
  balanced rows); denser folder cards (left accent strip, up to 4 preview
  icons, all text >= 17sp); bolder cloud/sun strokes. Verified async weather
  renders a few seconds after launch (earlier "Weather" blank shot was just
  fetch latency).
- Round 3 (audit + polish, 137k tokens): high-contrast AQI text on every tint,
  one-line status strip layout, balanced 3-column rows, tighter folder cards,
  writing hygiene (removed a duplicate `Intent` import, normalized line
  endings); wallpapers verified unchanged by checksum.
- Guard: full diff vs pre-round snapshot showed ZERO behavior-zone line
  changes (HIDDEN list, extras, openRef/openFolder, resolveDialerPkg/
  resolveSmsPkg, maybeFetchWeather/updateBattery, config parsing all intact).
- Build: `dist\Home.apk` freshly rebuilt + signed 2026-10-29 16:37:58
  (41,428 bytes); verified live in the emulator.
- AVD `granny` recreated in true Moto G35 proportions: pixel_6 profile with
  `hw.lcd.density=392` (1080x2400, 20:9). Same google_apis image.
- Emulator shows ALL 6 favorites: Phone, Messages, Radio, YouTube, Google
  Pay, Country Delight. Three stand-in stub APKs (correct package IDs +
  labels, lettered-circle placeholder icons: G/R/C) were built with the
  aapt2 pipeline and installed; replace with real APKs pulled off the Moto
  G35 at next cable-in (`pm path` + pull, ~49 packages listed in
  `%TEMP%\opencode\stage_pkglist.txt`). Launcher code untouched by staging.
  Screenshots: `test-shots\emu_home_r3.png`, `emu_folder_r3.png`,
  `emu_home6_stubs.png`, plus earlier `emu_home.png` baseline.
- Battery pill text fit (requested 2026-10-29): the "100%" label no longer
  collides with the outline. `LiquidBatteryView` now auto-fits the worst-case
  label (binary-search font shrink until "100%" + halo fits the tank interior
  minus 6dp padding, cap 46% of interior height); when charging, the bolt
  shares the fit. Pill widened 64dp -> 88dp wide (the only HomeActivity
  change). Wave/charging animation, colors, and the setLevel percentage
  pipeline untouched. Clips: `test-shots\battery_wave_before.mp4`,
  `test-shots\battery_wave_after.mp4`, stills in `emu_home_r4_battery.png`.
- Weather now follows the DEVICE location (requested 2026-10-29; was
  hardcoded 28.46/77.03): manifest gained exactly one line
  (`ACCESS_COARSE_LOCATION`); one-time runtime prompt at first launch;
  last-known fix chain Network/Passive/GPS -> cached `wx_lat`/`wx_lon`;
  a fix moved >15 km clears the 45-min `wx_ts` gate and refetches; when no
  permission or no fix exists the old fallback coordinates stay (no blank
  strip). Follow-up round added an ACTIVE fresh-fix path for devices with
  empty provider history: `getCurrentLocation` (API 30+) then
  `requestSingleUpdate` (API 29), GPS fallback, 45s timeout cleanup,
  India-bounds validation (rejects 0,0 / out-of-range). APK 45,526 bytes,
  17:02:24. Verified both directions on the emulator: Mumbai pin -> live
  31.0C clear / AQI 214 (dark-red zone), Gurugram pin -> 25.0C drizzle /
  AQI 179. Grandpa's phone UX: one location prompt on first launch (or
  pre-grant via adb during cable-in), then silent refetches when he moves.
  NOTE (test rig only): the emulator console `geo fix` applies once per
  cold boot on this AVD build; irrelevant on real phones.
  Stills: `test-shots\emu_weather_mumbai.png`, `emu_weather_home.png`.
- Real phone deployment + round 6 text fit (2026-10-29 evening): the Moto
  G35 was running the OLD 2026-10-27 build (41,428 B); installed the new
  builds directly (`adb -s ZD222R9BND install -r`, the phone's own runtime
  granted location on-screen once). Phone reality check: Moto G35 display
  override = 440dpi at font_scale 1.55, so labels the 392dpi emulator
  showed fine overflowed live: tile labels wrapped mid-word and clipped
  ("Messa ges"), temp truncated "Drizzl...". Round 6 (Codex xhigh) =
  universal fitter: largest 1-line size in 0.25sp steps (18sp target,
  14sp/12sp floors), word-boundary 2-line fallback, tiles 144->160dp,
  folder cards grow-able, weather wraps safely. Zero behavior-zone deltas
  (diff-scanned), only HomeActivity.java touched. Verified on the real
  phone after push: all labels fit, "Country Delight" splits cleanly,
  weather shows "Drizzle, 21C" wrapped, Air 179 red, live battery 78%.
  Stills: `test-shots\phone_before_textfix.png`,
  `phone_after_textfix.png`. Emulator path retired: future verification
  = direct on the phone. NOTE: `build.ps1 -Install` fails with two adb
  devices attached (bare `adb install`); push with an explicit
  `adb -s <serial> install -r`, and re-run
  `pm grant com.grannyhome.launcher android.permission.ACCESS_COARSE_LOCATION`
  after updates when the phone re-prompts with the dialog.
- Round 7 larger text (requested 2026-10-29 evening, "can u make the text
  larger? or is this the max?"): one readability bump later (Codex xhigh).
  Favorite labels 18/14 -> 22/16sp target/floor; weather 18/12 -> 20/14sp
  (initial size 20sp); Air pill 17 -> 20sp (vertical padding 3 -> 4dp);
  folder names 18/14 -> 20/16sp; counts 17/12 -> 18/14sp. Zero behavior-zone
  deltas, only HomeActivity.java touched. Built (45,526 B, 18:16:08) and
  pushed to the Moto. VERDICT: REVERTED the same evening on the user's
  look at the live screen (many things get cut off: at 440dpi/1.55 the
  3-up tiles only leave ~110dp of width, so 22sp text rides the card
  edges). Sources restored from the pre-round-7 snapshot, confirmed
  identical to round 6, rebuilt (45,526 B, 18:21:33), re-pushed, phone
  re-verified back at the round-6 look. Stills: `test-shots\phone_before_bigtext.png`
  = round 6 look, `phone_after_bigtext.png` = the reverted round 7 probe.
- Round 8 descender fix (2026-10-29 night): user-reported from the live
  phone: "GPay" y cut off; folder count "pp" in "4 apps"/"3 apps" cut off.
  Codex xhigh root cause: the code set includeFontPadding(false) with tight
  line boxes, leaving no room below the font descent once font_scale 1.55
  grows glyphs. Fix: includeFontPadding(true) + 2dp bottom safety cushions
  on tile labels, folder names, and counts; new textBlockHeightPx() helper
  reserves the REAL FontMetrics height for wrapped labels (2dp edge; the
  160dp tile flexes paddings and only then icon size if a much larger
  scale ever needs it, tiles stay equal-height). NO size changes (GPay
  kept its shared size; the shrink-down allowance went unused), zero
  behavior-zone deltas, only HomeActivity.java. Built (45,526 B,
  18:26:48), pushed, verified on the Moto: y and pp descenders render
  fully, everything else identical to the approved round-6 look. Stills:
  `test-shots\phone_after_descenderfix.png` (home top),
  `phone_descenders_folders_scroll.png` (folder counts down-page).
- Pending: user sign-off -> single commit of Launcher (rounds 2-8) + build
  outputs + test shots + Phone-Cleaner UI restyle. (The teardown list is
  done: Play Protect re-enabled, uiautomator2 helpers confirmed absent,
  2026-10-29. The phone-to-emulator real-app staging was abandoned with the
  emulator per the real-phone-only decision.)

## 2026-10-30/31: phone hijack rescue + rounds 9-11 + font restore + folder fit (commit pending)

- **Rounds 9-11 (2026-10-29 evening, Codex xhigh, pushed + verified):**
  - r9: favorites switched to 2-up tiles (479px cards, ~12dp row gap) with
    labels 22sp target / 16sp floor, honoring the "larger text" request the
    right way (width per glyph instead of a bigger global scale).
  - r10: Air pill renamed "AQI 179" style (20sp) after the owner reported
    grandpa reading "Air" as the weather.
  - r11: label-reservation math made metric-derived: `tileParams()` was
    stuck allocating the old fixed 160dp row, so 22sp 2-line labels clipped
    ("every text gets cut out"). Tiles now grow from the live 22sp
    FontMetrics (+ 2dp cushion, 6dp bottom edge) instead; folder cards and
    the status strip audited in the same pass. Verified on the Moto
    (440dpi / 1.55): all 6 labels full, "Country Delight" both lines,
    counts, weather ok. Stills in `test-shots\`.
- **2026-10-31 morning hijack rescue (grandpa's phone, serial ZD222R9BND):**
  our launcher had been UNINSTALLED and the default-home claim stolen by
  `com.fastsavemax.xnxviddownloader.vidnexsaver.xyxplayer`, a scam
  "downloader/player" launcher installed from the Play Store itself
  (`installer=com.android.vending`; it also blocked hand-taps into
  Settings). No device-admin, no accessibility hooks: killed over adb in
  ~2 min: `pm uninstall` the hijacker (Success), reinstall `dist\Home.apk`,
  `cmd package set-home-activity com.grannyhome.launcher/.HomeActivity`,
  re-grant `ACCESS_COARSE_LOCATION`. Rescue screenshot verified the home
  healthy (weather live, AQI 151, battery 100%).
  Junk census while there: 34 third-party apps total; scam-weather/adware
  suspects (`com.inmobi.weather`, `com.handmark.expressweather`,
  `com.weather.Weather`, `com.taboola.ody`, `co.sitic.pp`), factory
  AMX/Telcel bloat, and `com.payjoy.access` (device-financing lock company;
  handle decision-only). Play Store stays ENABLED per owner call (no
  download blocking, "if he downloads we can clear manually").
- **Geometry drift found + fixed (2026-10-31):** during the junk era the
  system display size and font scale were silently changed:
  `wm density` override 446 (verified: 440) and `font_scale 1.3` (verified:
  1.55). Restored both (`wm density 440`, `settings put system font_scale
  1.55`).
- **The font saga (root cause of post-restore clipping):** the theme-font
  customization got flipped sometime late 2026-10-30/early 10-31 (json
  `_applied_timestamp` Oct 31) to
  `android.theme.customization.font = com.android.theme.font.RobotoSlabRegular`
  (+ `persist.sys.overlayfonts=RobotoSlab-Regular`). Android 15 "sans-serif"
  then resolved to Roboto Slab: wider glyphs + different metrics, so the
  r11 fitter re-fit every label smaller (~18.6sp) and "Country Delight"
  fell out of its card: same APK, same geometry, different font.
  Debugging record (worth keeping): rewriting
  `theme_customization_overlay_packages` + flipping `cmd overlay` enable/
  disable changed the AOSP overlay state but NOT the render: on this
  Ontim-built Moto ROM the launcher font is driven by
  `persist.sys.overlayfonts` (prop), which adb shell cannot set and which
  is only consumed at boot/theming events, so per-session background state
  kept winning. The fix that worked: Settings > Display > Font style
  picker on the phone (uiautomator + input taps): the "Global" option maps
  to `MotoNotoSans-Regular`; the picker writes json + prop consistently;
  one reboot re-applied and the home rendered back at the approved Oct-29
  look (labels 132px blocks, 2-line Country Delight 178px, weather strip
  151px). Lesson: on Ontim ROMs `cmd overlay list` can lie; the prop +
  the picker are the truth. Forensics: identical device vs dist APK hashes
  (`45FCFB66...`), snapshots + ui dumps under
  `%TEMP%\opencode\{hashforensics,ui_*.xml}`.
- **r12 folder-screen text fit (2026-10-31, mine; Codex CLI was mid-update
  on the PC so the agreed Codex round ran by hand with the same guard):**
  FolderActivity.java was the only text surface never restyled (26sp static
  title, 20sp static row names, tiny unfitted "No apps here yet").
  Extended the proven fitter family into FolderActivity (fitText /
  applyFitText / largestSingleLineSize / wrapAtBestWordBoundary /
  setFitText / textBlockHeightPx, plus FitTextRule): header now 26/18sp
  target/floor with the word-boundary 2-line balancer, app rows 20/16sp
  2-line with metric-derived row minimum
  `max(96dp, 10dp + max(56dp, 2-line 20sp reserve) + 10dp)`, empty message
  gets a 1-line reserve as well. ZERO behavior-zone deltas
  (snapshot-diff + behavior-scan: click handler, launchable(), intent path
  untouched; only this file changed). Built 45,526 B,
  19:02:47 / 19:25:57 / 19:33:xx 2026-10-31 variants, final installed.
  Two live-verified corrections inside the round:
  - r12.1 status-bar rocket: the screen is full-bleed, so the title got
    its top half hidden under the punch-hole cutout (this screen was never
    verified on the real phone); root now pads by `status_bar_height`
    (dimen) + the usual dp(14).
  - r12.2 initial-size lesson: committing `setTextSize` inside the
    layout-pass fitter does NOT re-measure (requestLayout is swallowed
    mid-layout), so every fitted TextView stuck at its initial 14sp wrap
    block while bigger glyphs overflowed (title half-covered by the first
    card, descenders riding row card edges). Home never hit this because
    it initializes at target size first. FolderActivity now sets the
    target size upfront and lets the fitter only shrink.
  Verified on the Moto: Banking folder = title full, 4 rows
  (PayPal / PNB ONE / Paytm / iMobile) all clean with descenders, folder
  card counts render ("4 apps" with pp intact), home unchanged.
  Evidence: `test-shots\phone_r12_banking_v2.png`,
  `phone_r12_folders.png`, `phone_reboot_sans.png`.
- **Paytm into Banking:** `net.one97.paytm` was floating in the auto
  "All other apps" folder; added it to the Banking array in
  `src\assets\config.json` (3 -> 4 apps: PayPal, PNB ONE `com.Version1`,
  Paytm, iMobile `com.csam.icici.bank.imobile`).
- **Census + decisions (2026-10-31 evening):** full 34-package census
  pulled via `pm list packages -3` + per-APK aapt2 badging (APKs archived
  under `%TEMP%\opencode\census\`, installer attribution via
  `pm list packages -i`); presented to the owner grouped
  (config/keep vs system-security vs removal candidates). The historical
  scam/adware suspects were already gone except The Weather Channel.
  Owner decision: **KEEP ALL 34** (no uninstall pass; the three
  candidates, The Weather Channel `com.weather.Weather`, Apple Music
  `com.apple.android.music`, Amazon Music `com.amazon.mp3` (Amazon Music
  was installed by the preloaded Indus App Store, not grandpa via Play),
  stay for now, revisit later). #card #status/pending-owner-revisit
- **Protection state verified (2026-10-31 evening):** Play Store > Play
  Protect > settings: BOTH toggles on (Scan apps with Play Protect +
  Improve harmful app detection, i.e. Enhanced protection), screen reads
  "No harmful apps found", 46 apps scanned; `package_verifier_enable 1`
  + `verifier_verify_adb_installs 1`; uiautomator helpers already gone.
  The Oct-26 "pending teardown" items below are therefore DONE.
- **Install posture v2 (2026-10-31 night, owner wanted: everything blocked
  all day, updates still automatic): full split achieved.**
  Play's BACK END stays enabled for auto-updates while its front door is
  taken away piecewise:
  - Auto-updates set to "Update all apps over Wi-Fi or mobile data" (the
    radio screen reads "Data charges may apply") + "App download
    preference: Over any network" (Play > Settings > Network
    preferences). Updates flow whenever Play schedules them, even on
    data. Stock Android will not pin updates to a literal 2:00 stamp;
    watch the first days for the actual cadence.
  - Shell `pm disable com.android.vending/...MainActivity` is DENIED
    (`SecurityException: Shell cannot change component state`), so the
    front door moved into the launcher instead: HIDDEN list now contains
    `com.android.vending` (HomeActivity.java). Verified on the phone: the
    alphabetical All-other folder shows no Play Store entry (badge "11
    apps" = its 11 non-Play members) and no config array references it.
  - Play notifications BLOCKED (`cmd appops set com.android.vending
    POST_NOTIFICATION deny` at uid level; system notification page reads
    "You haven't allowed notifications from this app"): nothing baits
    grandpa into the store.
  - Residual vector (recorded, not blockable without root): any FUTURE
    installed app could deep-link `market://` into a store page; that
    still needs explicit Install taps on that page. Re-check fresh apps
    at cable-ins.
  - Day-zero supervised catch-up: "Update all" ran 1 of 2 pending
    updates; the other, Amazon Music, kept failing ("Can't install" /
    "Couldn't update") because its Indus-store-era build could not be
    replaced. Per owner decision it was uninstalled and freshly
    installed from Play (installer now `com.android.vending`, version
    26.38.1). Pipeline proof: "All apps up to date, Last updated 13
    minutes ago" (`test-shots\play_alluptodate.png`). Network pref proof:
    `test-shots\play_updatenetwork.png`.
- **Pending on this project:** the one vault commit (Launcher +
  Phone-Cleaner UI restyle + this README).

## 2026-11-04 junk resweep + install lockdown v3 (HARD)

- **Census:** 67 third-party packages live (re-junked from 34 since Oct-31;
  the flood arrived mostly Nov-02/03 through Play: scam cleaners, fake
  browsers, video-downloaders of the hijacker family, health/loan adware,
  plus grandkid games). Owner confirmed the list, 30 removed by
  `pm uninstall --user 0` (all Success): removal log =
  `..\Phone-Cleaner\removed-apps-2026-11-04.json`. Final surface = 39
  packages, all matched keep-set; baseline +
  disabled-pkg list saved to `census-2026-11-04.txt`.
  Keep-decisions that session: news (NDTV, Amar Ujala), Booking, Acko,
  NoBroker, Roblox + Pokemon TCGP (grandkid; removal would wipe progress)
  and DailyHoots stay. Firefox + a 3rd duplicate radio went.
- **Lockdown v3 (owner asked: nothing installable from anywhere):**
  - `pm disable-user --user 0 com.android.vending` -> SUCCESS
    ("Package com.android.vending new state: disabled-user"). Corrects the
    Oct-31 record: the COMPONENT form (`pm disable <pkg>/<activity>`) was
    the denied one; the package-level form works on this ROM. Play is now
    unlaunchable, hidden from Settings surface at user level
    (re-enabling requires walking Settings > Apps > disabled > Play >
    Enable: grandpa-resistant, not grandpa-proof), auto-updates OFF, and
    every `market://` deep-link residual dies with the package.
  - Sideload gate: NO source currently holds REQUEST_INSTALL_PACKAGES
    ("appops query-op ... allow" = empty). Explicitly DENIED the op on the
    realistic APK-transit sources: Chrome, Files-by-Google, Gmail,
    WhatsApp, Truecaller, Facebook + Messenger (APK files received in chat
    or downloaded in the browser stay inert).
  - Play Protect system verifier stays ON (`package_verifier_enable 1`,
    `verifier_verify_adb_installs 1`); Indus App Store exists only as a
    disabled `com.ontim.launcher3.overlay.indus.appstore` overlay.
- **Update-window procedure (replaces the Oct-31 "updates still automatic"
  posture; auto-updates are gone with the store):** at every cable-in:
  `pm enable com.android.vending` -> Play > Manage apps > Update all
  (driven over adb/uiautomator if convenient) ->
  `pm disable-user --user 0 com.android.vending` again. 2 minutes.
- **Home role re-claimed (again):** `cmd role get-role-holders ...HOME`
  returned `com.motorola.launcher3` (claim lost since the rescue; Moto's
  launcher was even in foreground focus). Fixed:
  `cmd package set-home-activity com.grannyhome.launcher/.HomeActivity`,
  verified holder + foreground = granny. If this recurs, suspect Settings
  loitering; the fix is the same one-liner.
- **Config Music folder synced** (amazon.mp3 + apple.music pins dropped ->
  now YT Music system + Radio India + Sound Recorder), rebuilt via
  build.ps1, installed with explicit `-s ZD222R9BND install -r`,
  location grant reissued, live verified: weather strip (Clear 22C,
  AQI 228), battery 99%, all 6 favorites fit; screenshot
  `test-shots\phone_lockdown_home.png`.
- Left AS-FOUND (flagged to operator): `com.facebook.orca` (Messenger) and
  `com.android.devicelockcontroller` are disabled-user, pre-existing and
  not ours; data preserved, re-enable anytime via `pm enable`. Decision
  only.
- Same-day follow-up (owner decision): removed Acko, Amar Ujala,
  DailyHoots, NDTV, Pokemon TCGP, Roblox, Booking.com (7, all
  unfixed/unpinned, no rebuild needed). "Cooking.com" named by the owner
  was never installed; no-op. Final third-party count: **32**, census
  file regenerated.

## Rebuild / update path

1. Launch in this folder (run `.\build.ps1` from here; paths are relative).
2. Needs `%LOCALAPPDATA%\Android\{jdk17, sdk}` — unchanged machine setup.
3. Same package + same keystore = in-place app updates stay possible.
4. `python play_install.py <pkg>...` and `python pin_apps.py` (the latter in
   [[04-Archives/Grandpa-Phone-Setup/Phone-Cleaner/README|Phone-Cleaner]]) drive the phone over
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

See also: [[04-Archives/Grandpa-Phone-Setup/Phone-Cleaner/README|Phone-Cleaner]] (same-day
companion tool: now its sibling under [[04-Archives/Grandpa-Phone-Setup/README|Grandpa-Phone-Setup]]),
[[01-Projects/README|01-Projects]] completed list,
[[01-Projects/OpenCode-Tasks|OpenCode-Tasks]].

---

*Archived: 2026-10-26 | APK v1.0 (versionCode 1) | min-sdk 29 / target 34*
