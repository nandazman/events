#!/usr/bin/env python3
"""Build a single self-contained scans/viewer.html from find-event output.

Opens offline (file://): no server, no scripts from a CDN. Fonts load from Google Fonts
when online and fall back to system fonts offline. Embeds as JSON:
  * every scans/<YYYY-MM-DD>/events.json (newest first)
  * data/events.md   (the log; its status column also drives the pills on each card)
  * data/debriefs.md (post-event feedback and category weights)

Run from F:\\Personal\\event after each scan or debrief:

    python .claude/skills/find-event/scripts/build_viewer.py            # private, scans/viewer.html
    python .claude/skills/find-event/scripts/build_viewer.py --public   # docs/index.html for GitHub Pages

--public embeds ONLY the scans: no log, no debriefs, no going/attended status.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "viewer.template.html"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def collect_runs(scans_dir: Path):
    runs = []
    if not scans_dir.exists():
        return runs
    for folder in sorted(scans_dir.iterdir(), reverse=True):
        fp = folder / "events.json"
        if not (folder.is_dir() and DATE_RE.match(folder.name) and fp.exists()):
            continue
        try:
            run = json.loads(fp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"WARN: skipping {fp}: {e}", file=sys.stderr)
            continue
        run.setdefault("date", folder.name)
        runs.append(run)
    return runs


def parse_status(log_md: str):
    """Map event id -> status from the markdown table in data/events.md."""
    status, header = {}, None
    for line in log_md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = dict(zip(header, cells))
        if row.get("id") and row.get("status"):
            status[row["id"]] = row["status"].strip("` ").lower()
    return status


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="project root (default: cwd)")
    ap.add_argument("--public", action="store_true", help="events only, written to docs/index.html")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    runs = collect_runs(root / "scans")
    if args.public:
        data = {"runs": runs, "public": True}
    else:
        log = read(root / "data" / "events.md")
        data = {
            "runs": runs,
            "log": log,
            "debriefs": read(root / "data" / "debriefs.md"),
            "status": parse_status(log),
        }
    # "</" inside a <script> would close it early; escape for safe embedding.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/", payload, 1)

    out = root / ("docs/index.html" if args.public else "scans/viewer.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.public:
        (out.parent / ".nojekyll").write_text("", encoding="utf-8")
    out.write_text(html, encoding="utf-8")
    n = sum(len(r.get("events", [])) for r in data["runs"])
    print(f"Wrote {out} ({len(data['runs'])} scans, {n} events)")


if __name__ == "__main__":
    main()
