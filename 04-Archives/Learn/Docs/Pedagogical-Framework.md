---
name: Pedagogical-Framework
tags: ["#status/archived", "#type/doc", "#domain/ai-learning"]
---
# Pedagogical Framework & Teaching Principles

This document specifies the pedagogical architecture adapted from Amos Blomqvist's `learn` system into the Hermes ecosystem.

---

## 1. Core Philosophy: Intuition & First Principles

Learning is not passive consumption of text; it is the iterative repair of mental models.

### Key Pedagogical Pillars:
1. **Never Assume Retention:** Learners naturally forget or require calibration. Sessions start with real-time diagnostic probing rather than relying on stale historical profiles.
2. **Diagnostic Edge Detection:** Probes find the exact boundary of what the user understands. Distractors represent common conceptual traps, not random wrong facts.
3. **Visual Architecture Over Prose:** High-density text walls are replaced by structured multi-tier diagrams (Mermaid flowcharts and standalone SVG vector diagrams).
4. **Consent-Gated Context:** Never scan personal notes in the background. The learner is asked directly if they wish to supply reference material.
5. **Continuous Spaced Repetition:** Every lesson synthesizes core mechanics into `#card` formatted decks for Obsidian Spaced Repetition.

---

## 2. The 4-Phase Teaching Lifecycle

```mermaid
flowchart TD
    classDef probe fill:#0369a1,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef dag fill:#0f766e,stroke:#2dd4bf,stroke-width:2px,color:#fff;
    classDef teach fill:#581c87,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef log fill:#831843,stroke:#f472b6,stroke-width:2px,color:#fff;

    P1["Phase 1: Topic & Diagnostic Probe<br/>• Ask for user-provided resources<br/>• Locate edge of understanding with clarify"]:::probe
    P2["Phase 2: Build DAG Roadmap<br/>• Deconstruct topic into fundamental axioms<br/>• Agree on scope & milestones"]:::dag
    P3["Phase 3: Socratic Delivery Loop<br/>• Motivate -> Establish -> Connect<br/>• Real-time Checkpoint Quiz with clarify"]:::teach
    P4["Phase 4: Synthesis & Flashcard Logging<br/>• Render multi-tier system diagrams<br/>• Generate #card decks in Obsidian note"]:::log

    P1 --> P2 --> P3 --> P4
```

---

## 3. Misconception Handling & Distractor Engineering

When crafting checkpoint quizzes via `clarify`:
- **Correct Option:** Represents the first-principles truth.
- **Distractor A (The Diff Trap):** Reflects treating systems like naive line diffs.
- **Distractor B (The In-Place Trap):** Reflects treating immutable stores like mutable in-place databases.
- **Distractor C (Path/Naming Trap):** Reflects confusing content bytes with metadata paths.

When a distractor is selected, the system logs the misconception directly in the session notes and provides a targeted mental model repair.

## See also
[[Architecture-and-Components]]
[[Adaptation-Plan]]
[[Codebase-Analysis]]
[[04-Archives/Learn/Docs/README|README]]
