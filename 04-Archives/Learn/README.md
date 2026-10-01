# AI Learning System (Learn) Archive

**Status:** COMPLETED
**Date Archived:** 2026-10-01
**Project Type:** Pedagogical Framework Adaptation & Live Obsidian Lesson Engine

---

## Summary

The **AI Learning System (Learn)** project adapted the conversational, visual-first teaching engine from the upstream repository [`amosblomqvist/learn`](https://github.com/amosblomqvist/learn.git) into the Hermes Agent ecosystem and this Obsidian Second Brain.

The system replaces passive lecture dumps with an interactive Socratic engine:
1. **Interactive Diagnostic Probing:** Identifies the edge of understanding before teaching without making assumptions about prior retention.
2. **Dynamic Visual Architecture:** Generates rich multi-tier system architecture diagrams (SVG and Mermaid) rather than dense walls of text.
3. **Live Note Generation:** Produces fully structured lesson notes with DAG roadmaps and Obsidian Spaced Repetition flashcard decks (`#card`).
4. **Consent-Gated Vault Integration:** Never reads or scans private vault files automatically; prompts the user directly for any specific study resources they wish to provide.

---

## Archive Structure

```
04-Archives/Learn/
├── README.md                          # Master archive index & summary
├── Project-Files/                     # Architecture, analysis & operating rules
│   ├── AGENTS.md                      # Instructions & guidelines for future AI agents
│   ├── Adaptation-Plan.md             # Hermes tool mapping & technical roadmap
│   ├── Architecture-and-Components.md # In-depth component & sub-agent analysis
│   ├── Codebase-Analysis.md           # SLOC breakdown & structural inspection
│   ├── plan.md                        # Project execution log & lifecycle
│   └── README.md                      # Project files folder index
├── Lessons/                           # Live generated lesson notes & demos
│   ├── Git-Internals-Blobs-Trees-Commits.md # Complete demo lesson note
│   └── README.md                      # Lessons folder index
├── Assets/                            # Standalone vector diagrams & visuals
│   ├── git-internals-architecture.svg # Multi-tier Git internal architecture SVG
│   └── README.md                      # Assets folder index
└── Source-Files/                      # Upstream repository source backup
    ├── agents/                        # Upstream subagent definitions (researcher, mermaid-maker, svg-maker)
    ├── extensions/                    # Upstream CLI tools (quiz, md-log, visual-tools)
    ├── skills/                        # Upstream skill files (teach, visualize)
    └── README.md                      # Source files folder index
```

---

## Key Achievements & Deliverables

- [x] Ingested and analyzed upstream `amosblomqvist/learn` repository (16 files, 1,784 SLOC).
- [x] Created native `teach` skill in Hermes under `pedagogy` category.
- [x] Implemented interactive diagnostic quizzes via Hermes `clarify` tool.
- [x] Verified live web fact-checking via `web_search` and `web_extract`.
- [x] Generated multi-tier system architecture SVG vector diagram (`git-internals-architecture.svg`).
- [x] Produced live demonstration lesson note (`Git-Internals-Blobs-Trees-Commits.md`) with 6-tier architecture Mermaid diagrams and 11 Spaced Repetition flashcards.
- [x] Enforced strict user-consent policy for vault file scanning and study resource inputs.

---

## Notes for Next AI / Pair Programmer

- **Operating Rules:** Read `Project-Files/AGENTS.md` before executing any teaching workflows or modifying skills.
- **Skill Location:** The active `teach` skill is installed in the Hermes pedagogy profile. Run `skill_view(name='teach')` to inspect or execute it.
- **Visual Standards:** User strictly prefers multi-tiered visual diagrams (similar to cloud/system architecture flowcharts) over long prose.
- **Flashcard Standard:** Always format flashcard blocks with Obsidian Spaced Repetition syntax (`Question #card` / `Q::A` or `==cloze== #card`).
- **Status:** This project is archived and complete. Future lessons should be placed directly in appropriate vault resource folders or new project folders as requested by the user.

---

*Last Updated: 2026-10-01*
