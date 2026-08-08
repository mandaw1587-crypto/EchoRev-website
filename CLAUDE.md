# With Manny — project context

This repo is the website for **With Manny** (Manny / Maverick Maltin) — automation, web
design, SEO, app development, YouTube growth, AI avatar videos, and a HighLevel-powered
"run your business in one place" platform, plus a free public library of guides, videos,
and prompt packs. Brand tagline: "Automate. Create. Scale. Be Free." Contact:
withmanny1587@gmail.com.

## Where things stand

- The rebuild is a **multi-page site**, not a single file (Manny explicitly asked for
  "buttons instead" of one page, each linking to its own page). Pages:
  - `index-new.html` — Home hub (hero, an "Explore" grid linking to the pages below,
    the ChatGPT Secret Codes freebie, About, Contact).
  - `services.html` — Web Design / SEO / App Creation (the original 3-card services).
  - `platform.html` — the HighLevel-powered "Platform" (funnels, CRM, websites, text/
    call-back automation, lead capture) pitched at SaaS founders and local businesses.
  - `youtube-growth.html` — YouTube growth services (content strategy, thumbnails,
    editing systems) and channel links.
  - `resources.html` — the PDF/video library, organized so each resource can show the
    thumbnail of the video it's paired with. Filterable (All/Guides/Videos/Links).
  - `avatar-calls.html` — AI avatar video generation + 1:1 strategy calls.
  - Shared chrome (top bar, glass nav panel, footer) is **duplicated markup** at the top/
    bottom of each page (no templating/build step) — when adding a new nav link, update
    it in all six files, not just one.
- Shared, non-duplicated code lives in `assets/css/site.css` (all shared styles: reset,
  buttons, top bar, glass panel, cards, mockups, footer, etc.) and `assets/js/site.js`
  (the `Spring` class exposed as `window.WMSpring`, top-bar scroll state, the glass panel
  open/close logic, and the scroll-reveal `IntersectionObserver`). Every page `<link>`s
  and `<script src>`s these instead of inlining them — keep new shared UI in these files
  rather than copy-pasting CSS/JS into individual pages.
