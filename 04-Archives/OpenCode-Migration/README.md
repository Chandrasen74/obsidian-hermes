---
name: README
tags: ["#status/archived", "#type/index", "#domain/productivity"]
---
# OpenCode-Migration Archive

**Status:** COMPLETED
**Date Archived:** 2026-10-25
**Project Type:** Vault migration tooling (retired Hermes agent -> OpenCode, 2026-10-17)

---

## Summary

Leftover tooling from the vault's own setup: the scripts that migrated the retired agent's
skills into OpenCode, plus two native-build logs kept per the owner's "document everything"
request. The migration itself is done; the live results are the OpenCode skills and the
consolidated rules in the vault-root `AGENTS.md`.

---

## Archive Contents

```
OpenCode-Migration/
├── README.md
├── Scripts/
│   ├── migrate_skills.py        # copied skills into OpenCode's skill locations
│   ├── skills_manifest.json     # what was migrated (source -> target paths)
│   ├── verify_frontmatter.py    # checked the migrated skill files' frontmatter
│   └── inspect_dbs.py           # inspected the old agent's data stores pre-migration
└── Logs/
    └── vcpkg-install.log        # vcpkg install of opus, soxr, FLAC, ogg, vorbis (16 min)
```

---

## Notes

- The snapcast build was an experiment run out of the `%TEMP%\opencode` workspace. Its
  build log now lives with the finished project in
  `04-Archives/Multiroom Audio (Snapcast)/logs/snapcast-build.log`, since that build
  became the working multi-room setup. Only the vcpkg dependency log remains here.
- Scripts come from `%TEMP%\opencode\hermes_migrate\` (now empty source side here, files
  kept verbatim).

---

*Last Updated: 2026-10-25*

## See also
[[04-Archives/README|README]]
