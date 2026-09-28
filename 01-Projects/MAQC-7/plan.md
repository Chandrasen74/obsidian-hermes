# MAQC Repository Planning and Markdown Maintenance Guide

## Purpose

This file explains **when to read, use, and update** the repository's Markdown files. It is the workflow guide; it is **not** the live task list. Current and future tasks belong in `.agent/PLANS.md`.

The agent should consult this guide at the start of meaningful MAQC work and keep the relevant files synchronized whenever the user confirms a durable fact, decision, preference, result, deadline, or correction.

## Planning workflow

### Before work

1. Read `AGENTS.md`, this file, and `.agent/PLANS.md`.
2. Read `.agent/USER.md` and `.agent/MEMORY.md` for user preferences and confirmed context.
3. Read the current week's brief and any task-specific file.
4. Give the user a short proposed plan before meaningful or multi-file work.
5. Confirm the plan with the user when it changes strategy, records, deadlines, outbound communication, or other important facts. A direct, specific user instruction already counts as approval for that requested work.
6. Ask instead of guessing when evidence or intent is unclear.

### During the conversation

Update the appropriate file in the same work session when new information is confirmed:

- New result, deadline, opponent, map, availability, or completed action → current week brief and `.agent/PLANS.md`.
- Official rule, announcement, or moderator ruling → `MAQC_Knowledge_Base.md`; cite its source and date.
- Moderator question, answer, or message status → current week's mod-questions file.
- New time or corrected conversion → `Time_Formula_Sheet.md` and the relevant live brief/draft.
- Durable user preference, roster/contact detail, or communication constraint → `.agent/USER.md`.
- Durable operational fact or technical lesson → `.agent/MEMORY.md`.
- Stable agent behavior or non-negotiable guardrail → `.agent/SOUL.md` or `AGENTS.md`.
- New actionable work, changed priority, blocker, or completed task → `.agent/PLANS.md`.

Do **not** record speculation, casual chatter, duplicate facts, secrets, credentials, or unsupported claims. Never rewrite official evidence to make it match a summary.

### Before finishing

1. Check every changed fact against the user's confirmation, an official document, or a dated moderator reply.
2. Synchronize duplicated live facts, especially record, match reference, deadlines, availability, and task status.
3. Mark tasks complete only when they actually happened; drafts are not sent messages.
4. Run targeted `grep`, `git diff --check`, and any task-specific verification.
5. Review the final diff, then commit and push meaningful changes to the current Arena session branch.
6. Tell the user what changed, what remains open, and what needs their action.

## File responsibilities

**Repository reorganized 24 Sep 2026:** `docs/` for week summaries, `evidence/` for PDFs/screenshots/exports.

| File | Read/use when | Update when |
| :--- | :--- | :--- |
| `plan.md` | Deciding which files and workflow to use. | The repository workflow, file responsibilities, or maintenance rules change. |
| `README.md` | Finding the current entry points and evidence. | A primary file is added, renamed, superseded, or changes purpose. |
| `docs/Season_Overview.md` | Need full season context (results, roster changes, precedents). | After a significant match result, mod ruling, or roster change. |
| `docs/Week_N.md` | Need per-week match summary with evidence links. | After each week's match is completed. |
| `evidence/` folder | Searching for PDFs, screenshots, exports by date (YYYYMMDD format). | When adding new evidence files (always use consistent naming). |
| `AGENTS.md` | Before repository work; authoritative repo operating rules. | A stable repo-wide convention or safety rule is confirmed. Avoid session-specific branch names. |
| `.agent/PLANS.md` | At the start and end of each task-oriented conversation. | A task is added, prioritized, blocked, skipped, or completed. Keep only current focus/backlog plus concise completed history. |
| `.agent/USER.md` | Before drafting messages or recommending schedules. | The user confirms a durable preference, roster/contact change, timezone constraint, or workflow preference. |
| `.agent/MEMORY.md` | Recovering context across sessions and handling known edge cases. | A durable confirmed fact or reusable technical lesson is learned. Do not use it as a task list. |
| `.agent/SOUL.md` | Checking stable behavior and invariants. | A long-term behavioral rule changes—not for weekly facts. |
| `Week_5_Brief.md` (and future `Week_N_Brief.md`) | Managing the active week: record, matchup, deadlines, checklist, run plan, and sent/drafted communications. | Any active-week fact or action changes. Label drafts and sent messages accurately with dates. |
| `Week_5_Mod_Questions.md` (and future equivalents) | Preparing and tracking moderator communication. | A question is drafted/sent/answered or a ruling is received. Record moderator, date, and exact substance. |
| `MAQC_Knowledge_Base.md` | Answering rules questions. This is the canonical rules summary. | Only official documents, announcements, or direct moderator rulings add or correct a rule. Never infer rules from outcomes. |
| `Time_Formula_Sheet.md` | Creating schedules, deadlines, and Discord timestamps. | A source time changes or a conversion/timestamp is verified or corrected. |
| `AI_Session_Handoff.md` | Consulting older roster/style context. | Only when intentionally maintaining historical handoff material. Do not treat old status as current. |
| `MAQC_Session_Handoff_Update.md` | Historical reference only; currently superseded. | Normally do not update. Prefer live `.agent/` files and weekly briefs. |

## Synchronization rules

- **One source by category:** rules → knowledge base; active tasks → `.agent/PLANS.md`; user preferences → `.agent/USER.md`; durable context → `.agent/MEMORY.md`; weekly operations → weekly brief.
- When a fact must appear in multiple places, update all live copies in one change and verify with `grep`.
- Preserve evidence and exact moderator wording; summaries must not silently strengthen a ruling.
- Match references always include the week, for example **Week 5 #665**.
- Discord payloads use UTC-first scheduling, a raw `<t:UNIX:F>` token, and `||IST||`/`||EDT||` spoilers. Never wrap the timestamp token in inline backticks inside a copy-paste payload, because Discord will show it as code instead of rendering it.
- Baby Bird has no Discord: use Google Messages or in-game chat with plain text and all time zones spelled out.
- Do not hardcode an old Arena session branch in guidance files; use the branch required by the current session instructions.

## Regular review cadence

- **Every task-oriented conversation:** review `.agent/PLANS.md`; update affected live files when something durable changes.
- **After a match/mod reply/team confirmation:** update immediately, verify, commit, and push.
- **At the start of a new MAQC week:** create the new weekly brief and mod-questions file, refresh README links, move completed work out of current focus, and preserve prior weeks as history.
- **Before deadlines/practice/matches:** verify timestamps, availability, message destination, and whether a message is merely drafted or actually sent.
- **When nothing durable changed:** do not edit files just to create activity.
