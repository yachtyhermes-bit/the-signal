// /api/tts.mjs — Vercel serverless — Google Translate TTS proxy
// Free, no API key, no rate limits, works from Vercel
// Splits long text into chunks, concatenates MP3 frames

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = req.query.text;
  if (!text || text.length > 5000) {
    return res.status(400).json({ error: 'Text required, max 5000 chars' });
  }

  // Split into Google TTS-friendly chunks (≤ 200 chars, split at word boundaries)
  const chunks = splitText(text, 190);

  try {
    const audioBuffers = [];
    for (const chunk of chunks) {
      const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=${encodeURIComponent(chunk)}`;
      const response = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; VercelBot/1.0)' }
      });
      if (!response.ok) {
        return res.status(502).json({ error: `Google TTS chunk failed: ${response.status}` });
      }
      const buf = Buffer.from(await response.arrayBuffer());
      audioBuffers.push(buf);
    }

    const total = Buffer.concat(audioBuffers);
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    res.setHeader('Content-Length', total.length);
    return res.send(total);
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}

function splitText(text, maxLen) {
  const chunks = [];
  let remaining = text.trim();
  while (remaining.length > maxLen) {
    let splitAt = remaining.lastIndexOf(' ', maxLen);
    if (splitAt <= 0) splitAt = maxLen; // hard split if no space
    chunks.push(remaining.substring(0, splitAt).trim());
    remaining = remaining.substring(splitAt).trim();
  }
  if (remaining) chunks.push(remaining);
  return chunks;
}
