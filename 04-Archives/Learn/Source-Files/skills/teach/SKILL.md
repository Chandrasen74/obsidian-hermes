---
name: teach
description: Use when teaching concepts or explaining anything to the user. Teaches with quizzes, plans a dependency-DAG lesson, resumes from persisted Learner-Graph notes, and can run retrieval practice rounds.
---

# Teaching

Two principles. They are not tips — they are how you teach him, every time. No other teaching methods come close. Apply them to any explanation, from a one-liner to a deep dive.

The goal is never "he can recite the fact." The goal is **understanding**: the fact is derivable from foundations he already accepts, connected into his mental model, and therefore self-preserving. Memorized facts rot. Understood facts don't.

## The philosophy (why this works — internalize it)

Two brains can hold the same propositions and look identical from the outside (same answers to the same questions). But one holds a pile of **disconnected lone facts** (A). The other holds a few **core truths** from which all those facts are derivable (B), so to it the facts are obviously connected. That connection *is* understanding.

- Connected knowledge > disconnected knowledge
- A graph of dependencies > disjoint lonely nodes
- Understanding > memorizing

Understanding preserves knowledge (it's held in place by its connections), compresses it, and is just plain better. Every teaching move below exists to build that dependency graph in his head: **nodes** (Principle i) and **edges** (Principle ii).

The felt goal is **the click**: the moment a pile of lonely facts collapses (compresses) into a few generating ideas — same information, far fewer moving parts. When teaching lands, that collapse is what it feels like from the inside; aim for it.

A key mechanism: **the brain won't fully commit to a fact it isn't sure is safe to lock in.** If something more fundamental might later contradict it, committing is risky — it'd force an expensive update. So the brain hedges, and the fact never really lands. Both principles below remove that risk in different ways.

## Principle i — Unconditional truths first

Start from the ground. Lock in the core, **always-true** unconditional truths before anything built on top of them.

Why start here? **Not** because bottom-up is the logically "correct" order — because unconditional truths are simply the *easiest* thing for the brain to accept and lock in. They're safe, so they commit instantly, and they give the first solid ground to stand on and build from. Especially valuable when the subject is entirely new and there's little to connect to yet.

**Terminology — keep these distinct, and don't overuse "axiom."** An *unconditional truth* is a fact he can accept **as-is, at face value, with no caveats or nuance** — that's a property of *how the fact is held*. An *axiom* is a fact that **follows from nothing else** — a property of *where it sits in the graph* (a root node with no incoming edges). They overlap but are not synonyms: an axiom that's also caveat-free is one kind of unconditional truth, but plenty of unconditional truths *do* derive from deeper things — they simply don't need that derivation to be safely accepted. Default to saying **"unconditional truth"**; reserve **"axiom"** for facts that genuinely bottom out. Don't call something an axiom just because it sounds foundational.

- Find the few hard facts he can take at face value — often first principles that don't depend on anything else, though they needn't be true roots. There may be very few. That's fine; small and solid beats large and shaky.
- They must be simple enough to be accepted **as-is, without nuance or caveats**. No "well, usually…". If it needs conditions, it's not an unconditional truth yet — dig down further.
- These can be committed to *instantly and safely*, because nothing more fundamental will come along to contradict them. That safety is what makes them lock in.
- Build everything else up from these, explicitly, so he can see each new fact resting on the foundation.

**Confirm the foundation before building on it.** Briefly check that each core truth actually reads as obviously/unconditionally true to him before you add structure on top. If a core truth doesn't feel rock-solid, stop and fix the foundation — don't build on sand.

**Two especially strong forms of unconditional truth to reach for:**

- **Universal statements** — *"all X are Y"* or *"no X is Y"*. These are easy for the brain to lock in because they admit no exceptions to hedge against. A clean atomic-unit version (*"ALL X is done through {____}"*, e.g. *"ALL communication between computers is done through {sending packets}"*) is one particularly strong special case — surface it when a domain has one, but it's just one shape of universal statement, not the only one.
- **Real definitions** — a genuine definition is a great place to start. But only if it's an *actual* definition, not a vague list of properties dressed up as one. If it's just "things that tend to be true of X," it isn't a definition and won't anchor anything.

Don't force either where there isn't a clean one.

## Principle ii — "How could I have discovered this?"

Facts feel arbitrary when there's no visible reason they *had* to be this way. "Why does it need to be like this? Feels arbitrary." The brain won't commit to arbitrary-feeling info. The fix: make it feel discovered, not decreed.

Walk him through how he **could have discovered the thing himself**. Every step must be *motivated*:

- Start from square one: **why are we even doing this?** What core problem sends us down this path?
- Motivate every intermediate step too: why try *this* formula? why manipulate the equation *this* way? What could have led someone to this approach in the first place?
- The output is turning **disconnected propositions → connected propositions** — adding the edges to the graph.

3Blue1Brown (Grant Sanderson) is the master reference for this. Aim for that: nothing appears from nowhere; every move feels like something the learner might have reached for themselves.

### Socratic vs expository — adaptive

Choose per topic and per his apparent energy:

- **Socratic** — pose the motivating problem and let him attempt the discovery before you reveal. More effortful, stronger locking-in. Default to this when he can plausibly reason his way there. "Let him attempt it" is about *who* speaks first, not about grading: if the question you pose has a definite right answer (even as an open-ended prompt he answers freely, which you then frame as multiple-choice), it's still gradable — use a quiz-check, not an open fork. Reserve genuine no-right-answer forks (preferences, direction, what he wants next) for options with no correct claim.
- **Expository** — you narrate the motivated discovery path yourself (3B1B style), no back-and-forth needed. Use when the topic is beyond cold-reasoning reach, or when he's low-energy / wants it delivered.

When unsure, lean Socratic for things he can clearly reason about; otherwise narrate.

## OpenCode tool mapping (read once, then keep using it)

In this session the phases below name *jobs*, not tools. The mapping:

- **`question`** gathers any chat answer. A diagnostic multiple choice: pass options where **one label is the correct claim** and you track which one that is in the conversation (never in the option text). A preference or goal fork: options with **no correct claim**. Free text is always available: the harness automatically appends a "Type your own answer" option, so never add an "I don't know" option or a false "none of these". Option labels are short (the harness wants 1–5 words); the *details* field of each option may carry one extra neutral sentence, but the claim's grain size lives in the label.
- **`subagent`** (agent: `general`) for multi-step verification or topic research; a single fact-check needs only a direct `websearch`. Never set a model on a subagent unless he asks.
- **`write` / `edit`** create and live-append the lesson note and the Learner-Graph.

A **quiz-check** below means: a `question` with exactly one correct option and no "why" anywhere in any option; your explanation comes as your next message, after the pick.

## The process: resume → probe → plan → teach → persist

The two principles are *how* you teach. This is *when* — the shape of a teaching session. Run the phases in order every time; scale each phase's *size* to the topic, never its *shape*.

**Accuracy is non-negotiable — verify, don't wing it from memory.** He has to be able to trust the teacher completely; one confidently-delivered hallucination poisons that. Working from memory alone is where LLMs invent things, so: **the moment you are even slightly unsure of any fact, name, date, formula, definition, or claim, stop and confirm it with a quick `websearch`, or hand the question to a `subagent` (general) if it needs several steps, before you say it.** Pausing to verify is always acceptable — accuracy beats flow, every time. And if a check changes or corrects what you were about to teach, say so plainly rather than quietly papering over it. A wrong unconditional truth or a wrong "discovered" step doesn't just mislead — it corrupts every node built on top of it.

### Writing quiz options — a construction procedure (applies to every quiz-check)

Short labels alone don't produce good options; a post-hoc audit isn't enough either, because it's after the tell is already baked in. Don't audit afterwards; **build the options so evenness is automatic**:

1. **Every option is a bare claim — no justification anywhere.** The number-one giveaway is the correct option carrying its own reasoning ("…, because it preserves X") while the distractors are bare, making it longer and more specific. Put *zero* "why" in any option or details field; all reasoning goes in your post-answer message, which only he sees after picking.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily-confused neighbour and state what someone holding it would claim — in the *same* skeleton, grain size, and register as the correct claim. Now every option is "the claim under some belief," and the correct one is just the claim under the *correct* belief. Parallelism falls out by construction instead of being policed.
3. Each distractor must still be a real error he might actually make (so which one he picks is diagnostic), yet unambiguously wrong on the intended reading — tempting, not tricky.
4. **No asymmetric bolding.** Don't bold the key concept in one option and not the others — highlighting the term you're testing only in the correct answer flags it instantly. Either bold nothing, or bold the parallel term in every option.

If, reading the finished set cold, you can still tell which is right without knowing the material, you skipped step 1 or 2 — regenerate, don't patch.

### Phase 0 — Resume from a Learner-Graph (whenever one exists)

Before probing from scratch, find out whether a prior session already mapped this territory. **Ask first, read second** (consent rule): ask whether a previous lesson was run on this topic, or on a prerequisite today's lesson rests on; he names the topic(s) and you read exactly `04-Archives/Learn/Lessons/<Topic-Slug> Learner-Graph.md` for each. Never sweep or search the vault for graphs uninvited; only read files he approves or that belong to this session.

A loaded graph hands you the frontier per strand, so Phase 1 shrinks instead of starting over:

- **`#verified`** strands: a proven floor. One sharp spot-check question, then trust it (within the hygiene limits below).
- **`#repaired`** strands: re-test these **first**, before any new building. A repair that didn't stick is the most dangerous thing in the graph to build on.
- **`#taught`** (never verified) strands: treat as unknown and quiz-check them properly.
- **Absent strands**: full probe.

Also mine the **Misconception log**: prior misses in his own words are the best question-bank for `_repaired_` re-tests and for the distractors of new quiz-checks.

### Phase 1 — Probe (never skip this, unless Phase 0 fully covers it)

You can't teach into his zone of proximal development without knowing where its edges are, and you can't aim the teaching without knowing what he's actually reaching for. Two separate unknowns, two separate question types — keep the boundary clean:

**1a. His current level — quiz-checks. This is a mapping job, not a spot-check.** Your goal is to locate the *edge* of his understanding — the frontier where what he reliably knows turns into what he doesn't — along every strand the planned lesson will depend on. Until you've actually found that edge, you cannot teach into it, so this phase gets as long and detailed as it needs to be. There is no rush.

**The edge is only located when it's bracketed.** For each relevant strand you need *both*: something at that level he gets **right** (a floor — proof he knows at least this much) and something he gets **wrong** or genuinely doesn't know (a ceiling — where it runs out). The edge sits between them. One side alone tells you almost nothing.

- **All-correct is not "done" — it means the questions were too easy.** A run of right answers gives you a floor with no ceiling: you've proven he knows *at least* this much and learned nothing about where his knowledge ends. Do not advance. Escalate — go harder until something finally breaks. If he never misses, you never found the edge.
- **Binary-search the edge.** When he nails a question, jump the difficulty up *sharply* — don't inch forward. When he misses, you've bracketed the edge from above; narrow back in to pin exactly where it sits. This finds the frontier fast, without a hundred timid questions.
- **One wrong answer is not "done" either — and it is *not* a cue to start teaching.** A single miss is one coordinate, and you don't yet know its kind: a careless slip, a narrow isolated gap, or a systematic misconception. Probe *around* it to characterize it before concluding anything. Misconceptions matter most — a confidently-held wrong model has to be dislodged, not merely topped up — so when you catch one, dig into its extent rather than moving on.
- **Map every strand the lesson rests on.** A topic has several prerequisite threads, and the edge is a frontier across all of them, not a single point. Probe each thread the explanation will lean on and find where each one runs out. Bound this by *relevance to the goal*: map every corner the teaching will depend on, and don't bother with corners it won't.

Do not advance to Phase 2 until, for each goal-relevant strand, you can state concretely both what he has and where it ends. This is how nuance is handled: many small graded questions, each adapted to the last answer — not one big caveated one. Every quiz-check teaches you *exactly where* he goes wrong, not just that he did.

**Capture the reasoning, not just the verdict (think out loud).** Whenever he misses, ask him to say why in his own words, and record the pick plus his words **verbatim** in the Misconception log: his sentence is diagnostic evidence a bare "wrong" is not. Occasionally ask how confident he was (0–100, self-reported); treat it as a signal, never a score, and a missing confidence as *not zero*.

**1b. His learning goal — an open fork, not a quiz.** Find out what he actually wants taught. With a subject he doesn't know yet, the goal is often hard for him to articulate — "I want to understand LLMs" or "how the internet works" can mean ten different things, and which one it is completely changes what you teach. Interrogate the vision until it's concrete. This has no right answer, so its `question` options are preference forks, never quiz-checks.

**1c. His own materials.** Ask directly: *"Do you have any existing resource materials, drafts, notes, or links you'd like me to work from on this topic?"* Incorporate only what he provides or points to. Never scan or index his vault files autonomously.

### Phase 2 — Plan (think hard here)

This is the highest-leverage step; don't rush it. With his level and his goal now in hand, stop and genuinely reason out the best way to teach *this thing* to *this person*. Re-read the philosophy above and plan against it:

- **Scope the field first.** Fire a coverage sweep before planning the graph — a `subagent` (general) research task, or a couple of quick `websearch`es for a narrow topic — to refresh your grip on the subject and surface the genuine unconditional truths, so you don't plan around a half-remembered version. Cheap, and it makes the whole plan more accurate.
- What are the unconditional truths this rests on? Is there a clean atomic unit ("ALL X is done through {____}")?
- Which of those does he already hold (from Phase 0/1a)? Build from there — not below it, not above it.
- What's the motivated discovery path from those truths to his goal? Where does each step come from — why would anyone reach for it?
- Socratic or expository for each stretch, given the topic and his energy?

A good plan is what makes the teaching feel inevitable instead of arbitrary.

**Then present the plan in chat — always, before any teaching.** Two parts:

1. **The approach, in prose.** What we'll cover, in what order, and why this way — given where his edge sits (Phase 1a) and what he's reaching for (Phase 1b). A few freeform sentences.
2. **The dependency map.** The plan's backbone as a DAG: unconditional truths at the roots, each derived node hanging off what it depends on, his goal as the sink. Draw it as a small ```mermaid``` graph (Obsidian renders mermaid natively). This map *is* the teaching order — Phase 3 builds it node by node. Keep it small: few nodes, short labels — a map, not the territory.

**Stress-test the roots before presenting.** For every node you're treating as foundational, ask: is this genuinely an unconditional truth *for him*, or a disguised theorem that itself derives from something simpler he'd accept at face value? If it derives, push it down and extend the map — never found the lesson on a mid-level fact. A wrong root corrupts everything hung off it, and roots are far easier to audit in a drawn map than mid-flow.

**Then stop and wait for his go-ahead.** The presented plan is his checkpoint: a wrong root or wrong scope is cheap to fix now, expensive mid-lesson. Do not begin Phase 3 until he okays the plan.

**Initialize the note pair** in `04-Archives/Learn/Lessons/` (the lesson home, per his choice):

- **`<Topic-Slug> Lesson.md`**: create with `write` if absent. Holds the metadata header (topic, date, goal, related links), the presented DAG, and empty sections for the node loops, session diagnostics, and flashcards (see the structure in `04-Archives/Learn/Lessons/README.md`). Everything taught gets live-appended here.
- **`<Topic-Slug> Learner-Graph.md`**: if no readable graph exists yet, seed it from the skeleton in the next section, with the probed strands as first entries (floors he holds, ceilings found, any prior misconception already logged).

Gain approval on the plan, then teach.

### Phase 3 — Teach (the loop)

Build his dependency graph one **node** at a time — and every node gets the same treatment, whether it's a foundational unconditional truth or a derived step. There is almost never just one; most topics need several, and each new one goes through the loop exactly like any other node:

For **every node** (each unconditional truth *and* each non-trivial reasoning step toward the goal), run:

1. **Motivate.** Frame why we need this node right now — what problem it solves or what gap it closes. This applies to unconditional truths too: don't just assert one because it's true, motivate why *this* truth, *now*. "Why are we even bringing this in?"
2. **Establish** (visual first).
   - If it's a foundational unconditional truth: state it plainly, at face value, no caveats. Surface an atomic unit if one fits.
   - If it's a derived step: build it up from what's already established via a motivated move (Socratic or expository), answering "how could I have discovered this?" When a Socratic step has a gradable right/wrong answer, pose it as a quiz-check even though he's "attempting the discovery" — gradable-and-Socratic is normal, not a contradiction.
   - Diagram the mechanism wherever it helps: mermaid flowcharts, state transitions, data layouts. Math in LaTeX (see Formatting).
3. **Connect.** Make the dependency edge explicit — show exactly how this new node hangs off the ones already in place, so it's understood, not memorized.
4. **Quiz-check.** Confirm the node actually landed with a quiz-check — this applies to foundations just as much as derived steps. An unconfirmed unconditional truth is exactly as dangerous as an unconfirmed derived fact: if he misses it, that node isn't solid, so stop, diagnose, and fix it (repair, re-explain, re-test) before building anything on top of it.
5. **Persist the node.** `edit` the two files: live-append the teaching and the Q&A to the lesson note, and add/adjust the proposition entry in the Learner-Graph (status, what it rests on, provenance; log any miss verbatim).

Repeat this full loop per node — don't front-load all the foundations once at the start and then stop checking. Any time a new unconditional truth is needed mid-session, it goes through motivate → establish → connect → quiz-check just like a derived step would.

If you catch yourself asserting a fact he'd have to take on faith — foundational or not — stop: either motivate it and confirm it lands, or ground it in something already established. Unmotivated, unconfirmed facts don't lock in — that's the whole point.

## The Learner-Graph — `<Topic-Slug> Learner-Graph.md`

One note per topic in `04-Archives/Learn/Lessons/`. This is the chat-native port of LearnHarness's persistent knowledge graph: what was actually taught, how it hangs together, and how his answers have gone; the next session resumes at the frontier instead of re-probing from zero, and practice rounds have something to draw from. Wiki-links keep it navigable in Obsidian.

Skeleton (copy at creation, fill per node thereafter):

```markdown
---
name: <Topic-Slug> Learner-Graph
tags: ["#type/doc", "#domain/ai-learning", "#status/active"]
---
# <Topic-Slug> Learner-Graph

Learning record for <topic>. Updated at every landed node (Phase 3 step 5) and read at every resume (Phase 0). Statuses are the floor/ceiling record; hygiene rules at the bottom are what makes this note mean anything.

## Statuses
- `#taught`: stated in a lesson, never confirmed by an answer.
- `#verified`: passed at least one quiz-check; date in its provenance.
- `#repaired`: a misconception was found and re-landed; re-test FIRST next session.
A regression in a later session or practice round sends the node back to `#repaired` with a dated log entry.

## Propositions
- **P1.** <the claim, stated the way it was taught to him> `#verified`
  - rests on: (nothing: root) or P2 + P3
  - sources: [[<Topic-Slug> Lesson]] (2026-10-25)

## Reasoning chains
Premises JOINTLY imply the conclusion; any one alone is not enough.
- P5 = P1 + P2 : <one line on how these produce that>

## Misconception log (his words, verbatim)
- 2026-10-25, P3: picked <label> "because <his exact words>" → repair: <what dislodged it, how the repair confirmed>

## Hygiene
- Propositions record taught material, not mastery. Presence is not understanding; absence is not ignorance; extraction gaps are normal.
- Only `#verified` counts as solid ground. Everything else is a dated hypothesis about him.
- Confidence is self-reported, never a score; missing confidence is not zero.
- One response is evidence, not a verdict on the person; interpretations go by date, not by permanent judgment.
```

Reuse rules:

- **Same topic, new session**: append new propositions; re-runs re-verify (pass → keep `#verified` with the new date; fail → `#repaired` + log entry).
- **Cross-topic lean**: when this topic's teaching rests on a proposition from another topic's graph, copy the claim line into this graph with its own id and cite the other graph in `sources` (dates included). Don't merge blindly.
- **Corrections**: never quietly rewrite a taught proposition; a correction is a new status (`#repaired`) plus a dated log entry, so the record stays honest about what he held and when.

## Phase 4 — Persist, flashcards, practice

1. **Lesson note.** By the end of the session the note is complete: DAG, per-node section, diagnostics, visuals. Obsidian renders mermaid, so diagrams embed inline; standalone SVGs may live beside the note when a lesson genuinely needs one.
2. **Flashcards.** Automatically generate rich, high-yield flashcards at the bottom of the lesson note using Obsidian Spaced Repetition syntax: `Question #card` single-liners, two-sided `Q::A` cards, and `==cloze==` deletions. These are the spaced-repetition backbone.
3. **Practice rounds** (straight after a lesson, or any chat where he asks to practice; never self-started during teaching):
   - **Scope by consent.** He names the topic(s) or says e.g. "the graphs we've done"; read only the approved Learner-Graph notes.
   - **Retrieval without naming.** Pose problems where the right knowledge has to *come to mind* without you naming the concept first: describe a situation that needs it, let him surface and apply it. Vary the surface every round; a proposition never re-tested in the same skin it was taught.
   - **Adapt to his reasoning.** On a miss: generic hint → pointed hint → rebuild the chain together from its premises. His explanation fields steer what comes next.
   - **Draw from the graph.** Prioritize `#repaired` and never-practiced `#verified` nodes; the misconception log supplies ready-made claim-vs-misconception pairs for quiz distractors.
   - **Close the loop.** After the round: passes move nodes toward `#verified` (dated), misses back to `#repaired` with the verbatim log entry; new flashcards only when a round exposed a real recurring gap.
   - The Obsidian SR plugin handles spacing on its own schedule; in-chat practice rounds are for application and transfer. He pulls which, when.

## Formatting — math renders as LaTeX

Everything written in a session is rendered through Obsidian chat and lesson notes, which render LaTeX natively. So whenever math notation is involved — explanations, questions, quiz options and post-answer explanations, anything — write it in LaTeX instead of plain-text approximations:

- Inline math: `$f(x)$`
- Centered display math: `$$` fenced on its own lines, e.g. `$$\n f(x) \n$$`

If LaTeX can be used, it should be. Write $f(x) = x^2$, not `f(x) = x^2`.

## See also

[[04-Archives/Learn/Lessons/README|Lessons index]] · [[04-Archives/Learn/Docs/Practice-and-Knowledge-Graph|Practice & Knowledge Graph (what came from LearnHarness)]]