- **`index.html` is still the old live page** ("The AI Syndicate — 1-on-1 AI
  Implementation with Manny," black/gold theme) — none of the new pages have been
  swapped in yet. Don't overwrite `index.html` without confirming with Manny first; when
  he says go, `index-new.html` becomes the new `index.html` and the other pages keep
  their names.
- `sales-script.html`, `content-pipeline/`, and `trading-strategy/` are older/unrelated
  material in this repo — not part of the current site rebuild.

## Navigation pattern (locked in)

Manny specifically asked for: a button fixed in the top-right corner that opens a glass
(translucent/blurred, not gradient) panel of links sliding in from the **left** edge of
the screen, with a dimming scrim behind it. This is the *only* nav — there's no separate
desktop nav-links row or separate mobile hamburger, the same trigger/panel works at every
breakpoint. Implementation: `#menu-trigger` button → `#glass-panel` (`translateX`, spring
damping 0.8/response 0.3, treated as a "drawer" per the apple-design skill) + `#glass-scrim`.
Panel has two groups: "Explore" (the six pages above) and "Links" (external — Newsletter,
Stan Store, YouTube, TikTok, each with an external-link arrow icon).

## Design direction (locked in — don't relitigate without asking)

Manny explicitly rejected a dark/gradient/glow "vibe-coded" AI-generated look, but *does*
want a frosted-glass nav panel — glass/blur is fine (it's genuine Apple materials
language), gradients-as-decoration and glow blobs are not. Otherwise:

- **Light theme**: white / `#f5f5f7` off-white sections, near-black ink (`#1d1d1f`) text.
- **Sharp and crisp**: minimal border-radius (6–8px on buttons/cards, small on chips),
  no pill-shaped buttons, no decorative circles/blobs/glows, no gradients as decoration.
- **System fonts only** (`-apple-system, system-ui, ...`) — no display/script webfonts.
- **Real imagery over abstract icons.** Services use hand-built CSS "interface mockups"
  (browser/search/app/thumbnail wireframes) rather than icon+gradient chips, and real
  photos are used wherever possible (see Assets below) instead of stock/placeholder art.
- One muted accent color, `#96702c` (bronze/gold), used sparingly for eyebrows/labels/
  icons — not a dominant color.
- Motion follows the `apple-design` skill (`~/.claude/skills/apple-design/SKILL.md` —
  note: that skill lives outside the repo and won't persist across sessions/containers;
  re-invoke `Skill({skill: "apple-design"})` if it's not available and motion work comes
  up again): spring physics (damping/response, not CSS keyframes) for the glass nav panel
  and the library filter-tab indicator; plain CSS transitions for hover/press states and
  scroll-reveals since those aren't gesture-driven.

## Real links on hand

- **GoHighLevel affiliate link**: `https://www.gohighlevel.com/?fp_ref=ssoori` — used for
  every "Start Free Trial" CTA on `platform.html` and the promo banner. Keep the
  `fp_ref=ssoori` query param intact; it's Manny's affiliate tracking.
- **Beehiiv newsletter**: `https://mannys-newsletter-bf191f.beehiiv.com/` — this *is* the
  freebie delivery mechanism. Joining the newsletter is how visitors get the ChatGPT
  Secret Codes PDF (Beehiiv handles the actual email automation/delivery — the site
  itself doesn't; don't rebuild a custom mailto-forwarding form for this again).
- **Stan Store**: `https://stan.store/LUNANOIR`
- **YouTube channel**: `https://www.youtube.com/channel/UChyejXI8BzsXQ6AT3Obonbg`
  (subscribe-confirmation variant used for CTAs: append `?sub_confirmation=1`)
- **TikTok**: `https://www.tiktok.com/@mannysaisuite`
- **Still placeholder (`href="#"`)**: Instagram, Facebook, LinkedIn — don't guess/invent
  handles, wait for Manny to send them.

## Real assets on hand (`assets/`)

All of these are real, Manny-provided photos/files — not placeholders:

- `assets/img/manny-hero.jpg` — navy suit studio portrait, used in the Home hero and the
  Platform page's promo photo. Background shows his real neon sign, which reads
  **"With Manny"** (confirmed with Manny directly; a cursive-script misread of it as
  "With Many" was investigated and ruled out).
- `assets/img/manny-onair.jpg` — portrait, studio/podcast setup with "ON AIR" sign, RODE
  mic, and a YouTube award frame. Used as the primary About-section photo (Home).
- `assets/img/manny-patagonia.jpg` — landscape, sunset/remote-work lifestyle shot in a
  Patagonia "with Manny" tee. Used as the secondary About-section photo (Home).
- `assets/img/thumb-claude-gemini.jpg` — a real YouTube thumbnail of his ("Claude vs.
  Gemini") — low native resolution (548×412), so don't display it larger than a library
  card thumbnail or it'll look soft. Used in `resources.html`'s library grid.
- `assets/img/highlevel-logo.png` — HighLevel logo, used on `platform.html`'s promo
  banner ("Powered by HighLevel"). Don't add other brand logos or partnership language
  without Manny confirming them first.
- `assets/downloads/chatgpt-secret-codes.pdf` — **real, finished lead magnet**:
  "Maverick's ChatGPT Secret Codes," 100 ChatGPT prompt shortcuts across 9 categories
  (Writing, Learning, Ideas, Analysis, Systems, Content, Coding, Utility, Prompts). Linked
  directly from the Library grid's PDF card; the Home/Library freebie block instead
  routes through the real Beehiiv newsletter (see Real links above) since that's the
  actual delivery mechanism. The freebie doc-mockup's category grid mirrors the PDF's
  real cover layout. If Manny sends more real PDFs/videos, add them to the `resources`
  array in `resources.html`'s script (each entry: `type`, `label`, `title`, `desc`,
  `href`, optional `img` for a real thumbnail) rather than inventing more placeholder
  titles.

**Uploaded-file mapping is unverified until double-checked**: filenames Manny's client
assigns on upload (e.g. `bab9c9f1-25146.png`) do not indicate content — a batch resize
once cross-mapped three photos to the wrong destinations (the patagonia shot, onair shot,
and video thumbnail all landed in each other's slots) and it wasn't caught until visually
re-checking each saved file. Always re-`Read` a freshly saved image before wiring it into
a page.

## Known placeholders still needing real data from Manny

- **Instagram, Facebook, LinkedIn** social icons are still `href="#"` (in the Home
  Contact section and every page's footer) — swap in real profile URLs when he sends
  them.
- A few Library resources on `resources.html` are still invented placeholder titles with
  `href="#"` ("The Automation Starter Kit," "SEO Fundamentals Checklist," "Build Your
  First AI Workflow," "From Idea to App in a Weekend," "Website Launch Checklist,"
  "Tools I Actually Use" link) — replace with real content/links as Manny sends them,
  same pattern as the ChatGPT Secret Codes entry above.
- `avatar-calls.html`'s CTAs are both `mailto:` (no real booking calendar link yet) — if
  Manny sets up Calendly/a HighLevel booking page, wire that in instead.

## Working conventions for this repo

- Multi-page static site, no build step, no bundler/framework, no external JS
  dependencies — shared CSS/JS lives in `assets/css/site.css` / `assets/js/site.js` and
  is linked from every page; page-specific styles/scripts stay inline in that page.
- Optimize any new photo before committing it (resize to a sane max width, convert to
  JPEG, strip to a reasonable file size) — see prior art in git history for the pattern
  (Pillow via `python3 -c "..."`).
- Before saying a UI change is done, actually serve the files locally
  (`python3 -m http.server`, launched with `setsid ... &` so it survives the tool call
  returning) and check every affected page with Playwright/screenshots — don't just
  eyeball the HTML source.
