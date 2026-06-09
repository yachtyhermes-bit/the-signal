"""Vercel Python serverless — Edge TTS Jenny voice"""
from http.server import BaseHTTPRequestHandler
import asyncio, edge_tts, json, urllib.parse, io

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        text = params.get('text', [None])[0]

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

        if not text or len(text) > 5000:
            body = json.dumps({'error': 'Text required, max 5000 chars'}).encode()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
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
            body = json.dumps({'error': str(e)}).encode()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress logs

async def _generate(text):
    buf = io.BytesIO()
    tts = edge_tts.Communicate(text[:5000], 'en-US-JennyNeural')
    async for chunk in tts.stream():
        if chunk['type'] == 'audio':
            buf.write(chunk['data'])
    return buf.getvalue()
