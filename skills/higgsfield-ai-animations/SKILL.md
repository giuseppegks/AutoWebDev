---
name: Higgsfield-AI-Animations
description: Use when you need to generate AI-powered video animations via Higgsfield's developer API (cloud.higgsfield.ai) — single-shot image-to-video from a real photo, illustrated brand-style loops (watercolor / Pixar / LEGO / Ghibli), or multi-scene narrative mini-stories stitched with ffmpeg. Covers auth setup with API key + secret, image hosting via catbox.moe, model selection (Soul for text-to-image, Kling/DoP/Seedance for image-to-video), parallel job submission, polling patterns, ffmpeg xfade stitching, character-consistency prompts across scenes, and HTML integration patterns (autoplay hero loops vs click-to-play story sections). Triggers on phrases like "animate this photo with Higgsfield", "make an AI video for [client]", "Pixar story animation", "create an illustrated hero loop", "multi-scene narrative video", "Higgsfield image-to-video", "image-to-video pipeline".
---

# Higgsfield AI Animations — Workflow Skill

## Overview

Reusable workflow for generating premium AI video content using Higgsfield's developer API. Three production patterns are covered:

- **Pattern A — Photo → Video:** real client photo gets a subtle 5-sec animated loop
- **Pattern B — Illustrated brand loop:** text-to-image then image-to-video, fully styled (watercolor, Pixar, LEGO, etc.)
- **Pattern C — Multi-scene narrative:** 3-5 scenes stitched into a 15-25 sec mini-story with smooth cross-fades

Plus a fourth pattern for **integrating the output into a website** (autoplay hero loops vs click-to-play story sections, with mobile fallbacks).

**Two Higgsfield products — pick the right one:**

| | higgsfield.ai (consumer) | cloud.higgsfield.ai (developer) |
|---|---|---|
| Auth | OAuth browser flow (`higgsfield auth login`) | API key + secret |
| CLI | Official `@higgsfield/cli` + MCP integration with Claude Code | Use `curl` directly |
| Credits | Subscription / in-app | Pay-per-use, separate balance |
| Best for | Casual + MCP-conversational use | Scripted, repeatable, multi-step pipelines |

**This skill uses the developer API path.** If the user has bought credits on cloud.higgsfield.ai (most common for scripted work), that's where their money is — don't mix it up with the consumer CLI's separate credit pool.

## When to Use

- Client website needs more life in the hero than a static photo
- Brand-stylized animation (illustrated / cartoon / cinematic) matching the site palette
- "How it works" / "our story" mini-narrative video for a service business
- Prospect-mockup with a "wow factor" beyond Pexels stock
- Marketing reels / social cuts derived from website assets

**Skip when:**
- Client already has high-quality original video/photo of their real space — don't replace authentic content with AI
- Budget < ~€10 USD (a 15-sec narrative burns ~€5-8 in credits)
- Compliance-sensitive industries (medical, financial) where AI content erodes trust
- The animation would be the ONLY animated thing on an otherwise static site (looks like a one-off gimmick)

## Setup (one-time per machine)

### 1. Get API credentials from cloud.higgsfield.ai

Settings → API Keys → Generate new key. You get a UUID-style **key** and a long hex **secret**. The secret is shown ONCE — copy it immediately.

### 2. Save to a creds file with locked permissions

Run in the user's own terminal (NOT in Claude Code chat, to keep keys out of conversation history):

```bash
cat > ~/.higgsfield-creds << EOF
HF_KEY=<your-uuid-key>
HF_SECRET=<your-long-hex-secret>
EOF
chmod 600 ~/.higgsfield-creds
```

Verify with `ls -la ~/.higgsfield-creds` — should show `-rw-------` (only user readable).

### 3. Tools you'll need locally

- `curl` (always installed on macOS/Linux)
- `python3` (for clean JSON parsing in the pipeline)
- `ffmpeg` for Pattern C — install with `brew install ffmpeg` if missing

### 4. Honest security note for the user

API key in a chat is a liability — anything in the conversation could end up in screenshots, support tickets, or training logs. Best practice:
- Generate a **dedicated key per project** (label it `claude-temp-{date}`)
- Revoke immediately after the session ends
- Max blast radius is whatever balance is on the account (often €30-50, capped)

## API Reference (essentials)

**Base URL:** `https://platform.higgsfield.ai/`

**Auth header:** `Authorization: Key {key}:{secret}` (colon-separated, NOT Bearer)

