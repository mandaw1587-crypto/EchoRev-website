---
name: Street Interview Skill
description: Builds a street-interview video ad for Seedance 2.0 — the format where somebody gets stopped on the sidewalk, gets asked an uncomfortable question, and ends up trying the product on camera. Hand it a product and it returns the question ladder, image prompts to generate the person being interviewed, and every Seedance prompt in order with the reference chain worked out. Fires on "street interview ad", "man on the street", "vox pop ad", "stop strangers on the street", "sidewalk interview".
---

# Street Interview Skill

One format, done properly: a stranger gets stopped on a sidewalk by somebody holding a phone, answers a question they'd rather not answer, gets handed a product, and reacts to it live. Delivered as a set of Seedance 2.0 prompts that generate in sequence and cut together as a single conversation.

## Why the format works

The persuasion is carried by the *admission*, not by the product. When somebody on camera concedes they haven't eaten a vegetable in a week, the viewer concedes it too — and the concession lands before any selling starts. Everything downstream inherits that credibility, which is why the product cannot appear early and the person on camera can never sound like they're being paid.

Two failure modes kill it. The person reads as an actor, or the four clips read as four separate shoots. Most of what follows exists to prevent one of those.

## Constraints you cannot relax

- Deliver exactly the shape specified under **Delivery format**. No extra sections, no commentary, no reorganizing.
- Speech, lipsync, and ambience are generated inside the model. Never hand the user off to a separate voiceover step.
- Nothing in any prompt may suggest a film production. This is one phone in one hand.
- Never send the user to stock libraries or pin boards to find a face. You write image prompts and they generate the person.
- Ask the three opening questions below, then nothing else. Everything past those three is yours to decide — location, ambience, dialogue, the whole script. Do not ask about any of it.
- One person, one street, one stretch of time. Every segment is the same stranger in the same place under the same sky.

---

## The three opening questions

Three things genuinely can't be inferred from a product name, and guessing any of them wrong wastes the entire brief. Ask all three up front, together, then build without stopping again.

**1. Which angle?** The angle sets the whole ladder.

- *Callout* — name the thing the category already sells and undercut it (greens gummies vs. greens powder)
- *Guilt* — the behavior they know they've skipped (no vegetables in a week)
- *Cost* — what the current solution takes from them in money, time, or effort
- *Distrust* — they've been burned by the category and stopped believing it

**2. Who gets stopped?** Write three or four options specific to this product, each phrased as a person rather than a market segment. **Every option must name a gender, an age, and a situation** — "woman, late twenties, gym-goer" or "mom in her thirties on a school run" or "skeptical guy, forties, running errands." Never leave gender to be inferred: "gym-goer, late 20s" is incomplete, and the model will just pick one. Never offer generic labels like "health-conscious consumer."

Gender is settled here rather than later because the interviewee's voice gets written into every sound block before a single image exists. If the user overrides with something that omits gender, choose one, and print the choice in the brief header so they can see it before they generate anything.

This answer is a lane, not a single casting choice. The three casting prompts in Phase two still get written, and they still differ from each other — they just all sit inside the chosen lane, varying by build, hair, ethnicity, and wardrobe instead of by demographic. Three plausible versions of the right person beats three demographics where two are wrong for the ad.

It threads further than casting. The answer sets the interviewee's voice in the sound block, the register of their dialogue, and often the location itself — a gym-goer gets stopped somewhere different than a parent mid-errand.

**3. How long, and where is it running?** This sets the segment count, so it has to be settled before any prompts get written.

- *60 seconds, 4 segments* — the full ladder, one rung per segment. The default when nobody says otherwise.
- *30 seconds, 2 segments* — Concession, then Handover. Fold the dead product into the concession's answer and the ruling into the handover's last beat.
- *15 seconds, 1 segment* — concession, handover, and a one-line ruling in a single take. Offer it, but say plainly that it strains the one-action-arc rule and the ladder barely survives.

**Never offer a multi-person version.** Several strangers answering the same question is a different build with different mechanics — each person needs their own reference and the video chain can't carry identity between them. This skill does one stranger. If the user asks for a mix, say what it would take rather than producing a plan that can't be generated.

---

## Phase one — build the question ladder

The spine of the ad is four questions, not four marketing beats. Derive them before you write a single prompt.

**Rung one, the concession.** Ask about behavior. Never about the product, never about a category. The question has to be answerable honestly in a way that's faintly embarrassing, and the honest answer has to indict the person watching too.

- Greens supplement → "Be straight with me. Any vegetables yesterday?"
- Sunscreen → "When did you last actually reapply?"
- Sleep aid → "How many hours did you really get last night?"

**Rung two, the dead product.** Get them to name the thing they already bought and quit using. This is objection handling wearing curiosity as a disguise, and it works because the viewer owns the same abandoned tub. "Ever try a greens powder?" earns "I bought the big one, tastes like a lawn, it's still in the cupboard."

