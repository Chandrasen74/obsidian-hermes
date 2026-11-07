---
name: README
tags: ["#status/archived", "#type/index", "#domain/device-setup"]
---
# Grandpa Phone Setup (Moto G35) - MERGED ARCHIVE 2026-11-07

Everything built for the setup, housekeeping, and upkeep of **grandpa's
Motorola Moto G35** (Android 15, Ontim-built Moto ROM, no root; serial
`ZD222R9BND`, already used in the linked logs below). USB debugging is left ON
deliberately: future tweaks stay a one-cable job. Phone display state: density
440, font scale 1.55 (both were restored deliberately on 2026-10-31).

Two companion tools, archived 2026-10-26 and merged 2026-11-07 into this one
navigable folder:

| folder | what it is | entry point | details |
|---|---|---|---|
| `Phone-Cleaner\` | USB GUI to uninstall/reinstall Moto junk apps over adb (3 tabs, safety-graylist, reversible) | double-click `Launch Phone Cleaner.bat`; pinning helper: `python pin_apps.py` | [[04-Archives/Grandpa-Phone-Setup/Phone-Cleaner/Archive-README|Archive-README]] + the untouched tool manual [[04-Archives/Grandpa-Phone-Setup/Phone-Cleaner/README|README]] |
| `Grandpa-Launcher\` | hand-built no-Gradle Android home launcher APK `com.grannyhome.launcher` (big-text elderly UI: favorites, folders, weather skycons, liquid battery, AQI strip) | `.\build.ps1` (+ `-Install` for adb install, `-SetRole` to set Home) | [[04-Archives/Grandpa-Phone-Setup/Grandpa-Launcher/README|README]] with the full build/lockdown timeline |

## Quick how-to

1. Plug the phone in, USB debugging on, accept the RSA prompt.
2. Junk sweep / reinstall: `Launch Phone Cleaner.bat` (needs adb).
3. Launcher rebuild + update: `.\build.ps1` from `Grandpa-Launcher\`; install
   with `.\build.ps1 -Install` or `adb -s ZD222R9BND install -r`; re-claim
   Home if needed: `cmd package set-home-activity com.grannyhome.launcher/.HomeActivity`.
4. Store updates (auto-updates are currently OFF): walk the update-window
   procedure in the Grandpa-Launcher README (Nov-04 section): enable Play,
   Update all, disable Play again.

## Kept-on-disk, not in git

- `Grandpa-Launcher\keys\granny.keystore` - signing key, git-ignored
  (`grannyhome` alias `granny`, passwords in the launcher README); same key +
  same package = in-place APK updates.
- Build outputs under `Grandpa-Launcher\build\`, installable signed APK at
  `Grandpa-Launcher\dist\Home.apk`.

## Timeline (see each README for the details)

| date | what happened |
|---|---|
| 2026-10-26 | Phone Cleaner built (15:20-16:32), ~150 junk removals; launcher built same afternoon (16:22-17:54) |
| 2026-10-28/29 | Launcher rounds 1-8: status strip, 3-up then 2-up tiles, metric text fitter, live weather + AQI, real-phone migration (emulator retired) |
| 2026-10-31 | Hijacker rescue (scam launcher uninstalled), junk census + Play-lockdown v1, folder-screen fit r12; install posture v2 |
| 2026-11-04 | Junk resweep (67 -> 32 third-party apps, removals logged in Phone-Cleaner `removed-apps-2026-11-04.json`), install lockdown v3 HARD (Play disabled at package level, sideload ops denied), Home role re-claimed, music pins rebuilt |
| 2026-11-07 | Both archives merged into this folder (links updated, nothing deleted) |

See also: [[01-Projects/README|01-Projects]] completed list,
[[01-Projects/OpenCode-Tasks|OpenCode-Tasks]].

---

*Archived: 2026-10-26 (both tools) | merged: 2026-11-07 | device: Motorola Moto G35, Android 15*
