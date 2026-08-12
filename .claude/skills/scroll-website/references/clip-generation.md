# Clip Generation — Start/End Frame Method

Two tools work with the exact same image prompts below; only the animation step differs.

**Option A — Higgsfield:** Generate a start image and an end image (16:9), then use Kling with both as start and end frames — it animates the motion between them. Settings: images at 16:9, video at 16:9, sound off, 10 seconds for flythroughs or any action shot (e.g. a bite).

**Option B — Google Flow:** Generate the same start and end images, then drop them into Flow as *ingredients* (Flow doesn't support a locked explicit end frame, so ingredients work better) and pick **Omni Flash**. Paste the motion line as the prompt.

**Continuity tip:** For a multi-scene journey, reuse each clip's end image as the next clip's start image, so the subject stays consistent and doesn't morph into a different object between scenes.

**Google Flow steps, explicitly:**
1. Generate the start image from the prompt, at 16:9.
2. Generate the end image from the prompt, at 16:9.
3. In Flow, add both images as ingredients (not as a locked end frame).
4. Choose Omni Flash.
5. Paste the motion line as the prompt.
6. Generate. If the object drifts, feed the previous clip's end image as the next start ingredient.

---

## 1. Game world

**Start frame:** Epic open-world video game key art, wide establishing shot of a breathtaking fantasy sci-fi world: floating islands connected by glowing light-bridges above a sea of clouds, a distant luminous citadel, bioluminescent flora, volumetric god rays at golden hour, ultra detailed Unreal Engine 5 render, cinematic depth of field, vibrant teal and amber palette, no text, no UI, no watermark, wide 16:9 composition.

**End frame:** Same fantasy sci-fi video game world, continuous art direction, now arriving at the luminous citadel: a massive ornate archway with glowing runes lighting up, first-person view entering a grand hall of floating crystals and towering shafts of light, bioluminescent detail, teal and amber palette, ultra detailed Unreal Engine 5 render, cinematic depth, no text, no UI, no watermark, wide 16:9 composition.

**Motion:** Smooth cinematic first-person camera flythrough gliding forward across the floating-island cloud vista toward the glowing citadel, then passing through the ornate runic archway into the grand crystal hall, continuous immersive game walkthrough motion, god rays, subtle parallax.

---

## 2. Real estate — full 6-stage journey

Chain: empty plot → under construction → finished exterior → living room → master bedroom → games room. Each arrow is one clip. Reuse each end image as the next start.

**Empty plot:** Architectural site at dusk, a bare cleared building plot for a modern luxury villa: flat poured-concrete foundation slab and footings on desert land, a rectangular pool excavation outlined in the foreground, palm trees around the edges, desert-modern Gulf setting, dramatic gradient dusk sky, ultra photoreal, three-quarter viewpoint, no text, no watermark, wide 16:9 composition.

**Under construction:** The same plot at dusk, villa under construction: exposed steel and concrete structural frame, partial floor slabs, some floor-to-ceiling glass panels being installed, scaffolding, a construction crane, palm trees, same three-quarter viewpoint and composition, ultra photoreal architectural render, no text, no watermark, wide 16:9 composition.

**Finished exterior:** Architectural photography, exterior of a modern luxury villa at dusk, floor-to-ceiling glass walls with warm interior glow, infinity pool reflection, palm trees, desert-modern Gulf luxury aesthetic, dramatic gradient sky, ultra photoreal, cinematic wide angle, same viewpoint, no text, no watermark, wide 16:9 composition.

**Living room:** Interior of the same modern luxury villa, expansive open-plan living room with floor-to-ceiling windows overlooking a glittering city skyline at dusk, designer furniture, warm ambient lighting, marble floors, continuous luxury aesthetic, ultra photoreal architectural interior render, cinematic, no text, no watermark, wide 16:9 composition.

**Master bedroom:** Interior of the same modern luxury villa, serene master bedroom at dusk, oversized upholstered bed with layered linens, floor-to-ceiling windows overlooking a glittering city skyline, warm ambient cove lighting, marble and warm wood, designer decor, continuous luxury aesthetic, ultra photoreal architectural interior render, cinematic, no text, no watermark, wide 16:9 composition.

**Games room:** Interior of the same modern luxury villa, a stylish games room at dusk with a luxury billiards pool table at the center, a low linear pendant light glowing over the table, floor-to-ceiling windows overlooking the city skyline, marble floor, warm ambient lighting, leather lounge seating, continuous luxury aesthetic, ultra photoreal architectural interior render, cinematic, no text, no watermark, wide 16:9 composition.

**Motion prompts, one per clip:**
- Plot → construction: Rapid architectural time-lapse, the villa's concrete foundation and exposed steel structure quickly rise from the bare desert plot, building constructs itself layer by layer, dynamic forward camera push, fast and smooth.
- Construction → finished: Rapid architectural time-lapse continuing, glass facade, walls and warm interior lights fill into the steel frame until it becomes the finished illuminated luxury villa at dusk, dynamic forward camera push.
- Exterior → living room: Fast smooth real estate walkthrough, the camera glides from the villa exterior across the pool, through the glass entrance, into the living room revealing the city skyline view, steadicam push-in.
- Living room → bedroom: Fast smooth walkthrough, the camera glides quickly out of the living room, down a hallway and into the serene master bedroom revealing the skyline, dynamic immersive tour.
- Bedroom → games room: Fast smooth walkthrough, the camera glides quickly from the master bedroom into the games room, revealing the billiards pool table and skyline, dynamic immersive tour.

---

## 3. Tech product — 4-stage

**Front:** Studio product shot of a sleek flagship smartphone floating against a dark gradient background, front screen glowing with an abstract wallpaper, soft rim light, subtle reflections, ultra photoreal premium Apple-style product photography, high detail, no text, no visible brand logos, no watermark, wide 16:9 composition with the phone centered.

**Back:** The same smartphone rotated to show its back, premium matte finish, refined dual camera module with glowing lens rings, floating against a dark gradient background, soft rim light, ultra photoreal product photography, no text, no brand logos, no watermark, wide 16:9 composition.

**Exploded:** The same flagship smartphone in a precise exploded technical view, internal components floating apart in mid-air: display panel, battery, dual camera module, logic board and chipset, neatly arranged with glowing accents, dark studio gradient background, premium tech product render, ultra detailed, no text, no brand logos, no watermark, wide 16:9 composition.

**Chipset close-up:** Extreme close-up of the phone's logic board and processor chip at the center, glowing orange circuitry traces lighting up, fine detail, dark studio gradient background, premium tech macro render, no text, no logos, no watermark, wide 16:9 composition.

**Motion prompts:**
- Front → back: The floating phone rotates smoothly from front to back, catching the rim light across its edges, slow controlled spin, studio lighting.
- Back → exploded: The phone elegantly disassembles, screen, battery, camera module, logic board and glowing chipset separating and floating apart into a clean exploded layout, smooth precise motion.
- Exploded → chipset: Camera pushes in slowly through the floating components toward the processor, the chip's circuitry lights up warmly, cinematic macro reveal.

---

## 4. Food — burger

**Exploded layers:** Appetising gourmet cheeseburger deconstructed, its layers floating and exploded apart in mid-air above a luscious plate, stacked in order: glossy sesame brioche top bun, melting cheddar, thick juicy grilled beef patty, crisp lettuce, tomato slice, red onion, bottom bun, hovering with space between each layer, golden crispy fries and the plate on red-and-white checkered paper below, warm studio food-photography light, ultra photoreal, mouthwatering, shallow depth of field, no text, no watermark, wide 16:9 composition.

**Stacked:** The same gourmet cheeseburger fully assembled and stacked on the luscious plate, thick juicy grilled beef patty, melting cheddar, fresh lettuce, tomato and red onion, glossy sesame brioche bun, golden crispy fries beside it on red-and-white checkered paper, warm studio food-photography light, steam rising, ultra photoreal, mouthwatering, shallow depth of field, no text, no watermark, wide 16:9 composition.

**Bite:** A hand holding the same gourmet cheeseburger with one big juicy bite taken out of it, dramatic melting cheese pull, juicy beef and fresh toppings visible at the bite, close up, golden fries and red-and-white checkered paper softly blurred in the background, warm studio food-photography light, ultra photoreal, extremely appetising, shallow depth of field, no text, no watermark, wide 16:9 composition.

**Motion prompts:**
- Exploded → stacked: Appetising food animation, the floating deconstructed burger layers drop and stack together one by one into a fully assembled juicy cheeseburger on the plate, dynamic satisfying motion, warm food lighting.
- Stacked → bite: A hand reaches into frame and picks up the whole juicy cheeseburger off the plate, lifts it up toward the mouth and takes a big bite so the burger rises up briefly, then brings it back down now with a large bite taken out of it and a dramatic melting cheese pull, natural eating motion, mouthwatering close up, warm food lighting. **Use 10 seconds for this one** so the full pick-up-and-bite fits.