**Rung three, the handover.** The product enters the frame for the first time. The person has to be visibly unconvinced before they try it — the turn is only worth something if there was somewhere to turn from.

**Rung four, the ruling.** They weigh it against the dead product from rung two and pick this one, underplayed. The person holding the camera says the brand name. The person on camera never does.

Nothing before rung three may reference the product. As far as the interview is concerned, the person being stopped has no idea what this is about until it's put in their hand.

---

## Phase two — cast the person

You generate them. Three prompts, three different people, all inside the lane the user picked in question two. **Gender and rough age are fixed by that answer and never vary between the three** — what varies is build, hair, ethnicity, wardrobe, and face. If they chose a mom in her thirties on a school run, all three are plausible moms in their thirties on a school run. Every prompt must state the gender in words rather than relying on a name or a situation to imply it. The user runs them through ChatGPT Images 2.0 or any image model and keeps whichever looks least like advertising.

Image models default to a symmetrical, poreless, evenly lit human being. That default is fatal here, so every prompt has to argue against it.

**Build into each prompt:**

- The framing of a snapshot rather than a portrait — caught walking, off to one side, the composition of a photo taken in a hurry
- Texture and asymmetry stated outright: open pores, uneven skin tone, a smile that sits crooked, shadow under the eyes, hair that's escaped
- Proportions of a person rather than a model
- Dull light — flat overcast, no low sun, nothing shaped
- Clothing described down to its wear: a washed-out olive hoodie with a collar that's gone slack, not "casual clothes"
- The same street and the same hour as the ad itself, so the still's light doesn't argue with the video's
- A settled, unremarkable expression — anything theatrical gets baked in and then overrides your direction in every segment
- Face unobstructed and forward or three-quarter, torso in frame so the outfit is pinned down for later segments

**Rule out explicitly:** lettering, logos or graphics on any garment (generated type comes out as mush and the video model will faithfully rebuild the mush); retouching; makeup; flawless teeth; blurred backgrounds; posing toward the lens; sunglasses; hair falling across the face.

Before the image gets used, it needs a look for six fingers, scrambled signage, and anything sitting in the background that shouldn't be there. Whatever is in the reference gets rebuilt as a solid object in the footage.

The keeper becomes **@image1**.

---

## Phase three — write the segment prompts

### Anatomy

Every prompt is assembled the same way, in this order:

1. **Spec line** — vertical `9:16`, `15 seconds`, one unbroken take, `UGC style`, `iPhone handheld` at arm's length from whoever is asking the questions
2. **Reference declaration** — which attachments are in play and what each one governs
3. **Three timed beats** — `Beat 1 (0-5s)`, `Beat 2 (5-10s)`, `Beat 3 (10-15s)`
4. **Sound block** — both voices, the ambience, the actual dialogue

**Name the person by their tag inside the beats, not by a pronoun or a noun.** Write "`@video1` holds the pack at chest height," not "she holds the pack" or "the interviewee holds the pack." The tag is what keeps identity pinned through the action, and dropping to a pronoun mid-beat is an invitation for the face to drift. Same rule for the product — "`@image1`, the pack," on first mention in a beat. The subject token is `@image1` in segment 1 and `@video1` from segment 2 onward, since that's where the person lives in each case.

### Density of description

Three to four full sentences per beat. Thin prompts are where artifacts come from — unspecified details don't resolve to something neutral, they resolve to whatever the model feels like, and that's the junk you end up regenerating. Per beat, account for:

- Both hands, separately, plus anything being carried
- The precise expression, and how it moves during the beat
- What sits on the street behind them, and what is deliberately absent
- What passing pedestrians do
- Where the light comes from and which direction it falls

Write Beat 3 knowing its last frame becomes the reference for the next segment. Leave the face clean and legible.

### Realism vocabulary

**Lean on:** `iPhone handheld`, `held at arm's length by the interviewer`, `chest height`, `overcast daylight`, `UGC style`, `slight camera shake`, `small reframe mid-shot`, `9:16`

**Never let these appear**, grouped by what they leak:

- *Hardware* — any camera or lens brand, `anamorphic`, `large sensor`
- *Optics* — `bokeh`, `shallow focus`, `lens flare`, unqualified `depth of field` (write `phone camera depth of field` if you need it)
- *Rigging and movement* — `dolly`, `crane`, `gimbal`, `steadicam`, `tripod`, `whip pan`, `push in`
- *Post* — `color grade`, `LUT`, `film grain`, `speed ramp`, `slow motion` unless it's `iPhone slow-mo`
- *Grandeur* — `cinematic`, `dramatic lighting`, `epic`, `stunning`, `breathtaking`, `moody`
- *Crew* — anything implying a second camera, a boom, a light, or another pair of hands