**Submit pattern (all models):**
```bash
curl -X POST "https://platform.higgsfield.ai/{model_id}" \
  --header "Authorization: Key ${HF_KEY}:${HF_SECRET}" \
  --header 'Content-Type: application/json' \
  --data '{"prompt": "...", ...}'
```

Returns:
```json
{
  "status": "queued",
  "request_id": "uuid-here",
  "status_url": "https://platform.higgsfield.ai/requests/{id}/status",
  "cancel_url": "..."
}
```

**Poll pattern:**
```bash
curl "${STATUS_URL}" --header "Authorization: Key ${HF_KEY}:${HF_SECRET}"
```

Statuses: `queued` → `in_progress` → `completed` (or `failed` / `nsfw`).

**Known model IDs (verified working):**

| Purpose | Model ID | Notes |
|---|---|---|
| Text-to-image | `higgsfield-ai/soul/standard` | Accepts: `prompt`, `aspect_ratio` (e.g. "16:9"), `resolution` ("1080p") |
| Image-to-video (cinematic) | `kling-video/v2.1/pro/image-to-video` | Best for stylized + photo, 5 sec output, slowest (~70-90s) |
| Image-to-video (DoP) | `higgsfield-ai/dop/standard` | Valid variants: `lite`, `standard`, `turbo`, `*/first-last-frame` |

**Pitfalls:**
- `bytedance/seedance/v1/pro/image-to-video` was 404 at time of writing — verify availability before using
- `higgsfield-ai/dop/preview` is NOT valid (will return 422 with valid options)
- A 500 Internal Server Error sometimes happens on first call to a model — retry once before assuming the model ID is wrong

## Pattern A — Photo → 5-sec animated loop

**Use for:** turning a real client photo into a subtle hero animation.

### Steps

1. **Make the photo accessible via a public URL.** Higgsfield needs to fetch it. Free options:

   ```bash
   IMG_URL=$(curl -sS -F "reqtype=fileupload" -F "fileToUpload=@/path/to/photo.jpg" \
     -H "User-Agent: curl/8" https://catbox.moe/user/api.php)
   echo "$IMG_URL"  # https://files.catbox.moe/xxxxx.jpg
   ```

   `0x0.st` has uploads disabled (AI bot abuse). Catbox is the working alternative as of late 2026.

2. **Submit the generation:**
   ```bash
   source ~/.higgsfield-creds
   curl -X POST "https://platform.higgsfield.ai/kling-video/v2.1/pro/image-to-video" \
     --header "Authorization: Key ${HF_KEY}:${HF_SECRET}" \
     --header 'Content-Type: application/json' \
     --data "{\"image_url\": \"${IMG_URL}\", \"prompt\": \"Subtle breathing motion, gentle eye blinks, no camera movement, warm cinematic atmosphere\"}"
   ```

3. **Poll until done** (template in "Polling helper" below).

4. **Download the result MP4.**

**Prompt guidance:** keep it subtle for hero loops. Camera-locked, breathing/blinking only, "no camera movement" explicitly. Big camera moves on a hero loop are nauseating after 3 plays.

## Pattern B — Brand-style illustrated loop

**Use for:** when you want a styled illustration that matches the site's design language, not a photo.

### Steps

1. **Generate an illustration with Soul** (text-to-image):
   ```bash
   source ~/.higgsfield-creds
   PROMPT="Soft watercolor children's book illustration of [scene description], picture book art, gentle line work, warm palette, [brand colors], no text"

   curl -X POST "https://platform.higgsfield.ai/higgsfield-ai/soul/standard" \
     --header "Authorization: Key ${HF_KEY}:${HF_SECRET}" \
     --header 'Content-Type: application/json' \
     --data "$(python3 -c "import json; print(json.dumps({'prompt': '''$PROMPT''', 'aspect_ratio': '16:9', 'resolution': '1080p'}))")"
   ```

2. **Poll → get the illustration's CDN URL.**

3. **Pass that URL into Kling** for animation (same call as Pattern A, just with the illustration URL).

**Style prompt presets (verified results):**

