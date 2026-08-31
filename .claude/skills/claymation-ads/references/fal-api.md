# FAL API reference

All calls go through FAL's queue API with `scripts/fal_run.sh`. Auth is the `FAL_KEY` env var. **Param names below are a starting point — if a model rejects a payload, open its page at `https://fal.ai/models/<model-id>` and check the current input schema before retrying.** Verify current per-call pricing on the same pages once per session and use those numbers in every cost quote.

## Queue mechanics (handled by fal_run.sh)

```
POST https://queue.fal.run/<model-id>        # body: the JSON payload → {request_id, status_url, response_url}
GET  <status_url>                            # poll until status == COMPLETED
GET  <response_url>                          # → result JSON with file URLs to download
```

The queue is server-side — a submitted job survives tool timeouts and killed shells. `fal_run.sh submit` writes the job's URLs to `<state-dir>/<name>.json`; `fal_run.sh poll` resumes from that file in any later tool call (exit 2 means still running — just call poll again). Use submit/poll for every image and clip generation; the one-shot form is for fast jobs like TTS.

Local files (packshot, masters, stills) must be publicly reachable URLs for reference inputs. Upload them first via FAL's storage endpoint (`fal_run.sh --upload <file>` handles this and prints the URL). Upload each file once per project and cache the URL in the project folder — re-uploading identical files wastes time.

## Models

### Style lock — `openai/gpt-image-2` (text-to-image)

```json
{ "prompt": "...", "image_size": "portrait_16_9" }
```

`image_size` is an ENUM, not pixel dimensions (schema changed 2026-08: `"1024x1536"` now 422s). Valid: `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`, `auto`. Vertical ads use `portrait_16_9`.

### Masters & keyframes — `openai/gpt-image-2/edit`

```json
{ "prompt": "...", "image_urls": ["<ref1>", "<ref2>", "..."], "image_size": "portrait_16_9" }
```

Observed pricing 2026-08: ~$0.06–0.11/image at medium quality, portrait — still verify per session.

Reference order carries authority: masters first, previous still next, packshot always LAST.

### Clips — `google/gemini-omni-flash/reference-to-video`

```json
{ "prompt": "...", "image_urls": ["<still-N>", "<still-N+1>"], "duration": "4", "aspect_ratio": "9:16", "resolution": "720p" }
```

There is no end-frame parameter — the second reference image is bound to the final frame by the prompt contract (see prompts.md). Duration stays "4": scene timing is enforced at assembly from measured VO durations, not at generation.

Two facts learned in production (2026-08):
- **Omni clips contain their own AAC audio track.** Any downstream mux MUST use explicit stream mapping (`-map 0:v:0 -map 1:a:0`) or ffmpeg silently prefers the clip's audio over the narration — the symptom is an ad with no VO until the final still-held segment. assemble.sh now maps explicitly; keep that if you ever hand-roll ffmpeg here.
- Observed pricing: ~$0.13/second at 720p → ~$0.52 per 4s clip. Verify per session.

### Voiceover — ElevenLabs via FAL (stock voices)

Confirmed working route (2026-08): `fal-ai/elevenlabs/tts/eleven-v3`. Payload is text + stock voice name; "Brian" is a good deep authoritative ad read. If the route 404s, probe siblings (`.../tts/multilingual-v2`, `.../tts/turbo-v2.5`) or search fal.ai.

```json
{ "text": "the narration line", "voice": "Brian" }
```

**Voice clones cannot resolve through FAL** — FAL calls ElevenLabs on FAL's own account, so a voice cloned in the user's ElevenLabs account does not exist there. If the user has `ELEVENLABS_API_KEY` and a clone, call ElevenLabs directly instead:

```
POST https://api.elevenlabs.io/v1/text-to-speech/<voice_id>
  header: xi-api-key: $ELEVENLABS_API_KEY
  body: { "text": "...", "model_id": "eleven_v3" }
```

## Cost quoting

Before each paid batch print: `<count> × $<per-call> = $<total>` with prices read from the model pages this session. A typical 10-scene ad is ~13 images (1 lock + 2-3 masters + 10 stills, plus repairs) and 9 clips; clips dominate the total.
