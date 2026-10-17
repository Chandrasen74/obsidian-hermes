---
version: alpha
name: Stitch Design System
description: Design system for UI projects generated with Google Stitch CLI.
colors:
  primary: "#0F172A"
  secondary: "#64748B"
  tertiary: "#2563EB"
  neutral: "#F8FAFC"
  on-primary: "#FFFFFF"
  on-tertiary: "#FFFFFF"
typography:
  h1:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  h2:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    lineHeight: 1.5
  label-caps:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: 600
    letterSpacing: "0.08em"
rounded:
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  card:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 24px
---

## Overview

This design system enforces consistency across all UI screens generated via the
Google Stitch CLI. Always reference DESIGN.md before generating or editing any
screen. Use `stitch generate screen --prompt "..." --device DESKTOP|MOBILE` for
new screens and `stitch generate variant --screen <id> --creative-range REFINE|EXPLORE|REIMAGINE`
for iterations.

## Colors

- **Primary (#0F172A):** Core text, headlines, high-emphasis surfaces.
- **Secondary (#64748B):** Supporting text, borders, metadata.
- **Tertiary (#2563EB):** Interaction driver — buttons, links, selected states.
  Use sparingly.
- **Neutral (#F8FAFC):** Page background and surface fills.

## Typography

Inter for all text. Hierarchy is driven by weight and size. Tight letter-spacing
on display sizes, default tracking on body.

## Layout

4px baseline spacing. Use `md` (16px) for intra-component gaps, `lg` (24px) for
inter-component gaps, `xl` (48px) for section breaks.

## Shapes

Modest rounded corners — `sm` on interactive elements, `md` on cards. `full` is
reserved for avatars and pill badges.

## Components

- `button-primary` is the only high-emphasis action per screen.
- `card` is the default surface for grouped content.

## Do's and Don'ts

- **Do** use `stitch serve` to preview generated screens locally before committing.
- **Do** run `stitch status --flow=design --json` when repository or project state matters.
- **Don't** write frontend code without first checking or updating DESIGN.md.
- **Don't** introduce colors outside the palette — extend it first.
- **Don't** use em dashes in Discord messages — use commas or colons instead.
