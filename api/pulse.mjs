// Pulse AI — Vercel serverless function for The Signal
// Uses Google Gemini API directly with Google Search Grounding
// for live web search answers on EVERY question — no tiers, no quotas.
// Article index is inlined at build time by build.js (compact format).

// ARTICLES_PLACEHOLDER — build.js replaces this with inline data
const articles = [];

// ─── Config ───
const GEMINI_MODEL = 'gemini-2.5-flash';
const GEMINI_BASE = 'https://generativelanguage.googleapis.com/v1beta';

const CACHE_TTL = 30 * 60 * 1000;
const CACHE_MAX = 100;
const answerCache = new Map();

function getCacheKey(q) {
  return q.toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').trim();
}

function cacheGet(key) {
  const entry = answerCache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.ts > CACHE_TTL) { answerCache.delete(key); return null; }
  answerCache.delete(key);
  answerCache.set(key, entry);
  return entry;
}

function cacheSet(key, data) {
  if (answerCache.has(key)) answerCache.delete(key);
  if (answerCache.size >= CACHE_MAX) {
    const oldest = answerCache.keys().next().value;
    if (oldest) answerCache.delete(oldest);
  }
  answerCache.set(key, { ...data, ts: Date.now() });
}

// ─── Find sources from answer ───
function findSources(answer) {
  const answerLower = answer.toLowerCase();
  const sources = [];
  for (const a of articles) {
    if (
      (a.t && answerLower.includes(a.t.toLowerCase())) ||
      (a.u && answerLower.includes(a.u.toLowerCase().slice(0, 30)))
    ) {
      if (!sources.find(s => s.t === a.t)) {
        sources.push({ title: a.u, slug: a.s, ticker: a.t });
        if (sources.length >= 4) break;
      }
    }
  }
  return sources;
}

// ─── Build article context from index ───
function buildArticleContext() {
  const sectors = {};
  for (const a of articles) {
    const sector = a.c || 'other';
    if (!sectors[sector]) sectors[sector] = [];
    sectors[sector].push(a);
  }
  let ctx = '';
  for (const [sector, arts] of Object.entries(sectors)) {
    ctx += `\n[${sector.toUpperCase()}]\n`;
    for (const a of arts.slice(0, 12)) {
      ctx += `  [${a.t}] ${a.u} (${a.d})\n`;
    }
  }
  return ctx.slice(0, 6000);
}

// ─── Gemini API call ───
async function callGemini(systemPrompt, userQuestion, history = []) {
  const key = process.env.GEMINI_API_KEY || '';
  if (!key) throw new Error('403: No GEMINI_API_KEY configured.');

  const url = `${GEMINI_BASE}/models/${GEMINI_MODEL}:generateContent?key=${key}`;

  // Build multi-turn contents array from history
  const contents = [];
  for (const msg of history) {
    contents.push({
      role: msg.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: msg.text }]
    });
  }
  contents.push({ role: 'user', parts: [{ text: userQuestion }] });

  const payload = {
    systemInstruction: { parts: [{ text: systemPrompt }] },
    contents,
    tools: [{ googleSearch: {} }],
    generationConfig: { temperature: 0.3, maxOutputTokens: 8192 },
    safetySettings: [
      { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_NONE' },
      { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_NONE' },
      { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_NONE' },
      { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_NONE' }
    ]
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const err = await res.text();
    if (res.status === 429) throw new Error('RATE_LIMITED');
    throw new Error(`${res.status}: ${err.slice(0, 200)}`);
  }

  const data = await res.json();

  // Join ALL parts from the response (Gemini can split into multiple parts)
  const parts = data.candidates?.[0]?.content?.parts || [];
  const text = parts.map(p => p.text || '').join('');

  const finishReason = data.candidates?.[0]?.finishReason;
  if (finishReason === 'MAX_TOKENS' || finishReason === 'SAFETY') {
    console.error(`Gemini finish reason: ${finishReason} for query`);
  }

  const groundMeta = data.candidates?.[0]?.groundingMetadata;
  const searched = groundMeta?.webSearchQueries?.length > 0;

  // Extract actual web search source URLs from Google's grounding data
  const webSources = [];
  const chunks = groundMeta?.groundingChunks || [];
  const seen = new Set();
  for (const chunk of chunks) {
    const uri = chunk.web?.uri;
    const title = chunk.web?.title || uri;
    if (uri && !seen.has(uri)) {
      seen.add(uri);
      webSources.push({ url: uri, title });
    }
    if (webSources.length >= 5) break;
  }

  return { text, searched, webSources };
}

// ─── Handler ───
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { question, articleContext: requestContext, history = [] } = req.body;
    if (!question || question.trim().length < 3) {
      return res.status(200).json({ answer: 'Ask me anything about markets or stocks.', sources: [], searched: false });
    }

    const cacheKey = getCacheKey(question);
    const cached = (!history.length) ? cacheGet(cacheKey) : null;
    if (cached) return res.status(200).json(cached);

    const articleContext = buildArticleContext();
    const articleCount = articles.length;

    const systemPrompt = `You are Pulse, AI on The Signal (readthesignal.net) — market intelligence.

TONE: Direct, punchy. Bold key numbers. Under 800 words.

CAPABILITIES:
1. Google Search — live web search for prices, earnings, news.
2. Article Library — Signal articles below. Use EXACT titles when referencing.

RULES:
- Search the web for current data on ALL companies asked about.
- When asked about "companies" plural, list ALL relevant ones, not just 2-3.
- Reference Signal articles by EXACT title from the list below.
- Our library has ${articleCount} articles. NEVER say we don't cover something without checking the list.
- NEVER make up article titles or stock prices.
${requestContext && requestContext.title ? `\nCURRENT ARTICLE CONTEXT:\nThis question is being asked from the article page for "${requestContext.title}".\nSlug: ${requestContext.slug}\nBody preview: ${(requestContext.bodyPreview || '').slice(0, 800)}\nUse this context to ground your answer in what the article covers.` : ''}

Covered: NVDA, AMD, AVGO, MRVL, PLTR, CRWD, RKLB, RDW, LMT, RTX, GOOGL, META, MSFT, AMZN, TSLA, AAPL, PANW, and more.

Article library (${articleCount} articles):
${articleContext}`;

    const { text: answer, searched, webSources } = await callGemini(systemPrompt, question, history);

    if (!answer) {
      return res.status(200).json({ answer: "Couldn't find a good answer. Try rephrasing.", sources: [], searched: false });
    }

    // Always prefer real web search URLs from Google grounding
    const sources = webSources && webSources.length > 0
      ? webSources.map(s => ({ title: s.title, url: s.url, source: 'web' }))
      : findSources(answer);
    const result = { answer, sources, searched };
    cacheSet(cacheKey, result);
    return res.status(200).json(result);

  } catch (error) {
    const errMsg = error.message || String(error);
    console.error('Pulse error:', errMsg);
    if (error.message === 'RATE_LIMITED') {
      return res.status(200).json({ answer: 'Rate limited. Try again in a minute.', sources: [], searched: false });
    }
    return res.status(200).json({ answer: `Issue: ${errMsg.slice(0, 100)}`, sources: [], searched: false });
  }
}
