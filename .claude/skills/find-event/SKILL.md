---
name: find-event
description: Find the nearest worthwhile business events (UMKM/SME, export-import, manufacturing, property/finance/franchise) around Bandung — and Jakarta/Jabodetabek when worth the trip — where a software engineer can meet business owners and land clients. Runs the scan in a separate event-scanner subagent, writes networking prep, keeps a log, publishes events to GitHub Pages, and runs post-event debriefs that re-weight future rankings. Use when the user says "find event", "cari event", "what events are coming up", "debrief", or "mark event as going/attended".
---

# Find Event: finding clients at business events

## Purpose (read this first)

**The purpose is to meet more people who could become clients.** The user is a
software engineer who builds custom business software. They go to business events,
not tech events, to meet business owners and domain experts in rooms where an engineer
is rare and memorable. Every scan, score and prep note serves that one goal.

**Who counts as a potential client:**
- **Buyers:** owners, founders, directors and managers of businesses that could pay
  for custom software (UMKM/SME, exporters/importers, factories, property, franchise).
- **Referrers:** people who can introduce the user to buyers: association and
  community heads (HIPMI, KADIN, TDA, IWAPI, API), business consultants and coaches,
  bank relationship managers, and government program officers (Dinas KUKM, Kemendag, BI).

**Only events anyone can join:**
- **`open`:** anyone can register, free or paid. Always in scope.
- **`apply`:** anyone can apply, and the organizer selects (coaching cohorts,
  business matching, curated programs). In scope, flagged "Apply, selection", with
  who qualifies and the deadline in `access_note`.
- **Out of scope:** members-only, invite-only, closed internal events, and any event
  that only accepts a group the user can't belong to (e.g. "farmers only").

If a request is ambiguous about any of this (who counts as a lead, whether an event
type is in scope, a new city), **ask the user questions with AskUserQuestion before
scanning. Ask as many as needed;** don't guess.

Work from `F:\Personal\event`. Read first:

- `data/profile.md`: who the user is, what they build, proof points, pitch stance
- `data/events.md`: every event already shown, with status
- `data/debriefs.md`: feedback and the **current category weights**

`data/` is **private** (gitignored). Never commit it and never copy its contents into
`scans/` or `docs/`.

## Modes

| User says | Mode |
|---|---|
| "find event", "cari event", nothing specific | **Find** (default) |
| "debrief", "I went to X", "feedback for X" | **Debrief** |
| "going to X", "skip X", "mark X" | **Update status** |
| "prep for X" | **Prep** (networking prep for one event) |

---

## Mode: Find

### 1. Dispatch one scanner subagent per location (every run)

**Every run spawns a separate `event-scanner` subagent for each location, all in
parallel**, so each region gets a full search and their pages stay out of this
conversation. Send all four Agent calls in **one message**, with
`subagent_type: "event-scanner"` and `run_in_background: true`:

| Region | Covers | Output |
|---|---|---|
| `bandung` | Bandung, Cimahi, Kab. Bandung, Bandung Barat, Sumedang/Jatinangor | `scans/<today>/bandung.json` |
| `jabodetabek` | Jakarta, Bogor, Depok, Tangerang, Bekasi | `scans/<today>/jabodetabek.json` |
| `jabar` | Other West Java: major expos and business matching only | `scans/<today>/jabar.json` |
| `online` | Online events, only when clearly useful | `scans/<today>/online.json` |

If the user named another home base, center the four regions on it. If they asked
for only one region, spawn only that one. Give **each** scanner in its prompt:

- **its region** (search only that one) and its output path
- today's date and the window: today → +30 days, unless the user gave another
- home base: Bandung, unless the user named another city
- the Purpose section above: who counts as a potential client, open/apply only
- the category weights table from `data/debriefs.md`, plus its Learnings section
- every `id` already in `data/events.md`, so it skips repeats
- the full text of `data/profile.md`, which the prep needs
- any event the user asked prep for

