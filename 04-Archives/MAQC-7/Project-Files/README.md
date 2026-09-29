# MAQC Season 7 — Team akulmach74 Tournament Database

**Tournament:** Mech Arena Quarterly Clash (MAQC) Season 7
**Team:** akulmach74 (Captain: Akulmach74 / Eipstenian) | **Bracket:** 10 | **Registered SP:** 23,000
**Season:** 17 Aug 2026 to 27 Sep 2026 (6 weeks) | **Final roster:** 3 players | **Record:** 1-4 (W6 pending)

---

## Quick navigation

| What you need | Go to |
| :--- | :--- |
| Current week status and checklist | `Week_6_Brief.md` |
| W6 mod ticket and DQ ruling | `Week_6_Mod_Questions.md` |
| All MAQC rules (canonical, never invent beyond this) | `MAQC_Knowledge_Base.md` |
| Time zones and Discord timestamps | `Time_Formula_Sheet.md` |
| Workflow and file maintenance guide | `plan.md` |
| Agent operating rules | `AGENTS.md` |
| Agent tasks and memory | `.agent/PLANS.md` · `.agent/MEMORY.md` · `.agent/USER.md` |
| Full season summary | `docs/Season_Overview.md` |
| Per-week match summaries | `docs/Week_1.md` through `docs/Week_6.md` |
| PDFs, screenshots, exports | `evidence/` folder |

---

## Season results — all 6 weeks

| Week | Match | Opponent | Opp SP | Map | Mode | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W1 | #640 | @ita_lev06 | 23,000 | Biogear Lab | Bo3 CPC | Loss |
| W2 | #671 | @shegotyou88 / TӨXIC&TƛƧTY | 23,758 | Skyship 11 | Bo3 CPC | Auto-loss (scheduling dispute) |
| W3 | #668 | @mrjama0586 | 22,364 | Paradise Plaza | Bo3 CPC | Loss 1-2 |
| W4 | #665 | @mecharenazim / ZiM | 22,200 | Site 313 | Bo3 CPC | Loss 1-2 |
| W5 | #665 | vs BOT | — | Forbidden City | Bo3 CPC | Win 2-0 |
| W6 | #630 | vs BOT (charliebrown0002 DQ) | — | Imperial Temple | Bo3 CPC | Pending |

---

## Team roster (final, 20 Sep 2026)

| Player | Discord | In-game ID | Timezone | Role |
| :--- | :--- | :--- | :--- | :--- |
| Akulmach74 (Captain) | Eipstenian | 64516590 | IST (UTC+5:30) | Captain, Eclipse support |
| Gunshot | gunshot9099 | 56671448 | IST (UTC+5:30) | Outlaw (Gemini Outlaw) |
| BoWolf | — | 77849365 | EDT (UTC-4) | Voidghost opener (mobile player) |

