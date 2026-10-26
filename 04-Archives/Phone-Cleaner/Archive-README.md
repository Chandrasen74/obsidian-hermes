---
name: Archive-README
tags: ["#status/archived", "#type/index", "#domain/device-setup"]
---
# Phone Cleaner (Moto G35) — ARCHIVED 2026-10-26

USB GUI tool to uninstall/reinstall Motorola junk apps from grandpa's
Moto G35 (no root). Built and archived same day (session 15:20-16:32).
The tool's own usage manual is untouched at [[README]].

## Files

- `PhoneCleaner.ps1` (36 KB) — the whole GUI: 3 tabs (user apps / system
  preloads / reinstall), safety-graylisted for WhatsApp, Truecaller, Kotak,
  shopping+delivery apps; reversible removals
- `Launch Phone Cleaner.bat` — double-click entry (relative paths, so this
  folder works from the archive location as-is)
- `removed-apps.json` — removal log/state (what was taken off the phone)
- `pin_apps.py` — uiautomator2 helper that pins WhatsApp + Truecaller to the
  home screen (drawer->workspace drags the stock Motorola launcher accepts)
  and drops one icon on the other to auto-create the folder
- `README.md` — original manual (use / safety / troubleshooting)

## Stepwise creation timeline (file stamps, 2026-10-26)

| time | step |
|---|---|
| 15:20 | PhoneCleaner.ps1 first version |
| 15:23 | README + Launch .bat |
| 15:39-15:43 | first removal run -> removed-apps.json written |
| 16:03-16:04 | pin_apps.py written |
| 16:32 | PhoneCleaner.ps1 last update (kept current version) |
| 16:22-17:54 | (sibling project) Grandpa-Home launcher built; see its README |

## How to use again

Phone on, USB debugging on, accept RSA prompt, double-click
`Launch Phone Cleaner.bat`. Needs `adb` (.Android\platform-tools or PATH).
For pinning: `uiautomator2 init` once, then `python pin_apps.py`.

See also: [[04-Archives/Grandpa-Launcher/README|Grandpa-Launcher]]
(companion: the launcher APK built for the same phone that afternoon),
[[01-Projects/README|01-Projects]] completed list,
[[01-Projects/OpenCode-Tasks|OpenCode-Tasks]].

---

*Archived: 2026-10-26 | target device: Moto G35 over adb*
