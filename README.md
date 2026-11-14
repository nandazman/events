# events

Business events around Bandung (and Jakarta when worth the trip) where a software
engineer can meet business owners: UMKM, exporters/importers, manufacturing,
property/finance/franchise. Built for finding clients, not tech meetups.

**Live list:** https://nandazman.github.io/events/

## How it works

In Claude Code, from this folder, say **"find event"** (or "cari event").

1. The `find-event` skill (`.claude/skills/find-event/`) runs four `event-scanner`
   subagents in parallel (`.claude/agents/event-scanner.md`), one per location:
   Bandung, Jabodetabek, other West Java, online. Each searches the web, checks
   every event on organizer and ticket pages, scores it for client potential, and
   writes networking prep. `scripts/merge_scans.py` merges them into
   `scans/<date>/events.json`.

Only events anyone can join are listed: open registration, or open application
where the organizer selects (flagged). The goal is meeting potential clients:
business owners who could buy, and people who can refer them.
2. The skill logs the events locally, builds the viewers, then commits and pushes.
3. GitHub Pages serves `docs/index.html`.

| Command | What it does |
|---|---|
| "find event" | Scan the next 30 days and publish the results |
| "prep for X" | Networking prep for one event |
| "going to X" / "skip X" | Update the local log |
| "debrief" | Post-event feedback that re-weights future scans |

## Public vs private

| Path | Published | Contents |
|---|---|---|
| `scans/<date>/events.json`, `docs/` | yes | events + networking prep |
| `data/` | **no** (gitignored) | profile, event log, debriefs (leads' contacts) |
| `scans/viewer.html` | **no** (gitignored) | local viewer with the Log and Debriefs tabs |

## Rebuild by hand

```bash
python .claude/skills/find-event/scripts/build_viewer.py            # private viewer
python .claude/skills/find-event/scripts/build_viewer.py --public   # docs/index.html
```

Animation skills come from `emilkowalski/skills`; reinstall them with
`npx skills@latest experimental_install` (reads `skills-lock.json`).
