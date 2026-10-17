---
name: Adaptation-Plan
tags: ["#status/archived", "#type/doc", "#domain/ai-learning"]
---
# Adaptation Plan: Integrating `learn` into OpenCode & Obsidian

**Goal:** Adapt the teaching, visualization, and interactive assessment capabilities of `amosblomqvist/learn` into our OpenCode agent and Obsidian Second Brain environment.

---

## 1. Mapping Components to OpenCode Agent Architecture

| Learn (pi) Component | Upstream Implementation | OpenCode Native Equivalent / Adaptation Strategy |
| :--- | :--- | :--- |
| **`teach` Skill** | [[04-Archives/Learn/Source-Files/skills/teach/SKILL|SKILL]] (pi skill) | Convert into native OpenCode skill (`skill_manage` / `skills/pedagogy/teach`) |
| **`visualize` Skill** | [[04-Archives/Learn/Source-Files/skills/visualize/SKILL|SKILL]] | Integrate with OpenCode visual skills (`excalidraw`, `mermaid`, `architecture-diagram`) |
| **`quiz` & `ask-user-question`** | Custom TUI extensions in TypeScript | Adapt via the `clarify` tool or custom interactive scripts |
| **`md-log`** | Live TUI listener to Obsidian file | Direct Obsidian note authoring using native `write_file` / `patch` in `00-Inbox` or `01-Projects` |
| **`researcher` Agent** | Subagent Markdown spec | Delegate via `delegate_task` or autonomous web tools (`web_search`, `web_extract`) |
| **Diagram Makers** | `mermaid-maker`, `svg-maker` | Delegate via `delegate_task` with vision verification |

---

## 2. Recommended Action Items

- [ ] **Step 1:** Ingest and register `teach` and `visualize` skills into the agent's local skills directory.
- [ ] **Step 2:** Configure an automated session note logger in [[00-Inbox/README|README]] or active project directories for interactive learning sessions.
- [ ] **Step 3:** Set up a diagram generation template for Obsidian (`viz/` folder with Mermaid / Excalidraw support).
- [ ] **Step 4:** Test an end-to-end teaching session on a selected topic (e.g., a technical concept) following the Probe -> Plan -> Teach loop.

---

## 3. Immediate Status
- [x] Repository cloned and inspected.
- [x] Codebase SLOC analyzed with `pygount`.
- [x] Full source code organized in `01-Projects/Learn/Source/`.
- [x] Overview, architecture, and codebase notes created in Obsidian vault.
- [ ] Waiting for user go-ahead on target integration steps.

## See also
[[Pedagogical-Framework]]
[[04-Archives/Learn/Docs/README|README]]
