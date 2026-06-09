#!/usr/bin/env python3
"""Edge TTS helper — reads text from stdin, writes MP3 to stdout."""
import sys, asyncio, edge_tts

async def main():
    text = sys.stdin.read()[:5000]
    voice = sys.argv[1] if len(sys.argv) > 1 else 'en-US-JennyNeural'
    tts = edge_tts.Communicate(text, voice)
    async for chunk in tts.stream():
        if chunk['type'] == 'audio':
            sys.stdout.buffer.write(chunk['data'])

asyncio.run(main())
