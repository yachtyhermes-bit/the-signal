import fs from 'fs';
import path from 'path';
import https from 'https';

const imgPath = process.argv[2];
const extraQ = process.argv[3] || '';

// load OPENROUTER_API_KEY: env first, then fall back to hermes env files
let KEY = process.env.OPENROUTER_API_KEY || null;
const candidates = ['/home/chino/.hermes/.env', '/home/chino/.hermes/profiles/yachty/.env'];
if (!KEY) {
  for (const p of candidates) {
    if (!fs.existsSync(p)) continue;
    for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
      if (line.trim().startsWith('OPENROUTER_API_KEY=')) {
        const v = line.split('=').slice(1).join('=').trim().replace(/^["']|["']$/g, '');
        if (v.length > 20) { KEY = v; break; }
      }
    }
    if (KEY) break;
  }
}
if (!KEY) { console.error('no key'); process.exit(1); }

const b64 = fs.readFileSync(imgPath).toString('base64');

const question = `You are a photo editor QC-ing an editorial hero image. Be brutally literal and concise.

1) Describe exactly what this image shows (main subject, setting, lighting, any people).
2) Is it a real-looking press photograph, or does it look like a CGI/3D render/digital art? Say which.
3) Is there ANY text visible anywhere — letters, words, numbers, labels, signage, logos, brand names, screen content, UI? Quote exactly what you see, or say "NO TEXT".
4) Any of these present: data center, server room, server racks, server aisles, cable runs, GPU hardware, neon/synthwave, glowing lines, abstract geometric patterns, HUD overlays?
5) Does it plausibly show a semiconductor fab lithography area / chip manufacturing?
${extraQ}
Answer in plain numbered lines. Do not be polite.`;

const payload = JSON.stringify({
  model: process.env.MODEL || 'google/gemini-2.5-flash',
  messages: [{ role: 'user', content: [
    { type: 'text', text: question },
    { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
  ]}],
  max_tokens: 600
});

const req = https.request({
  hostname: 'openrouter.ai',
  path: '/api/v1/chat/completions',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${KEY}`,
    'HTTP-Referer': 'https://readthesignal.net',
    'X-Title': 'The Signal Hero QC'
  }
}, res => {
  let body = '';
  res.on('data', c => body += c);
  res.on('end', () => {
    try {
      const j = JSON.parse(body);
      if (j.error) console.log('API ERROR: ' + (j.error.message || JSON.stringify(j.error)));
      else console.log(j.choices[0].message.content.trim());
    } catch (e) { console.log('PARSE: ' + e.message + ' ' + body.slice(0, 300)); }
  });
});
req.on('error', e => console.log('REQ ERR: ' + e.message));
req.write(payload);
req.end();
