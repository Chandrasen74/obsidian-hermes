#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
update_config.py
  Adds all *.gguf files found under one or more directories
  to the current‑directory config (llm_launcher_config.json).

  Usage:
      python update_config.py /path/to/dir1 /path/to/dir2 ...

  Options:
      -c, --config        Path to config.json (default: cwd/llm_launcher_config.json)
      --prune-missing     Remove models whose model_file does not exist
"""

import argparse
import json
from pathlib import Path
import sys

CONFIG_DEFAULT = Path.cwd() / "llm_launcher_config.json"


def load_config(path: Path) -> dict:
    if not path.exists():
        # Create an *empty* config if none exists
        data = {
            "default_executable": "",
            "executables": {},
            "default_args": [],
            "models": []
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_gguf(dirs: list[Path]) -> list[Path]:
    files = []
    for d in dirs:
        if not d.is_dir():
            print(f"[WARN] Not a directory: {d}", file=sys.stderr)
            continue
        files.extend(d.rglob("*.gguf"))
    return files


def main():
    parser = argparse.ArgumentParser(description="Add *.gguf files to the launcher config.")
    parser.add_argument("folders", nargs="+", type=Path, help="Folders to search recursively")
    parser.add_argument("-c", "--config", type=Path, default=CONFIG_DEFAULT,
                        help="Path to config.json (default: cwd/llm_launcher_config.json)")
    parser.add_argument("--prune-missing", action="store_true",
                        help="Remove models whose model_file does not exist")
    args = parser.parse_args()

    cfg = load_config(args.config)
    changed = False

    if args.prune_missing:
        kept = []
        removed = 0
        for entry in cfg.get("models", []):
            model_file = entry.get("model_file", "")
            if not model_file or not Path(model_file).expanduser().exists():
                removed += 1
                continue
            kept.append(entry)
        if removed:
            cfg["models"] = kept
            print(f"[INFO] Removed {removed} missing model(s)")
            changed = True

    # Quick lookup of already known files
    existing = {Path(m["model_file"]).resolve() for m in cfg.get("models", [])}

    new = 0
    for gguf in find_gguf(args.folders):
        resolved = gguf.resolve()
        if resolved in existing:
            continue

        # Build a *minimal* model entry
        entry = {
            "name": gguf.stem,          # e.g. "SicariusSicariiStuff_Impish_LLAMA_4B-IQ4_XS"
            "model_file": str(resolved)
            # no executable_name → defaults
        }

        cfg["models"].append(entry)
        existing.add(resolved)
        new += 1
        print(f"[INFO] Added model: {entry['name']} ({resolved})")

    if new:
        changed = True

    if changed:
        save_config(args.config, cfg)
        if new:
            print(f"[DONE] {new} new model(s) added to {args.config}")
        else:
            print(f"[DONE] Config updated (pruned missing models)")
    else:
        print("[INFO] No changes made.")



if __name__ == "__main__":
    main()
