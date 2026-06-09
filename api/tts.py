"""Vercel Python serverless — Edge TTS Jenny (free, no API key)"""
from http.server import BaseHTTPRequestHandler
import asyncio, edge_tts, json, urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        text = params.get('text', [None])[0]

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

        if not text or len(text) > 5000:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Text required, max 5000 chars'}).encode())
            return

        try:
            audio = asyncio.run(_generate(text))
            self.send_header('Content-Type', 'audio/mpeg')
            self.send_header('Cache-Control', 'public, max-age=86400')
            self.send_header('X-TTS-Backend', 'edge-tts-jenny')
            self.send_header('Content-Length', str(len(audio)))
            self.end_headers()
            self.wfile.write(audio)
        except Exception as e:
            err = json.dumps({'error': str(e)})
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(err)))
            self.end_headers()
            self.wfile.write(err.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()

async def _generate(text):
    buf = bytearray()
    tts = edge_tts.Communicate(text, 'en-US-JennyNeural')
    async for chunk in tts.stream():
        if chunk['type'] == 'audio':
            buf.extend(chunk['data'])
    return bytes(buf)
