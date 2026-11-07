---
name: README
tags: ["#status/archived", "#type/index", "#domain/device-setup"]
---
# Coolita TV Attempt (Infinix TV) - FAILED AND CLOSED 2026-11-07

An attempt to debloat an **Infinix smart TV running Coolita TV OS** using the
[CleanYourTV](https://github.com/Gathin23/cleanyourtv) method. It never got off
the ground: Coolita is not Android TV, so the whole ADB-based approach does not
apply to the set.

## What was tried

1. Cloned the upstream CleanYourTV repo (ADB debloat scripts, reference
   launcher `com.gathin.tvhome`, themes, docs) and kept it as a project copy,
   with frontmatter added across the project docs (vault commit `288f28d`).
2. Staged a USB break-in kit at `Project-Files/cleanyourtv/work/apks/`:
   an HTML page titled "Infinix Break-in" hosting
   `ActivityLauncher-2.4.1.apk`, meant to be opened from a USB stick in the
   TV so it could download and sideload Activity Launcher as a first foothold.
3. Multiple attempts to load the USB page / get an APK into the TV. All failed.

## Why it failed

Coolita TV OS is a closed, non-Android smart TV OS:

- No ADB surface on the TV (the CleanYourTV pipelines are all `adb`-driven;
  the upstream project's own rule says stop on non-Android sets).
- No browser to open the USB-hosted page.
- No Android APK install path at all, so even a downloaded APK is blocked.

Conclusion: **nothing sideloads onto this TV in any way we tried**. There is no
repair short of an Android TV. Keep CleanYourTV upstream for the next Android
TV in the house (any set with an ADB developer port works out of the box).

## What is preserved

| path | what it is |
|---|---|
| `Project-Files/cleanyourtv/` | the full upstream repo copy as used (docs frontmattered, tools + launcher + themes intact); the failed attempt's artifacts live under `work/apks/` |
| `Project-Files/cleanyourtv/work/apks/index.html` | the "Infinix Break-in" USB page |
| `Project-Files/cleanyourtv/work/apks/ActivityLauncher-2.4.1.apk` | the APK it offered (v2.4.1, 3.4 MB) |
| `Git-Metadata/` | the upstream clone's `.git`, preserved here when the clone was de-gitted (moved in from `04-Archives/cleanyourtv-origin-clone`) |

Repo hygiene note: `work/` and `*.apk` are ignored by CleanYourTV's own
`.gitignore`, but both files were force-tracked in this vault and the owner
explicitly wants them published, so they are committed (vault override).

## Takeaway for future sessions

- Coolita TV = no sideload, no browser, no ADB: stop, do not retry unless the
  firmware ever changes.
- CleanYourTV only helps on Android TV models (ADB port). For future TV
  work, verify the OS *first*, before you clone anything.
- Upstream repo remains at https://github.com/Gathin23/cleanyourtv (MIT).

See also: [[04-Archives/README|04-Archives index]],
[[01-Projects/OpenCode-Tasks|OpenCode-Tasks]].

---

*Archived: 2026-11-07 | Outcome: blocked at step one (OS gap) | TV: Infinix, Coolita TV OS*
