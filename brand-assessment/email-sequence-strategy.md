# Email Sequence Strategy — The AI Syndicate
### Strategy layer on top of the existing `content-pipeline/email-automation/` pipeline

---

## 0. What's actually built today (audit)

Before proposing anything, here's the real state of the pipeline — I read all six files plus the workflow and the sales script.

| File | What it does today | Constraint this creates |
|---|---|---|
| `leads.py` | Sources **cold** leads only: Google Places textsearch → `get_place_website` → Hunter.io `domain-search` for a guessed email. No inbound capture. | There is no code path for a warm lead (site visitor, challenge opt-in, discovery-call booking) to ever enter `contacts.csv`. This is the single biggest gap — see §3. |
| `generate.py` | One `SYSTEM_PROMPT`, hardcoded to a **3-email cold outreach sequence** (Day 0 / Day 3 / Day 5). `generate_email_sequence()` always returns exactly `email_1`, `email_2`, `email_3` keys and regenerates the *entire sequence from scratch on every call* — including when `main.py` only needs email 2 or 3 for a followup. | Any new sequence type (welcome, nurture, post-call, win-back) needs its **own system prompt and its own dict shape**, or it'll get mixed with cold-outreach copy. Also: regenerating all 3 emails just to send 1 is wasted tokens and a source of drift if Claude's copy differs run-to-run — flagged in §4. |
| `tracker.py` | CSV schema (`FIELDS`) is hardcoded to `email_1_sent/date`, `email_2_sent/date`, `email_3_sent/date`, `replied`, `unsubscribed`. `get_followups_due()` loops `FOLLOW_UP_DAYS = [3, 5]` against exactly those 3 columns. | The schema has **no concept of sequence type or lifecycle stage** — it assumes every contact is on the same 3-email cold sequence forever. It cannot represent "this contact is now on the nurture sequence" or "this contact had a call and didn't close." This has to be extended, not replaced (see §3.1). |
| `sender.py` | Gmail SMTP (587/STARTTLS), single `GMAIL_ADDRESS`, plain-text MIME, footer = `"reply with 'unsubscribe' in the subject line."` | No `List-Unsubscribe` header, no bounce handling, no separation between marketing and transactional sends. See §5. |
| `config.py` | `DAILY_SEND_LIMIT = 20`, `FOLLOW_UP_DAYS = [3, 5]`, `BUSINESS_TYPES` (10 local-business categories), `CITY`. | 20/day is shared across *all* sends in `main.py` — followups get priority, cold outreach gets the leftover budget. Adding 4 more sequence types onto the same shared budget without allocation logic will starve one or more of them silently. |
| `main.py` | `send_followups()` then `send_new_outreach()`, gated by one global `sent_today` counter and `DAILY_SEND_LIMIT`. | This is the only orchration layer that exists. New sequences plug in here as new functions called in priority order, each respecting the shared daily budget (§3.4). |
| `.github/workflows/daily-email.yml` | Cron `0 14 * * 1-5` (9am ET, Mon–Fri), runs `python main.py`, commits `contacts.csv` back to the repo. | CSV-as-database, committed via git, on a 24h cadence. Fine for cold outreach at this volume; becomes a real limitation once a sequence needs *same-day* triggering (e.g., "email fires 4 hours after a form is abandoned") — flagged where relevant. |

**`sales-script.html` voice/offer reference** — this is the material every email in this doc pulls tone and structure from:
- Never opens with "I." Opens with them.
- One ask per message. No stacked CTAs.
- Scarcity is *literal*, not manufactured: "I typically work with 2–3 people at a time... one of those spots is open right now." This is Manny's real operating model (solo consultant, capacity-constrained), not a fake urgency trick — the email sequences below use it the same way, only when it's true.
- Objection handling reflects the real objection, not a decoy: "what specifically do you need to think through — the investment, the timing, or whether this works for your situation?"
- The funnel referenced is: cold DM/email → follow-up → discovery call → close, with a "14 Days to Freedom Challenge" as the top-of-funnel offer (site opt-in).

---

## 1. Lifecycle map

The existing pipeline only builds **Stage 1**. Everything else is new.

