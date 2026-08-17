#!/usr/bin/env node
// Strict Morningstar-style moat re-rating for all moat-covered tickers.
// One batched OpenRouter call (json_object), retry on parse failure.
const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, '..', 'data');
const moatFiles = fs.readdirSync(DATA).filter(f => f.startsWith('moat-') && f.endsWith('.json'));
const tickers = moatFiles.map(f => f.slice(5, -5)).sort();
const existing = {};
for (const f of moatFiles) existing[f.slice(5, -5)] = JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8'));

const apiKey = process.env.OPENROUTER_API_KEY;
if (!apiKey) { console.error('OPENROUTER_API_KEY not set'); process.exit(1); }

const prompt = `You are a Morningstar-style economic moat analyst. Re-rate the economic moat for each company below with STRICT, conservative standards.

Morningstar moat criteria:
- WIDE MOAT: exceptional, durable structural advantage lasting 10+ years — sustained ROIC well above cost of capital, pricing power that survives downturns, switching costs that lock customers in for decades, network effects that get stronger with scale, or a cost advantage competitors cannot replicate. Wide is RARE: typically 10-15% of companies.
- NARROW MOAT: a real but less durable advantage (5-10 years) — good brand, moderate switching costs, decent scale economics. This is the DEFAULT for solid companies.
- NONE: commodity business, no pricing power, easily replicated advantage, or advantage too new/unproven.

Be skeptical. Recent momentum, hot products, or fast growth are NOT moats. New IPOs and young companies almost never have wide moats — their advantages are unproven. Capital-intensive commodity infrastructure (cloud compute, chips on contract, energy) rarely merits Wide. Default to Narrow; require exceptional evidence for Wide.

Companies to rate:
${tickers.map(t => `- ${t}: ${existing[t].industry || 'n/a'} (current rating: ${existing[t].rating} ${existing[t].stars}★)`).join('\n')}

For EACH ticker output:
{
  "symbol": "TICKER",
  "rating": "Wide" | "Narrow" | "None",
  "stars": 1-5 (Wide: 4-5, Narrow: 2-3, None: 1),
  "confidence": "High" | "Medium" | "Low",
  "rationale": "one sentence, Morningstar-style",
  "factors": {
    "Switching Costs": {"score": 1-5, "rationale": "..."},
    "Intangible Assets": {"score": 1-5, "rationale": "..."},
    "Network Effect": {"score": 1-5, "rationale": "..."},
    "Cost Advantage": {"score": 1-5, "rationale": "..."},
    "Efficient Scale": {"score": 1-5, "rationale": "..."}
  }
}

Output ONE JSON object with ticker symbols as keys. Be strict. Output ONLY valid JSON.`;

async function call(messages) {
  const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'google/gemini-2.5-flash', messages, response_format: { type: 'json_object' } }),
  });
  if (!r.ok) throw new Error(`OpenRouter ${r.status}: ${await r.text()}`);
  const d = await r.json();
  return (d.choices[0]?.message?.content || '').replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
}

(async () => {
  const userMsg = { role: 'user', content: prompt };
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const text = await call([userMsg]);
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) throw new Error('no JSON in response');
      const out = JSON.parse(m[0]);
      const keys = Object.keys(out);
      console.log(`✅ parsed ${keys.length} tickers (attempt ${attempt})`);
      fs.writeFileSync('/tmp/moat-rerate.json', JSON.stringify(out, null, 2));
      console.log('saved /tmp/moat-rerate.json');
      process.exit(0);
    } catch (e) {
      console.log(`attempt ${attempt} failed: ${e.message}`);
    }
  }
  console.error('❌ all attempts failed');
  process.exit(1);
})();
