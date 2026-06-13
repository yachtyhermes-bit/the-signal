// /api/tts.mjs — Vercel serverless — Edge TTS Jenny ← R2 cache
// Generates Jenny audio via edge-tts (Python), caches in R2
import { execSync, spawnSync } from 'child_process';
import fs from 'fs';

const CF_ACCOUNT_ID = process.env.CF_ACCOUNT_ID;
const CF_API_TOKEN = process.env.CF_API_TOKEN;
const BUCKET = 'the-signal-audio';
const VOICE = 'en-US-JennyNeural';
const TMP = '/tmp';

let edgeTTSInstalled = false;

function ensureEdgeTTS() {
  if (edgeTTSInstalled) return true;
  if (fs.existsSync(`${TMP}/edge_tts_done`)) {
    edgeTTSInstalled = true;
    return true;
  }
  try {
    const r = spawnSync('pip3', [
      'install', '--target', `${TMP}/edge_tts_deps`, 'edge-tts',
      '--break-system-packages', '-q'
    ], { timeout: 60000, stdio: 'pipe' });
    if (r.status === 0) {
      fs.writeFileSync(`${TMP}/edge_tts_done`, 'ok');
      edgeTTSInstalled = true;
      console.log('edge-tts installed to /tmp');
      return true;
    }
    console.error('pip3 install failed:', r.stderr?.toString().substring(0, 200));
    return false;
  } catch (e) {
    console.error('pip3 error:', e.message);
    return false;
  }
}

function genEdgeTTS(text) {
  ensureEdgeTTS();
  const pyCode = `import sys;sys.path.insert(0,'${TMP}/edge_tts_deps')
import asyncio,edge_tts
async def g():
    tts=edge_tts.Communicate(sys.stdin.read()[:5000],'${VOICE}')
    async for c in tts.stream():
        if c['type']=='audio':sys.stdout.buffer.write(c['data'])
asyncio.run(g())`;
  try {
    const audio = execSync(`python3 -c '${pyCode}'`, {
      input: text,
      maxBuffer: 2 * 1024 * 1024,
      timeout: 15000
    });
    return audio?.length > 500 ? audio : null;
  } catch (e) {
    console.error('Edge TTS gen error:', e.message?.substring(0, 100));
    return null;
  }
}

async function fetchFromR2(slug) {
  if (!CF_ACCOUNT_ID || !CF_API_TOKEN) return null;
  try {
    const r = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/r2/buckets/${BUCKET}/objects/v2/${slug}.mp3`,
      { headers: { 'Authorization': `Bearer ${CF_API_TOKEN}` } }
    );
    if (!r.ok) return null;
    return Buffer.from(await r.arrayBuffer());
  } catch { return null; }
}

async function uploadToR2(slug, audio) {
  if (!CF_ACCOUNT_ID || !CF_API_TOKEN) return;
  try {
    await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/r2/buckets/${BUCKET}/objects/v2/${slug}.mp3`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${CF_API_TOKEN}`,
          'Content-Type': 'audio/mpeg'
        },
        body: audio
      }
    );
  } catch (e) {
    console.error('R2 upload error:', e.message);
  }
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = req.query.text;
  const slug = req.query.slug;
  if (!text || text.length > 5000) {
    return res.status(400).json({ error: 'Text required, max 5000 chars' });
  }

  // If slug provided: try R2 cache, generate + cache if missing
  if (slug) {
    const cached = await fetchFromR2(slug);
    if (cached) {
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.setHeader('X-TTS-Backend', 'r2-jenny');
      return res.send(cached);
    }

    // Generate Jenny audio
    const jennyAudio = genEdgeTTS(text);
    if (jennyAudio) {
      uploadToR2(slug, jennyAudio); // fire-and-forget cache
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.setHeader('X-TTS-Backend', 'edge-tts-jenny');
      return res.send(jennyAudio);
    }
  }

  // Fallback: Google Translate
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
    res.setHeader('X-TTS-Backend', 'google-translate');
    return res.send(total);
  } catch (e2) {
    return res.status(500).json({ error: e2.message });
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
