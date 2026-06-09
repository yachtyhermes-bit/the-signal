// /api/tts.mjs — Vercel serverless — Edge TTS Jenny via edge-tts
// edge-tts installed at build time (requirements.txt). Falls back to Google Translate.

import { execSync } from 'child_process';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = req.query.text;
  if (!text || text.length > 5000) {
    return res.status(400).json({ error: 'Text required, max 5000 chars' });
  }

  // Edge TTS Jenny via Python (edge-tts installed at build)
  try {
    const pyScript = `import asyncio,edge_tts,sys
async def gen():
    tts=edge_tts.Communicate(sys.stdin.read(),'en-US-JennyNeural')
    async for c in tts.stream():
        if c['type']=='audio':
            sys.stdout.buffer.write(c['data'])
asyncio.run(gen())`;

    const audio = execSync(`python3 -c '${pyScript}'`, {
      input: text,
      maxBuffer: 2 * 1024 * 1024,
      timeout: 12000
    });

    if (audio && audio.length > 500) {
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      return res.send(audio);
    }
  } catch (e) {
    console.warn('Edge TTS failed, falling back to Google:', e.message?.substring(0, 80));
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
