# MAQC Season 7 — AI Session Handoff Document

**Created:** August 19, 2026  
**Purpose:** Transfer full conversation context, team data, and AI usage instructions to a new AI agent continuing this work.  
**Original Conversation ID:** d1e0ded0-1474-4b96-b208-baad7b0315e5

---

## 🤖 AI Usage Instructions for the Receiving Agent

You are continuing an ongoing MAQC Season 7 tournament management session. Read this document fully before responding to any user request. Key rules:

- **Answer only using the MAQC Knowledge Base** (`MAQC_Knowledge_Base.md`) for any rule-related questions.
- **Never invent rules, deadlines, or player data.**
- **All team data** comes from the Google Form CSV responses file.
- **All ongoing match info** (opponent, timing negotiations) is captured in this handoff document.
- When drafting Discord messages, use **Discord markdown formatting** (bold with `**`, spoiler tags with `||text||`, bullet points with `-`).
- The user is the **team Captain** (`akulmach74`). Always draft messages from the Captain's perspective.
- Keep messages **casual and concise** unless the user asks for something formal.
- Always give **UTC as the primary time** and use `||IST: XX:XX||` and `||EDT: XX:XX||` spoiler tags for local conversions.
- The user's team has **India-timezone players** who cannot play past ~**11:30 PM IST** and **US-EDT players** who prefer afternoon/evening.

---

## 📁 Files in the Workspace

All files are located at: `c:/Users/Kanchan Verma/OneDrive/Desktop/MAQC S7/`

| File | Description |
| :--- | :--- |
| `MAQC_Knowledge_Base.md` | **Primary source of truth.** All rules, workflows, deadlines, glossary, FAQs. Always consult this first. |
| `MAQC Season 7 - Week 1 Matchmaking.pdf` | Official Week 1 matchmaking bracket PDF. Team is in Bracket 8, Match #640. |
| `MAQC Season 7 Team Information (Responses) - Form responses 1 (1).csv` | Google Form responses with all 5 player details. |
| `Mech Arena Quarterly Clash - Information Guide.pdf` | Original official MAQC information guide PDF. |
| `discord text shared by admins.txt` | Original Discord admin announcements and official rulebook text. |
| `create_form.gs` | Google Apps Script that auto-generates the team information Google Form. |

---

## 👥 Team Roster

| Role | Name | Discord | Player ID | Max SP | Timezone |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Captain** | Akulmach74 | akulmach74 | 64516590 | 18000 | UTC+05:30 (IST) |
| Player 2 | Destroyer | DΣ2TRØYΣR | 67665771 | 15825 | UTC+05:30 (IST) |
| Player 3 | Bowolf | BoWolf | 77849365 | 19181 | UTC-04:00 (EDT) |
| Player 4 | Gunshot | gunshot9099 | 56671448 | 21597 | UTC+05:30 (IST) |
| Player 5 | Baby Bird | slimpickles. | 26410318 | 22550 | UTC-04:00 (EDT) |

- **Highest Team Max SP (for MAQC Registration):** `22550` (Baby Bird)
- **Team Size:** 5 players ✅
- **All Player IDs:** 8-digit numbers only ✅

### Player Availability Notes
- **Akulmach74:** Evening IST. Either DM or Ping.
- **Destroyer:** Evening + Late Night IST. Discord DM preferred.
- **Bowolf:** Morning + Late Night EDT. Either DM or Ping. **Has tattoo appointment Saturday at 18:00 UTC (2:00 PM EDT / 11:30 PM IST). Not available Saturday.**
- **Gunshot:** Late Night IST. Discord DM preferred.
- **Baby Bird:** Evening EDT. Server Ping preferred. **Did not explicitly confirm Sunday availability — assume tentative.**

---

## ⚔️ Week 1 Match Status

| Field | Details |
| :--- | :--- |
| **Match Number** | #640 |
| **Bracket** | Bracket 8 |
| **Opponent Leader** | @ita_lev06 |
| **Opponent Registered SP** | ~23,000 |
| **Week 1 Map** | Biogear Lab |
| **Gamemode** | CPC (Control Point Clash) |
| **Format** | Best of 3 |
| **Week 1 Deadline** | 23rd August 2026, 6:00 AM UTC |
| **Scheduling Deadline** | Friday, 22nd August 2026, 6:00 AM UTC |
| **Battle Post Channel** | #s07-battle-posts-week-01 |

