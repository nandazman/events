#!/usr/bin/env python3
"""Merge per-region scanner output into one scans/<date>/events.json.

Each event-scanner subagent writes scans/<date>/<region>.json (bandung,
jabodetabek, jabar, online). This merges them, drops duplicate ids (keeps the
higher score), sorts by score, and reports which regions are missing or broken.

    python .claude/skills/find-event/scripts/merge_scans.py scans/2026-11-14

Exit code 1 if no region file could be read.
"""
import json
import sys
from pathlib import Path

REGIONS = ["bandung", "jabodetabek", "jabar", "online"]


def main():
    folder = Path(sys.argv[1])
    events, sources, notes, meta = {}, [], [], {}
    for region in REGIONS:
        fp = folder / f"{region}.json"
        if not fp.exists():
            notes.append(f"{region}: no results file")
            continue
        try:
            run = json.loads(fp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            notes.append(f"{region}: broken JSON ({e})")
            continue
        for k in ("date", "home", "window"):
            meta.setdefault(k, run.get(k))
        if run.get("sources"):
            sources.append(f"{region}: {run['sources']}")
        if run.get("note"):
            notes.append(f"{region}: {run['note']}")
        for e in run.get("events", []):
            e.setdefault("region", region)
            old = events.get(e.get("id"))
            if old is None or e.get("score", 0) > old.get("score", 0):
                events[e.get("id")] = e
    if not meta:
        print("ERROR: no region file could be read. " + "; ".join(notes), file=sys.stderr)
        sys.exit(1)
    out = {
        "date": meta.get("date") or folder.name,
        "home": meta.get("home") or "Bandung",
        "window": meta.get("window") or {},
        "sources": " · ".join(sources),
        "note": " · ".join(notes),
        "events": sorted(events.values(), key=lambda e: -e.get("score", 0)),
    }
    (folder / "events.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    by = {r: sum(1 for e in out["events"] if e.get("region") == r) for r in REGIONS}
    print(f"Merged {len(out['events'])} events: " + ", ".join(f"{r} {n}" for r, n in by.items()))
    for n in notes:
        print("NOTE:", n)


if __name__ == "__main__":
    main()