```
[Stage 1] COLD OUTREACH        (EXISTS — leads.py + generate.py cold prompt)
    │  no reply after 3 emails
    ▼
[Stage 2] COLD → DORMANT        (NEW — win-back/re-engagement)
    │
    │  reply received (any stage)
    ▼
[Stage 3] REPLIED / CALL BOOKED (NEW — pre-call confirmation, no-show recovery)
    │
    │  call happens
    ▼
[Stage 4a] CALL → WON           (NEW — onboarding, not a nurture email problem)
[Stage 4b] CALL → NO CLOSE      (NEW — highest-priority sequence, see §2 and §6)
    │  no reply after 3 follow-ups
    ▼
[Stage 5] DORMANT (post-call)   (NEW — longer win-back, different angle than Stage 2)

[Separate entry point, NOT sourced by leads.py today]
[Stage 0] SITE / CHALLENGE OPT-IN  (NEW — requires new capture, see §3.2)
    │
    ▼
[Stage 3] REPLIED / CALL BOOKED  (same as above once they book)

[After a Won client's project delivers]
[Stage 6] POST-DELIVERY REVIEW + REFERRAL  (NEW — low volume, high value, manual trigger)
```

A contact only ever sits in **one** active sequence at a time. Moving from one stage to the next always **replaces** the sequence, never stacks it — a contact who replies mid–cold-outreach is pulled out of Stage 1 immediately (`replied` already does this — good, keep it) and dropped into Stage 3.

---

## 2. Sequences — trigger, cadence, exit conditions

### Sequence A — Cold Outreach (EXISTS, unchanged)
- **Trigger**: new lead sourced via `leads.py`, no prior contact.
- **Cadence**: Day 0, Day 3, Day 5 (`FOLLOW_UP_DAYS`).
- **Exit**: `replied == true` → move to Sequence C. `unsubscribed == true` → suppress permanently. No reply after email 3 + 14 days idle → move to Sequence B.
- No changes needed here except the schema extension in §3.1 so it can coexist with the other sequences in the same CSV.

### Sequence B — Cold Win-Back / Re-engagement (NEW)
- **Trigger**: `sequence = "cold_outreach"`, `email_3_sent = true`, `replied = false`, and 14+ days since `email_3_date`.
- **Cadence**: 2 emails, Day 0 and Day 10 of the win-back sequence (21-day total window, per your own benchmark of 14–21 days for reactivation).
- **Segment**: language n/a (English-only for now), business_type + city (already on the contact record) — this is a 2-variable segment (`business_type` × `time-since-last-touch`), satisfying the "no single-attribute segment" rule.
- **Content angle**: different from cold outreach — leads with a new proof point or a seasonal/timing hook ("Q4 planning season for [business_type]s"), not a rehash of email 1–3. This is why it needs its **own system prompt** in `generate.py`, not a re-run of the cold one.
- **Exit conditions**: replies → Sequence C. No reply after email 2 + 21 days → mark `lifecycle_stage = "suppressed_dormant"`, remove from all future sends (do not delete the row — you need it for CAN-SPAM audit trail and to prevent Hunter/Places re-discovering the same business and re-adding it as a "new" lead).

### Sequence C — Replied / Discovery Call Booked (NEW)
This is where volume is lowest and stakes are highest — every email here is 1:1, not a batch send. Two branches:

**C1 — Call confirmation + no-show recovery**
- **Trigger**: `replied = true` and a call gets booked (manually logged — see §3.3).
- **Cadence**: confirmation email immediately on booking (not cron-dependent — see §3.4 on same-day sends), reminder Day -1 (day before the call), no-show recovery email same day if the call is missed.
- **Exit**: call happens → move to Sequence D. No response to no-show recovery after 3 days → Sequence E (post-call dormant, treated as a lost call).

**C2 — Pre-call nurture (only if more than 3 business days between booking and the call)**
- **Trigger**: gap between booking and call date > 3 days.
- **Cadence**: 1 email, sent 2 days before the call — a light value-add (a relevant case study or a 1-line prep question: "what's the one thing you want this call to solve?"). Keeps them warm without over-emailing before a call that's already booked.
- **Exit**: superseded by the call itself.