While they run, tell the user in one line that four scanners are running. Wait for
**all** completion notifications rather than polling, then merge:

```bash
python .claude/skills/find-event/scripts/merge_scans.py scans/<today>
```

That writes `scans/<today>/events.json`, drops duplicates and notes missing regions.

### 2. Check the result

Load the merged `scans/<today>/events.json` and confirm every event has
`id, name, score, region, category, access`. `start` may be `""` only when the
organizer hasn't published a date. If a region's file is missing or broken, tell the
user and re-dispatch **that region's** scanner once with the error, then merge again.
Never fill gaps yourself from memory. Drop any event that is members-only or
invite-only.

Also list events from `data/events.md` with status `shown` whose date is still
upcoming, as "Still open from last time" (one line each).

### 3. Report in chat

English; event names stay in their original language.

1. Summary table: `# | Event | Date | City | Category | Price | Score | Worth trip`
2. The **top 3** as short cards: name · score · date/time · venue · organizer ·
   target audience · who can join (open / apply) · ticket + **book link** ·
   which buyers and referrers will be there
3. Count of the rest by region, plus any unverified ones
4. Links to the viewer (local `scans/viewer.html`) and the public site
   (https://nandazman.github.io/events/)
5. Ask: *"Which are you going to? Want prep for any of the others?"*

### 4. Log, build, publish

1. Append each new event to `data/events.md` with status `shown`.
   Columns: `id | date | event | city | category | organizer | score | price | link | status | notes`.
2. Build both viewers:
   ```bash
   python .claude/skills/find-event/scripts/build_viewer.py            # private: scans/viewer.html (log + debriefs)
   python .claude/skills/find-event/scripts/build_viewer.py --public   # public:  docs/index.html (events only)
   ```
3. Publish. The user set up GitHub Pages for this, so publishing is expected:
   ```bash
   git add scans/*/events.json docs/
   git commit -m "Scan <today>: <n> events"
   git push
   ```
   Stage only those paths. If `git status` shows anything under `data/` staged, stop
   and unstage it. The site updates about a minute after the push.

The viewer's layout follows gstack's design-html doctrine, and its animations follow
Emil Kowalski's rules. Change the design in
`.claude/skills/find-event/assets/viewer.template.html`, never in the generated files.

---

## Mode: Prep

Find the event in the latest `scans/*/events.json`. If it has no `prep`, write one
following section 5 of `.claude/agents/event-scanner.md`, save it into that JSON,
rebuild both viewers and push. Show the prep in chat.

## Mode: Update status

Set the event's status in `data/events.md` to `going`, `skipped` (ask for a one-line
reason and keep it in notes, since skip reasons are signal) or `attended`. Setting
`attended` starts a debrief. Rebuild the private viewer only; status is not published.

## Mode: Debrief

Ask with AskUserQuestion when possible:

1. Which event? (offer the `going`/`attended` ones from the log)
2. How many real conversations? How many were business owners?
3. Leads: any WhatsApp numbers or follow-ups? What problem did each one have?
4. Quality 1–5: was it worth your time?
5. What surprised you? (different crowd than expected, wrong format, a great host…)
6. Would you go to this kind of event again?

Then:
- Append an entry to `data/debriefs.md` with: date, event id, category, conversations, owners met, leads with their problems, quality, notes.
- **Recompute category weights:** for each category, average `quality × (1 + leads)`
  over its debriefs. Normalise so the best category = 15, keep a minimum of 3, and
  leave categories with no debriefs at 10. Rewrite the weights table and tell the user what changed and why.
- Add any **pattern** to "Learnings" (e.g. "expos with booths beat seminars").
  The scanner gets these on the next run.
- Mark the event `attended` in `data/events.md`.
- For each lead, draft a WhatsApp follow-up in Bahasa Indonesia.
- Rebuild the **private** viewer only. Debriefs are never published.
