---
name: Codebase-Analysis
tags: ["#status/archived", "#type/doc", "#domain/ai-learning"]
---
# Codebase & SLOC Analysis: amosblomqvist/learn

**Source Repo:** https://github.com/amosblomqvist/learn.git
**Inspection Tool:** `pygount` v3.2.0

---

## 1. Summary Statistics

| Language | Files | % Files | Code Lines (SLOC) | % Code | Comment Lines | % Comment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TypeScript** | 7 | 43.8% | 1,771 | 63.6% | 280 | 10.1% |
| **JSON** | 1 | 6.2% | 13 | 72.2% | 0 | 0.0% |
| **Markdown** | 6 | 37.5% | 0 | 0.0% | 220 | 50.0% |
| **Generated / Binary** | 2 | 12.5% | 0 | 0.0% | 0 | 0.0% |
| **Total** | **16** | **100.0%** | **1,784** | **55.0%** | **500** | **15.4%** |

*Note: In `pygount`, Markdown files and skill definitions are counted under documentation/comment lines.*

---

## 2. File-by-File Line Count Breakdown

| File Path | Language | SLOC | Purpose / Description |
| :--- | :--- | :--- | :--- |
| `extensions/quiz.ts` | TypeScript | 713 | Graded multi-choice / multi-select TUI quiz system with instant feedback |
| `extensions/ask-user-question.ts` | TypeScript | 466 | Interactive TUI prompt for open-ended or choice clarifications |
| `extensions/md-log.ts` | TypeScript | 269 | Live session mirror to an Obsidian Markdown note |
| `extensions/visual-tools/tools/mermaid_tools.ts` | TypeScript | 130 | Mermaid compilation & PNG renderer |
| `extensions/visual-tools/tools/svg_tools.ts` | TypeScript | 124 | SVG authoring, rendering, and PNG export tools |
| `extensions/visual-tools/tools/_common.ts` | TypeScript | 93 | Common file/renderer utilities for visual tools |
| `extensions/visual-tools/index.ts` | TypeScript | 27 | Visual tools extension registration entrypoint |
| [[04-Archives/Learn/Source-Files/skills/visualize/SKILL|SKILL]] | Markdown | 23 | Directing subagents to create minimal, verified diagrams |
| [[mermaid-maker]] | Markdown | 18 | Prompt & tool specs for Mermaid diagram generator subagent |
| [[svg-maker]] | Markdown | 18 | Prompt & tool specs for precise geometric SVG subagent |
| [[04-Archives/Learn/Docs/README|README]] | Markdown | 13 | Upstream project overview and installation instructions |
| [[04-Archives/Learn/Source-Files/skills/teach/SKILL|SKILL]] | Markdown | 9 | Core pedagogical skill: axioms, motivated discovery, probe-plan-teach |
| `extensions/visual-tools/package.json` | JSON | 13 | Node dependencies for Mermaid rendering tools |
| [[researcher]] | Markdown | 2 | Spec for web search & truth verification subagent |
| `assets/thumbnail.png` | Binary | 0 | Video cover asset |
| `extensions/visual-tools/package-lock.json` | Generated | 0 | Dependency lockfile |

---

## 3. Technology Stack & Dependencies

1. **Host Environment:** `pi` coding agent runtime (`@mariozechner/pi-coding-agent`, `@mariozechner/pi-tui`).
2. **UI Framework:** TUI editor and custom render loop supporting keyboard navigation (arrows, space, enter, tab), live terminal sizing, and ANSI color styling.
3. **Diagram Engines:**
   - `@mermaid-js/mermaid-cli` (Chromium-backed rendering).
   - `rsvg-convert` / ImageMagick for SVG to PNG conversion.
4. **Markdown Bridge:** Live appending of conversation and quiz states into Obsidian-compatible markdown callouts (`[!quote]`, `[!abstract]`, `[!question]`, `[!success]`, `[!failure]`).

## See also
[[Pedagogical-Framework]]
