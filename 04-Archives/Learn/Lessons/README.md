---
name: README
tags: ["#status/archived", "#type/index", "#domain/ai-learning"]
---
# Lessons & Generated Study Notes

This folder stores lesson notes and study artifacts generated during interactive teaching sessions.

---

## Lesson Archive

| Lesson | Topic | Visuals | Flashcards | Date |
|---|---|---|---|---|
| **[[Git-Internals-Blobs-Trees-Commits]]** | Git Internals (Blobs, Trees, Commits, Refs) | 6-Tier Architecture Diagram, Immutability Graphs | 11 Cards (`#card` & Cloze) | 2026-10-01 |

---

## Lesson Note Standard Structure

1. **Metadata Header:** Topic, date, goal, and related vault links.
2. **System Architecture Flowchart:** Multi-tiered engineering layout (Mermaid & SVG embedding).
3. **Deep-Dive Visual Mechanisms:** Subsystem diagrams, data flows, and state transitions.
4. **Session Diagnostics & Checkpoint Insights:** Log of questions, misconceptions identified, and mental model repairs.
5. **Spaced Repetition Flashcards:** `#card` formatted Q&A and cloze deletions for Obsidian Spaced Repetition plugin.

## Learner-Graph Notes

Every new session also maintains a per-topic learning record alongside the lesson note:

| File | Holds | Status tags |
|---|---|---|
| **`<Topic-Slug> Lesson.md`** | The lesson itself: DAG, diagrams, diagnostics, flashcards | (plain note) |
| **`<Topic-Slug> Learner-Graph.md`** | Propositions, reasoning chains, verbatim misconception log, provenance to the lesson note | `#taught` / `#verified` / `#repaired` |

The graph is read at the start of the next session (Phase 0 resume: re-test `#repaired` first, spot-check `#verified`, full-probe the absent) and written at every landed node. It is a learning record, not a mastery record; rules and rationale: [[04-Archives/Learn/Docs/Practice-and-Knowledge-Graph|Practice-and-Knowledge-Graph]].

## See also
[[04-Archives/Learn/README|README]]
