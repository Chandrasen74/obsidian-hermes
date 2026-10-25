import os, sys

TARGET = os.path.join(os.path.expanduser("~"), ".config", "opencode", "skills")
bad = []
ids = {}
count = 0
for root, dirs, files in os.walk(TARGET):
    for f in files:
        if f == "SKILL.md":
            count += 1
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8-sig") as fh:
                text = fh.read()
            lines = text.splitlines()
            if not lines or lines[0].strip() != "---":
                bad.append((p, "no frontmatter start"))
                continue
            end = None
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    end = i
                    break
            if end is None:
                bad.append((p, "no frontmatter end"))
                continue
            fm = [l for l in lines[1:end]]
            keys = [l.split(":")[0] for l in fm if l.strip() and not l.strip().startswith("#")]
            keys = [k.strip() for k in keys]
            if set(keys) != {"name", "description"}:
                bad.append((p, f"keys={keys}"))
                continue
            vals = {}
            for l in fm:
                if ":" in l:
                    k, v = l.split(":", 1)
                    vals[k.strip()] = v.strip()
            if not vals.get("name") or not vals.get("description"):
                bad.append((p, f"empty name/description: {vals}"))
                continue
            sid = os.path.basename(root)
            if sid in ids:
                bad.append((p, f"DUPLICATE ID {sid} also at {ids[sid]}"))
            ids[sid] = p

print(f"SKILL.md scanned: {count}")
print(f"unique IDs: {len(ids)}")
if bad:
    print("PROBLEMS:")
    for p, why in bad:
        print("  -", p, "|", why)
    sys.exit(1)
print("ALL VALID: every frontmatter is exactly name+description, no empty fields, no ID conflicts")