### Sequence D — Post-Call, No Close (NEW — highest priority, see §6)
- **Trigger**: call outcome logged as `completed`, `won = false` (manual entry — §3.3).
- **Cadence**: Day 1, Day 4, Day 9 after the call (short and tight — this is a hot lead, not a cold one; per your own data, behavior-triggered sequences convert far better than long drip cadences, and a 9-day window matches how fast a "let me think about it" goes cold).
- **Segment**: 2+ variables — `objection_type` (price / timing / partner-approval / past-bad-experience, captured from the call) × `days_since_call`. This determines which of the four objection-handler angles from `sales-script.html` email 1 leads with.
- **Content**: pulls directly from the 4 objection handlers in `sales-script.html` §5 — each email addresses the *specific* objection surfaced on the call, not a generic "just checking in."
- **Exit**: replies with a yes → Won (Sequence F, manual). Replies with a hard no → suppress. No reply after email 3 + 7 days → Sequence E.

### Sequence E — Post-Call Dormant / Long Win-Back (NEW)
- **Trigger**: Sequence D exhausted with no reply, OR no-show with no response to recovery.
- **Cadence**: 2 emails, at Day 14 and Day 45 post-D-exhaustion (this segment gets a longer runway than cold win-back, because they already invested 30 minutes on a call — that intent decays slower than a cold open).
- **Content angle**: capacity/scarcity-driven re-approach ("a spot opened up" / "closing out this quarter's client list") — this is the one place the literal "2–3 clients at a time" scarcity line from the sales script is used as a *re-approach* trigger rather than a close trigger.
- **Exit**: reply → Sequence C. No reply after email 2 + 30 days → suppress permanently.

