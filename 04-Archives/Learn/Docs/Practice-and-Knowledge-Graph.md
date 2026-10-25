---
name: Practice-and-Knowledge-Graph
tags: ["#status/active", "#type/doc", "#domain/ai-learning"]
---
# Practice Rounds & the Persistent Learner-Graph

Recorded 2026-10-25. This documents the second adaptation of the Learn project: what was adopted from the successor repository [`amosblomqvist/learnharness`](https://github.com/amosblomqvist/learnharness) into the `teach` skill, chat-native, without installing anything from it.

---

## What LearnHarness changed upstream

The original `amosblomqvist/learn` (this archive's source) exposed a **probe → plan → teach** conversational engine. LearnHarness evolved that into an Electron app with three mechanisms the old repo lacked:

1. **A persistent knowledge graph**: propositions and reasoning chains (premises that *jointly* imply a conclusion) accumulated across sessions, with provenance back to the session that produced them. Future teaching sessions read the graph instead of probing from scratch; practice sessions draw their problems from it.
2. **Separate practice sessions**: retrieval and application drills distinct from teaching, where the right knowledge must come to mind *without being named first*, adapting to the learner's reasoning.
3. **Think-out-loud capture**: the learner's reasoning, uncertainty, and reactions recorded as first-class evidence, not just right/wrong verdicts. Plus self-reported confidence.

Its sharpest epistemic idea is the **two-kinds-of-evidence rule**: *sessions* record what the learner actually did (evidence about the person); *the graph* is a model-authored map of taught material, and a proposition being present proves nothing about the learner's understanding or retention.

---

## What we adopted, and where it landed

| LearnHarness mechanism | Chat-native port | Land |
|---|---|---|
| Persistent knowledge graph | Per-topic `Learner-Graph.md` notes: propositions with `#taught` / `#verified` / `#repaired` statuses, reasoning chains, verbatim misconception log, `[[wiki-link]]` provenance | `04-Archives/Learn/Lessons/<Topic-Slug> Learner-Graph.md` |
| "Knowledge that carries forward" | **Phase 0 Resume**: read the graph before probing; `#verified` strands get one spot-check, `#repaired` strands are re-tested first, absent strands get a full probe | `teach` skill, Phase 0 |
| Two-kinds-of-evidence rule | The graph's **Hygiene section**: teaches ≠ knows, absence ≠ ignorance, confidence ≠ score, missing confidence ≠ zero; only `#verified` is solid ground | `teach` skill, Learner-Graph skeleton |
| Separate practice sessions | **Phase 4 practice rounds**: retrieval-without-naming problems drawn from approved graphs, adaptive hint ladder, statuses updated after the round | `teach` skill, Phase 4.3 |
| Think-out-loud capture | Misses recorded verbatim in the Misconception log; optional self-reported confidence treated as signal, never a score | `teach` skill, Phase 1a |
| Read-only boundary on learning data | Graphs are written by the skill that taught them and only read by approved sessions; the vault is never swept uninvited (consent rule preserved) | `teach` skill, Phase 0 / 1c |

### Also fixed in the same pass (not from LearnHarness)

- The live skill had drifted into a lossy condensation: it called a `clarify` tool that does not exist in this OpenCode harness and pointed lessons at the deleted `01-Projects/Learn/Lessons/` path. The skill was **rebased on this archive's full 151-line version** (edge bracketing by binary search, quiz-options construction procedure, verify-before-teach accuracy clause) and remapped to real OpenCode tools (`question`, `subagent`, `websearch`).
- Lessons now write to `04-Archives/Learn/Lessons/<Topic-Slug> Lesson.md` (user decision, 2026-10-25), so the archive is the master again, and the live skill (`%USERPROFILE%\.config\opencode\skills\pedagogy\teach\SKILL.md`) is byte-identical to `Source-Files/skills/teach/SKILL.md`.

---

## Deliberately skipped

- **The LearnHarness app itself** (Electron, 30+ provider keys, cost meter). Our engine is the chat session; the app would be a second harness.
- **Its JSON data format and Python readers.** Their reader skill exists because their graph ships as JSON/JSONL in an app-managed data folder. Ours is plain Obsidian markdown, already indexed, linked, and greppable by the vault itself.
- **Verbatim AGPL text or code.** Ideas were ported and re-expressed in our own skill wording; nothing is copied file-for-file.

## See also

[[04-Archives/Learn/README|Learn Archive README]] · [[04-Archives/Learn/Docs/Pedagogical-Framework|Pedagogical Framework]] · [[04-Archives/Learn/Lessons/README|Lessons index]]
