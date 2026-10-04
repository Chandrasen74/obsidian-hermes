---
name: OMNIROUTE_STARTUP
tags: ["#status/active", "#type/doc", "#domain/productivity"]
---
# Omniroute Startup Guide

**Purpose:** Quick-start command for launching your Obsidian second brain with logging

## Startup Command

```batch
Set-ExecutionPolicy Bypass -Scope Process -Force; omniroute --log
```

## Files

- **omniroute_launcher.bat** - Double-click to run the command above
- **omniroute startup.txt** - Contains the raw command for reference

## Usage

1. **Double-click** `omniroute_launcher.bat` to start omniroute with logging
2. Or run the command directly in PowerShell/Command Prompt:
   ```
   Set-ExecutionPolicy Bypass -Scope Process -Force; omniroute --log
   ```

## Notes

- The `-Scope Process -Force` bypasses execution policy only for the current process
- `omniroute --log` starts omniroute with logging enabled for debugging
- These files are kept in the vault root for quick access before starting any work session

---
*Startup guide for Obsidian second brain initialization*

## See also
- [[Hermes-Tasks]]
- [[01-Projects/README|README]]
