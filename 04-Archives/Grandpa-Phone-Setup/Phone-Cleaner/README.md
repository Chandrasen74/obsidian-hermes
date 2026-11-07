# Phone Cleaner for Moto G35

GUI checkbox tool to uninstall junk apps from the phone over USB (no root, all removable).

## Use

1. Connect the phone (USB debugging on, accept the RSA prompt on first plug).
2. Double-click `Launch Phone Cleaner.bat`.
3. Tab 1 = user apps (junk pre-ticked) → press **Uninstall**.
4. Tab 2 = system preloads (curated junk pre-ticked, advanced toggle optional).
5. Tab 3 = restore: tick and **Reinstall selected** to bring anything back.

## Safety

- WhatsApp, Truecaller, Kotak, shopping/delivery/delivery apps are grayed
  out and can never be removed by this tool.
- Removal is reversible; `removed-apps.json` logs every removal.
- If a user app cannot be reinstalled by `install-existing`, it must be
  reinstalled from Play Store (its APK was deleted with user data).

## Troubleshooting

- `adb not found` → install Android platform-tools to
  `%LOCALAPPDATA%\Android\platform-tools` or add `adb` to PATH.
- `unauthorized` → unlock the phone and tap Allow on the USB debugging prompt.