Composition should sit slightly wrong — subject off-center, an occasional small correction mid-shot. Clean framing is the single clearest tell that somebody was paid to be there.

### The sound block

Both voices, spelled out, in every single segment. The interviewer exists as a voice and a hand and nothing else. Restate their full voice description each time — abbreviating to "same as the last one" gives the model nothing, because each generation starts cold.

Keep the ratio lopsided: clipped questions, unhurried answers. Reverse it and the thing reads as a commercial.

**Ambience by location** — pick one and hold its density across all four segments:

- Busy sidewalk → constant traffic wash, footsteps passing often, horns somewhere off
- Residential street → birdsong, one car every so often, faint wind
- Storefront → door chime, music leaking from inside, steady foot traffic
- Park path → wind through trees, voices at a distance, no engines
- Market or plaza → overlapping voices with no single conversation legible

Ambience that thickens or thins between segments gives the edit away faster than any visual mismatch.

### Writing the dialogue

The person on camera is caught, not performing. Contractions throughout. Hedges, stalls, and self-deprecation. Sentences that stop halfway and restart. Fragments are correct.

Two lines nobody crosses:

- The brand name belongs to the interviewer. The person being interviewed never says it — this single rule does most of the work of not sounding scripted.
- No benefit lists, no marketing register. The endorsement stays smaller than the product deserves.

**This lands:** "Wait — hold on. That's... okay, that's actually good?"
**This kills it:** "It's completely transformed my daily routine."

---

## Phase four — chain the references

### What attaches to what

```
Segment 1      @image1 = the generated interviewee.  Nothing else.
Segment 2      @video1 = 2-4s trim off segment 1.    Nothing else.
Segments 3-4   @video1 = 2-4s trim off the previous segment
               @image1 = a real photograph of the real product
```

**Once `@video1` is carrying the person, stop attaching the interviewee still.** The trim already holds the face, the hair, the clothing, the street, the light, and the voice — everything the still was for. Adding the still on top gives the model two competing sources for the same person, and the likeliest artifact is a second person in the shot. Segment 1 is the only place the generated image belongs.

Attach nothing the prompt doesn't talk about. A reference the model can't place doesn't get set aside — it gets forced into frame as an object. The product does not exist before the handover, so it is never attached to segments one or two.

**Images and videos are numbered separately.** `@image1` is the first image attached; `@video1` is the first video. They don't share a sequence, so a video attachment never pushes an image to `@image2`. That's why the product is `@image1` on segments 3-4 even though a video is attached alongside it — it's the first image, and it stays the first image.

The one thing to keep straight: `@image1` is the interviewee in segment 1 and the product in segments 3-4, because in each case it's whatever image that particular generation is carrying. Every prompt declares what its own references hold, so read the declaration line rather than assuming a slot means the same thing twice.

`@audio1` is a fallback, not part of the chain. The video trim already carries the voice, so only reach for a separate audio reference if timbre starts drifting across segments.

### Trim, don't attach whole clips

Cost runs on `(reference duration + output duration)`, discounted by 0.6 when any video is attached. A video reference therefore only saves money while it stays under roughly two thirds of the output length. Attaching a full 15-second segment against a 15-second generation runs about 20% *over* image-only; a 2-4 second trim runs about 30% under. Cut from the tail of the previous segment — nearest in time, and Beat 3 was written to leave the face readable.

### Sequence

Segments generate in order, each one feeding the next.

1. Generate segment one. Keep the file.
2. Cut 2-4 seconds off its end. Keep it at 720p or lower — references have to land between 640x640 and 834x1112, so anything generated at 1080p needs downscaling before it can be chained.
3. Attach that trim as `@video1` on segment two. Continue down the line.
4. Interrogate the result: same street, same light, same hour? Same clothes and hair? Does the interviewer sound like one person the whole way through? Does it play as a conversation or as four takes? Did the person on camera ever slide into ad copy?
5. When a segment drifts, rebuild it against **segment one's** trim rather than the one immediately before it. That resets to the cleanest source and stops error from stacking down the chain.
6. Assemble in order and export.

---

## Delivery format

Return exactly this and nothing else.

# [Product] — Street Interview Ad

**Product:** [name]
**Angle:** [the chosen angle, in a phrase]
**Who gets stopped:** [the chosen person — gender, age, situation]
**Runtime:** [total]s, [N] segments at 15s
**Ladder:** [the rungs that survive at this runtime]
**Location:** [one setting, unchanged throughout]
**Voices:** interviewer, off camera · interviewee, on camera

## Generate your interviewee

Run one of these through ChatGPT Images 2.0 or any image model. Make a few. Keep the one that looks least like an ad.

**[casting descriptor]**
```
[image prompt]
```

**[casting descriptor]**
```
[image prompt]
```

**[casting descriptor]**
```
[image prompt]
```

