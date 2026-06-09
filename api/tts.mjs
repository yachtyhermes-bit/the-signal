// /api/tts.mjs — Vercel serverless — Edge TTS Jenny voice
// Installs edge-tts at runtime, then shells out to Python helper.
// Falls back to Google Translate on failure.
import { execSync } from 'child_process';
import { writeFileSync, readFileSync, existsSync, unlinkSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

let edgeTtsReady = false;
function ensureEdgeTts() {
  if (edgeTtsReady) return true;
  try {
    execSync('python3 -c "import edge_tts"', { timeout: 3000, stdio: 'pipe' });
    edgeTtsReady = true;
    return true;
  } catch (e) {
    try {
      execSync('pip3 install edge-tts --break-system-packages -q 2>/dev/null', { timeout: 25000, stdio: 'pipe' });
      edgeTtsReady = true;
      return true;
    } catch (e2) {
      console.warn('edge-tts install failed:', e2.message?.substring(0, 80));
      return false;
    }
  }
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = req.query.text;
  if (!text || text.length > 5000) {
    return res.status(400).json({ error: 'Text required, max 5000 chars' });
  }

  // Try Edge TTS Jenny via helper script
  if (ensureEdgeTts()) {
    const tmpPath = join(tmpdir(), `tts_${Date.now()}.txt`);
    try {
      writeFileSync(tmpPath, text);
      const helperPath = join(process.cwd(), 'api', 'edge_tts_helper.py');
      if (existsSync(helperPath)) {
        const cmd = `cat "${tmpPath}" | python3 "${helperPath}" en-US-JennyNeural`;
        const audio = execSync(cmd, {
          maxBuffer: 2 * 1024 * 1024,
          timeout: 18000,
          env: { ...process.env, PYTHONUNBUFFERED: '1' }
        });
        unlinkSync(tmpPath);
        if (audio && audio.length > 500) {
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('Cache-Control', 'public, max-age=86400');
          return res.send(audio);
        }
      }
    } catch (e) {
      try { unlinkSync(tmpPath); } catch (_) {}
      console.warn('Edge TTS helper failed:', e.message?.substring(0, 80));
    }
  }

  // Fallback: Google Translate TTS
  try {
    const chunks = splitText(text, 190);
    const bufs = [];
    for (const chunk of chunks) {
      const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=${encodeURIComponent(chunk)}`;
      const r = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
      if (!r.ok) throw new Error(`status ${r.status}`);
      bufs.push(Buffer.from(await r.arrayBuffer()));
    }
    const total = Buffer.concat(bufs);
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    return res.send(total);
  } catch (e2) {
    return res.status(500).json({ error: 'All TTS backends failed' });
  }
}

function splitText(text, maxLen) {
  const chunks = [];
  let r = text.trim();
  while (r.length > maxLen) {
    let i = r.lastIndexOf(' ', maxLen);
    if (i <= 0) i = maxLen;
    chunks.push(r.substring(0, i).trim());
    r = r.substring(i).trim();
  }
  if (r) chunks.push(r);
  return chunks;
}
