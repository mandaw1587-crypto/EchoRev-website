# The AI Syndicate — LinkedIn Content Strategy

**For**: Manny, founder of The AI Syndicate (solo 1-on-1 AI implementation consulting: builds AI/automation systems that save clients 10+ hrs/week, plus SEO/social/web growth as an attached offer)
**Positioning reference**: black-and-gold luxury aesthetic, Playfair Display + Inter, direct/no-fluff/psychological-trigger-driven voice (see `sales-script.html`)
**Existing system this extends**: `.claude/agents/strategist.md` → `researcher.md` → `writer.md` → `editor.md` → `publisher.md`, currently running VIDEO and EMAIL modes only

---

## 0. Why LinkedIn, and why it's a different animal than VIDEO/EMAIL

The existing pipeline has two audiences and two jobs:
- **VIDEO** (YouTube/TikTok): broad, top-of-funnel, side-hustlers and creators — "how to make money with AI." High volume, low intent, algorithm-fed.
- **EMAIL**: cold outreach to local business owners — pure sales copy, sent to strangers who didn't ask for it.

LinkedIn is neither. It's the one channel where Manny's *actual buyer* — a founder, agency owner, or ops lead who could pay four or five figures for done-for-you AI implementation — will see him being credible before he ever DMs them. VIDEO builds reach; EMAIL builds outbound pipeline; **LinkedIn builds the authority that makes outbound work and makes inbound happen at all.** It is the trust layer that sits between "saw a TikTok" and "booked a call."

This means LinkedIn content has a different job: not entertain-and-scroll, not pitch-a-stranger, but **demonstrate expertise in public until the right people slide into his DMs.** That requires its own content pillars, its own cadence, and its own MODE in the writer pipeline — this document specs all three.

---

## 1. Audience & Goal

**Primary outcome**: B2B inbound pipeline (founders/operators who need AI implementation) + authority that makes his cold outreach (`sales-script.html`) land harder because the prospect has already half-recognized him.

**The one reader**: A founder or ops lead at a 5–50 person service business (agency, e-commerce brand, professional services firm) who knows AI is a competitive threat/opportunity but has no idea where to start, has already tried ChatGPT for something and been underwhelmed, and is quietly worried a competitor will figure this out first. Friday-afternoon frustration: "I have three people manually doing something a workflow could do, and I don't have the time or expertise to fix it myself."

**Secondary readers** (content should also work for these without diluting the primary):
- Solo/small agency owners who want to resell or white-label AI implementation
- Other AI/automation consultants (peer credibility → referrals, community, potential JV)

---

## 2. Content Pillars (specific to his positioning — not generic "AI thought leadership")

1. **The Automation Teardown** — "Here's the exact workflow that saved [client type] 10+ hours/week." Concrete, systems-level, screenshots/description of the before/after. This is the pillar that does the selling without selling.
2. **The Hidden Cost of Manual Work** — reframes "you're fine without AI" as "you're bleeding hours and money and don't have a way to see it." Opinion + data posts. This creates the urgency that the EMAIL sequence's pain-amplification question (`sales-script.html` script #3) later capitalizes on.
3. **AI Myths & Bad Advice** — contrarian takes correcting what LinkedIn's AI-influencer noise gets wrong ("You don't need a custom GPT, you need a workflow" / "Prompt engineering is not a skill you should be paying someone for in 2026"). Builds authority by disagreeing with the crowd, which is where his "direct, a little contrarian" voice already lives.
4. **Behind the Build** — solo-operator build-in-public: real client work (anonymized), real decisions, real numbers ("Client X was spending 14 hrs/week on manual reporting. Built this in 6 days. Here's what it does."). This is his single highest-leverage format — story + proof + systems credibility in one post.
5. **The Full-Stack Growth Angle** — SEO/social/web presence posts that tie back to "AI implementation isn't just internal ops, it's how you get found." Keeps the pillar from being purely "backend automation" and reflects the full scope of what The AI Syndicate sells. Used more sparingly (1x per 2 weeks) so it doesn't crowd out the automation-authority pillars.

