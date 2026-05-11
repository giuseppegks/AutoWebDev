---
name: Booking-System
description: Use when adding a Cal.com-driven booking system to a local business website (barbershop, salon, massage, beauty, fysio). Covers Cal.com setup, Vercel serverless proxy for keeping the API key server-side, and the multi-step booking modal that lives in the site's frontend. Triggers on phrases like "add booking to this site", "integrate Cal.com", "wire up the booking widget", "booking system for [shop]".
---

# Booking System — Cal.com + Vercel Proxy

## Overview

A premium-looking, fully branded booking widget on the client's site, backed by Cal.com's free / Teams plan as the calendar engine. The client sees real bookings appear in their Cal.com dashboard (and synced to Google/Apple Calendar). Customers book in 4 steps without leaving the site.

**Why this stack:**
- **No SaaS fee from you** — the shop pays Cal.com directly (free for single user, ~$15/user/mo for Teams).
- **No backend to maintain** — Cal.com handles availability logic, conflict prevention, email confirmations, reminders, ICS invites.
- **Branded UI stays yours** — customers never see the generic Calendly-style widget; you keep full control of the booking experience.
- **Per-shop isolation** — each shop's `CALCOM_API_KEY` lives in their Vercel project's env vars; no cross-talk.

## When to Use

- Building or extending a presentational site for an appointment-based business
- Client OK with using Cal.com as the underlying calendar
- Vercel hosting (the proxy uses Vercel's serverless functions)

**Skip when:** the client insists on Salonized / Treatwell / Phorest (none expose APIs you can drive a custom UI from — see "Why not Salonized?" below). For those, embed their official widget in an iframe on a dedicated `/boeken` page and accept the visual mismatch.

## Architecture

```
Browser (your branded widget)
       │
       │  fetch /api/event-types
       │  fetch /api/slots?eventTypeId=…
       │  POST /api/bookings
       ▼
Vercel serverless functions (api/*.js)
       │  CALCOM_API_KEY (env var, never in browser)
       ▼
Cal.com API v2  (Bearer auth + cal-api-version header)
```

**Critical:** the API key MUST stay server-side. Never embed it in `js/main.js` or any file served to the browser. Anyone reading page source could create / read / cancel bookings on the shop's calendar.

## Why Not Salonized / Treatwell?

These are walled-garden SaaS — their booking widget *is* their product. They don't expose a public API for driving bookings from a custom UI. Specifically:

- **Salonized**: no public booking API. You can only embed their iframe.
- **Treatwell**: directory + booking platform; their widget, not yours.
- **Phorest, Acuity, SimplyBook**: APIs exist but charge per-shop, eating the value prop.

**Cal.com (open-source, free for single user, has full v2 REST API)** is the only mature option that lets you keep your custom UI while owning zero booking logic.

## Setup Workflow

### 1. Cal.com account + event types

Client (or you on their behalf) creates a Cal.com account.

For each service, create an **Event Type** at `cal.com/event-types`:
- Slug **must match** the value used in the site's `SERVICE_SLUG` map
- Length = service duration (30 min, 45 min, etc.)
- Price (optional but useful for confirmation emails)
- Set up custom fields if needed (notes, phone)

**Example mapping (barbershop):**

| Service in site | Cal.com slug | Length | Price |
|---|---|---|---|
| Haar (knippen + styling) | `haar` | 30 min | €30 |
| Haar & Baard | `haar-baard` | 45 min | €45 |
| Baard | `baard` | 20 min | €25 |

Verify each event type works at `cal.com/<username>/<slug>` before continuing.

### 2. Set availability

Cal.com → Settings → My Availability. Configure working hours per day. **Match these exactly to the `SHOP_HOURS` constant in `js/main.js`** — desync = customers see slots that aren't really available.

For multi-barber shops on Teams plan, each barber's availability is set on their own Cal.com user under the team.

### 3. Generate API key

Cal.com → Settings → Developer → API Keys → "+ New API Key".
- Label it (e.g. "Vercel deploy — barbershop-080")
- No expiration is fine for production; rotate annually
- **Copy the key once** — you cannot retrieve it later
- **Never paste it in chat, commits, screenshots, or terminal commands.** Type it directly into Vercel's env-var prompt.

### 4. Project files (already in the template)

The template ships with these:

```
/api/_cal.js          # Bearer auth, cal-api-version, response normalization
/api/event-types.js   # GET — lists Cal.com event types for the authenticated user
/api/slots.js         # GET — available slots for an event type on a given day
/api/bookings.js      # POST — creates a booking via Cal.com v2
/vercel.json          # cleanUrls: true
/package.json         # type: module, no runtime deps (Vercel provides fetch)
```

### 5. Frontend integration (already wired)

In `js/main.js` the booking modal:
1. On open, calls `/api/event-types` to get the live list of Cal.com event types
2. Maps `data-service` values from the HTML buttons → event type IDs via `SERVICE_SLUG`
3. On step 3, calls `/api/slots?eventTypeId=…&startTime=…&endTime=…&timeZone=…`
4. Builds the full day grid from `SHOP_HOURS`, marks each slot as available (clickable) or taken (disabled, strike-through)
5. On submit, POSTs to `/api/bookings` with the v2 payload shape:

```json
{
  "start": "2026-05-12T10:00:00.000Z",
  "eventTypeId": 123,
  "responses": { "name": "...", "email": "...", "phone": "..." },
  "metadata": { "source": "...", "barberPreference": "..." },
  "timeZone": "Europe/Amsterdam",
  "language": "nl"
}
```

The proxy translates this into Cal.com v2's `attendee` + `bookingFieldsResponses` shape.

### 6. Deploy + env var

```bash
npx vercel                              # initial link, or accept defaults if linked
npx vercel env add CALCOM_API_KEY production
# paste the key when prompted (never visible — that's correct)
npx vercel --prod                        # deploy with the key attached
```

`vercel env add` cannot accept Production + Preview + Development together for sensitive values — add Production first, then Preview / Development separately if needed.

### 7. End-to-end test

Open the production URL → BOEK NU → walk through service → date → time → details → confirm.

Verify:
- Slot list reflects real availability (book a test slot, see it disappear from the grid on next page load)
- Confirmation screen shows the right summary
- "Voeg toe aan agenda" downloads a valid `.ics`
- Cal.com sends the customer email
- Cal.com sends the shop owner email (or it appears in their connected Google Calendar)

## API Version Pinning

Cal.com's v2 uses `cal-api-version` header to lock response shapes. The template uses:

| Endpoint | Version |
|---|---|
| `/v2/event-types` | `2024-06-14` |
| `/v2/slots` | `2024-09-04` |
| `/v2/bookings` | `2024-08-13` |

If response shapes change in the future, bump these in `api/_cal.js` callers. The proxy normalizes multiple shapes defensively (see `slots.js`) so minor changes don't break the frontend.

## Common Failure Modes

| Symptom | Diagnosis | Fix |
|---|---|---|
| `410 Gone` from `/v2/event-types` | Using old v1 endpoints | Switch to v2 base URL + Bearer auth (already done in template) |
| `401 Unauthorized` | API key missing / wrong / not deployed | Re-run `vercel env add` then `vercel --prod` |
| Page loads but `/api/*` returns HTML "Authentication Required" | Vercel Deployment Protection enabled | Use the canonical `<project>.vercel.app` URL, OR turn off protection in project Settings |
| Time step shows "Geen beschikbare tijden" for every day | Cal.com availability not configured, or wrong event type slug | Check Cal.com → Availability + Event Types |
| Slot shows as available but booking fails with 409 | Two customers booked the same slot near-simultaneously | Cal.com handles this, but the second customer must pick another slot — UI shows the error |
| Booked slots still appear available after a fresh booking | Frontend caching | Already removed in v=4+ — make sure `js/main.js?v=` is bumped on each deploy |
| Slots show outside opening hours | `SHOP_HOURS` desynced from Cal.com availability | Edit `SHOP_HOURS` in `js/main.js` to match exactly |

## Multi-Barber Setup (Cal.com Teams)

For shops with multiple barbers each having independent availability:

1. Client subscribes to **Cal.com Teams** (~$15/user/mo)
2. Each barber = a Cal.com user under the team
3. Create per-barber event types: `haar-mo`, `haar-yusuf`, `haar-karim` (or use Cal.com's "Round Robin" event type for any-available booking)
4. In `js/main.js`, change `SERVICE_SLUG` from a flat map to a `(service, barber) → slug` lookup
5. When a barber chip is selected, fetch slots for the barber-specific event type ID

Single-barber-account shops should keep the current setup — the barber field is recorded as a preference note on the booking but doesn't filter availability.

## Security Hygiene

- Rotate the API key annually, or immediately after suspected exposure
- Never log API keys in server logs (the proxy doesn't, but custom additions might)
- Don't commit `.env` files (template's `.gitignore` already excludes `.env` and `.vercel/`)
- For high-stakes shops, set up Cal.com webhook signing on incoming webhooks (out of scope for the basic template)
- If the shop has GDPR concerns, link Cal.com's DPA in the site's footer (Cal.com is GDPR-compliant by default but the shop may need to formalize)

## Cost Model

| Component | Who pays | Cost |
|---|---|---|
| Cal.com (single user) | Shop | Free |
| Cal.com Teams (multi-barber) | Shop | ~$15/user/month |
| Vercel Hobby (hosting + serverless) | You or shop | Free |
| Domain | Shop | ~€10/year |
| Site build + integration | Shop pays you | One-time fee |

**Your value prop in pitch**: "Premium-looking, fully integrated booking — no monthly fee to me, you pay Cal.com directly only if you have multiple barbers. The site is yours."
## Reference Implementation (drop-in template)

The `template/` folder next to this SKILL.md ships a working, generic implementation of everything described above. To wire booking into a new site:

```
template/
├── api/
│   ├── _cal.js          # shared Bearer + version header helper
│   ├── event-types.js   # GET — list event types (slug → ID map)
│   ├── slots.js         # GET — available slots per day
│   └── bookings.js      # POST — create a booking
├── js/
│   └── booking.js       # multi-step branded modal (~580 lines)
└── package.json         # type: module — Vercel uses native ESM here
```

### Step-by-step usage

1. `cp -r skills/booking-system/template/api    websites/<niche>/<slug>/api`
2. `cp -r skills/booking-system/template/js     websites/<niche>/<slug>/js`
3. `cp    skills/booking-system/template/package.json websites/<niche>/<slug>/`
4. Open `js/booking.js` and edit ONLY the `SHOP_CONFIG` block at the top (shopName, phone, domain, addressICS, hours, services, price). Nothing below the `═══` divider needs editing for normal customization.
5. In every HTML page that should have a booking button:
   - Include the script before `</body>`: `<script src="js/booking.js" defer></script>`
   - Add `data-book` to any CTA `<a>` or `<button>`. Optional `data-service="<service.key>"` pre-selects a service (used by per-service "Book this one" links).
6. Deploy with the env var (see "Setup Workflow" §6 above).

### Design system assumptions

The modal markup uses Tailwind utility classes that the host site is assumed to provide via Tailwind Play CDN config. Specifically these custom colors must exist:

- `bg-bg-deep` `bg-bg-surface` `bg-bg-elevated`  — page → card → hover backgrounds
- `border-border-subtle`                          — divider/card borders
- `text-ink-primary` `text-ink-muted` `text-ink-faint` — body / secondary / fine-print
- `bg-gold` `text-gold` `bg-gold-soft`             — accent color (CTAs, kickers)
- `tracking-kicker`                               — 0.18em letter-spacing for the stepper

If the host site uses different token names, find/replace inside `template/js/booking.js`. The classes appear in `viewService`, `viewDuration`, `viewDate`, `viewTime`, `viewDetails`, `viewConfirm` and the `ensureModal` markup.

### Reference site

`websites/massage-salons/gerrit-jonker-massage` is a complete site built on this template — single-practitioner massage practice with 12 event-types (6 massages × 2 durations, plus stoel-30 and intake-30). Use it as a sanity check that the integration is wired correctly.
