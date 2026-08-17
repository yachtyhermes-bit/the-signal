// /api/tts.mjs — Vercel serverless — Edge TTS Andrew ← R2 cache
// Generates Andrew audio via edge-tts (Python), caches in R2
import { execSync, spawnSync } from 'child_process';
import fs from 'fs';

// Env var resolution: prefer non-empty values. Handles Vercel env where
// CF_ACCOUNT_ID may be set to "" (empty string) masking the real CLOUDFLARE_ACCOUNT_ID.
function envVal(...keys) {
  for (const k of keys) {
    const v = process.env[k];
    if (v && v.trim()) return v.trim();
  }
  return '';
}
const CF_ACCOUNT_ID = envVal('CF_ACCOUNT_ID', 'CLOUDFLARE_ACCOUNT_ID');
const CF_API_TOKEN = envVal('CF_API_TOKEN', 'CLOUDFLARE_API_TOKEN');
const BUCKET = 'the-signal-audio';
const PRIMARY_VOICE = 'en-US-AndrewNeural';
const FALLBACK_VOICES = ['en-US-JennyNeural', 'en-US-GuyNeural', 'en-GB-SoniaNeural'];
const MAX_TTS_RETRIES = 3;
const TMP = '/tmp';
// R2 key prefixes to try — supports both new (v2/) and legacy (root) uploads
const R2_PREFIXES = ['v2/', ''];

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

function genEdgeTTS(text, voice) {
  ensureEdgeTTS();
  const pyCode = `import sys;sys.path.insert(0,'${TMP}/edge_tts_deps')
import asyncio,edge_tts
async def g():
    tts=edge_tts.Communicate(sys.stdin.read()[:5000],'${voice || PRIMARY_VOICE}')
    async for c in tts.stream():
        if c['type']=='audio':sys.stdout.buffer.write(c['data'])
asyncio.run(g())`;
  for (let attempt = 1; attempt <= MAX_TTS_RETRIES; attempt++) {
    try {
      const audio = execSync(`python3 -c '${pyCode}'`, {
        input: text,
        maxBuffer: 10 * 1024 * 1024,
        timeout: 120000
      });
      if (audio?.length > 500) return audio;
      console.error(`Edge TTS too small (${audio?.length || 0} bytes), attempt ${attempt}/${MAX_TTS_RETRIES}`);
    } catch (e) {
      console.error(`Edge TTS attempt ${attempt}/${MAX_TTS_RETRIES} (${voice || PRIMARY_VOICE}):`, e.message?.substring(0, 100));
    }
    if (attempt < MAX_TTS_RETRIES) {
      const wait = Math.pow(2, attempt) * 1000;
      const start = Date.now();
      while (Date.now() - start < wait) { /* busy-spin — execSync in sh */ }
    }
  }
  return null;
}

async function genTTSWithFallback(text) {
  const voices = [PRIMARY_VOICE, ...FALLBACK_VOICES];
  for (const voice of voices) {
    const audio = genEdgeTTS(text, voice);
    if (audio) {
      return audio;
    }
    console.error(`Voice ${voice} exhausted all retries, trying next voice`);
  }
  console.error('All TTS voices exhausted');
  return null;
}

async function fetchFromR2(slug) {
  if (!CF_ACCOUNT_ID || !CF_API_TOKEN) return null;
  // Try all known key prefixes (v2/ for new uploads, root for legacy)
  for (const prefix of R2_PREFIXES) {
    try {
      const key = `${prefix}${slug}.mp3`;
      const r = await fetch(
        `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/r2/buckets/${BUCKET}/objects/${encodeURIComponent(key)}`,
        { headers: { 'Authorization': `Bearer ${CF_API_TOKEN}` } }
      );
      if (r.ok) {
        return Buffer.from(await r.arrayBuffer());
      }
    } catch { /* try next prefix */ }
  }
  return null;
}

async function uploadToR2(slug, audio) {
  if (!CF_ACCOUNT_ID || !CF_API_TOKEN) return;
  try {
    const key = `v2/${slug}.mp3`;
    await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/r2/buckets/${BUCKET}/objects/${encodeURIComponent(key)}`,
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

  // If slug provided: try R2 cache → local static fallback → generate + cache
  if (slug) {
    const cached = await fetchFromR2(slug);
    if (cached) {
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.setHeader('X-TTS-Backend', 'r2-jenny');
      return res.send(cached);
    }

    // Fallback: pre-generated MP3 from local public/audio/ directory
    try {
      const fs = await import('fs');
      const possiblePaths = [
        `/var/task/audio/${slug}.mp3`,       // Vercel Lambda
        `/var/runtime/audio/${slug}.mp3`,
        `${process.cwd()}/audio/${slug}.mp3`,
        `${process.cwd()}/public/audio/${slug}.mp3`,
      ];
      for (const localPath of possiblePaths) {
        if (fs.existsSync(localPath)) {
          const audio = fs.readFileSync(localPath);
          if (audio && audio.length > 500) {
            res.setHeader('Content-Type', 'audio/mpeg');
            res.setHeader('Cache-Control', 'public, max-age=86400');
            res.setHeader('X-TTS-Backend', 'static-andrew');
            return res.send(audio);
          }
        }
      }
    } catch {}

    // Fallback 2: fetch from public URL (static audio CDN)
    // Verify Content-Type is actually audio to avoid serving HTML error pages
    try {
      const host = req.headers['x-forwarded-host'] || req.headers.host || 'readthesignal.net';
      const audioUrl = `https://${host}/audio/${slug}.mp3`;
      const r = await fetch(audioUrl);
      if (r.ok) {
        const ct = (r.headers.get('content-type') || '').toLowerCase();
        // Only accept if it's genuinely an audio file (audio/mpeg, audio/*, or octet-stream for binary)
        const isValidAudio = ct.includes('audio/') || ct.includes('octet-stream');
        if (isValidAudio) {
          const audio = Buffer.from(await r.arrayBuffer());
          // Also verify MP3 magic bytes (0xFF 0xFB or ID3 tag) to be sure
          const hasMP3Header = audio.length >= 3 && (
            (audio[0] === 0xFF && (audio[1] & 0xE0) === 0xE0) ||  // MPEG sync word
            (audio[0] === 0x49 && audio[1] === 0x44 && audio[2] === 0x33)  // ID3 tag
          );
          if (audio && audio.length > 500 && hasMP3Header) {
            res.setHeader('Content-Type', 'audio/mpeg');
            res.setHeader('Cache-Control', 'public, max-age=86400');
            res.setHeader('X-TTS-Backend', 'static-url-andrew');
            return res.send(audio);
          }
        }
      }
    } catch {}

    // Generate Andrew audio with retry + fallback voices
    const jennyAudio = await genTTSWithFallback(text);
    if (jennyAudio) {
      uploadToR2(slug, jennyAudio); // fire-and-forget cache
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=3600');
      res.setHeader('X-TTS-Backend', 'edge-tts-with-fallback');
      return res.send(jennyAudio);
    }
  }

  // No audio available — return 404 instead of robotic Google TTS fallback
  // Users will see "Audio not available" in the player rather than hearing
  // the low-quality Google Translate voice.
  return res.status(404).json({
    error: 'Audio not available for this article yet',
    slug: slug,
    hint: 'Audio generation may be pending. Try again later.'
  });
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