| Style | Key phrases |
|---|---|
| Watercolor picture-book | `"Soft watercolor children's book illustration", "picture book art", "gentle line work", "warm pastel colors"` |
| Pixar 3D cinematic | `"Pixar 3D animation style cinematic scene", "emotional Pixar quality", "expressive faces", "soft warm natural lighting"` |
| LEGO Movie | `"Cinematic LEGO Movie scene", "brick-built", "minifigure", "glossy plastic LEGO surface", "stop-motion style"` |
| Studio Ghibli | `"Studio Ghibli hand-painted style", "soft anime watercolor", "Miyazaki atmosphere", "warm dreamy lighting"` |
| Flat 2D motion-graphics | `"Flat 2D vector illustration", "bold simple shapes", "bright cheerful colors", "modern motion graphics aesthetic"` |

## Pattern C — Multi-scene narrative

**Use for:** a 15-25 sec mini-story that arcs across multiple scenes (e.g., problem → process → resolution).

### Architecture

```
3-5 scenes → 3-5 Soul images (run in parallel) → 3-5 Kling videos (run in parallel) → ffmpeg xfade concat → single MP4
```

### Critical: character consistency

The hardest problem in multi-scene AI video is keeping characters looking the same across independent generations. Solution: **paste an identical character description block in every prompt.**

```bash
CHARS="a young woman veterinarian with long brown hair in a ponytail, round black glasses, and a clean white doctor's coat, a young man with short brown hair wearing a casual blue shirt, and a brown short-haired friendly dog with a kind face"

P1="$CHARS in a [scene 1 context with specific actions and emotions]"
P2="$CHARS in [scene 2 context]"
P3="$CHARS in [scene 3 context]"
```

The more concrete the character description (hair color + length + accessory + outfit details), the better the cross-scene consistency. Soul respects these specs surprisingly well.

### Parallel submit + poll (shell template)

```bash
source ~/.higgsfield-creds

# Submit 3 Soul jobs in parallel, save request IDs
for n in 1 2 3; do
  prompt_var="P$n"
  ( resp=$(curl -sS -X POST "https://platform.higgsfield.ai/higgsfield-ai/soul/standard" \
      --header "Authorization: Key ${HF_KEY}:${HF_SECRET}" \
      --header 'Content-Type: application/json' \
      --data "$(python3 -c "import json,os; print(json.dumps({'prompt': os.environ['P'], 'aspect_ratio': '16:9', 'resolution': '1080p'}))" P="${!prompt_var}")")
    echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin)['request_id'])" > "/tmp/soul-$n.txt"
  ) &
done
wait

# Poll all 3 in parallel
poll_one() {
  local id="$1"; local label="$2"
  for i in $(seq 1 30); do
    local resp=$(curl -sS "https://platform.higgsfield.ai/requests/${id}/status" \
      --header "Authorization: Key ${HF_KEY}:${HF_SECRET}")
    local st=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','?'))")
    if [ "$st" = "completed" ]; then
      echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin)['images'][0]['url'])" > "/tmp/img-$label.txt"
      return 0
    fi
    [ "$st" = "failed" ] || [ "$st" = "nsfw" ] && return 1
    sleep 5
  done
}

for n in 1 2 3; do poll_one "$(cat /tmp/soul-$n.txt)" "$n" & done
wait
```

Same pattern repeats for Kling submissions (in parallel) + Kling polls.

### Stitching with ffmpeg xfade

Once all N MP4s are downloaded (typically 5 sec each):

```bash
# For 3 clips of 5 sec each with 0.5s cross-fade overlap → final length = 5 + 4.5 + 4.5 = 14 sec
ffmpeg -y \
  -i scene-1.mp4 -i scene-2.mp4 -i scene-3.mp4 \
  -filter_complex "
    [0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v01];
    [v01][2:v]xfade=transition=fade:duration=0.5:offset=9.0[v]
  " \
  -map "[v]" -an -c:v libx264 -pix_fmt yuv420p -preset slow -crf 22 story.mp4
```

**xfade offset formula:** offset[n] = `(clip_duration × n) - (fade_duration × n)`. For 5-sec clips with 0.5s fades:
- 2 clips: offset = 4.5
- 3 clips: offsets = 4.5, 9.0
- 4 clips: offsets = 4.5, 9.0, 13.5
- 5 clips: offsets = 4.5, 9.0, 13.5, 18.0

**Other xfade transition options:** `fade`, `wipeleft`, `wiperight`, `slideleft`, `circleopen`, `radial`, `dissolve`. Default `fade` is safest for emotional content.

## Pattern D — Website integration

### Autoplay hero loop (Pattern A or B output)

