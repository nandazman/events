---
name: find-event
description: Find the nearest worthwhile business events (UMKM/SME, export-import, manufacturing, property/finance/franchise) around Bandung — and Jakarta/Jabodetabek when worth the trip — where a software engineer can meet business owners and land clients. Runs the scan in a separate event-scanner subagent, writes networking prep, keeps a log, publishes events to GitHub Pages, and runs post-event debriefs that re-weight future rankings. Use when the user says "find event", "cari event", "what events are coming up", "debrief", or "mark event as going/attended".
---

# Find Event: finding clients at business events

**Goal:** the user is a software engineer looking for **clients**, not tech friends.
They want rooms full of business owners and domain experts, where an engineer is rare.

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

### 1. Dispatch the scanner subagent

The web search runs in the **`event-scanner` subagent** (`.claude/agents/event-scanner.md`),
so the many pages it reads stay out of this conversation. Spawn it with the Agent tool,
`subagent_type: "event-scanner"`. Run it in the background, and wait for the
completion notification rather than polling. Give it in the prompt:

- today's date and the window: today → +30 days, unless the user gave another
- home base: Bandung, unless the user named another city
- the category weights table from `data/debriefs.md`, plus its Learnings section
- every `id` already in `data/events.md`, so it skips repeats
- the full text of `data/profile.md`, which the prep needs
- output path: `scans/<today>/events.json`
- any event the user asked prep for

If the user asked for a narrower search (one category, one city), say so in the prompt.

While it runs, tell the user in one line that the scan is running.

### 2. Check the result

When it returns, load `scans/<today>/events.json` and confirm it parses and every event
has `id, name, score, region, category, start`. If it's missing or broken, tell the
user and re-dispatch once with the error. Never fill gaps yourself from memory.

Also list events from `data/events.md` with status `shown` whose date is still
upcoming, as "Still open from last time" (one line each).

### 3. Report in chat

English; event names stay in their original language.

1. Summary table: `# | Event | Date | City | Category | Price | Score | Worth trip`
2. The **top 3** as short cards: name · score · date/time · venue · organizer ·
   target audience · ticket + **book link** · why it's worth it
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
