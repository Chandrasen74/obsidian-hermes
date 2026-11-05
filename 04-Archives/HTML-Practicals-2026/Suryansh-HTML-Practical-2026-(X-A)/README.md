---
name: README
tags: ["#status/archived", "#type/index", "#domain/education"]
---
# Suryansh-HTML-Practical-2026-(X-A)

**Status:** COMPLETED  
**Date Archived:** 2026-11-05  
**Project Type:** School Assignment (HTML Practical File)

---

## Summary

Built Suryansh's (Class X-A, Computer Applications 165) HTML practical file from
Manas's completed set: the 10 practical HTML files are identical, the only
student-specific value anywhere is the name. Changed `practical10_submitted.html`
(form value `suryansh`), re-rendered that screenshot with Chrome headless at the
original 4096x3072 / 4x device scale (crop matches the original: 1043x1003), and
rebuilt the 14-page PDF with the same assembly pipeline: screenshot under each
Expected Output, cover (Suryansh / X-A) and certificate (Suryansh / Section A)
filled via white-out + insert_text. Verified page count, per-page images, and
rendered visuals of cover, certificate, and the practical10 form. Delivered to
the user's phone over LAN with a small auto-download HTTP server.

---

## Archive Contents

```
Suryansh-HTML-Practical-2026-(X-A)/
├── Project-Files/
│   ├── practical1.html ... practical10.html
│   ├── practical10_submitted.html
│   └── Scripts/
│       ├── build_practical_pdf_suryansh.py   (PDF assembly + name fill)
│       └── serve_suryansh.py                (LAN auto-download server)
├── Source-Files/
│   ├── Grade_10_Computer_Applications_165_HTML_Practical_File.pdf
│   └── school.jpg
├── Output/
│   └── Grade_10_HTML_Practical_File_with_outputs.pdf
└── Screenshots/
    ├── practical1.png ... practical10_submitted.png
    └── cropped/ (PNG + JPG crops with black borders)
```

---

## Key Information

- **Deliverable:** `Output/Grade_10_HTML_Practical_File_with_outputs.pdf` (14 pages, 1.1 MB)
- **Class:** X-A | Session 2026-2027 | Subject: Computer Applications (165)
- **Name changes only here:** cover row "Student's Name", certificate inline blank,
  and the practical10 feedback form screenshot. Roll Number / Subject Teacher left
  blank, same as Manas's copy.
- **Portrait/attribution note:** sibling project
  [[04-Archives/HTML-Practicals-2026/Manas-HTML-Practical-2026-(X-A)/README|Manas README]]
  documents the original build from the school PDF.
- **Serve script:** run `Project-Files\Scripts\serve_suryansh.py` to reshare the
  PDF on port 8890 (auto-download, redirect from `/`), paths derive from the
  script's own location.
- **Build script:** `build_practical_pdf_suryansh.py` needs `pillow` + `pymupdf`;
  name constants live in `VALUES` and the two `write_centered` certificate calls.

---

## Notes for Next AI/Human

- The 10 practical HTML files are shared with Manas's set; if a fix applies to the
  template, re-render + rebuild both kits with their own scripts.
- Re-rendering the form screenshot requires: Chrome headless
  `--window-size=1024,768 --force-device-scale-factor=4` (window-size is CSS px;
  8899 is cursed with a zombie listener on this machine, use 8890).

---

## See also

[[04-Archives/HTML-Practicals-2026/README|HTML-Practicals-2026 index]] ·
[[04-Archives/README|Archive root]]
