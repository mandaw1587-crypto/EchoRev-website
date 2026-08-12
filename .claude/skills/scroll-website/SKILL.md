---
name: scroll-website
description: Build a single-file, no-build "builds itself as you scroll" website with a scroll-scrubbed video hero — the Apple-product-page effect where a video plays forward and backward tied to scroll position. Use this whenever the user wants a scroll-animated landing page, a scroll-scrubbed hero video, a cinematic "site that assembles as you scroll," a wishlist/coming-soon page, a product/real-estate/portfolio microsite with an immersive video intro, or mentions "scroll website," "scroll-linked video," "video that plays as I scroll," or references the AETHERIA/real-estate/tech-product/food example builds. Also trigger this if the user has a short clip (6-10s) of a product, space, dish, or themselves and wants it turned into a website. Covers both generating the source clip (Higgsfield or Google Flow, start/end frame method) and building the final single-file HTML/CSS/JS site.
---

# Scroll Website Builder

Turns one short cinematic clip (6-10s) into a single-file, no-build, scroll-linked landing page — the video's playback position is tied directly to scroll position, so it feels like the page "assembles itself" as you scroll. No frameworks, no build step, one HTML file.

This is the same trick behind Apple-style product pages. The whole build is: **one clip in, one HTML file out.**

## Workflow

1. **Get the source clip.** Either the user already has a 6-10s video, or you need to generate one. If generating, see `references/clip-generation.md` for start/end-frame image prompts and motion prompts (game world, real estate walkthrough, tech product, food) plus the Higgsfield/Kling and Google Flow steps. Reuse the end image of one clip as the start image of the next when chaining multiple scenes, so subjects don't morph between scenes.
2. **Gather the brand block.** Before building, get from the user (see `references/brand-block-template.md` for the exact shape): brand name, accent color + background color, hero headline, hero subhead, primary CTA text, 3 feature/benefit lines, a stats row (real numbers only — never invent stats), a 3-step "how it works," and a closing CTA band (headline/subhead/button). If anything is missing, use `[PLACEHOLDER]` — do not invent copy, stats, or quotes.
3. **Re-encode the source video first**, always, before touching the page. Seeking must be instant:
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -x264-params keyint=1 -an scrub.mp4
   ```
   If multiple clips need to be chained into one continuous scrub, concatenate them in order with `ffmpeg concat` first, then run the all-keyframe re-encode on the joined result.
4. **Build the single HTML file** exactly per the Engine Spec below, filling in the brand block content.
5. **Run the Self-Check** (breakpoint list below) before calling it done. Report what you checked and any fixes made.
6. **Print the local run command** (e.g. `python3 -m http.server 8000`) so the user can open it.

## Engine Spec — build this exactly

Single self-contained `.html` file. All CSS and JS inline. No build step, no external frameworks.

**Video element**
- `<video>` with `muted`, `playsinline`, `preload="auto"`, no `controls`, no `autoplay` attribute (JS drives playback).
- Source = the re-encoded `scrub.mp4`.

**Scroll spacer + pin**
- A tall scroll spacer (~500vh) with the video pinned via `position: sticky` (or fixed, matched to spacer height) for the full spacer duration.

**Scrub logic**
- On scroll, compute `progress` (0 to 1) across the spacer's scroll range.
- `target time = progress * video.duration`.
- In a `requestAnimationFrame` loop, lerp the video's actual `currentTime` toward `target` (factor ~0.12) so playback feels smooth, not jumpy/stepped.
- Wait for the `loadedmetadata` event before enabling scrubbing (so `video.duration` is known).
- Respect `prefers-reduced-motion: reduce` — if set, skip scrubbing entirely: just quietly `.play()` the video muted/looped and show all content without the scroll-linked effect.

**Page flow after the hero**
- Normal sections flow underneath the pinned hero.
- Each section fades/rises in on scroll via `IntersectionObserver` (not scroll-linked — just a one-time reveal-on-enter).

**Hero overlay**
- Headline + subhead + primary CTA overlaid on the video, pinned in the first viewport.
- Fades out as scrubbing begins (tie its opacity to early scroll progress, e.g. fully visible at progress 0, faded by progress ~0.08).

**Accessibility**
- Semantic landmarks (`header`, `main`, `section`, etc.), alt text on any images, `:focus-visible` styling on the CTA, WCAG AA contrast on all text against its background.
- Must work when opened via a local static server (not `file://`).

**Design defaults** (override with the brand block)
- Dark, premium, generous whitespace, one accent color, large type, subtle grain/vignette optional.

## Hard requirement: fully responsive

This is not optional polish — build it in from the start:

- Fluid type scale using `clamp()`, relative units, `%`/`vw`/`vh` for spacing — never fixed pixel widths that can overflow.
- The sticky scrub video must always fully cover its viewport (`object-fit: cover`) at every ratio, portrait phone through ultrawide desktop — no letterboxing, no clipping the key subject.
- Multi-column sections collapse to a single column on narrow screens.
- Tap targets ≥ 44×44px.
- No horizontal scroll at any width.
- Body text stays ≥ ~16px on mobile.
- Respect safe-area insets on notched phones (`env(safe-area-inset-*)`).
- Test the scrub interaction conceptually against both touch (mobile) and wheel/trackpad (desktop) input.

## Self-Check — do this before calling it done

Walk the CSS/layout at each of these widths and confirm: no horizontal overflow, no overlapping/cut-off text, the video still covers with no letterboxing, and the CTA is reachable and tappable.

**Widths:** 320, 360, 390, 414, 768, 834, 1024, 1280, 1440, 1920, 2560

**Also check:** one short-and-wide case — landscape phone, ~740×360 — confirm the hero still works.

If a headless browser / screenshot tool is available, script screenshots at those widths and visually verify. Otherwise, walk the CSS mentally at each breakpoint and fix anything that would break. **Report what you checked and any fixes you made** — don't just claim it's responsive.

## Never invent

Never fabricate stats, testimonials, or results in the copy. If the user hasn't supplied a real number, quote, or fact, use an explicit placeholder like `[YOUR STAT HERE]` and flag it back to them — don't fill the gap with a plausible-sounding fake.

## Reference files

- `references/clip-generation.md` — Start/end-frame image prompts and motion prompts for 4 example builds (game world, real estate 6-stage journey, tech product 4-stage, food/burger), plus the Higgsfield (Kling start/end frame) and Google Flow (Omni Flash, ingredients) generation steps.
- `references/brand-block-template.md` — The exact fields to collect from the user before building, with a filled example (AETHERIA game wishlist page) showing the expected shape and tone.
