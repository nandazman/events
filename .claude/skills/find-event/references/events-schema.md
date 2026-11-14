# scans/<YYYY-MM-DD>/events.json schema

The viewer (`assets/viewer.template.html`) reads exactly these keys. Unknown → `""`
(the card shows "not stated"). Never invent values.

```jsonc
{
  "date": "2026-11-14",                 // scan date
  "home": "Bandung",                    // home base used for distance
  "window": { "from": "2026-11-14", "to": "2026-12-14" },
  "sources": "WebSearch 24 queries · 31 pages read",  // one line, how the scan was done
  "note": "",                           // optional warning shown at the top
  "events": [
    {
      "id": "2026-11-22-umkm-expo-bdg", // same slug as in data/events.md (drives status pills)
      "name": "Original event name",
      "score": 86,                      // 0–100
      "worth": "yes",                   // "yes" | "no"  (only meaningful outside Bandung Raya)
      "worth_reason": "",               // shown when worth = "no"
      "region": "bandung",              // "bandung" | "jabodetabek" | "jabar" | "online"
      "city": "Bandung",
      "category": "umkm",               // "umkm" | "export" | "manufacturing" | "property"
      "format": "Expo",                 // expo / seminar / workshop / business matching / bazaar / coaching cohort ...
      "description": "1–3 sentences",
      "start": "2026-11-22",            // ISO date
      "end": "2026-11-24",              // ISO date, or "" for single-day
      "time": "09:00–16:00",
      "deadline": "20 Nov 2026",
      "venue": "Trans Convention Centre",
      "address": "Jl. Gatot Subroto No. 289, Bandung",
      "maps_url": "https://maps.google.com/?q=...",
      "distance": "In city, ~20 min",
      "organizer": "Dinas KUKM Jawa Barat",
      "organizer_url": "https://...",
      "co_organizers": "Bank BJB, BI Jabar",
      "audience": "Official target audience",
      "crowd": "Expected size and who actually attends",
      "speakers": "Notable speakers or exhibitor count",
      "price": "Free (register) / Rp 150.000 regular, Rp 100.000 early bird",
      "price_flag": false,              // true when > Rp 500k
      "book_url": "https://...",        // registration / ticket page
      "contact": "WA 0812-xxxx (panitia), email",
      "links": [ { "label": "Official page", "url": "https://..." },
                 { "label": "Instagram post", "url": "https://..." } ],
      "why": "1–2 lines on client potential",
      "verified": true,                 // false if any key fact is unconfirmed
      "verified_note": "Confirmed on loket.com and @dinaskukmjabar post",
      "prep": {                          // optional; include for the top 3 and any the user asked for
        "who": "Typical attendee and their daily pains",
        "icebreakers": ["...Bahasa Indonesia..."],
        "questions": { "cost": ["..."], "revenue": ["..."] },
        "one_liner": "Bahasa Indonesia one-liner",
        "solution": "One sentence, only if they show real pain",
        "follow_up": "WhatsApp within 24h ..."
      }
    }
  ]
}
```