### Sequence F — Won Client Onboarding (NEW, light-touch)
- **Trigger**: call outcome logged `won = true`.
- **Cadence**: 1 email — welcome/next-steps, sent same day as the agreement is sent (per the sales script close: *"Perfect. I'll send over the agreement tonight."*). This is not a marketing sequence; treat it as **transactional** (see §5's rule on never mixing the two) — no unsubscribe footer, no tracking pixel.
- **Exit**: superseded once the project kicks off.

### Sequence G — Post-Delivery Review + Referral (NEW, low volume)
- **Trigger**: project delivery marked complete (manual).
- **Cadence**:
  - Day 7 post-delivery: results/impact check-in + soft ask for a testimonial (personal touch first if you're already talking to them, per your own real-estate playbook principle — the email follows a personal touch, it doesn't replace one).
  - Day 60–90 post-delivery: referral ask (quarterly "thinking of you" cadence beyond that, not built here since it's a single manual send at this client volume).
- **Segment**: `lifecycle_stage = "won"` × `days_since_delivery` — at 2–3 clients at a time, this will never be a list-based send, always a named, 1:1 email.
- **Exit**: n/a — this is a relationship-maintenance sequence, not a conversion funnel; it just stops after the referral ask unless they refer someone (new lead enters at Stage 0/1 with `source = "referral"`).

### Site / Challenge Opt-In Nurture (Stage 0, NEW — requires new capture, see §3.2)
- **Trigger**: someone opts into the "14 Days to Freedom Challenge" (referenced in `sales-script.html` footer) via the site, but doesn't book a call.
- **Cadence**: welcome/nurture hybrid — 5 emails over 14 days (Day 0, 2, 5, 9, 14), matching the challenge's own 14-day arc so the emails narrate the challenge rather than compete with it.
- **Exit**: books a call → Sequence C. Completes the 14 days with no booking → Sequence B-equivalent win-back (reuse Sequence B's cadence/logic, different copy angle: "reply of the challenge" instead of "local business timing hook").
- **This cannot be built without new capture code — see §3.2.** It is real, common outreach volume being left on the table right now (anyone who opts into the challenge today gets zero follow-up unless they book a call manually).

---

## 3. Exactly where each sequence plugs into the existing files

### 3.1 `tracker.py` — schema change (do this first, everything else depends on it)

Current `FIELDS` hardcodes 3 email slots. Replace with a generic step-tracking schema that supports variable-length sequences per contact:

```python
FIELDS = [
    "email", "name", "business_name", "business_type", "city", "domain",
    "source",              # cold_outreach | site_optin | referral
    "lifecycle_stage",     # new | replied | call_booked | call_completed_won |
                            # call_completed_no_close | dormant_cold | dormant_post_call |
                            # won_active | won_delivered | suppressed
    "sequence",             # cold_outreach | cold_winback | pre_call | post_call_no_close |
                            # post_call_winback | won_onboarding | review_referral | site_optin_nurture
    "sequence_step",        # int, current position within the active sequence
    "last_sent_date",       # ISO date of most recent send in current sequence
    "objection_type",       # price | timing | partner_approval | past_bad_experience | "" (set manually after a call)
    "call_date",            # ISO date, blank until booked
    "call_outcome",         # "" | completed_won | completed_no_close | no_show
    "replied", "unsubscribed",
]
```

- `mark_sent(email, sequence, step)` replaces `mark_sent(email, email_number)` — same idea, generalized.
- `get_followups_due()` replaces the hardcoded `FOLLOW_UP_DAYS` loop with a lookup against a new `SEQUENCE_CADENCES` dict in `config.py` (below), keyed by `sequence`, so each sequence's own Day-N spacing is used instead of one global list.
- New helper: `advance_stage(email, new_stage, new_sequence)` — called wherever a stage transition happens (reply detected, call outcome logged, challenge completed). This is the function every new trigger point below calls.
- This is a **migration**, not an addition — the existing `contacts.csv` rows need `email_1_sent/date` etc. backfilled into `sequence="cold_outreach", sequence_step=N, last_sent_date=...` once, since the column names change. Do this in a one-off script before deploying, not inside `main.py`.

### 3.2 `leads.py` — new capture path for Stage 0 and reply detection

Two gaps, both currently unhandled:

1. **Site/challenge opt-ins never reach `contacts.csv`.** There is no webhook or form-processing code in this repo. Concretely: add a `capture_optin(email, name, source="site_optin")` function that a simple form handler (Zapier/Make webhook, or a Google Form + Sheet you poll) calls, writing a row with `lifecycle_stage="new", sequence="site_optin_nurture", sequence_step=0`. This is infrastructure that doesn't exist yet in this repo — flagging it rather than pretending `leads.py`'s Google-Places sourcing covers it, because it doesn't.
2. **Reply detection is entirely manual today.** `mark_replied()` exists in `tracker.py` but nothing calls it automatically — there's no IMAP/Gmail-API polling anywhere in this pipeline. Two options, in order of effort: (a) manually mark replies via a small CLI wrapper you run when you see a reply in your inbox (fastest to ship, fine at current volume), or (b) add a Gmail API read-only poll in `main.py` before `send_followups()` that searches the inbox for replies from addresses in `contacts.csv` and calls `mark_replied()` + `advance_stage()` automatically. At 2–3 clients and dozens of daily cold sends, (a) is the right call for now — don't build (b) until reply volume makes manual tracking a bottleneck.

### 3.3 Call outcome logging (new, small) — feeds Sequences C/D/E/F/G

There's no CRM here, so this needs to be a deliberate manual step, not automation you're pretending exists: a one-line CLI command (e.g. `python log_call.py contact@email.com --outcome no_close --objection price`) that calls `tracker.advance_stage()` and sets `objection_type`/`call_outcome`. This is the single manual touchpoint the entire post-call half of this strategy depends on — if it's skipped, Sequence D/E never fire. Worth 20 minutes to build as a tiny script since it's the highest-leverage sequence in this whole plan (§6).

### 3.4 `main.py` — orchestration and budget allocation

Today: `send_followups()` then `send_new_outreach()`, one shared `DAILY_SEND_LIMIT`. With 7 new sequence types added, an unweighted "first come first served" loop will let whichever function runs first (currently followups) eat the entire 20/day budget on quiet days and starve everything else. Restructure the priority order and give each tier a floor:

```
1. Sequence D (post-call, no close)     — always send these first, uncapped (low volume, highest $ value)
2. Sequence C (call confirm/no-show)    — always send, uncapped (time-sensitive, tiny volume)
3. Sequence F (won onboarding)          — always send, uncapped (transactional, tiny volume)
4. Sequence A followups (cold_outreach) — up to 60% of remaining daily budget
5. Sequence B / E (win-back)            — up to 20% of remaining daily budget
6. Sequence 0 (site opt-in nurture)     — up to 20% of remaining daily budget
7. send_new_outreach() (new cold leads) — whatever's left of DAILY_SEND_LIMIT
8. Sequence G (review/referral)         — not cron-driven at all; call directly/manually, it's 1-2 emails a quarter
```

Tiers 1–3 are 1:1, time-sensitive, and near-zero volume (you have 2–3 clients at a time) — they should never compete with batch cold outreach for send budget. This also means `daily-email.yml`'s single daily cron is *too slow* for tiers 1–3 (a call-confirmation email needs to go out same-day, not next-morning) — add a second, more frequent trigger (e.g. every 2 hours on weekdays) that runs only tiers 1–3, keeping the once-daily 9am run for the batch tiers.

### 3.5 `generate.py` — one prompt per sequence, not one prompt reused

Add a `SEQUENCE_PROMPTS` dict keyed by sequence name, each with its own system prompt (voice/rules stay constant — no "I" opener, no buzzwords, one ask, short) but different structural instructions per sequence (length, angle, which objection to lead with, whether it's transactional). `generate_email_sequence(sequence_type, **context)` dispatches to the right prompt and returns `email_1..email_N` for however many steps that sequence actually has (3 for cold outreach, 2 for win-back, 3 for post-call, 5 for the challenge nurture, 1 for onboarding). Also fix the current waste: `send_followups()` regenerates the *entire* 3-email sequence via Claude just to pull one key back out. Cache the generated sequence at Step 1 (store it, e.g. as a JSON blob alongside the contact row, or regenerate deterministically with a fixed seed/temperature) so email 2 and 3 are the *same copy* that was drafted alongside email 1, not a fresh, potentially-inconsistent regeneration each time.

---

## 4. Deliverability considerations (Gmail SMTP, not a dedicated ESP)

- **Volume**: `DAILY_SEND_LIMIT = 20` is well under Gmail's 500/day (or 2,000 for Workspace), and adding the new sequences per §3.4's tier structure keeps total daily volume in the 30–50/day range even fully built out — you don't need warmup ramping the way a 5,000/day list would; you need it because `.env.example` shows this is likely sending from a **plain `@gmail.com` address**, which has zero sender history for cold B2B outreach at all. Ramp: Week 1–2 at 10–15/day, Week 3–4 at 20–25/day, Week 5+ settle at the 30–50/day this strategy needs. Don't front-load Sequence 0's launch and Sequence A's volume in the same week.
- **Authentication**: `.env.example`'s `GMAIL_ADDRESS=you@gmail.com` implies sending from consumer Gmail, not a custom domain on Google Workspace. On a bare `@gmail.com` address, SPF/DKIM/DMARC are Google's own records — you have no visibility or control, and you share reputation with every other Gmail consumer account. **Recommendation: move `SENDER_NAME`/`GMAIL_ADDRESS` to a Google Workspace account on a custom domain** (e.g. `manny@theaisyndicate.com`) so you can add your own DNS: `SPF: v=spf1 include:_spf.google.com ~all`, DKIM enabled + verified in Workspace admin, `DMARC: v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@theaisyndicate.com`. This also unlocks BIMI later and is required if you ever cross into Google's bulk-sender threshold (5,000+/day) — you're nowhere near that now, but the DNS work is cheap to do once, early, rather than mid-campaign.
- **One-click unsubscribe**: `sender.py`'s footer ("reply with 'unsubscribe' in the subject line") is not RFC 8058 one-click and creates friction that increases complaint risk rather than reducing it — a frustrated recipient hits "Report spam" before they'll compose a reply. Minimum fix: add a `List-Unsubscribe` and `List-Unsubscribe-Post` header pointing to a `mailto:` address that `leads.py`'s reply-detection (§3.2) already needs to poll anyway, so one unsubscribe inbox serves both purposes.
- **Bounce handling**: `sender.py` only catches SMTP-level exceptions at send time (auth failures, connection errors) — it cannot see a bounce that comes back as a *reply* to the Gmail inbox after acceptance, which is how most bounces surface over SMTP. There's no code path today that reads bounce-backs and calls anything like a `mark_bounced()`/suppression function. At current volume, a manual weekly scan of the inbox for bounce notifications is enough; if `HUNTER_API_KEY` guesses ever produce a meaningfully high hard-bounce rate, that's a data-quality problem in `leads.py`'s email-guessing logic (falling back to `info@{domain}` with no verification), not a deliverability-tooling problem — worth adding an MX-check step in `enrich_leads()` before accepting a guessed address.
- **Transactional vs marketing**: Sequence F (won-client onboarding) and Sequence C1 (call confirmation) are transactional in spirit — they should never carry the unsubscribe footer or be part of complaint-rate tracking the way batch marketing sends are. `sender.py` currently applies the same `compliance_footer` to every send regardless of type; add a `is_transactional: bool` param to `send_email()` that skips the footer for these two sequences.

---

## 5. Post-Apple MPP measurement note

None of this pipeline currently tracks opens, clicks, or replies as structured metrics — `tracker.py`'s only "engagement" signal is the boolean `replied`. That's actually the right instinct for this volume and this business model: **reply rate and call-booked rate are the two numbers that matter here**, not open rate. Do not add open-tracking pixels to chase a vanity number that Apple Mail proxy-fetches into false 100% opens anyway. If you want a dashboard later, track per sequence: reply rate, call-booked rate (from replies), and close rate (from calls) — that's CTR/CTOR's equivalent for a 1:1 consulting funnel where "click" isn't the meaningful action, "reply" is.

---

## 6. Example email — highest-priority sequence: Sequence D, Email 1 (Day 1 post-call, no close)

This is the highest-priority sequence to build first: it's the smallest volume, the highest revenue-per-send, and the only sequence with **zero coverage today** sitting directly on top of your hottest leads — someone who already gave you 30 minutes on a call. Cold outreach already exists; this doesn't, and every day it doesn't exist is a warm lead going cold with no system behind it.

Written for the `objection_type = "price"` branch (the most common one per the sales script), in Manny's direct, no-fluff voice, one ask, no stacked CTAs:

**Subject:** the number vs. the problem

**Body:**

```
Hey {{FIRST_NAME}},

Been thinking about what you said on the call — the investment
felt like the sticking point, not whether this works for {{BUSINESS_NAME}}.

Fair. So let's actually run the number: what's it costing you right
now to keep doing this by hand? Not in a vague "time is money" way —
actual hours a week, times what your time's worth.

If that number's bigger than what I quoted you, the math already
works. If it's not, tell me and I'll say so — I'm not going to talk
you into something that doesn't pencil out.

I've got one spot open this month. Want to hop on a quick call to
run the actual numbers together?

— Manny
```

This structure pulls directly from the "It's too expensive" objection handler in `sales-script.html` §5 (reframe cost vs. value, invite them to do the math themselves rather than being told), keeps the literal scarcity line honest ("one spot open this month" — only send this if it's true), and has exactly one ask.

Email 2 (Day 4) and Email 3 (Day 9) of this same sequence should be generated per-contact by the new `SEQUENCE_PROMPTS["post_call_no_close"]` prompt in `generate.py` (§3.5), branching on whichever `objection_type` was logged for that contact at call time (§3.3) — timing and partner-approval objections need a different email 1 than price does, which is exactly why this sequence needs its own prompt rather than reusing the cold-outreach one.

---

## Build order (given everything above)

1. `tracker.py` schema migration (§3.1) — nothing else works without it.
2. Call-outcome logging script (§3.3) + Sequence D prompt in `generate.py` (§3.5, §6) — highest revenue impact, lowest build effort.
3. `main.py` tiering + a second, more frequent GitHub Actions trigger for tiers 1–3 (§3.4).
4. `sender.py` List-Unsubscribe header + transactional flag (§4).
5. Site opt-in capture (§3.2) + Sequence 0 — biggest scope, do it once the above is stable.
6. Reply-detection automation, win-back sequences (B/E), and won-client sequences (F/G) — lower urgency, build once tiers 1–4 are live and generating data.
