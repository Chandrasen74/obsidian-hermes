# Project: AI Learning System (Learn)

**Repository:** [amosblomqvist/learn](https://github.com/amosblomqvist/learn.git)
**Status:** Active
**Category:** Knowledge Management / Interactive Pedagogy
**Date Started:** 2026-10-01

---

## Project Overview

This project adapts the interactive AI teaching and learning system designed by Amos Blomqvist (from the video *"How I Use AI to Learn Things"*) into our personal Obsidian knowledge base and Hermes Agent workflows.

The system shifts AI interactions from standard question answering to a structured pedagogical loop that builds durable mental models through first-principles understanding, motivated discovery, active probing, and automated visual diagrams.

---

## Key Components

- **[[Codebase-Analysis|Codebase Analysis & SLOC]]**: Full breakdown of languages, code volume, and file statistics.
- **[[Architecture-and-Components|Architecture & Core Modules]]**: In-depth review of the pedagogy engine (`teach`), diagram tools (`visualize`, `svg-maker`, `mermaid-maker`), research verification (`researcher`), and UI interactive extensions (`quiz`, `ask-user-question`, `md-log`).
- **[[Adaptation-Plan|Adaptation Plan & Next Steps]]**: Roadmap for integrating these capabilities natively into our Hermes agent, Obsidian vault logging, and custom workflows.

---

## Repository Structure in Vault

```text
01-Projects/Learn/
├── README.md                          <- This project index
├── Codebase-Analysis.md               <- Code metrics, SLOC, and file breakdown
├── Architecture-and-Components.md     <- Pedagogical philosophy & system architecture
├── Adaptation-Plan.md                 <- Integration roadmap & action items
└── Source/                            <- Full upstream source code
    ├── agents/                        <- Subagent prompt specifications
    ├── extensions/                    <- TypeScript interactive UI & tools
    ├── skills/                        <- Teaching and visualization skills
    └── assets/                        <- Project assets
```

---

## Related Notes & Links
- [[01-Projects/Hermes-Tasks|Hermes Task Log]]
- [[01-Projects/README|Projects Index]]
- [[03-Resources/Welcome|Vault Welcome & Resources]]