```html
<div class="reveal-img relative overflow-hidden rounded-[40px] aspect-[16/9] shadow-2xl bg-{soft-fallback-color}">
  <video
    autoplay
    loop
    muted
    playsinline
    preload="auto"
    poster="images/hero-poster.png"
    class="w-full h-full object-cover">
    <source src="images/hero-loop.mp4" type="video/mp4">
    <img src="images/hero-poster.png" alt="..." class="w-full h-full object-cover" />
  </video>
</div>
```

**Critical attributes:**
- `muted` — required for `autoplay` on most browsers (Chrome, Safari)
- `playsinline` — prevents iOS fullscreen takeover
- `loop` — for ambient hero use
- `preload="auto"` — start downloading immediately (acceptable for hero, since user is here for it)
- `poster` — shown until video starts; **match first frame of video** for clean handoff
- `bg-{fallback-color}` on container — avoids ugly black flash during load

### Story video section (Pattern C output)

```html
<section>
  <div class="text-center mb-10">
    <p class="kicker">Hoe wij werken</p>
    <h2 class="display-heading">Een klein verhaal over <em>zorg.</em></h2>
    <p>Short intro to set context for what they're about to watch.</p>
  </div>
  <div class="overflow-hidden rounded-[32px] shadow-xl aspect-[16/9]">
    <video controls preload="metadata" poster="images/story-poster.png" class="w-full h-full">
      <source src="images/story.mp4" type="video/mp4">
    </video>
  </div>
  <p class="text-center text-xs mt-5">14 sec · {Style} animation, made for {Client}</p>
</section>
```

**Key differences from hero:**
- `controls` instead of `autoplay loop muted` (story content needs viewer intent)
- `preload="metadata"` only (lighter — story video is heavier, no need to download until they click)
- Centered layout, narrower max-width (~960px) for focused viewing

### Loop transition gotcha

