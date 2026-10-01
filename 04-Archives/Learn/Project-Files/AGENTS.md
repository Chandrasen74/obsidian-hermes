# AGENTS.md — Operating Rules & Guidelines (Learn System)

Use this guide whenever an AI agent is tasked with teaching, generating study notes, or extending the pedagogy subsystem.

---

## 1. Core Operating Principles

1. **No Autonomous Vault Scanning:**
   - NEVER scan the user's private vault files in the background without explicit permission.
   - ALWAYS ask the user directly during the topic setup: *"Do you have any existing resource material (notes, drafts, links, or files) you'd like to use for this topic?"*
   - Only inspect specific resources the user explicitly provides.

2. **Visual-First Explanations:**
   - Avoid long text blocks. Break down concepts into multi-tier system architecture diagrams, state machines, and DAG flowcharts.
   - Use categorized Mermaid subgraphs (`subgraph Tier1`, `Tier2`, etc.) with distinct styling and directional data flows.
   - When appropriate, generate standalone dark-themed SVG diagrams under an `Assets/` directory.

3. **No Assumptions About Retention:**
   - Do not maintain a persistent profile that assumes knowledge is retained across sessions.
   - Start every new lesson with an interactive diagnostic probe via the `clarify` tool to establish current baseline understanding.

4. **Interactive Diagnostic Quizzes (`clarify` tool):**
   - Use targeted distractors representing common misconceptions rather than trivial recall.
   - Allow open-ended answers and long reasoning.
   - Repair mental models immediately when misconceptions surface.

5. **Spaced Repetition Integration:**
   - Always append a dedicated `#card` deck at the end of generated lesson notes.
   - Support both Q&A cards and cloze deletions (`==highlighted term== #card`).

---

## 2. File Map & Subsystems

| Path | Purpose |
|---|---|
| `04-Archives/Learn/README.md` | Master archive summary and status |
| `04-Archives/Learn/Project-Files/` | System design, SLOC analysis, adaptation plans, and agent rules |
| `04-Archives/Learn/Lessons/` | Generated live markdown lesson notes with embedded diagrams and cards |
| `04-Archives/Learn/Assets/` | Vector SVG architecture diagrams and visual artifacts |
| `04-Archives/Learn/Source-Files/` | Upstream TypeScript and prompt source files from `amosblomqvist/learn` |

---

## 3. Tool Mapping for Hermes

| Upstream Pi Harness | Hermes Tool Equivalent |
|---|---|
| `extensions/quiz.ts` (TUI quiz) | `clarify` tool (single-choice & open-ended questions) |
| `extensions/md-log.ts` | Direct Obsidian `.md` file generation via `write_file` / `patch` |
| `agents/researcher.md` | `web_search` and `web_extract` for live technical verification |
| `agents/mermaid-maker.md` | Inline Mermaid architecture diagrams with custom styling |
| `agents/svg-maker.md` | Standalone SVG vector generation in `Assets/` |

---

## 4. Vault Conventions

- All Git commits in the vault repository must use `akulmach74` as the author name.
- Keep `README.md` files updated across all PARA directories (`00-Inbox`, `01-Projects`, `02-Areas`, `03-Resources`, `04-Archives`).
- Avoid em dashes (`—`) in draft outputs.
