# AGENTS.md — Repo Operating Rules (MAQC-7)

Use the current Arena session branch specified by the environment/system instructions. Never switch, create, or push another branch.

## Layout (flat, repo root)
- `plan.md` — workflow guide: when to read, use, and maintain every Markdown file.
- `Week_5_Brief.md` — live status: record, deadlines, checklist, run plan.
- `Week_5_Mod_Questions.md` — mod Q&A log + copy-paste Discord drafts + tracking table.
- `Time_Formula_Sheet.md` — conversions, `<t:>` stamps, weekly locks/slots.
- `MAQC_Knowledge_Base.md` — rules only (canonical; never invent beyond it).
- `README.md` — file map. PDFs/CSVs/screenshots/`.txt` — evidence, in place.
- Canonical agent memory lives in repo `.agent/` (SOUL/USER/MEMORY/PLANS); home-directory copies are only mirrors.

## Conventions
- Discord drafts: UTC-first, `<t:UNIX:F>` stamps, `||IST||`/`||EDT||` spoilers, casual tone, code blocks. Inside copy-paste payloads, keep `<t:...>` raw—inline backticks stop Discord from rendering it.
- **NO EM DASHES (`—`):** Never use em dashes in Discord messages/drafts (they look like obvious AI tells). Use commas, periods, colons, or parentheses instead.
- Clipboard: automatically pipe ready-to-send Discord drafts / copy-paste payloads directly into the user's Windows clipboard (`clip.exe` / Python) so the captain can immediately paste them into Discord.
- Baby Bird = Google Messages only: plain text, all zones spelled out, no Discord markdown.
- Match refs always include the week ("Week 5 #665") — numbers repeat across weeks.
- Follow `plan.md`; briefly plan meaningful work and confirm consequential changes with the user.
- Commit + push to the session branch after each meaningful change.
- Never invent rules/results; mod replies and official docs only. Log mod answers with dates.
