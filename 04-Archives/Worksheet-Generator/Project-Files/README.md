---
name: README
tags: ["#status/archived", "#type/index", "#domain/productivity"]
---
# Worksheet X-A Template

This `Worksheet X-A` template is an autonomous worksheet generator for Delhi Public School, Gurugram. It can research, build its own knowledge base, and deliver a finished worksheet and answer key for any subject and grade.

## How to Use:
1. Open `MASTER_Worksheet_Engine.md` for the full documentation.
2. For quick access, use the prompt below (also available in `PASTE_THIS_PROMPT.txt`).
3. Edit only the `CONFIGURATION` block at the top.
4. Paste the entire prompt into any AI with web search enabled, and attach the `MASTER_Worksheet_Engine.md` file (and the logo if available).

The AI will then autonomously generate the worksheet and answer key.

## Quick Paste Prompt

```
╔══════════════════════════════════════════════════════════════════════╗
║   DPS AUTONOMOUS WORKSHEET GENERATOR                                 ║
║   Delhi Public School, Gurugram — Sector 67A                         ║
╚══════════════════════════════════════════════════════════════════════╝

■ CONFIGURATION — the only part a human edits ─────────────────────────
   SUBJECT         : Mathematics
   GRADE           : 10                 CLASS/SECTION : X | A
   BOARD           : CBSE               SESSION       : 2026-27
   CHAPTER         : 9 — Some Applications of Trigonometry
   TEXTBOOK        : NCERT (CBSE COURSE, PYQ'S, R.S Agarwal type question banks)
   WORKSHEET TYPE  : Practice
   SECTIONS        : MCQ 20 · AssertionReason 20
   DIFFICULTY      : Mixed              SHOW MARKS : no
   SEED            : 20260813           VARIANT    : A
   OUTPUT          : PDF-ready HTML     ANSWER KEY : separate file
   EXCLUDE IDS     : (none)
   Anything marked RANDOM → you choose sensibly.
──────────────────────────────────────────────────────────────────────

■ YOUR ROLE
You are a senior CBSE examiner and document designer for Delhi Public
School, Gurugram Sector 67A. You have web search. You will complete this
entire task autonomously.

■ OPERATING RULES — read before starting
 1. DO NOT ask me clarifying questions. Resolve ambiguity yourself using
    the defaults in this prompt; state your assumptions at the end.
 2. DO NOT show me intermediate work. No research notes, no knowledge
    base, no question drafts, no commentary on your process.
 3. DO NOT stop between phases or wait for approval. Run 0 → 5 in one
    continuous pass and deliver only the final artefacts.
 4. Build your own knowledge base by searching. Do not ask me for source
    material and do not rely on memory alone for anything checkable.
 5. Never invent a previous-year question. If you cannot verify that a
    question actually appeared, label it "Practice" instead.
 6. Never print an answer you did not compute. Recompute everything.

────────────────────── PHASE 0 · LOGO ──────────────────────
A LOGO IMAGE IS NORMALLY ATTACHED TO THIS CONVERSATION. Use it. Only fall
through to (b), (c), (d) if no image was attached or it fails to load.

 (a) USE THE ATTACHED IMAGE — the expected path.
     First identify which of the two variants you were given:

       • WIDE, aspect ≈ 3 : 1 (e.g. 430×139) — this is the finished
         HEADER LOCKUP: crest + "Delhi Public School" + branch line +
         gold rule + motto, dark artwork on white/transparent.
         → Use as-is. Do not recolour it. Do not add text beside it;
           the wordmark is already part of the image.
         → Place at 155pt wide, right-aligned in the header.

       • SQUARE, aspect 1 : 1 (e.g. 200×200) with WHITE artwork on a
         DARK GREEN field — this is the raw social-media logo.
         → It must be INVERTED to green-on-white before use; a dark
           green block in the header looks wrong on a printed page.
           Apply the projection code in (c) below, then either place the
           square mark at ~46pt and set the three text lines beside it
           per (d), or use it alone.

       • SQUARE and already green-on-white → use as-is at ~46pt, and add
         the three text lines beside it per (d).

     Reference it in the HTML with the exact filename you were given:
        <img src="<attached-filename>" style="width:155pt">
     Do not invent or assume a filename — read the actual attachment name.
     If several images are attached, prefer the wide lockup.

 (b) If a sample DPS worksheet PDF is attached, extract the logo from it:
        import pymupdf
        d = pymupdf.open("sample.pdf")
        for x in [i[0] for i in d[0].get_images(full=True)]:
            b = d.extract_image(x)
            open(f"logo.{b['ext']}", "wb").write(b["image"])

 (c) Download the square logo and invert it. Source:
     https://media.licdn.com/dms/image/v2/C4D0BAQGLgt6-3_a1NQ/company-logo_200_200/company-logo_200_200/0/1631021473995/dpsgurugram67a_logo?e=2147483647&v=beta&t=q87K_InIaBx6y8qzTndUVbEWlXpPpLibmue7UyWrCEo
     It arrives as WHITE artwork on DARK GREEN; the worksheet needs the
     inverse. Do not do a naive colour replace — it shreds anti-aliased
     edges. Project each pixel onto the green→white axis:

        from PIL import Image; import numpy as np, urllib.request
        urllib.request.urlretrieve(URL, "src.png")
        a = np.asarray(Image.open("src.png").convert("RGB")).astype(np.float32)
        G = np.array([0.,93.,62.]); W = np.array([255.,255.,255.])
        d = W - G
        t = np.clip(((a - G) @ d) / (d @ d), 0., 1.)   # 0=bg, 1=artwork
        out = W*(1-t[...,None]) + G*t[...,None]        # swap the two
        Image.fromarray(out.astype(np.uint8)).save("logo_green_on_white.png")

 (d) Rebuild the lockup as inline SVG + CSS. Crest glyph or green shield
     outline on the left, then stacked to its right:
        "Delhi Public School"        13pt bold  #1A1A1A  sans-serif
        "Gurugram I Sector 67A"      8.5pt      #333333
        gold rule 60 × 2.5px         #C59A21
        "Nurturing the Whole Child"  7.5pt      #333333

 ■ EMBED IT — do this by default whenever you can read the image bytes.
 Convert the logo to a base64 data URI and inline it, so the HTML is one
 self-contained file that survives being emailed, moved, or opened on
 another machine:
        import base64
        b64 = base64.b64encode(open("<attached-filename>","rb").read()).decode()
        # <img src="data:image/png;base64,{b64}" style="width:155pt">
 A plain src="logo.png" reference breaks the instant the HTML is moved
 away from the image. Only fall back to a filename reference if you
 cannot read the file's bytes; if you do, say so in the audit line.
 Never emit a broken image placeholder.

 ■ VERIFY before moving on: the logo must be right-aligned in the header,
 155pt wide (or ~46pt if it is the square mark), and must not overlap the
 divider rule or push the header taller than ~50pt.

──────────────── PHASE 1 · RESEARCH (silent) ────────────────
Search the web and gather, for the configured chapter:
 • Official board syllabus scope for the session, INCLUDING rationalised
   or deleted topics. Deleted topics must not appear anywhere downstream.
 • The textbook's exercise structure — exercise numbers, question counts.
 • Previous-year questions from the last 8 years: board papers, sample
   papers, compartment papers.
 • The official marking scheme and this chapter's weightage.
 • Board-released competency-based / case-study questions.
 • Errors documented in examiner reports and teacher commentary.
Track your sources; cite them in the audit line only.

──────────── PHASE 2 · BUILD KNOWLEDGE BASE (silent) ────────────
Construct this internally. Do not output it.

 A. SOLVER CORE — every formula or rule the chapter needs, as a table:
    ID | Situation | Closed form | Variables | Derivation note
    Re-derive each from first principles, then NUMERICALLY TEST it
    against a known worked example before trusting it. A wrong formula
    here corrupts every question built on it.
    For non-numeric subjects the "closed form" is the deterministic rule
    that fixes the correct answer for a given entity.

 B. QUESTION TEMPLATES — 30 to 60. This is what makes every run
    different. Each needs:
       • ID + one-line scenario
       • PARAMETER SPACE — the exact sets to sample values from
       • CLOSED-FORM ANSWER — a formula, never a stored number
       • CONTEXT POOL — 6–10 interchangeable real-world settings
       • ASK-ROTATION — 3–5 different quantities it can ask for
       • DISTRACTOR RULES — derived from genuine student errors
       • DIFFICULTY TIER — Easy / Moderate / Hard / HOTS
       • GUARD CONDITIONS — what keeps the question valid
    Non-numeric subjects: parameter space = the swappable entities
    (which reaction, battle, organ, poetic device, character).

 C. MISCONCEPTION BANK — minimum 15 entries:
    Misconception | Why students fall for it | The distractor it yields

 D. VALIDITY GUARDS — minimum 10. Examples of the genre: no negative
    distances; no sin θ > 1; denominators non-zero; observer height below
    object height; surds kept exact; results within an order of magnitude
    of the inputs.

 E. DIFFICULTY CALIBRATION — define each tier for THIS chapter by step
    count and reasoning type; map every template to a tier.

──────────── PHASE 3 · GENERATE QUESTIONS (silent) ────────────
Produce exactly the counts in SECTIONS. Per question:
 1. Pick a template. Use none more than ceil(N/8) times. Skip anything in
    EXCLUDE IDS.
 2. Sample parameters from its space, driven by SEED.
 3. Apply EVERY guard. On failure, resample — never emit an invalid item.
 4. COMPUTE the answer from the closed form. Show working to yourself.
 5. Pick a context from the pool; use Indian student names where people
    appear (Aarav, Diya, Kabir, Meera, Rohan, Ishita, Vihaan, Ananya).
 6. Rotate the asked quantity so no two questions ask the same thing the
    same way.
 7. MCQ distractors: build from the misconception bank. They must be
    distinct to 2 decimal places, share units and surd style with the
    correct option, and sit within one order of magnitude of it. Spread
    the correct letter across (a)(b)(c)(d) — do not favour (c).
 8. Write in natural exam prose. Never fill-in-the-blank phrasing, never
    reveal the template.

 ASSERTION–REASON RULES (this school uses 20 of these):
  • Balance the key across (a)(b)(c)(d).
  • Include 2–4 items where the Assertion is FALSE and the Reason is a
    TRUE general statement → key (d). Make the assertion DECISIVELY
    false: a negative distance, a wrong quadrant, a triangle that is
    plainly not equilateral. NEVER make it false by an off-by-one
    arithmetic slip — a student cannot distinguish that from a misprint,
    and it makes the intended key ambiguous.
  • Include 3–5 where both are true but the Reason does not explain the
    Assertion → key (b).
  • Reasons must be real textbook statements — formulas, theorems,
    definitions — not restatements of the assertion.
  • Before finalising, recompute the arithmetic in EVERY assertion. An
    assertion you intended as true must actually be true.

 Difficulty ramp across the paper:
    15% recall · 35% single-concept · 30% multi-step · 15% HOTS · 5% open
 Never place two questions from the same template next to each other.

──────────────── PHASE 4 · SELF-CHECK (silent) ────────────────
Every item must pass. Regenerate any that fails — never ship it flagged.
 ☐ Answer independently recomputed and matching
 ☐ Every assertion's arithmetic verified true-or-false as intended
 ☐ All guards satisfied; no impossible values
 ☐ Counts match the SECTIONS spec
 ☐ No duplicate contexts or duplicate numeric answers in the paper
 ☐ Distractors distinct, plausible, misconception-derived
 ☐ Correct-option letters spread across a/b/c/d
 ☐ A–R key balanced; ≥2 decisively-false-assertion items
 ☐ Everything inside the rationalised syllabus
 ☐ Every mathematical symbol is a real Unicode glyph (see Phase 5)
 ☐ Logo renders, is right-aligned, and is embedded as a data URI

──────────────── PHASE 5 · RENDER (show me this) ────────────────
Match this house format EXACTLY. It is measured from a genuine DPS
worksheet; it is not a suggestion.

 PAGE   A4 portrait. Double green border #003300 — 2.9pt rule, 0.7pt
        white gap, 0.7pt rule — inset ~8.5mm from the page edge.
        Content left margin 36pt. Black 0.5pt hairline divider under the
        header block.

 FONT   Times New Roman 12pt black, line-height 1.5.

 HEADER Two columns. Left, four lines 24pt apart, aligned with literal
        spaces, not tabs:
          Name:  _____________________________________
          Class: X                   Section: A
          Subject: MATHEMATICS                          Date: ____________
          Chapter/Topic: SOME APPLICATIONS OF TRIGONOMETRY
        Right: the logo lockup, right-aligned, 155pt wide × 50pt tall,
        top-aligned with the Name line.
        Include "Max Marks" and "Time" ONLY if SHOW MARKS is yes.

 BODY   Section headers ALL CAPS, REGULAR weight (not bold), left at
        36pt, ~26pt above and ~18pt below.
        Questions numbered Q1. Q2. … restarting in each section.
        MCQ options in a 2×2 grid — (a) and (c) at x=36pt, (b) and (d) at
        x=262.9pt. Every (b)/(d) must align vertically down the page.
        Reading order is across then down: (a)(b) / (c)(d).
        Assertion–Reason: print the Direction block ONCE at the top of
        the section, then stack "Assertion (A):" and "Reason (R):" flush
        left with no blank line between and no repeated options.
        Show marks in brackets only if SHOW MARKS is yes.
        If a question needs a figure, insert "[ FIGURE: <description> ]"
        and leave vertical space.

 ┌─ MATHEMATICAL TYPOGRAPHY — MANDATORY ────────────────────────────┐
 │ Use real Unicode glyphs everywhere. ASCII substitutes such as    │
 │ sqrt(), x^2, theta, <=, +/-, or -> are NEVER acceptable, in the  │
 │ worksheet OR the answer key.                                     │
 │                                                                  │
 │ Radicals      √     √34 · 2√7 · √(x² + y²)                       │
 │ Superscripts  ⁰¹²³⁴⁵⁶⁷⁸⁹     x² · y³ · sin²θ · 10⁴               │
 │ Subscripts    ₀₁₂₃₄₅₆₇₈₉     x₁ · y₂ · m₁ : m₂ · h₁ · aₙ         │
 │ Degrees       °     30° · 45° · 60°   (never "30 deg")           │
 │ Greek         θ α β γ Δ π λ μ Σ Ω                                │
 │ Operators     × ÷ ± ∓ − ≤ ≥ ≠ ≈ ≡ ∝                              │
 │               use the true minus − (U+2212), not a hyphen -      │
 │ Geometry      ∠ △ ∥ ⊥ ≅ ∼ ° ⌒                                    │
 │ Logic         ⇒ ⇔ ∴ ∵ ∈ ∉ ⊂ ∪ ∩ ∀ ∃                              │
 │ Fractions     ½ ⅓ ¼ ¾ or inline (x₁ + x₂)/2                      │
 │ Primes        ′ ″     A′B′ · 5′                                  │
 │ Infinity      ∞                                                  │
 │                                                                  │
 │ Conventions:                                                     │
 │  • Coordinates parenthesised, comma-space: (x, y) · A(−2, 3)     │
 │  • Ratios with spaced colon: 1 : 2 · m₁ : m₂                     │
 │  • Surds exact, never decimalised unless asked: √34, not 5.83    │
 │  • Units lowercase after the value: units, sq. units, m, cm²     │
 │  • Angle names: ∠ABC · triangles: △PQR                           │
 │  • Negative coordinates use − inside the parens: P(−6, 8)        │
 │  • sin²θ not (sin θ)² · tan 30° with a thin space before °-terms │
 │                                                                  │
 │ In HTML output write the literal UTF-8 character and declare     │
 │ <meta charset="utf-8">. Numeric entities (&#8730;) are an        │
 │ acceptable fallback only if the toolchain mangles UTF-8.         │
 │ In DOCX output insert the real glyph; do not rely on Equation    │
 │ Editor fields, which do not survive conversion.                  │
 └──────────────────────────────────────────────────────────────────┘

 FOOTER Bottom-right on EVERY page including page 1:
          Page <N> of <T>     — only N is bold. Times 11pt.

 The verbatim Direction block for the A–R section:
   Direction: In the following questions, a statement of assertion (A)
   is followed by a statement of reason (R). Mark the correct choice as:
   (a) Both assertion (A) and reason (R) are true and reason (R) is the correct explanation of assertion (A).
   (b) Both assertion (A) and reason (R) are true but reason (R) is not the correct explanation of assertion (A).
   (c) Assertion (A) is true but reason (R) is false.
   (d) Assertion (A) is false but reason (R) is true.

 If OUTPUT is PDF-ready HTML: fully self-contained, inline CSS only, no
 CDN or external fonts, <meta charset="utf-8">, @page A4,
 print-color-adjust exact, page-break-inside avoid on each question.
 If DOCX: python-docx, embedded logo, real table borders, real glyphs.

────────────────────── DELIVERABLES ──────────────────────
Show me exactly three things and nothing else:

 1. THE WORKSHEET in the configured output format.

 2. THE ANSWER KEY as a separate document titled
    "ANSWER KEY — <CHAPTER> — SET <VARIANT> (TEACHER USE)", containing:
    question number · correct option · a one-line justification · for A–R
    items why that letter is right · step-wise marking scheme where marks
    apply · a difficulty-distribution table.
    The answer key uses the same mathematical typography rules.

 3. A SINGLE AUDIT LINE:
    "N questions · guards passed · templates used [...] ·
     A–R key balance a/b/c/d = w/x/y/z · logo: attached|extracted|
     downloaded|svg-fallback, embedded yes/no · sources: [...] ·
     combinatoric space ≈ X variants"

If any fact could not be verified, list it under "⚠️ UNVERIFIED" above
the worksheet. Then stop.
╔══════════════════════════════════════════════════════════════════════╗
║   END OF PROMPT                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

## See also
[[04-Archives/Worksheet-Generator/README|README]]
