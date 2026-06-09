// /api/tts.mjs — Vercel serverless — proxies text → Edge TTS Jenny voice
// Free, no API key, no rate limits

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = req.query.text;
  if (!text || text.length > 5000) {
    return res.status(400).json({ error: 'Text required, max 5000 chars' });
  }

  const voice = req.query.voice || 'en-US-JennyNeural';
  const rate = req.query.rate || '+0%';

  const ssml = `<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
    xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="${escapeXml(voice)}">
      <prosody rate="${escapeXml(rate)}" pitch="+0Hz">
        ${escapeXml(text)}
      </prosody>
    </voice>
  </speak>`;

  try {
    const response = await fetch(
      'https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1?TrustedClientToken=6A5AA1D4EAFF4E9FB37E23D68491D6F4',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/ssml+xml',
          'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
          'Accept': '*/*',
          'Origin': 'chrome-extension://jdkknkkbebbapilgoeccciglkfbmbnfm',
        },
        body: ssml,
      }
    );

    const status = response.status;
    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('audio')) {
      const audio = await response.arrayBuffer();
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      return res.send(Buffer.from(audio));
    }

    // Edge returned error
    const errBody = await response.text();
    return res.status(502).json({ error: 'Edge TTS returned non-audio', status, contentType, body: errBody.substring(0, 200) });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}

function escapeXml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}
