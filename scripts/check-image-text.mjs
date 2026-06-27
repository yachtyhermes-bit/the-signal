// check-image-text.mjs — vision check for garbled text in article hero images
// Uses OpenRouter vision models to inspect images and flag garbled/misspelled text.
// Silent on pass, alerts on FAIL. Designed for no_agent cron job (watchdog pattern).
// Run: node scripts/check-image-text.mjs [limit=N]
//
// ENV: OPENROUTER_API_KEY must be set

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.resolve(__dirname, '..');
const POSTS_DIR = path.join(ROOT, 'articles', 'posts');
const IMG_DIR = path.join(ROOT, 'public', 'img', 'articles');

const LIMIT = parseInt(process.argv.find(a => a.startsWith('limit='))?.split('=')[1] || '5', 10);

const OPENROUTER_KEY = process.env.OPENROUTER_API_KEY;
if (!OPENROUTER_KEY) {
  console.error('❌ OPENROUTER_API_KEY not set');
  process.exit(1);
}

function toBase64(filePath) {
  const data = fs.readFileSync(filePath);
  return Buffer.from(data).toString('base64');
}

function callVision(imageBase64, mimeType) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      model: 'google/gemini-2.5-flash',
      messages: [{
        role: 'user',
        content: [
          { type: 'text', text: `You are an image quality inspector. Look at this article hero image carefully.

TASK: Read ALL text visible in this image — company names, logos, labels, captions, numbers, any text at all.
Then answer: Is there ANY garbled, misspelled, or incorrect text?

Examples of garbled text: "CONSTELLIATR" instead of "Constellation", "EPTYC" instead of "EPYC", random letters that don't form real words, AI-hallucinated fake text.

Reply in exactly this format with NOTHING ELSE:
PASS — [explain why, e.g. "All text is correct" or "No text found"]
FAIL — [describe the garbled text found, e.g. "Logo says 'CONSTELLIATR' instead of 'Constellation'"]` },
          { type: 'image_url', image_url: { url: `data:${mimeType};base64,${imageBase64}` } }
        ]
      }],
      max_tokens: 100
    });

    const req = https.request({
      hostname: 'openrouter.ai',
      path: '/api/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENROUTER_KEY}`,
        'HTTP-Referer': 'https://readthesignal.net',
        'X-Title': 'The Signal Image Check'
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (json.error) {
            reject(new Error(json.error.message || JSON.stringify(json.error)));
          } else if (json.choices && json.choices[0]) {
            resolve(json.choices[0].message.content.trim());
          } else {
            reject(new Error('Unexpected response: ' + body.slice(0, 200)));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}. Body: ${body.slice(0, 200)}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function checkImage(slug, imgPath) {
  try {
    if (!fs.existsSync(imgPath)) {
      return { slug, status: 'SKIP', detail: 'Image file not found' };
    }

    const imageData = toBase64(imgPath);
    const mimeType = imgPath.endsWith('.png') ? 'image/png' : 'image/jpeg';

    const response = await callVision(imageData, mimeType);
    const status = response.startsWith('PASS') ? 'PASS' :
                   response.startsWith('FAIL') ? 'FAIL' : 'UNKNOWN';
    return { slug, status, detail: response };
  } catch (err) {
    return { slug, status: 'ERROR', detail: err.message };
  }
}

async function main() {
  // Load articles sorted by date desc (newest first)
  const files = fs.readdirSync(POSTS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => {
      const data = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, f), 'utf8'));
      return { ...data, file: f };
    })
    .sort((a, b) => (b.date || '').localeCompare(a.date || ''));

  const toCheck = files.slice(0, LIMIT);
  let failed = 0;

  for (const article of toCheck) {
    const slug = article.slug;
    const imageSrc = article.image?.src || '';
    const imgFilename = path.basename(imageSrc);
    const imgPath = path.join(IMG_DIR, imgFilename);

    process.stdout.write(`  ${slug}... `);
    const result = await checkImage(slug, imgPath);
    
    if (result.status === 'FAIL') {
      console.log(`❌ FAIL — ${result.detail}`);
      failed++;
    } else if (result.status === 'ERROR') {
      console.log(`⚠️  ERROR — ${result.detail}`);
    } else {
      console.log(`✅ ${result.status} — ${result.detail}`);
    }
  }

  if (failed > 0) {
    console.log(`\n⚠️  ${failed} image(s) with garbled text detected! Regenerate before deploying.`);
    process.exit(1);
  } else {
    console.log(`\n✅ All ${toCheck.length} article images passed text check.`);
  }
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