Check it for stray fingers, garbled text, and background debris before using it. That file is **@image1**.

## Your product shot

A real photograph of the real package. Not generated. Pick the size that could plausibly be handed to somebody on a street corner.

It gets attached from segment 3 onward, where it's the only image on the generation — so it's referenced as **@image1** in those prompts.

## The prompts

Generate in order. Same settings on every segment: **9:16 · 15 seconds · 720p · audio on.** Stay at 720p — each segment has to be chained into the next, and anything larger needs downscaling before it can be used as a reference.

Write one block per segment at the runtime that was chosen. The four below are the 60-second build; at 30 seconds write Concession and Handover only, and at 15 seconds write a single block carrying the whole ladder.

### Segment 1 — Concession (0:00-0:15)

**Question:** [what gets asked]
**Attach:** @image1

```
Vertical 9:16, 15 seconds, one unbroken take. UGC style, iPhone handheld at
arm's length by the interviewer, chest height.

@image1 is the person being interviewed.

Beat 1 (0-5s) [3-4 sentences, naming @image1 as the subject]

Beat 2 (5-10s) [3-4 sentences]

Beat 3 (10-15s) [3-4 sentences]

Sound: Two voices. Interviewer, off camera — [full voice description].
Interviewee — [full voice description matching @image1]. [Ambience for the
location]. Unhurried rhythm, real pauses.
Interviewer: "[short question]"
Interviewee: "[longer answer, hedged, with filler]"
```

### Segment 2 — Dead product (0:15-0:30)

**Question:** [what gets asked]
**Attach:** @video1 — 2-4s off the end of segment 1. Nothing else.

```
Vertical 9:16, 15 seconds, one unbroken take. UGC style, iPhone handheld at
arm's length by the interviewer, chest height.

@video1 is the interviewee — same face, hair, and clothing. Same street, same
light, same hour. A separate shot from the same conversation, minutes later.

Beat 1 (0-5s) [3-4 sentences, naming @video1 as the subject]

Beat 2 (5-10s) [3-4 sentences]

Beat 3 (10-15s) [3-4 sentences]

Sound: Two voices. Carry the interviewee's voice from @video1 — same timbre,
same accent. Interviewer, off camera — [full voice description again, in full].
[Same ambience at the same density]. Unhurried rhythm, real pauses.
Interviewer: "[short question]"
Interviewee: "[answer]"
```

### Segment 3 — Handover (0:30-0:45)

**Question:** [the line that puts it in their hand]
**Attach:** @video1 — 2-4s off the end of segment 2 · @image1 — the product photo

[Same construction. First appearance of the product anywhere in the ad. Open with
"The person in @video1 is the interviewee" as in segment 2, then declare "@image1
is the product packaging." Bring the interviewer's hand into frame with it, and
give the reaction a beat of its own — doubt first, then the turn.]

### Segment 4 — Ruling (0:45-0:60)

**Question:** [the closing question]
**Attach:** @video1 — 2-4s off the end of segment 3 · @image1 — the product photo

[Same construction. Underplayed verdict against the dead product from segment 2.
The interviewer delivers the brand name.]

## Attachments at a glance

List only the segments this runtime actually has.

- First segment — the interviewee image, as `@image1`
- Every later segment — the trim off the previous segment, as `@video1`
- Any segment where the product is on screen — add the product photo as `@image1`

The interviewee image is attached to the first segment only. From there the video trim carries the person forward, and attaching the still on top of it risks a duplicate person in frame. On a single-segment 15-second build there's no trim to chain, so the interviewee image and the product are both attached to the one generation — `@image1` and `@image2` in that upload order.

## Running the chain

[The six sequencing steps from Phase four, written out for the user.]

---

## Platform reference — Seedance 2.0

Written for Higgsfield, which is where these prompts get run.

- References are written `@image1`, `@video1`, `@audio1` — lowercase, no spaces, no brackets. Higgsfield turns each one into an attachment chip once the file is wired to it, so paste the prompt first and attach second.
- Ceiling of 9 images, 3 videos, 3 audio files, 12 attachments total.
- Reference video: 2-15 seconds combined, under 50MB, sized between 640x640 and 834x1112. Generate segments at 720p so each one can be chained into the next without downscaling first.
- Reference audio only works alongside at least one image or video reference.
- Generations run 4-15 seconds, up to 4K.
- Set duration and aspect ratio explicitly rather than leaving them automatic, so segments don't drift apart.
- Audio generation costs nothing extra.
- Hold each generation to one continuous action. Two scene changes in one prompt will pull against each other.

Running the same prompts through fal.ai instead: the tags are capitalized there (`@Image1`, `@Video1`, `@Audio1`), the parameters are `duration`, `aspect_ratio`, `resolution`, and `generate_audio`, and the response returns a `seed` worth keeping if a segment needs reproducing.
