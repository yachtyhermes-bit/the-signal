// /api/tts.mjs — Vercel serverless — Edge TTS Jenny
// edge-tts installed to api/edge_tts_deps/ during build
// Falls back to Google Translate TTS if unavailable

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = req.query.text;
  if (!text || text.length > 5000) {
    return res.status(400).json({ error: 'Text required, max 5000 chars' });
  }

  // Try Edge TTS Jenny — use local deps dir if available
  try {
    const depsDir = join(process.cwd(), 'api', 'edge_tts_deps');
    const importCheck = existsSync(depsDir) 
      ? `PYTHONPATH="${depsDir}" python3 -c "import edge_tts"`
      : 'python3 -c "import edge_tts"';
    execSync(importCheck, { timeout: 3000, stdio: 'pipe' });

    const pyCode = `import asyncio,edge_tts,sys
async def gen():
    tts=edge_tts.Communicate(sys.stdin.read()[:5000],'en-US-JennyNeural')
    async for c in tts.stream():
        if c['type']=='audio':
            sys.stdout.buffer.write(c['data'])
asyncio.run(gen())`;

    const env = { ...process.env, PYTHONUNBUFFERED: '1' };
    if (existsSync(depsDir)) env.PYTHONPATH = depsDir;

    const audio = execSync(`python3 -c '${pyCode}'`, {
      input: text,
      maxBuffer: 2 * 1024 * 1024,
      timeout: 15000,
      env
    });

    if (audio && audio.length > 500) {
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.setHeader('X-TTS-Backend', 'edge-tts-jenny');
      return res.send(audio);
    }
  } catch (e) {
    console.warn('Edge TTS failed:', e.message?.substring(0, 80));
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
