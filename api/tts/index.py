# /api/tts/ — Vercel Python serverless
# Uses edge-tts (same library that generated your Jenny samples)
import json, io, asyncio
from http.server import BaseHTTPRequestHandler

import edge_tts

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query string
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        text = qs.get('text', [''])[0]
        voice = qs.get('voice', ['en-US-JennyNeural'])[0]
        
        self.send_response(200)
        self.send_header('Content-Type', 'audio/mpeg')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'public, max-age=86400')
        self.end_headers()
        
        if not text or len(text) > 5000:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error":"text required, max 5000"}).encode())
            return
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def gen():
            communicate = edge_tts.Communicate(text, voice)
            chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    chunks.append(chunk["data"])
            return b''.join(chunks)
        
        audio = loop.run_until_complete(gen())
        self.wfile.write(audio)
