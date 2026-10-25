"""Hermes -> OpenCode skill migration.

Source: %LOCALAPPDATA%\\hermes\\skills\\<category>[/<subcat>]\\<skill>\\...
Target: ~/.config/opencode/skills\\<category>[/<subcat>]\\<skill>\\... (SKILL.md at any
depth is discovered by OpenCode; ID = leaf directory name).

Each SKILL.md frontmatter is rewritten to the exact OpenCode-compatible form:

---
name: <name>
description: <description>
---

Body is preserved verbatim. supporting files/dirs are copied unmodified.
"""
import json
import os
import re
import shutil
import sys

HERMES_SKILLS = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "skills")
TARGET = os.path.join(os.path.expanduser("~"), ".config", "opencode", "skills")
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills_manifest.json")


def parse_frontmatter(text: str):
    """Return (mapping, body, had_frontmatter)."""
    if not text.startswith("---"):
        return {}, text, False
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text, False
    body = "\n".join(lines[end + 1:])
    fm_lines = lines[1:end]
    keys = {}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2)
            # folded / literal scalar block
            if val.strip() in (">-", ">", "|-", "|"):
                i += 1
                buf = []
                while i < len(fm_lines) and (fm_lines[i].startswith(" ")
                                             or fm_lines[i] == ""):
                    buf.append(fm_lines[i])
                    i += 1
                joined = " ".join(s.strip() for s in buf if s.strip())
                val = joined
            else:
                i += 1
                # plain scalar continuation (indented lines that aren't key:value)
                cont = []
                while i < len(fm_lines):
                    nxt = fm_lines[i]
                    if not nxt.startswith(" ") or re.match(r"^\s+[A-Za-z0-9_-]+:\s", nxt) is not None:
                        break
                    cont.append(nxt.strip())
                    i += 1
                val = (val + (" " + " ".join(cont) if cont else "")).strip()
            if isinstance(val, str):
                if val.startswith(("'", '"')) and val.endswith(("'", '"')) and len(val) >= 2:
                    val = val[1:-1].replace('\\"', '"')
            keys[key] = val
        elif line.startswith(" ") and keys and not keys.get("_nested"):
            # nested block under a previous key (e.g. metadata:) -> skip
            i += 1
        else:
            i += 1
    return keys, body, True


def main():
    results = []
    seen_ids = {}
    conflicts = []
    for root, dirs, files in os.walk(HERMES_SKILLS):
        dirs[:] = [d for d in dirs if d not in (".curator_backups", ".locks", ".git")]
        for f in files:
            if f != "SKILL.md":
                continue
            src_path = os.path.join(root, f)
            rel = os.path.relpath(os.path.dirname(src_path), HERMES_SKILLS)
            src_dir = os.path.dirname(src_path)
            dest_root = os.path.join(TARGET, rel)
            dest_path = os.path.join(dest_root, "SKILL.md")

            try:
                shutil.copytree(src_dir, dest_root, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            except Exception as e:
                results.append({"id": os.path.basename(rel), "status": "COPY_ERROR",
                                "error": str(e), "src": src_dir})
                continue

            with open(src_path, "r", encoding="utf-8-sig", errors="replace") as fh:
                text = fh.read()
            keys, body, had = parse_frontmatter(text)
            if not had:
                results.append({"id": os.path.basename(rel), "status": "NO_FRONTMATTER",
                                "path": dest_root})
                continue
            name = (keys.get("name") or os.path.basename(rel)).strip()
            desc = (keys.get("description") or "").strip()
            # single-line safe description
            desc = re.sub(r"\s+", " ", desc).strip()
            if not desc:
                # synthesise from body: first non-heading, non-empty line
                desc = next((l.strip() for l in body.splitlines()
                             if l.strip() and not l.strip().startswith("#")),
                            os.path.basename(rel))
                desc = re.sub(r"\s+", " ", desc)[:200]
                results.append({"id": os.path.basename(rel), "status": "DESC_SYNTHESIZED",
                                "path": dest_root})
            if name != os.path.basename(rel):
                results.append({"id": os.path.basename(rel), "status": "NAME_DIFFERS",
                                "frontend_name": name, "path": dest_root})
            fm = f"---\nname: {name}\ndescription: {desc}\n---\n\n"
            # strip original frontmatter from body already done; ensure body starts clean
            body = body.lstrip("\n")
            with open(dest_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(fm + body + ("\n" if not body.endswith("\n") else ""))

            sid = os.path.basename(rel)
            if sid in seen_ids:
                conflicts.append(f"{sid}: {seen_ids[sid]} AND {rel}")
            seen_ids[sid] = rel
            results.append({"id": sid, "status": "OK", "path": dest_root,
                            "src": src_dir})

    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    ok = sum(1 for r in results if r["status"] == "OK")
    problems = [r for r in results if r["status"] != "OK"]
    print(f"migrated OK: {ok}/{len(results)}")
    print("unique ids:", len(seen_ids))
    if conflicts:
        print("ID CONFLICTS:", conflicts)
    for p in problems:
        print("PROBLEM:", json.dumps(p))
    print("done")


if __name__ == "__main__":
    main()
