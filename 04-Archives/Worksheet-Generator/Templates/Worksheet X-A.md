---
name: Worksheet X-A
tags: ["#status/archived", "#type/template", "#domain/productivity"]
---
&lt;div align="center"&gt;

# DPS MASTER WORKSHEET ENGINE
### One prompt. The AI researches, builds its own knowledge base, and delivers a finished worksheet.
**Delhi Public School, Gurugram · Sector 67A** · *Nurturing the Whole Child*

`v4.0` · Autonomous · Any subject · Any grade · Different every run

&lt;/div&gt;

---

## HOW TO USE

1. **Download the logo** from `assets/dps_logo_header_lockup.png` — see §2. One-time.
2. Open **§1 — THE MASTER PROMPT**. Edit only the `CONFIGURATION` block at the top (12 lines).
3. Paste the prompt into any AI **with web search enabled**, and attach **two files**: this `.md` and the logo `.png`.

The AI then researches the chapter itself, builds its own knowledge base, writes the questions, and renders the worksheet. It does not ask you anything in between. You see only the finished worksheet and answer key.

Everything after §1 is reference the prompt relies on. You don't need to read it.

---

# ⭐ §1 — THE MASTER PROMPT

&gt; Copy everything between the `╔` and `╝` rules. It is self-contained and works even if the attachments are stripped.

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
   TEXTBOOK        : NCERT
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
        &lt;img src="&lt;attached-filename&gt;" style="width:155pt"&gt;
     Do not invent or assume a filename — read the actual attachment name.
     If several images are attached, prefer the wide lockup.

 (b) If a sample DPS worksheet PDF is attached, extract the logo from it:
        import pymupdf
        d = pymupdf.open("sample.pdf")
        for x in [i[0] for i in d[0].get_images(full=True)]:
            b = d.extract_image(x)
            open(f"logo.{b['ext']}", "wb").write(b["image"])

 (c) Download the square logo and invert it. Source:
     https://media.licdn.com/dms/image/v2/C4D0BAQGLgt6-3_a1NQ/company-logo_200_200/company-logo_200_200/0/1631021473995/dpsgurugram67a_logo?e=2147483647&amp;v=beta&amp;t=q87K_InIaBx6y8qzTndUVbEWlXpPpLibmue7UyWrCEo
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
        b64 = base64.b64encode(open("&lt;attached-filename&gt;","rb").read()).decode()
        # &lt;img src="data:image/png;base64,{b64}" style="width:155pt"&gt;
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
    distances; no sin θ &gt; 1; denominators non-zero; observer height below
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
        If a question needs a figure, insert "[ FIGURE: &lt;description&gt; ]"
        and leave vertical space.

 ┌─ MATHEMATICAL TYPOGRAPHY — MANDATORY ────────────────────────────┐
 │ Use real Unicode glyphs everywhere. ASCII substitutes such as    │
 │ sqrt(), x^2, theta, &lt;=, +/-, or -&gt; are NEVER acceptable, in the  │
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
 │ &lt;meta charset="utf-8"&gt;. Numeric entities (&amp;#8730;) are an        │
 │ acceptable fallback only if the toolchain mangles UTF-8.         │
 │ In DOCX output insert the real glyph; do not rely on Equation    │
 │ Editor fields, which do not survive conversion.                  │
 └──────────────────────────────────────────────────────────────────┘

 FOOTER Bottom-right on EVERY page including page 1:
          Page &lt;N&gt; of &lt;T&gt;     — only N is bold. Times 11pt.

 The verbatim Direction block for the A–R section:
   Direction: In the following questions, a statement of assertion (A)
   is followed by a statement of reason (R). Mark the correct choice as:
   (a) Both assertion (A) and reason (R) are true and reason (R) is the correct explanation of assertion (A).
   (b) Both assertion (A) and reason (R) are true but reason (R) is not the correct explanation of assertion (A).
   (c) Assertion (A) is true but reason (R) is false.
   (d) Assertion (A) is false but reason (R) is true.

 If OUTPUT is PDF-ready HTML: fully self-contained, inline CSS only, no
 CDN or external fonts, &lt;meta charset="utf-8"&gt;, @page A4,
 print-color-adjust exact, page-break-inside avoid on each question.
 If DOCX: python-docx, embedded logo, real table borders, real glyphs.

────────────────────── DELIVERABLES ──────────────────────
Show me exactly three things and nothing else:

 1. THE WORKSHEET in the configured output format.

 2. THE ANSWER KEY as a separate document titled
    "ANSWER KEY — &lt;CHAPTER&gt; — SET &lt;VARIANT&gt; (TEACHER USE)", containing:
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

---

# 📥 §2 — THE LOGO: WHAT TO ATTACH

**Attach the logo image to the chat along with this file.** That is the intended workflow and gives the best result — Phase 0(a) picks it up automatically.

### Step 1 — Download the logo from this workspace
In the workspace file browser, open `assets/` and download:

```
dps_logo_header_lockup.png        430 × 139 px   ← attach this one
dps_logo_header_lockup_1290.png   1290 × 417 px  ← same artwork, print-res
```

Either works. The wide one is the finished lockup — crest, "Delhi Public School", branch line, gold rule, and motto already composed together — so the AI drops it straight into the header with no assembly.

### Step 2 — Attach both files when you paste the prompt
- `DPS_MASTER_Worksheet_Engine.md` (this file)
- `dps_logo_header_lockup.png` (the logo)

### Step 3 — Ask for it embedded
The prompt already instructs the AI to inline the logo as a base64 data URI by default, so the returned HTML is **one self-contained file**. That matters: a worksheet that references `logo.png` externally will show a broken image the moment you email it or move it to another folder. If you ever get a worksheet with a missing logo, that's the cause — reply:

&gt; Embed the logo as a base64 data URI so the HTML is fully self-contained.

### Which file you attach — and what the AI does with it

|| What you attach | What Phase 0 does |
||---|---|
|| **Wide lockup** (≈3:1, dark on white) | Uses it as-is at 155pt. **Recommended.** |
|| **Square logo** (1:1, white on dark green) | Inverts it to green-on-white first, then places the mark at ~46pt and sets the three text lines beside it |
|| **Square, already green-on-white** | Places at ~46pt, adds the text lines beside it |
|| **A DPS worksheet PDF** | Extracts the embedded logo straight out of the PDF |
|| **Nothing** | Downloads from the public URL and inverts it; if that fails, rebuilds the lockup in SVG |

The prompt reads the actual attachment filename rather than assuming one, and prefers the wide lockup if you attach several images.

### If you attach nothing at all
It still works — you always get a branded header. The fallback URL is:

```
https://media.licdn.com/dms/image/v2/C4D0BAQGLgt6-3_a1NQ/company-logo_200_200/company-logo_200_200/0/1631021473995/dpsgurugram67a_logo?e=2147483647&amp;v=beta&amp;t=q87K_InIaBx6y8qzTndUVbEWlXpPpLibmue7UyWrCEo
```

---

# §3 — CONFIGURATION PRESETS

Swap the `CONFIGURATION` block for one of these.

**Trigonometry practice, house format**
```
SUBJECT Mathematics · GRADE 10 · CLASS/SECTION X | A · BOARD CBSE
CHAPTER 9 — Some Applications of Trigonometry · TEXTBOOK NCERT
WORKSHEET TYPE Practice · SECTIONS MCQ 20 · AssertionReason 20
DIFFICULTY Mixed · SHOW MARKS no · SEED 20260813 · VARIANT A
OUTPUT PDF-ready HTML · ANSWER KEY separate file
```

**Hard trigonometry pre-board, full exam shape**
```
SUBJECT Mathematics · GRADE 10 · CLASS/SECTION X | C · BOARD CBSE
CHAPTER 8+9 — Introduction to Trigonometry + Some Applications
TEXTBOOK NCERT · WORKSHEET TYPE Pre-Board
SECTIONS MCQ 10 · AssertionReason 4 · VSA 5 · SA 4 · LA 3 · Case 2
DIFFICULTY Hard · SHOW MARKS yes · TOTAL MARKS 40 · DURATION 1.5 hr
SEED RANDOM · VARIANT A · OUTPUT PDF-ready HTML · ANSWER KEY separate file
```

**A different subject entirely — the engine is subject-agnostic**
```
SUBJECT Science · GRADE 10 · CLASS/SECTION X | B · BOARD CBSE
CHAPTER 6 — Life Processes · TEXTBOOK NCERT
WORKSHEET TYPE Unit Test
SECTIONS MCQ 15 · AssertionReason 8 · VSA 5 · Case 2
DIFFICULTY Mixed · SHOW MARKS yes · TOTAL MARKS 40 · DURATION 1.5 hr
SEED RANDOM · VARIANT A · OUTPUT DOCX · ANSWER KEY separate file
```
Phase 1 researches Life Processes from scratch; in Phase 2 the "parameter space" becomes the swappable set of organs, enzymes and processes, and the "closed form" becomes the rule fixing the right answer for each.

**Four parallel sets for one class**

Run the prompt four times with `VARIANT` A/B/C/D and `SEED` 1001–1004, everything else identical, and append:

&gt; All four sets must use the SAME template ids in the SAME order and the SAME structure, but DIFFERENT sampled parameters and DIFFERENT contexts. Verify the mean step-count per question is within ±0.5 across the four sets. Print the comparison table.

Keep a cumulative `EXCLUDE IDS` list for a whole term without repeats.

---

# §4 — CONFIGURATION REFERENCE

```
SUBJECT        Mathematics | Science | Physics | Chemistry | Biology |
               Social Science | English | Computer Science | Economics
GRADE          6 … 12
BOARD          CBSE | ICSE | IB | State Board
SECTIONS       any mix of: MCQ · AssertionReason · VSA · SA · LA · Case
               house default → MCQ 20 · AssertionReason 20
WORKSHEET TYPE Practice | Revision | Pre-Board | Unit Test | Remedial |
               Enrichment | Diagnostic | Holiday Homework
DIFFICULTY     Easy | Moderate | Hard | HOTS | Mixed | RANDOM
SHOW MARKS     no  ← house default; the reference worksheet omits marks
               yes → also set TOTAL MARKS and DURATION
SEED           any integer, or RANDOM. Same seed ⇒ identical paper.
VARIANT        A | B | C | D
OUTPUT         PDF-ready HTML | DOCX | Markdown | JSON
ANSWER KEY     separate file | separate page | inline | none
CONTEXT FLAVOUR Indian urban | rural | sports | space | environment |
               monuments | festivals | technology | daily life | RANDOM
```

---

# §5 — HOUSE FORMAT: THE MEASURED SPECIFICATION

Measured from the reference worksheet `GRADE X COORDINATE GEOMETRY.pdf` by reading fonts, coordinates and colours directly out of the file. **That worksheet is the format sample — this layout applies to every chapter and every subject**, not just coordinate geometry.

### Page geometry (points; A4 = 595.2 × 841.9)
```
Outer green border : x 24.0 → 571.4,  y 24.0 → 818.2   (~8.5mm inset)
Border style       : DOUBLE — 2.9pt green / 0.7pt white / 0.7pt green
Border colour      : #003300
Text left margin   : x = 36.0pt
Text right limit   : x = 559.0pt
Header divider     : black 0.5pt hairline at y = 150.0, x 28.5 → 567.8
Footer baseline    : y ≈ 795.4, right-aligned, ends x ≈ 559.8
```

### Typography
```
Body   : Times New Roman 12pt black
Footer : Times New Roman 11pt, page number BOLD
Leading: ~1.5 (question baselines 26–28pt apart)
```

### Header
Left column at x = 36.0, four lines at y ≈ 48.8 / 72.8 / 96.6 / 120.4 (24pt apart), aligned with literal spaces, not tabs. Name rule ≈ 37 underscores, Date rule ≈ 12.

Right column: the logo lockup, bbox `[404.8, 33.9, 559.8, 84.1]` → **155 × 50pt**, right-aligned.

### Section headers
```
ALL CAPS, REGULAR weight (not bold), left at 36.0pt
~26pt above, ~18pt below. No fill, no underline, no numbering.
e.g.  MULTIPLE CHOICE QUESTIONS     ASSERTION-REASON QUESTIONS
```

### MCQ option grid
```
Column 1  x = 36.0    → (a) and (c)
Column 2  x = 262.9   → (b) and (d)
Row pitch ~22–26pt.  Reading order across then down.
```
Every (b)/(d) aligns vertically across all questions on the page.

### Assertion–Reason
Direction block printed once at the top of the section. Each item is `Q&lt;n&gt;. Assertion (A): …` then `Reason (R): …` stacked, both flush left at 36pt, no blank line between, no repeated options. ~26pt between items.

### Footer
```
Bottom-right, y ≈ 795.4.  "Page &lt;N&gt; of &lt;T&gt;", only N bold. Times 11pt.
On every page including page 1.
```

### Colour palette
|| Role | Hex |
||---|---|
|| Page border | `#003300` |
|| Crest green | `#1B7A4B` |
|| Brand green (square logo) | `#005D3E` |
|| Gold separator in lockup | `#C59A21` |
|| Body text / divider | `#000000` |

### Content-style conventions
20 MCQs + 20 A–R, **no marks printed**, no "Max Marks" or "Time" — practice, not a test. No answer key in the student copy. Difficulty ramps from recall to composite reasoning. The A–R set deliberately includes decisively false assertions to test whether students actually check the claim.

---

# §6 — MATHEMATICAL SYMBOL REFERENCE

Every glyph below was verified for correct Unicode codepoint. Copy directly from this table.

### Core set
|| Need | Glyph | Codepoint | HTML entity |
||---|---|---|---|
|| Radical | `√` | U+221A | `&amp;radic;` |
|| Superscript 2, 3 | `²` `³` | U+00B2, U+00B3 | `&amp;sup2;` `&amp;sup3;` |
|| Superscripts 0–9 | `⁰¹²³⁴⁵⁶⁷⁸⁹` | U+2070… | `&amp;#x2070;`… |
|| Subscripts 0–9 | `₀₁₂₃₄₅₆₇₈₉` | U+2080… | `&amp;#x2081;`… |
|| Degree | `°` | U+00B0 | `&amp;deg;` |
|| Minus (true) | `−` | U+2212 | `&amp;minus;` |
|| Plus-minus | `±` | U+00B1 | `&amp;plusmn;` |
|| Multiply | `×` | U+00D7 | `&amp;times;` |
|| Divide | `÷` | U+00F7 | `&amp;divide;` |
|| Approx | `≈` | U+2248 | `&amp;asymp;` |
|| Not equal | `≠` | U+2260 | `&amp;ne;` |
|| ≤ ≥ | `≤` `≥` | U+2264/5 | `&amp;le;` `&amp;ge;` |

### Greek
|| `θ` U+03B8 | `α` U+03B1 | `β` U+03B2 | `γ` U+03B3 | `Δ` U+0394 | `π` U+03C0 | `λ` U+03BB | `μ` U+03BC | `Σ` U+03A3 | `Ω` U+03A9 |
||---|---|---|---|---|---|---|---|---|---|

### Geometry &amp; logic
|| `∠` angle U+2220 | `△` triangle U+25B3 | `∥` parallel U+2225 | `⊥` perp U+22A5 | `≅` congruent U+2245 | `∼` similar U+223C |
||---|---|---|---|---|---|
|| `⇒` implies U+21D2 | `∴` therefore U+2234 | `∵` because U+2235 | `∈` element U+2208 | `∞` infinity U+221E | `′ ″` primes U+2032/3 |

### Worked examples of correct output
```
✅  The distance of P(−6, 8) from the origin is 10 units.
❌  The distance of P(-6, 8) from the origin is 10 units.        (hyphen, not minus)

✅  d = √((x₂ − x₁)² + (y₂ − y₁)²)
❌  d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

✅  In △ABC, ∠ABC = 90° and sin²θ + cos²θ = 1
❌  In triangle ABC, angle ABC = 90 deg and sin^2(theta) + cos^2(theta) = 1

✅  The ratio is 1 : 2, so p = ±4 and the area is ½ × b × h
❌  The ratio is 1:2, so p = +/-4 and the area is 1/2 * b * h

✅  h = f·tanA/(tanB − tanA),  A(−2, 3),  2√7 units,  30°
❌  h = f*tanA/(tanB - tanA),  A(-2, 3),  2 root 7 units,  30 degrees
```

---

# §7 — REFERENCE HTML SKELETON

Verified: rendered in headless Chromium and compared against the reference PDF — header, border, option grid and footer all match.

```html
&lt;!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;&lt;meta charset="utf-8"&gt;
&lt;style&gt;
@page { size: A4; margin: 8.5mm; }
* { box-sizing: border-box; }
body { margin:0; font-family:"Times New Roman",Times,serif; font-size:12pt;
       line-height:1.5; color:#000; -webkit-print-color-adjust:exact;
       print-color-adjust:exact; }
.page { position:relative; width:210mm; min-height:297mm;
        padding:14mm 12.7mm 18mm 12.7mm; border:3px double #003300;
        page-break-after:always; }
.page:last-child { page-break-after:auto; }
.hdr { display:flex; justify-content:space-between; align-items:flex-start; }
.hdr-l { flex:1; }
.hdr-l div { margin-bottom:9pt; white-space:pre; }
.hdr-r { width:175pt; text-align:right; }
.lockup { display:flex; align-items:center; gap:8px; justify-content:flex-end; }
.crest { width:38px; height:46px; flex:0 0 auto; }
.lockup-txt { text-align:left; font-family:Arial,Helvetica,sans-serif; }
.dps  { font-size:13pt; font-weight:700; color:#1A1A1A; line-height:1.05;
        white-space:nowrap; }
.brch { font-size:8.5pt; color:#333; letter-spacing:.2px; white-space:nowrap; }
.gold { width:60px; height:2.5px; background:#C59A21; margin:3px 0; }
.motto{ font-size:7.5pt; color:#333; }
hr.div { border:none; border-top:.5pt solid #000; margin:10pt 0 22pt 0; }
.sec  { text-transform:uppercase; margin:26pt 0 18pt 0; }
.q    { margin:0 0 8pt 0; page-break-inside:avoid; }
.opts { width:100%; border-collapse:collapse; margin:0 0 14pt 0; }
.opts td { width:50%; padding:3pt 0; vertical-align:top; }
.dirn { margin-bottom:14pt; }
.ar   { margin-bottom:14pt; page-break-inside:avoid; }
.foot { position:absolute; bottom:8mm; right:12.7mm; font-size:11pt; }
&lt;/style&gt;&lt;/head&gt;&lt;body&gt;

&lt;div class="page"&gt;
  &lt;div class="hdr"&gt;
    &lt;div class="hdr-l"&gt;
      &lt;div&gt;Name:  _____________________________________&lt;/div&gt;
      &lt;div&gt;Class: X                   Section: A&lt;/div&gt;
      &lt;div&gt;Subject: MATHEMATICS                          Date: ____________&lt;/div&gt;
      &lt;div&gt;Chapter/Topic: SOME APPLICATIONS OF TRIGONOMETRY&lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="hdr-r"&gt;
      &lt;div class="lockup"&gt;
        &lt;!-- Preferred: &lt;img src="dps_logo_header_lockup.png" style="width:155pt"&gt;
             Self-contained: &lt;img src="data:image/png;base64,…" style="width:155pt"&gt;
             Fallback below. --&gt;
        &lt;svg class="crest" viewBox="0 0 40 48"&gt;
          &lt;path d="M20 2 C12 2 6 5 4 7 v22 c0 9 8 15 16 17 8-2 16-8 16-17 V7 c-2-2-8-5-16-5z"
                fill="none" stroke="#1B7A4B" stroke-width="2.4"/&gt;
          &lt;circle cx="20" cy="24" r="9" fill="none" stroke="#1B7A4B" stroke-width="1.4"/&gt;
          &lt;path d="M20 17 v14 M15 22 h10" stroke="#1B7A4B" stroke-width="1.4"/&gt;
        &lt;/svg&gt;
        &lt;div class="lockup-txt"&gt;
          &lt;div class="dps"&gt;Delhi Public School&lt;/div&gt;
          &lt;div class="brch"&gt;Gurugram I Sector 67A&lt;/div&gt;
          &lt;div class="gold"&gt;&lt;/div&gt;
          &lt;div class="motto"&gt;Nurturing the Whole Child&lt;/div&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
  &lt;hr class="div"&gt;

  &lt;div class="sec"&gt;Multiple Choice Questions&lt;/div&gt;

  &lt;div class="q"&gt;Q1. A pole 6 m high casts a shadow 2√3 m long on the ground. The Sun's elevation is&lt;/div&gt;
  &lt;table class="opts"&gt;
    &lt;tr&gt;&lt;td&gt;(a) 30°&lt;/td&gt;&lt;td&gt;(b) 45°&lt;/td&gt;&lt;/tr&gt;
    &lt;tr&gt;&lt;td&gt;(c) 60°&lt;/td&gt;&lt;td&gt;(d) 90°&lt;/td&gt;&lt;/tr&gt;
  &lt;/table&gt;

  &lt;div class="foot"&gt;Page &lt;b&gt;1&lt;/b&gt; of 5&lt;/div&gt;
&lt;/div&gt;

&lt;div class="page"&gt;
  &lt;div class="sec"&gt;Assertion-Reason Questions&lt;/div&gt;
  &lt;div class="dirn"&gt;
    Direction: In the following questions, a statement of assertion (A) is
    followed by a statement of reason (R). Mark the correct choice as:
    &lt;div&gt;(a) Both assertion (A) and reason (R) are true and reason (R) is the correct explanation of assertion (A).&lt;/div&gt;
    &lt;div&gt;(b) Both assertion (A) and reason (R) are true but reason (R) is not the correct explanation of assertion (A).&lt;/div&gt;
    &lt;div&gt;(c) Assertion (A) is true but reason (R) is false.&lt;/div&gt;
    &lt;div&gt;(d) Assertion (A) is false but reason (R) is true.&lt;/div&gt;
  &lt;/div&gt;
  &lt;div class="ar"&gt;
    &lt;div&gt;Q1. Assertion (A): If the length of the shadow of a vertical pole equals its height, the Sun's elevation is 45°.&lt;/div&gt;
    &lt;div&gt;Reason (R): For an angle θ, tan θ = perpendicular / base.&lt;/div&gt;
  &lt;/div&gt;
  &lt;div class="foot"&gt;Page &lt;b&gt;2&lt;/b&gt; of 5&lt;/div&gt;
&lt;/div&gt;

&lt;/body&gt;&lt;/html&gt;
```

---

# §8 — WORKED KNOWLEDGE BASE: CLASS 10 TRIGONOMETRY (Ch. 8 + 9)

A completed example of what Phase 2 produces internally, and the quality bar for any chapter. **Every formula below was numerically verified.** For this chapter the AI may use these directly instead of re-deriving.

### Standard values
|| θ | 30° | 45° | 60° |
||---|---|---|---|
|| sin θ | ½ | 1/√2 | √3/2 |
|| cos θ | √3/2 | 1/√2 | ½ |
|| tan θ | 1/√3 | 1 | √3 |
|| cot θ | √3 | 1 | 1/√3 |

### Solver core — heights and distances (all ✅ verified)
|| ID | Situation | Closed form |
||---|---|---|
|| M1 | Object of length `f` atop a tower; elevations A (tower top), B (object top) | `h = f·tanA/(tanB − tanA)`, `d = f/(tanB − tanA)` |
|| M2 | Observers on **opposite** sides, elevations A, B | `dist = h(cotA + cotB)` |
|| M3 | Two objects **same** side, depressions A, B (B &gt; A) | `dist = h(cotA − cotB)` |
|| M4 | Equal poles across a road of width `w`, elevations A, B from between | `h = w/(cotA + cotB)`, `d₁ = h·cotA` |
|| M5 | From a window at height `p`: elevation A of top, depression B of foot | `H = p(1 + tanA·cotB)`, `width = p·cotB` |
|| M6 | Depressions A (top), B (bottom) of a building of height `b` | `H = b·tanB/(tanB − tanA)` |
|| M7 | Elevations of a tower from top and bottom of a building `b` | `H = b·tanB/(tanB − tanA)` |
|| M8 | Cloud: from `p` above a lake, elevation A, depression B of reflection | `H = p(tanB + tanA)/(tanB − tanA)` |
|| M9 | Elevation A from X; B from Y, `v` above X | `d = v/(tanA − tanB)`, `H = d·tanA` |
|| M10 | Complementary elevations from distances `a`, `b` | `h = √(ab)` |
|| M11 | Object at height `H`, observer eye `g`, elevation A→B | `dist = (H − g)(cotB − cotA)` |
|| M12 | Car: depression A→B in time `t`; time still to reach | `t·cotB/(cotA − cotB)` — height cancels |
|| M13 | Tree broken at `x`, top touches ground `d` away at θ | `x = d·tanθ`, `slant = d·secθ`, `total = d(tanθ + secθ)` |
|| M14 | Two towers subtending A, B at the midpoint of their feet | `h₁ : h₂ = tanA : tanB` |
|| M15 | Sun's altitude A→B, shadow change for pole `h` | `Δ = h(cotA − cotB)` |
|| M16 | Two aircraft vertically aligned, elevations A (upper, `H`), B | `h_low = H·tanB/tanA` |
|| M17 | Tower subtends A at a point; from `p` above, foot depressed B | `h = p·cotB·tanA` |
|| M18 | Object from P, Q (`L` apart) at angles A, B to the line | `y = L/(cotA + cotB)`, `BP = y/sinA` |

### Solver core — identities (all ✅ verified)
`sin²θ + cos²θ = 1` · `sec²θ − tan²θ = 1` · `cosec²θ − cot²θ = 1`
`sinθ/(1 + cosθ) + (1 + cosθ)/sinθ = 2cosecθ`
`tanθ/(1 − cotθ) + cotθ/(1 − tanθ) = 1 + tanθ + cotθ`
`√((1 + sinθ)/(1 − sinθ)) = secθ + tanθ`
`sin⁶θ + cos⁶θ = 1 − 3sin²θcos²θ` · `sin⁴θ + cos⁴θ = 1 − 2sin²θcos²θ`
`2(sin⁶θ + cos⁶θ) − 3(sin⁴θ + cos⁴θ) = −1`
If `sinθ + cosθ = k` then `sinθcosθ = (k² − 1)/2` · `tanθ + cotθ = secθ·cosecθ`

### Templates (★ = HOTS)
`T01` flagstaff on tower · `T02` opposite-side observers · `T03` cloud &amp; reflection ★ · `T04` depressions of a building's top/bottom · `T05` window elevation + depression · `T06` ship's deck &amp; hill · `T07` poles across a road · `T08` complementary angles ★ · `T09` observer raised by `v` · `T10` balloon moving · `T11` car approaching, time cancels ★ · `T12` broken tree · `T13` tower &amp; building mutual · `T14` two aircraft aligned · `T15` sun's altitude change · `T16` tower subtends, foot depressed ★ · `T17` two towers at midpoint · `T18` triangulation from two stations ★ · `T19` walking towards a building · `T20` ramp design · `T21` non-standard angle via Pythagorean triple · `T22` wire between poles · `T23` bird seen by two observers ★ · `T24` two ships from a lighthouse · `T25` staircase &amp; landings · `T26` inverse angle-finding · `T27` ratio comparison ★ · `T28` consistency check ★ · `T29` optimisation ★ · `T30` symbolic proof ★
`S01` identity proof · `S02` given a ratio, evaluate · `S03` complementary simplification · `S04` solve for the angle · `S05` eliminate the parameter ★ · `S06` `sinθ + cosθ = k` chain ★ · `S07` composite figure · `S08` hard A–R

**A template, fully specified — the detail level Phase 2 must reach:**
```
T03 — CLOUD AND ITS REFLECTION IN A LAKE            [HOTS · 5 marks]
Scenario : From p m above a lake, a cloud's elevation is A and the
           depression of its reflection is B.
Params   : p ∈ {10,15,20,25,30,40,50,60}; (A,B) ∈ {(30,60),(30,45),(45,60)}
Answer   : H = p(tanB + tanA)/(tanB − tanA)     [height above the lake]
           distance from observer = (H − p)/sinA
Contexts : cloud over Dal Lake · drone over a reservoir · bird over a pond ·
           balloon over a lagoon · kite over a step-well · parasail over a bay
Ask      : height above lake / distance from observer / height above observer
Distract : p(tanB − tanA)/(tanB + tanA) · 2p · p(tanA + tanB)/tanB
Guards   : require B &gt; A, else the geometry is impossible
Insight  : the reflection is as far BELOW the surface as the cloud is above,
           so the drop to the reflection is (H + p), not (H − p)
Check    : p = 30, A = 30°, B = 60° → H = 30(√3 + 1/√3)/(√3 − 1/√3) = 60 m ✅
```

### Misconception bank
|| # | Misconception | Distractor produced |
||---|---|---|
|| 1 | Angle from the **wall** treated as from the ground | Uses the complement |
|| 2 | Observer height (1.2 / 1.5 m) never added back | `H(…)` instead of `(H − g)(…)` |
|| 3 | Same-side vs opposite-side sign confusion | `cotA + cotB` for `cotA − cotB` |
|| 4 | `tan` / `cot` inverted | Reciprocal of the answer |
|| 5 | Reflection treated as `H − p` | Wrong cloud height |
|| 6 | Gives horizontal distance when height was asked | The intermediate value |
|| 7 | Uses `sin` where `tan` applies | Hypotenuse for base |
|| 8 | Stops at the intermediate step | Partial answer |
|| 9 | Staircase landings counted as height | Inflated rise |
|| 10 | `√3` divided instead of multiplied | Off by a factor of 3 |
|| 11 | Believes `sin θ` can exceed 1 | Accepts `sin θ = 4/3` |
|| 12 | Complementary case answered as `(a + b)/2` | AM instead of GM |
|| 13 | Forgets height cancels in the car problem | Invents `h` |
|| 14 | Adds the flagstaff before applying the ratio | Double-counts `f` |
|| 15 | Confuses elevation with depression | Angles swapped |

### Guards
```
1  Angles ∈ {30°, 45°, 60°} unless a Pythagorean ratio is allowed
2  (tanB − tanA) in a denominator ⇒ B &gt; A
3  (cotA − cotB) ⇒ B &gt; A so the result is positive
4  Observer height g &lt; object height H
5  Building height b &lt; computed tower height H
6  T03 requires B &gt; A
7  T08: choose (a, b) with √(ab) rational
8  T21: m &lt; n and √(n² − m²) an integer
9  S06: k² ≤ 2, since max(sinθ + cosθ) = √2
10 Reject negative, zero, or absurd results (&gt; 10× the largest input)
11 Round to 2 dp; keep the exact surd alongside
12 If the paper says "use √3 = 1.73", compute with 1.73
```

### Combinatorics
```
per template : 6 angle pairs × ~40 magnitudes × ~8 contexts × 4 asks = 7,680
× 38 templates ≈ 291,000 distinct questions
× option orderings (≥6) ≈ 1.75 million MCQ variants
T28–T30 and S05 take free symbolic parameters → practically unbounded.
```

### Calibration seeds
|| # | Template | Question | Answer |
||---|---|---|---|
|| 1 | T03 | 30 m above a lake, cloud 30°, reflection 60° | **60 m** |
|| 2 | T11 | Depression 30° → 60° in 12 s; time still to reach | **6 s** |
|| 3 | T08 | Complementary elevations from 9 m and 16 m | **12 m** |
|| 4 | T18 | Stations 25 km apart, 60° from P, 30° from Q | BP **12.5 km**, BQ **≈ 21.65 km** |
|| 5 | T05 | Window 24 m up; top 60°, foot depressed 45° | width **24 m**, house **≈ 65.57 m** |
|| 6 | T09 | 60° from X; 45° from Y, 30 m above X | d **≈ 40.98 m**, H **≈ 70.98 m** |
|| 7 | T21 | Tether 130 m, sin α = 5/13 | height **50 m**, horizontal **120 m** |
|| 8 | T16 | Subtends 30°; from 18 m above, foot depressed 60° | **6 m** (= p/3) |
|| 9 | S06 | sin θ + cos θ = 7/5 | sinθcosθ = **12/25**, sin³θ + cos³θ = **91/125** |
|| 10 | T10 | Drone 200 m, eye 1.5 m, 60° → 30° in 40 s | **≈ 229.21 m**, **≈ 5.73 m/s** |

---

# §9 — WORKED KNOWLEDGE BASE: CLASS 10 COORDINATE GEOMETRY (Ch. 7)

A second completed example. Verified against the reference worksheet's own answers.

### Solver core (all ✅ verified)
|| ID | Situation | Closed form |
||---|---|---|
|| C1 | Distance between two points | `d = √((x₂ − x₁)² + (y₂ − y₁)²)` |
|| C2 | Distance from the origin | `d = √(x² + y²)` |
|| C3 | Distance from the x-axis | `|y|` |
|| C4 | Distance from the y-axis | `|x|` |
|| C5 | Midpoint | `((x₁ + x₂)/2, (y₁ + y₂)/2)` |
|| C6 | Section formula, internal, m₁ : m₂ | `((m₁x₂ + m₂x₁)/(m₁ + m₂), (m₁y₂ + m₂y₁)/(m₁ + m₂))` |
|| C7 | Ratio in which the **x-axis** divides AB | `−y₁ : y₂` |
|| C8 | Ratio in which the **y-axis** divides AB | `−x₁ : x₂` |
|| C9 | Centroid | `((x₁ + x₂ + x₃)/3, (y₁ + y₂ + y₃)/3)` |
|| C10 | Area of a triangle | `½|x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|` |
|| C11 | Collinearity test | area `= 0` |
|| C12 | Fourth vertex of parallelogram ABCD | `D = A + C − B` |
|| C13 | Point on the perpendicular bisector of AB | equidistant: `PA = PB` |
|| C14 | Point on an axis equidistant from A, B | set `P(x, 0)`, solve `PA² = PB²` |
|| C15 | `P(a cos θ, a sin θ)` distance from origin | `= |a|`, since `cos²θ + sin²θ = 1` |

### Templates
`C-T01` distance between two points · `C-T02` distance from origin · `C-T03` distance from an axis · `C-T04` midpoint · `C-T05` midpoint with unknowns ★ · `C-T06` section formula, find the point · `C-T07` find the dividing ratio · `C-T08` axis-division ratio · `C-T09` collinearity condition ★ · `C-T10` perimeter of a triangle · `C-T11` area of a triangle · `C-T12` centroid · `C-T13` fourth vertex of a parallelogram · `C-T14` unknown coordinate from a distance ★ · `C-T15` equidistant point on an axis ★ · `C-T16` type of quadrilateral ★ · `C-T17` diagonal of a rectangle · `C-T18` which quadrant a divided point falls in · `C-T19` perpendicular bisector ★ · `C-T20` parametric point `(a cos θ, a sin θ)` ★

**A template, fully specified:**
```
C-T14 — UNKNOWN COORDINATE FROM A GIVEN DISTANCE      [Hard · 1 mark]
Scenario : The distance between (x₁, p) and (x₂, y₂) is d. Find p.
Params   : pick a Pythagorean triple so p is an integer —
           (3,4,5), (6,8,10), (5,12,13), (8,15,17), (9,12,15)
Answer   : p = y₂ ± √(d² − (x₂ − x₁)²)   → usually TWO values
Contexts : plotting points · map coordinates · grid navigation
Ask      : the value(s) of p / why two answers exist / the positive root
Distract : the positive root only · the negative root only · 0
Guards   : require d² ≥ (x₂ − x₁)², else no real solution
Trap     : students give one root; the correct option is often "± k"
Check    : (4, p) and (1, 0), d = 5 → p = ±√(25 − 9) = ±4 ✅
```

### Misconception bank
|| # | Misconception | Distractor produced |
||---|---|---|
|| 1 | Distance from the x-axis given as `x` not `|y|` | Swapped coordinate |
|| 2 | Distance reported as negative | "−5 units" — a useful false assertion |
|| 3 | Section formula weights reversed | Reciprocal ratio |
|| 4 | Ratio `y₁ : y₂` without the minus | Wrong sign |
|| 5 | Centroid computed as a midpoint of two vertices | Wrong point |
|| 6 | Forgets the ½ in the area formula | Double the area |
|| 7 | Forgets absolute value ⇒ negative area | Negative answer |
|| 8 | Parallelogram fourth vertex as `A + B − C` | Wrong vertex |
|| 9 | Assumes equal sides ⇒ square (ignores diagonals) | Square vs rhombus |
|| 10 | Only one root when squaring | Misses `±` |
|| 11 | Confuses midpoint with section formula at ratios ≠ 1 | Wrong point |
|| 12 | Believes collinear points bound a non-zero area | Wrong `k` |

### Guards
```
1  Distances are non-negative — never emit a negative distance
2  Ratios in lowest terms, written "m : n" with spaces
3  For C-T14, require d² ≥ (Δx)² so the root is real
4  Area zero ⇒ collinear; do not then ask for "the triangle's perimeter"
5  Squares / rhombi: verify BOTH the four sides AND the two diagonals
6  Section-formula ratios positive for internal division
7  Keep surds exact (√34, 2√7); do not decimalise unless asked
8  Keep coordinates within ±20 for clean arithmetic
9  If two answers are valid, the correct option must show "±"
10 Verify any claimed quadrant against the computed signs
```

### Assertion–Reason patterns
|| Pattern | Example | Key |
||---|---|---|
|| Both true, R explains A | Distance of (3, 4) from origin is 5; R: `OP = √(x² + y²)` | (a) |
|| Both true, R does not explain | Perimeter is 12 units; R: area of a right triangle is ½bh | (b) |
|| A true, R false | — | (c) |
|| **A false, R true** | Distance of P(−3, −4) from origin is −5; R: distance is non-negative | (d) |
|| **A false, R true** | A(−2, 0), B(2, 0), C(0, 3) is equilateral; R: equilateral ⇒ all sides equal | (d) |

Both (d) examples are *decisively* false — a negative distance is impossible, and 4 ≠ √13 is not a near miss. That is the standard to hit.

### Combinatorics
```
per template : ~200 coordinate pairs × ~6 contexts × 3 asks ≈ 3,600
× 20 templates ≈ 72,000 distinct questions
× option orderings ≈ 430,000 MCQ variants
```

---

&lt;div align="center"&gt;

**Delhi Public School, Gurugram — Sector 67A**
*Nurturing the Whole Child*

`DPS_MASTER_Worksheet_Engine.md` · v4.0 · Session 2026-27
One autonomous prompt · self-researching · logo · house format · worksheet · answer key

&lt;/div&gt;

## See also
[[04-Archives/Worksheet-Generator/README|README]]