### Scheduling Negotiation Status (as of August 19, 2026)
The captain and opposing leader are actively negotiating a match time. Here is the timeline:

1. **Captain proposed:** 13:30–15:30 UTC (any day) ||IST: 7:00–9:00 PM || ||EDT: 9:30–11:30 AM||
2. **Opposing leader responded:** They prefer **Saturday or Sunday, 20:00–02:00 UTC** ||IST: 1:30 AM–7:30 AM || ||EDT: 4:00–10:00 PM||
3. **Problem identified:** 20:00 UTC = 1:30 AM IST — too late for India players.
4. **Captain's plan:** Propose **Sunday at 16:00–17:00 UTC** ||IST: 9:30–10:30 PM || ||EDT: 12:00–1:00 PM||
5. **Why Sunday:** Bowolf has a tattoo appointment Saturday at 18:00 UTC (unavailable Saturday).
6. **Baby Bird status:** Did not confirm Sunday availability. Assumed tentative.
7. **Last draft sent to opponent:** Asked if Sunday 16:00 UTC or 17:00 UTC works, citing that Saturday is unavailable for one player and that 20:00 UTC is too late for India players.

### ⚠️ Next Steps Required
- [ ] Wait for @ita_lev06 reply on Sunday timing.
- [ ] Confirm Baby Bird's Sunday availability.
- [ ] Once time is agreed, one leader creates the Custom Match and shares the code in the Battle Post.
- [ ] Scheduling must be finalized before **Friday 22nd August, 6:00 AM UTC**.
- [ ] If no agreement by Friday, ping a MAQC Moderator immediately.

---

## 📋 What Was Done in This Session

### Documents Created / Updated
1. **MAQC_Knowledge_Base.md** — Built from scratch and updated 5 times across the session to incorporate:
   - Initial PDF + Discord text rules
   - Official Rulebook additions
   - Honor System Clarification (Aug 17)
   - Week 1 Announcement (map, channels, scheduling guide, submission guide, bot rules)
2. **create_form.gs** — Google Apps Script to auto-generate the team information Google Form with:
   - Auto-removes a player's name from dropdown after they submit
   - Descriptive country-based timezone options
   - Number-only validation for Player IDs and SP fields
   - Auto-closes form when all 4 players have submitted

### Messages Drafted
- Team confirmation briefing (for internal team Discord).
- Opponent contact message for Match #640 (@ita_lev06).
- Multiple rounds of scheduling negotiation messages.
- Team availability check message (asking Bowolf and Baby Bird about Sunday noon EDT).
- Final Sunday proposal message to opponent with spoiler-tagged timezone conversions.

### Registration Data Extracted
From Google Form CSV responses, the captain's registration-ready block was:
```
Highest Team Max SP: 22550
Team Size: 5 players
Captain Discord: akulmach74 — ID: 64516590
Player 2: Destroyer — 67665771
Player 3: Bowolf — 77849365
Player 4: Gunshot — 56671448
Player 5: Baby Bird — 26410318
```

---

## 🗓️ Critical Upcoming Deadlines

| Deadline | Date & Time (UTC) |
| :--- | :--- |
| **Scheduling must be agreed** | Friday 22nd August, 6:00 AM UTC |
| **Match must be played & submitted** | Sunday 23rd August, 6:00 AM UTC |
| **Week 1 officially ends** | Sunday 23rd August, 6:00 AM UTC |

---

## 💬 Discord Message Style Guide (For the Receiving Agent)

- **Tone:** Casual, friendly, conversational. No corporate language.
- **Length:** Short paragraphs. Avoid excessive bullet lists in casual messages.
- **Timings:** Always lead with UTC. Use `||IST: XX:XX||` and `||EDT: XX:XX||` spoiler tags inline.
- **Mentions:** Use `@Username` format for Discord mentions.
- **Bold:** Use `**text**` for important info.
- **No over-formatting** in casual messages. Avoid headers and long tables in Discord drafts.
- **Internal team messages:** Slightly more detailed, can include bullet points.
- **Opponent messages:** Keep it brief, friendly, and to the point.
