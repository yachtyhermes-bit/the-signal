# Video Generation Tool Research — "The Signal"

## Existing Environment (Already Installed)

| Tool | Status | Use |
|------|--------|-----|
| matplotlib 3.10.9 | ✅ Installed | Financial chart generation |
| Pillow 12.2.0 | ✅ Installed | Image composition, text overlays |
| numpy 2.4.4 | ✅ Installed | Data processing |
| requests 2.31.0 | ✅ Installed | API calls, stock data fetching |
| playwright 1.59.0 | ✅ Installed | HTML/CSS screenshot rendering |
| fastapi 0.136.1 | ✅ Installed | API server |
| Node.js v22.22.1 | ✅ Installed | Remotion, Node tools |
| ffmpeg | ✅ Installed | Video encoding, audio mixing |

## Option 1: Custom Python Pipeline — ★ STRONGLY RECOMMENDED

Build a custom video generator using matplotlib+Pillow for frame generation, edge-tts for voiceover, and ffmpeg for video assembly. Zero external API costs.

**Pipeline:**
1. Read article JSON → extract title, summary, ticker, sector, key numbers
2. Generate 4-6 Bloomberg-style frames (dark bg, neon accents)
3. Generate voiceover script from summary + key takeaways
4. edge-tts → natural-sounding TTS audio (free, Microsoft Neural voices)
5. ffmpeg compositing → synchronize frames with voiceover → MP4
6. Generate VideoObject schema markup for SEO

**Cost:** FREE (zero cost per video)
**Voiceover Quality:** 8/10 (Microsoft Neural TTS via edge-tts)
**Visual Quality:** 8/10 (properly styled matplotlib + Pillow)
**Automation:** Fully automatable
**Effort:** 3-5 days to production quality

## Option 2: Remotion (47K⭐ React-based Video Framework)

Full CSS/HTML rendering → pixel-perfect Bloomberg aesthetic. Server-side MP4 output via headless Chrome.

**Cost:** FREE
**Visual Quality:** 9/10 (pixel-perfect CSS)
**Setup:** Medium-High (needs Chromium rendering)
**Note:** You already have Playwright installed, which can do similar HTML→screenshot→video

## Option 3: Manim — NOT RECOMMENDED

Problems: No financial chart primitives, slow Cairo-based rendering, requires LaTeX, output is "mathematical" not "Bloomberg Terminal".

## Option 4: Commercial AI Video Tools — None Fit

Synthesia (0/mo) - Avatar-centric, no stock charts
HeyGen (4/mo) - Avatar-centric, no stock charts
Pictory (9/mo) - Stock footage-based, limited API
Runway ML (2-76/mo) - Unpredictable generative output
None can produce accurate financial data visualizations with guaranteed accuracy.

## Option 5: Open Source Components

edge-tts - FREE, 8/10 quality, pip install edge-tts
ElevenLabs - ~/usr/bin/bash.10-0.50/video, 10/10 quality, pip install elevenlabs
mplfinance - FREE, candlestick/OHLC charts, pip install mplfinance
yfinance - FREE, stock data, pip install yfinance

## Google SEO Requirements

Duration: 30-180s ✅ (60-90s target is ideal)
Thumbnail: 1280x720 minimum
Schema: VideoObject JSON-LD (name, description, thumbnailUrl, uploadDate, contentUrl, duration)
Hosting: Self-host MP4 on domain (better than YouTube embed)
Transcript: Include full video transcript on page

## FINAL RECOMMENDATION: Custom Python Pipeline

Pipeline flow:
  Article JSON → generate_chart.py → generate_frames.py → compose_video.py → MP4
  Article JSON → generate_voiceover.py → audio.wav ↗
                                           → generate_schema.py → JSON-LD

Wins on: zero cost, full visual control, deterministic/reliable output, fully automated, scales to any volume, SEO-optimal (self-hosted MP4 + VideoObject schema).
Optional upgrade: ElevenLabs for premium voiceover (~/usr/bin/bash.10-0.50/video)
