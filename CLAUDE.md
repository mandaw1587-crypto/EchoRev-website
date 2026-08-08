# With Manny — project context

This repo is the website for **With Manny** (Manny / Maverick Maltin) — automation, web
design, SEO, and app development, plus a free public library of guides, videos, and
prompt packs. Brand tagline: "Automate. Create. Scale. Be Free." Contact:
withmanny1587@gmail.com.

## Where things stand

- `index-new.html` is the current draft rebuild — a self-contained, dependency-free
  single-file site (inline CSS/JS, no build step). **`index.html` is still the old live
  page** ("The AI Syndicate — 1-on-1 AI Implementation with Manny," black/gold theme);
  `index-new.html` has not been swapped in yet. Don't overwrite `index.html` without
  confirming with Manny first.
- `sales-script.html` and `content-pipeline/` and `trading-strategy/` are older/unrelated
  material in this repo — not part of the current site rebuild.

## Design direction (locked in — don't relitigate without asking)

Manny explicitly rejected a dark/gradient/glow "vibe-coded" AI-generated look. Current
direction is the opposite of that:

- **Light theme**: white / `#f5f5f7` off-white sections, near-black ink (`#1d1d1f`) text.
- **Sharp and crisp**: minimal border-radius (6–8px on buttons/cards, small on chips),
  no pill-shaped buttons, no decorative circles/blobs/glows, no gradients as decoration.
- **System fonts only** (`-apple-system, system-ui, ...`) — no display/script webfonts.
- **Real imagery over abstract icons.** Services use hand-built CSS "interface mockups"
  (browser/search/app wireframes) rather than icon+gradient chips, and real photos are
  used wherever possible (see Assets below) instead of stock/placeholder art.
- One muted accent color, `#96702c` (bronze/gold), used sparingly for eyebrows/labels —
  not a dominant color.
- Motion follows the `apple-design` skill (`~/.claude/skills/apple-design/SKILL.md` —
  note: that skill lives outside the repo and won't persist across sessions/containers;
  re-invoke `Skill({skill: "apple-design"})` if it's not available and motion work comes
  up again): spring physics (damping/response, not CSS keyframes) for the mobile menu
  and the library filter-tab indicator; plain CSS transitions for hover/press states and
  scroll-reveals since those aren't gesture-driven.

## Real assets on hand (`assets/`)

All of these are real, Manny-provided photos/files — not placeholders:

- `assets/img/manny-hero.jpg` — navy suit studio portrait, used in the Hero. Background
  shows his real neon sign, which reads **"With Manny"** (confirmed with Manny directly;
  a cursive-script misread of it as "With Many" was investigated and ruled out).
- `assets/img/manny-onair.jpg` — portrait, studio/podcast setup with "ON AIR" sign, RODE
  mic, and a YouTube award frame. Used as the primary About-section photo.
- `assets/img/manny-patagonia.jpg` — landscape, sunset/remote-work lifestyle shot in a
  Patagonia "with Manny" tee. Used as the secondary About-section photo.
- `assets/img/thumb-claude-gemini.jpg` — a real YouTube thumbnail of his ("Claude vs.
  Gemini") — low native resolution (548×412), so don't display it larger than a library
  card thumbnail or it'll look soft.
- `assets/img/highlevel-logo.png` — HighLevel (CRM/automation platform) logo, used in a
  small "Built and automated with tools like…" trust strip. Don't add other brand logos
  or partnership language without Manny confirming them first.
- `assets/downloads/chatgpt-secret-codes.pdf` — **real, finished lead magnet**:
  "Maverick's ChatGPT Secret Codes," 100 ChatGPT prompt shortcuts across 9 categories
  (Writing, Learning, Ideas, Analysis, Systems, Content, Coding, Utility, Prompts). This
  is linked from both the Library grid and the dedicated Freebie section — the Freebie
  section's category grid mirrors the PDF's real cover layout. If Manny sends more real
  PDFs/videos, add them to the `resources` array in `index-new.html`'s script (each
  entry: `type`, `label`, `title`, `desc`, `href`, optional `img` for a real thumbnail)
  rather than inventing more placeholder titles.

**Uploaded-file mapping is unverified until double-checked**: filenames Manny's client
assigns on upload (e.g. `bab9c9f1-25146.png`) do not indicate content — a batch
resize once cross-mapped three photos to the wrong destinations (the patagonia shot,
onair shot, and video thumbnail all landed in each other's slots) and it wasn't caught
until visually re-checking each saved file. Always re-`Read` a freshly saved image
before wiring it into the page.

## Known placeholders still needing real data from Manny

- **Social links** are `href="#"` in both the Contact section and the footer
  (Instagram, TikTok, YouTube, Facebook, LinkedIn icons already built) — swap in real
  profile URLs when he provides them. Don't guess/invent handles.
- **Newsletter/freebie form** (`#newsletter-form` in the script) currently forwards
  signups via a `mailto:` fallback to withmanny1587@gmail.com — it is not a real
  mailing list. If Manny connects a real ESP (Mailchimp/ConvertKit/beehiiv/etc.),
  replace the JS handler with a real POST to that provider instead.
- A few Library resources are still invented placeholder titles with `href="#"`
  ("The Automation Starter Kit," "SEO Fundamentals Checklist," "Build Your First AI
  Workflow," "From Idea to App in a Weekend," "Website Launch Checklist," "Tools I
  Actually Use" link) — replace with real content/links as Manny sends them, same
  pattern as the ChatGPT Secret Codes entry above.

## Working conventions for this repo

- Single self-contained HTML file, no build step, no external JS dependencies — keep
  it that way unless Manny asks for a framework.
- Optimize any new photo before committing it (resize to a sane max width, convert to
  JPEG, strip to a reasonable file size) — see prior art in git history for the
  pattern (Pillow via `python3 -c "..."`).
- Before saying a UI change is done, actually serve the file locally
  (`python3 -m http.server`) and check it with Playwright/a screenshot — don't just
  eyeball the HTML source.