Removed 20 Sep (Ticket #583): Destroyer (ID 67665771) · Baby Bird (ID 26410318)
Team mentor: Gladiator (`gladiator_22837`, `<@1217130504357413015>`)

---

## Key mod rulings

| Date | Ticket | Ruling | Impact |
| :--- | :--- | :--- | :--- |
| 14 Sep 2026 | W5 Q&A | Must play full Bo3 vs bots; Equalize; 1 human minimum | Bot match procedure defined |
| 20 Sep 2026 | #583 | Roster removal allowed anytime; team min 2; SP recalculated | Roster finalized at 3 |
| 24 Sep 2026 | #267 | charliebrown0002 DQ for gross misconduct and DM threats | W6 match converted to bot match |
| All season | W2 #671 | Lock = one exact UTC time + yes from both leaders in battle post | Scheduling rule (precedent) |

---

## File map

### Active (open every session)

| File | Purpose |
| :--- | :--- |
| `Week_6_Brief.md` | W6 live status: match #630, bot match checklist, thread log, DQ details, strat |
| `Week_6_Mod_Questions.md` | Ticket #267 full transcript and disqualification ruling |
| `MAQC_Knowledge_Base.md` | Canonical rules reference v1.2. Do not invent beyond this. |
| `Time_Formula_Sheet.md` | UTC conversions, Discord `<t:UNIX:F>` timestamps, weekly slot tables |
| `plan.md` | When to read, update, and sync every file. Read at session start. |
| `AGENTS.md` | Repo-wide conventions and agent invariants |

### Agent memory (`.agent/`)

| File | Purpose |
| :--- | :--- |
| `.agent/PLANS.md` | Open tasks, backlog, completed history |
| `.agent/MEMORY.md` | Confirmed domain facts and technical lessons |
| `.agent/USER.md` | Captain profile, roster, constraints, communication preferences |
| `.agent/SOUL.md` | Agent identity, tone, non-negotiable invariants |

### History (read-only reference)

| File | Purpose |
| :--- | :--- |
| `Week_5_Brief.md` | W5 operations, roster saga (Ticket #583), W5 2-0 bot match details |
| `Week_5_Mod_Questions.md` | 8 mod Q&As on bot match procedure; full Ticket #583 transcript |
| `docs/Season_Overview.md` | Full 6-week season summary: results, roster changes, all precedents |
| `docs/Week_1.md` through `docs/Week_6.md` | Per-week match summaries with context and evidence links |

### Evidence (`evidence/`)

| File | What it is |
| :--- | :--- |
| `MAQC_Information_Guide_v1.0.pdf` | Official MAQC S7 rules and info guide |
| `MAQC_S7_Week1_Matchmaking.pdf` through `MAQC_S7_Week5_Matchmaking.pdf` | Official MM lists |
| `MAQC_S7_Team_Registration_Responses.csv` | Google Form registration data |
| `Discord_Admin_Announcements_and_Rulebook.txt` | Raw Discord announcements and rulebook text |
| `Discord_Community_Channel_2026-08-14_to_2026-08-30.html` | W2 #671 battle-post export (double-loss case study) |
| `Earlier_Chat_Export_W2-W4_drafts.txt` | AI chat export, W2-W4 drafts and style reference |
| `AI_Session_Handoff_W1_era.md` | Week 1 era handoff (roster, style guide) |
| `Screenshot_20260924_185314_lock_confirmed.png` | W6 Draft 6 sent (match time locked, mod thumbs-up) |
| `Screenshot_20260924_185252_team_brief_sent.png` | W6 Draft 7 sent (team strategy brief) |
| `Screenshot_20260916_*.png` | W4/W5 era screenshots |
| `Screenshot_20260829_*.png` and `Screenshot_20260830_*.png` | Early season screenshots |
| `Screenshot_20260910_074204_Discord.jpg` | Sep 10 Discord context screenshot |

---

## Glossary

| Term | Meaning |
| :--- | :--- |
| MAQC | Mech Arena Quarterly Clash |
| Bo3 CPC | Best of 3, Control Point Clash gamemode |
| SP | Squad Power (matchmaking bracket metric) |
| Equalize | Mandatory lobby bot setting for all MAQC matches |
| Bracket 10 | Highest of 10 matchmaking SP tiers (our bracket) |
| Battle post | Assigned Discord forum thread for all match communication and result submission |
| Ticket cutoff | Friday 06:00 UTC each week (last chance to raise scheduling or dispute tickets) |
| Match deadline | Sunday 06:00 UTC each week (results must be posted before this or it is a loss) |
| DQ | Disqualification |
| IST | India Standard Time (UTC+5:30) |
| EDT | Eastern Daylight Time (UTC-4) |
| AKDT | Alaska Daylight Time (UTC-8) |

---

## How to search this repo

All Markdown files use consistent heading levels and keyword phrases:

- Rules and rulings: search `MAQC_Knowledge_Base.md` for rule name, "Penalty", or "precedent"
- Match scheduling: search `Week_N_Brief.md` for "Draft", "SENT", "locked", or "UTC"
- Time conversions: search `Time_Formula_Sheet.md` by week number or timezone abbreviation
- Mod tickets: search `Week_N_Mod_Questions.md` for "Ticket #", "Ruling", or "night fury"
- Open tasks: search `.agent/PLANS.md` for `[ ]` (open) or `[x]` (done)
- Player info: search `.agent/USER.md` by player name or in-game ID
- Evidence files: `evidence/` filenames use YYYYMMDD format for date-sorted browsing

**Search keywords:** Mech Arena Quarterly Clash, MAQC Season 7, MAQC S7, akulmach74, Imperial Temple, Forbidden City, Bo3 CPC, Bracket 10, Squad Power, charliebrown0002, night fury, Ticket #267, Ticket #583, mod ruling, disqualification, gross misconduct, scheduling, Discord timestamps, UTC IST EDT AKDT