Multi-scene narratives have an **abrupt jump** when looping (end of story → beginning, no cross-fade). For autoplay-loop heroes:
- Accept the jump (most users won't watch full loops anyway)
- OR generate an extra "tail" scene that fades back to scene 1 in ffmpeg
- OR use single-scene Pattern B for hero, save Pattern C for click-to-play sections

## Prompt Engineering Cheatsheet

### For Soul (text-to-image)

- Specify aspect ratio explicitly in prompt AND in the `aspect_ratio` param ("16:9 cinematic frame")
- Avoid text-in-image requests (Soul is unreliable) — use "no text" explicit
- For consistency across runs: lock down lighting + camera + color palette in every prompt
- Resolution `1080p` is the sweet spot — `720p` is noticeably soft

### For Kling (image-to-video)

- Describe what *moves*, not what *is* (the image already shows what is)
- "Subtle [X]" is safer than "dynamic [X]" — over-prompting often produces glitchy motion
- "No camera movement" explicitly if you want a locked-off shot
- Don't ask for things the image doesn't support (e.g., character walking off-frame from a stationary close-up)
- For emotional scenes: `"emotional acting"`, `"expressive face"`, `"subtle eye blinks"` work well
- For dynamic scenes: `"slight handheld camera motion"`, `"warm light shifts"`, `"bouncy energy"`

### Animation prompt structure (template)

```
[Style] [subject motion]: [what main character does], [what secondary character does],
[what environment does], [camera instruction], [lighting/atmosphere]
```

Example:
```
Pixar joyful dynamic animation: the brown dog bounces excitedly up and down with ears
flopping, the veterinarian smiles broadly and extends the treat, the man laughs with
relief raising his hands, slight subtle camera motion, warm golden hour lighting
```

## Cost Awareness

Approximate as of late 2026 (verify in cloud.higgsfield.ai dashboard before quoting clients):

| Operation | ~Cost |
|---|---|
| Soul image (1080p, 16:9) | ~$0.05-0.15 |
| Kling-pro 5-sec image-to-video | ~$1.00-2.00 |
| DoP image-to-video | varies by variant (lite cheapest) |

**Project cost estimates:**
- Pattern A (single Kling): ~$1-2
- Pattern B (Soul + Kling): ~$1.50-2.50
- Pattern C (3 scenes): ~$5-8 (3× Soul + 3× Kling)
- Pattern C (5 scenes): ~$8-12

The account-level pricing endpoint is **not exposed** to API key auth — users must check the cloud.higgsfield.ai dashboard for their actual balance. Don't promise "free credits" or specific amounts unless verified.

## Pitfalls & Fallbacks

### Image hosting

| Service | Status (late 2026) | Notes |
|---|---|---|
| catbox.moe | ✅ Working | Anonymous, requires `User-Agent` header, indefinite hosting |
| 0x0.st | ❌ Disabled | "AI botnet spam" — uploads off, no ETA for return |
| file.io | ⚠️ Single-download | Higgsfield needs to fetch the URL, but file.io deletes after first download — race condition |
| tmpfiles.org | ⚠️ Untested in this skill | Backup option |

### Shell gotchas

- **zsh `read`** differs from bash: use `read "var?prompt"` not `read -p "prompt" var`
- **`printf` with embedded `%s`** can fail when user data has format specifiers — use Python's `json.dumps` to safely encode prompts
- **Read-only variables**: zsh reserves `status` — use `st` or `result` instead

### API gotchas

- 500 on first call to a model — retry once before debugging the prompt
- 422 with `enum` validation error tells you valid variants (read the `expected` field carefully)
- Polling too fast (< 3 sec) won't get faster results — set 5-10 sec intervals
- `image_url` must be publicly accessible AND return Content-Type starting with `image/`

### ffmpeg gotchas

- xfade requires both inputs to have **matching dimensions** — Kling outputs are 1280×720 at 24fps consistently, so this rarely bites
- `-pix_fmt yuv420p` is critical for web playback — without it, some browsers won't decode
- Don't use `-c:v copy` with xfade (xfade re-encodes; copy mode breaks)

### Loop-friendliness

For seamless loop output (Pattern C → autoplay hero), generate an explicit "loop-bridge" frame:
- After scene N, regenerate a final Kling from scene-N-last-frame → scene-1-first-frame using DoP's `first-last-frame` variant
- Concat that bridge as the last clip — now end→start is smooth

## Optional: MCP Integration

For interactive Claude Code sessions where the user wants to *describe* what they want and have it generate inline (no curl), install Higgsfield's MCP server:

```bash
npm install -g @higgsfield/cli
higgsfield auth login    # OAuth — uses CONSUMER credits, separate from API
npx skills add higgsfield-ai/skills    # adds MCP server to Claude Code
```

**Important:** the MCP server uses Higgsfield's CONSUMER auth (OAuth), NOT the developer API key. The credit pools are SEPARATE. If the user has only bought credits on cloud.higgsfield.ai (developer side), the MCP route won't have credit. Use the API-key + curl path documented above instead.

## Polling helper (reusable across all patterns)

```bash
poll_until_done() {
  local id="$1"
  local kind="${2:-video}"  # "image" or "video"
  local url="https://platform.higgsfield.ai/requests/${id}/status"
  for i in $(seq 1 60); do
    local resp=$(curl -sS "$url" --header "Authorization: Key ${HF_KEY}:${HF_SECRET}")
    local st=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','?'))")
    if [ "$st" = "completed" ]; then
      if [ "$kind" = "image" ]; then
        echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin)['images'][0]['url'])"
      else
        echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin)['video']['url'])"
      fi
      return 0
    fi
    if [ "$st" = "failed" ] || [ "$st" = "nsfw" ]; then
      echo "$resp" >&2; return 1
    fi
    sleep 8
  done
  return 1
}
```

Usage: `URL=$(poll_until_done "$request_id" video)` or `URL=$(poll_until_done "$request_id" image)`.

## Verify-before-publish checklist

- [ ] **All MP4s downloaded locally** — don't rely on Higgsfield CDN URLs for production (uncertain TTL)
- [ ] **Cache headers in deploy config** (e.g. Vercel `vercel.json`): `Cache-Control: public, max-age=31536000, immutable` for `/images/*.mp4`
- [ ] **Poster image matches first video frame** for smooth load transition
- [ ] **Fallback `<img>` inside `<video>`** for browsers blocking video
- [ ] **`muted` attribute present** if `autoplay` is set (else Chrome/Safari block playback)
- [ ] **File size sanity check**: 5-sec Kling-pro output is ~6-10 MB; if you see <1 MB or >20 MB, something went wrong
- [ ] **Mobile data warning** if total video assets >15 MB on a page — consider compression with `ffmpeg -crf 28` or 720p variants for mobile

## Cleanup

After project ends:
1. **Revoke the API key** in cloud.higgsfield.ai dashboard
2. `rm ~/.higgsfield-creds` (or move to encrypted backup)
3. Remove temp uploads from catbox.moe (manual on their site, if privacy matters)
4. Higgsfield CDN URLs eventually expire — production builds must use downloaded local copies
