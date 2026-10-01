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

## 🗂️ Archive Navigation & Map

```
04-Archives/Learn/
├── README.md                           # Master archive index & summary (this note)
├── Docs/                               # Technical & pedagogical documentation
│   ├── README.md                       # Docs folder index
│   ├── Pedagogical-Framework.md        # Teaching philosophy, Socratic loops & probes
│   ├── Architecture-and-Components.md  # Upstream subsystems & sub-agent analysis
│   ├── Adaptation-Plan.md              # Hermes tool mapping & technical roadmap
│   └── Codebase-Analysis.md            # SLOC breakdown & structural inspection
├── Lessons/                            # Live generated lesson notes & demos
│   ├── README.md                       # Lessons folder index
│   └── Git-Internals-Blobs-Trees-Commits.md # Complete demo lesson note
├── Assets/                             # Standalone vector diagrams & visual artifacts
│   ├── README.md                       # Assets folder index
│   └── git-internals-architecture.svg  # 6-Tier Git internal architecture SVG
├── Project-Files/                      # AI operating rules & project lifecycle
│   ├── README.md                       # Project files folder index
│   ├── AGENTS.md                       # Canonical guidelines for future AI agents
│   └── plan.md                         # Milestone execution log & lifecycle
└── Source-Files/                       # Upstream repository source backup
    ├── README.md                       # Original repository README
    ├── agents/                         # Upstream subagent definitions (researcher, svg, mermaid)
    ├── extensions/                     # Upstream CLI tools (quiz, md-log, visual-tools)
    └── skills/                         # Upstream skill files (teach, visualize)
```

---

## 🚀 Quick Links to Core Artifacts

- **Live Demonstration Note:** [[04-Archives/Learn/Lessons/Git-Internals-Blobs-Trees-Commits|Git Internals Lesson (Visuals + 11 Cards)]]
- **Vector Architecture Diagram:** [[04-Archives/Learn/Assets/git-internals-architecture.svg|Git Engine Architecture SVG]]
- **AI Operating Manual:** [[04-Archives/Learn/Project-Files/AGENTS|AGENTS.md]]
- **Pedagogical Spec:** [[04-Archives/Learn/Docs/Pedagogical-Framework|Pedagogical Framework]]
- **Architecture Spec:** [[04-Archives/Learn/Docs/Architecture-and-Components|Architecture & Components]]

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
