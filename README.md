# events

A list of upcoming business events around Bandung, and Jakarta when worth the trip,
for one goal: **meeting more people who could become clients** for custom business
software.

**Live list:** https://nandazman.github.io/events/

## Purpose

I'm a software engineer. Tech meetups are full of other engineers; business events
are full of the people who actually have problems software can solve, and an
engineer in that room is rare and remembered. This repo finds those rooms.

**Who I want to meet**
- **Buyers:** owners, founders, directors and managers of businesses that could pay
  for custom software: UMKM/SME, exporters/importers, manufacturing, property,
  finance and franchise.
- **Referrers:** people who can introduce me to buyers: association and community
  heads (HIPMI, KADIN, TDA, IWAPI, API), business consultants and coaches, bank
  relationship managers, government program officers.

**Which events count:** only ones **anyone can join**.
- **Open:** anyone can register, free or paid.
- **Apply:** anyone can apply and the organizer selects (coaching cohorts, business
  matching). Shown with an "Apply, selection" flag.
- Not listed: members-only, invite-only, or restricted to a group I can't belong to.

At each event the approach is problem discovery first (is the pain cost or
revenue?), and a pitch only if there's real pain.

## How it works

In Claude Code, from this folder, say **"find event"** (or "cari event").

1. The `find-event` skill (`.claude/skills/find-event/`) runs four `event-scanner`
   subagents in parallel (`.claude/agents/event-scanner.md`), one per location:
   Bandung, Jabodetabek, other West Java, online. Each searches the web, checks
   every event on organizer and ticket pages, scores it for client potential, and
   writes networking prep. `scripts/merge_scans.py` merges them into
   `scans/<date>/events.json`.
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