Pillar-to-post-type mapping and cadence below.

---

## 3. Post Formats & Cadence

**Frequency**: 3–4x/week (Tue–Thu core, one flex day). LinkedIn punishes daily posting from personal profiles with a thin content bench more than it rewards volume — quality and comment depth matter more than frequency here, unlike TikTok/YouTube where volume is the algorithm's main lever.

**Posting windows**: Tue–Thu, 7–9 AM or 12–1 PM in the audience's timezone (default to Eastern/Central US given target = US small-business owners, confirm against actual audience analytics once there's data).

| Day | Pillar | Format |
|---|---|---|
| Tue | Pillar 2 (Hidden Cost) or Pillar 3 (Myths) | Opinion post |
| Wed | Pillar 1 (Teardown) | Expertise post (sometimes carousel) |
| Thu | Pillar 4 (Behind the Build) | Story post |
| Flex (Sat or 2nd Tue) | Pillar 5 (Growth) or Pillar 2 (Data) | Data post |

**Format definitions** (same discipline as the standalone `marketing-linkedin-content-creator` agent already in this repo, applied to Manny's actual pillars):
- **Story post**: specific client moment → tension (what was breaking, costing, or risking) → resolution (what was built) → transferable insight. Never "AI can help your business" — always the specific build.
- **Expertise post**: one thing business owners get wrong about AI/automation → the correct mental model → concrete proof (a workflow, a number, a screenshot description).
- **Opinion post**: state the take → acknowledge what most people believe → defend with evidence from actual implementation work → invite disagreement.
- **Data post**: lead with a surprising number (hours saved, cost of manual work, adoption stat) → why it matters to a 5–50 person business specifically → one actionable implication.
- **Carousel** (native document upload, not images): used for the Teardown pillar when a workflow has enough steps to warrant a swipe-through — 1x every 2–3 weeks, not weekly.

**Hook discipline carries over from `sales-script.html`'s Content Hook Scripts section** — every LinkedIn hook must do one of: create a curiosity gap, speak to an identity ("if you're still doing X manually, this is for you"), or make a specific claim they don't believe until they read on. Same rule, applied to a text-first, professional-register format instead of a spoken-word short-form hook.

---

## 4. Repurposing YouTube/TikTok Scripts Into LinkedIn Posts (the actual process)

This is not "post the transcript." A VIDEO script is written for ears, is conversational and fast, and is aimed at side-hustlers/beginners. A LinkedIn post is read, is scannable, and is aimed at a business owner deciding whether Manny is worth a DM. The adaptation is a rewrite through a specific filter, not a copy-paste.

**Step-by-step process**:

1. **Pull the strategist's brief and the researcher's source material, not the finished script.** The VIDEO script's [HOOK]/[BODY]/[CTA] structure and spoken cadence don't transfer — go back one step in the pipeline to the underlying facts, angle, and key points.

2. **Re-audience the angle.** A VIDEO topic like "5 AI tools to make money in 2026" (side-hustler audience) has to be reframed for a business-owner reader: not "make money with this tool" but "here's what this tool means for how you run your operation" or "here's why your team shouldn't be using this tool the way everyone's using it." If the underlying research doesn't support a B2B-relevant angle, the video topic isn't a LinkedIn candidate — skip it rather than force it. Roughly 1 in 3 VIDEO topics will genuinely repurpose; the rest stay VIDEO-only.

3. **Extract the single strongest section, not the whole script.** A 60–90 second video covers 3–5 points. A LinkedIn post covers one. Identify the [SECTION HOOK] with the most standalone insight — usually the one with the most specific proof or the most counterintuitive claim — and build the whole post around it.

4. **Convert spoken rhythm to scroll rhythm.** Video is written to be heard continuously; LinkedIn is written to be read in short vertical bursts with a "...see more" break. Take the extracted section and:
   - Cut any line that only works with vocal delivery (asides, "and I mean it," filler transitions)
   - Break every 2–3 lines into its own paragraph — one idea per paragraph, white space as a formatting tool
   - Move the strongest proof point or number earlier — video can bury the payoff because audio has no scroll-away risk; text does
   - Insert a hard break right before the insight lands, so the "...see more" cutoff sits at a genuine tension point

5. **Swap the CTA.** VIDEO CTAs point to watch-more/subscribe. EMAIL CTAs are direct pitches. LinkedIn CTAs must invite a reply or a DM — "What would you add?" / "Drop your biggest manual bottleneck below and I'll tell you how I'd automate it" — never "like if you agree," never a hard pitch in the body.

6. **Rebuild for the pillar, not just the topic.** Once repurposed, file the post under one of the 5 pillars above and make sure the angle matches that pillar's job (teardown = show the system; myths = take a position; behind-the-build = tell the story). If the repurposed draft doesn't cleanly fit a pillar, it's a sign the angle conversion in step 2 was incomplete — redo it rather than force-fit a pillar tag.

7. **Run it through editor.md and publisher.md exactly like any other content** — the LINKEDIN mode plugs into the same downstream steps as VIDEO and EMAIL, it just needs its own writer MODE (below) and a corresponding publisher MODE for hashtags/formatting/timing (see note in section 6).

**What repurposes well**: myth-busting segments, single concrete tool/workflow demos, any moment with a specific number or before/after.
**What doesn't repurpose**: pure entertainment hooks, beginner-101 explainers with no business angle, anything that only works because of tone-of-voice delivery (sarcasm, exaggeration for comic effect) rather than the underlying content.

---

## 5. Profile & Engagement Layer (not content, but required for content to convert)

**Headline formula**: [What you do] + [who you help] + [outcome]
Example: *"I build AI automation systems for small businesses — 10+ hours/week back, without hiring."*

**About section** (funnel structure): hook line → what you do / who for → one specific proof story (a real build, real hours saved) → social proof (numbers/outcomes, no client names needed if confidentiality requires it) → CTA ("Comment 'AUDIT' and I'll tell you where I'd start with your business" — mirrors the low-friction, no-pitch-yet tone of the cold DM script in `sales-script.html`).

**Featured section**: best-performing Teardown post, pinned; if/when a lead magnet (workflow checklist, automation audit template) exists, feature that first.

**Engagement routine** (feeds the comment-to-pipeline system already in the standalone LinkedIn agent, applied here to his actual target list):
- Pre-publish: 5–10 substantive comments/day on posts from small-business-owner and agency-owner accounts, and other AI/automation consultants (peer visibility → referral pipeline)
- Post-publish: respond to every comment within the first 60 minutes — this is non-negotiable, same rule already documented in the standalone LinkedIn agent's Critical Rules
- DM only after a real comment exchange, referencing the specific thread, before ever mentioning an offer

---

## 6. Where this plugs into the existing pipeline

- **strategist.md** needs a `MODE: LINKEDIN` added alongside its existing VIDEO/EMAIL modes, briefing the writer with: pillar, post type (story/expertise/opinion/data/carousel), audience (business-owner primary / consultant-peer secondary), angle, key points, CTA style (reply-inviting, never a hard pitch).
- **writer.md** needs the `MODE: LINKEDIN` block specified in section 7 below.
- **publisher.md** should get a matching `MODE: LINKEDIN` output package: clean post copy (no editorial markup), a first-comment draft (for "link in comments" or a source citation, since links in the body get suppressed), 3–5 specific hashtags, and posting-time recommendation (Tue–Thu 7–9 AM / 12–1 PM). Not written in full here since the task scope is the writer MODE, but flagged so the pipeline stays consistent end-to-end.
- The already-present `marketing-linkedin-content-creator.md` standalone agent in `.claude/agents/` is a generic, unbranded LinkedIn expert (audience-agnostic — job seekers, founders, developers, B2B sellers). It's a good reference for LinkedIn mechanics but isn't wired into Manny's actual strategist → researcher → writer → editor → publisher chain and isn't scoped to his specific pillars/voice. The recommendation here is to fold LinkedIn into the existing pipeline via the writer MODE below rather than running a second, parallel content system — one editorial calendar, one voice, one set of pillars.

---

## 7. Proposed `writer.md` addition — `MODE: LINKEDIN`

Add this as a third MODE block in `.claude/agents/writer.md`, in the same style as the existing `MODE: VIDEO` and `MODE: EMAIL` blocks. (Shown here for review — not applied to the file.)

```markdown
### MODE: LINKEDIN
All LinkedIn content is written for **founders, ops leads, and small-business owners deciding whether Manny is worth a DM** — not for the side-hustler/creator audience of VIDEO or the cold-outreach targets of EMAIL. This is the authority layer: it has to read as premium, direct, and specific, never like generic AI-thought-leadership filler.

Every post is one idea, built from a strategy brief tagged with one of five pillars:
1. **Automation Teardown** — a specific workflow, what it replaced, hours/cost saved
2. **Hidden Cost of Manual Work** — the case for urgency, framed in time/money bled, not fear
3. **AI Myths & Bad Advice** — a contrarian, defensible take against common LinkedIn AI noise
4. **Behind the Build** — a real (anonymized) client story, in public, with real numbers
5. **Full-Stack Growth** — ties automation to SEO/social/web presence (used sparingly, ~1x/2 weeks)

Format output as:
- **[HOOK]** — first line only, must earn "...see more." Use one of three types: curiosity gap, bold/contrarian claim, or specific-story opener. Provide all 3 variants, then mark which one is recommended and why.
- **[BODY]** — 2–3 line paragraphs, one idea per paragraph, white space as formatting. Break at the point of maximum tension so the "...see more" cutoff lands mid-thought, not after the payoff.
- **[CTA]** — must invite a reply or DM, never "like if you agree" and never a direct pitch in the body. If a source, tool, or link needs to be shared, write "(link in comments)" and draft that first comment separately.

Example structure:
```
[HOOK - Bold Claim]
"Your team doesn't need more AI tools. It needs one less manual process."

[BODY]
Last month a client was spending 14 hours a week on manual reporting.

Three people. One spreadsheet. Every Friday.

[SECTION HOOK] Here's what actually ate that time — not the reporting itself, but the copy-pasting between four systems that don't talk to each other.

[continues, one idea per paragraph]

[CTA]
What's the process in your business that everyone complains about but nobody's fixed? Drop it below — I'll tell you how I'd automate it.
```

LinkedIn writing rules:
- No corporate throat-clearing: never open with "Excited to share," "I'm humbled to announce," or similar
- Every post needs a defensible point of view — neutral restatements of "AI is changing business" get neutral engagement
- Concrete over inspirational: real numbers, real client situations (anonymized where needed), never "leadership is hard" — style abstraction
- Match the direct, no-fluff register already established in the sales scripts — this is the same voice in a public, authority-building register, not a softer one
- No links in the post body — first-comment placement only
- 3–5 specific hashtags max (e.g. `#aiautomation`, `#smallbusinessowner` — never generic tags like `#business` or `#technology`)
- Tag other people only when the post is genuinely about an exchange with them
```

---

## Summary of deliverable files/paths

- Plan (this document): `/home/user/EchoRev-website/brand-assessment/linkedin-content-plan.md`
- Existing pipeline files read for context: `/home/user/EchoRev-website/.claude/agents/writer.md`, `/home/user/EchoRev-website/.claude/agents/strategist.md`, `/home/user/EchoRev-website/.claude/agents/publisher.md`
- Voice/tone reference read for context: `/home/user/EchoRev-website/sales-script.html`
- Existing standalone (generic, not wired into the pipeline) LinkedIn agent found during this work: `/home/user/EchoRev-website/.claude/agents/marketing-linkedin-content-creator.md` — referenced in section 6 as prior art, not modified.
