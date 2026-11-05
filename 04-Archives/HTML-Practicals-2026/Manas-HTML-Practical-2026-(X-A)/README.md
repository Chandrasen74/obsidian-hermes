---
name: README
tags: ["#status/archived", "#type/index", "#domain/education"]
---
# Manas-HTML-Practical-2026-(X-A)

**Status:** COMPLETED  
**Date Archived:** 2026-10-25  
**Project Type:** School Assignment (HTML Practical File)

---

## Summary

Assisted Manas (Class X-A, Computer Applications 165) with his HTML practical file. Extracted the requirements from the school PDF, created all 10 practical HTML files, verified outputs in-browser, fixed `practical5.html` with `school.jpg`, produced a filled, image-annotated PDF (with outputs, borders, name/class filled) ready for printing and submission. The work is complete and submitted.

---

## Archive Contents

```
Manas-HTML-Practical-2026-(X-A)/
├── Project-Files/
│   ├── practical1.html
│   ├── practical2.html
│   ├── practical3.html
│   ├── practical4.html
│   ├── practical5.html
│   ├── practical6.html
│   ├── practical7.html
│   ├── practical8.html
│   ├── practical9.html
│   ├── practical10.html
│   └── practical10_submitted.html
├── Source-Files/
│   ├── Grade_10_Computer_Applications_165_HTML_Practical_File.pdf
│   └── school.jpg
├── Output/
│   └── Grade_10_HTML_Practical_File_with_outputs.pdf
├── Screenshots/
│   ├── practical1.png
│   ├── practical2.png
│   ├── practical3.png
│   ├── practical4.png
│   ├── practical5.png
│   ├── practical6.png
│   ├── practical7.png
│   ├── practical8.png
│   ├── practical9.png
│   ├── practical10.png
│   ├── practical10_submitted.png
│   └── cropped/
│       ├── practical1.jpg
│       ├── practical1.png
│       ├── practical2.jpg
│       ├── practical2.png
│       ├── practical3.jpg
│       ├── practical3.png
│       ├── practical4.jpg
│       ├── practical4.png
│       ├── practical5.jpg
│       ├── practical5.png
│       ├── practical6.jpg
│       ├── practical6.png
│       ├── practical7.jpg
│       ├── practical7.png
│       ├── practical8.jpg
│       ├── practical8.png
│       ├── practical9.jpg
│       ├── practical9.png
│       ├── practical10.jpg
│       ├── practical10.png
│       ├── practical10_submitted.jpg
│       └── practical10_submitted.png
└── Processing/
    └── source_text.txt
```

---

## To-Do List

**Completed:**
- [x] Created folder structure in `01-Projects/projects/`
- [x] Extracted full practical text from PDF
- [x] Generated all 10 HTML files matching the index
- [x] Added `school.jpg` for practical 5
- [x] Tested all outputs in browser (headless)
- [x] Captured screenshots and cropped to visible output with black borders
- [x] Filled cover page (Manas, X-A) and certificate (Manas, Section A)
- [x] Created annotated PDF with outputs placed under each practical
- [x] Printed and submitted

**Future Tasks:**
- [x] None - project fully completed and archived

---

## Key Information

- **Deliverable:** `Output/Grade_10_HTML_Practical_File_with_outputs.pdf`
- **Class:** X-A | Session: 2026-2027 | Subject: Computer Applications (165)
- **Practical 5 note:** Uses `school.jpg` in same folder; if reused, replace that image or edit `src`
- **practical10_submitted.html:** Demo variant with filled form values and submit intercepted (for screenshot only; not part of the original 10-file set required)
- **Source PDF:** Original untouched copy kept in `Source-Files/` for reference
- **Build scripts:** `Project-Files/Scripts/` holds the pipeline tooling, added 2026-10-25
  on the owner's request: `build_practical_pdf.py` (PDF assembly), `fill_blanks.py`
  (cover/certificate fill), `inspect_blanks.py` + `verify_pdf.py` (verification),
  `inspect_cert.py` / `inspect_cert_pixels.py` (certificate alignment checks).

---

## Notes for Next AI/Human

- This is a simple one-to-one extraction + render task. The pattern (extract PDF text, generate static HTML, headless render, crop/annotate) is reusable for similar practical files.
- The fill approach (overwrite underscores with same font/size/position) works well for this template; certificate baseline must match the sentence baseline to avoid crossing the line.
- Archived to keep `01-Projects` clean. No active work remains.

---

## See also

[[04-Archives/README|README]]
