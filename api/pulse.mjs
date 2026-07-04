// Pulse AI — serverless function for The Signal
// Answers any question using Gemini's knowledge + article library as context.
// Premium tier: Serper web search for real-time data (5/day/IP).

import fs from 'fs';
import path from 'path';

const GEMINI_MODEL = 'gemini-2.5-flash';
const SERPER_URL = 'https://google.serper.dev/search';

function getGeminiURL() {
  const key = process.env.GEMINI_API_KEY || '';
  return `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${key}`;
}

function getSerperKey() {
  return process.env.SERPER_API_KEY || '';
}

const PREMIUM_LIMIT = 5;

// Module-level caches — persist across warm Vercel invocations
const answerCache = new Map();
const quotaMap = new Map(); // IP -> { count, date }

function getDateStr() { return new Date().toISOString().slice(0, 10); }

function getClientIP(req) {
  return req.headers['x-forwarded-for']?.split(',')[0]?.trim()
    || req.headers['x-real-ip']
    || req.connection?.remoteAddress
    || 'unknown';
}

function checkQuota(ip) {
  const today = getDateStr();
  const entry = quotaMap.get(ip);
  if (!entry || entry.date !== today) {
    quotaMap.set(ip, { count: 0, date: today });
    return { remaining: PREMIUM_LIMIT, used: 0 };
  }
  return { remaining: PREMIUM_LIMIT - entry.count, used: entry.count };
}

function useQuota(ip) {
  const today = getDateStr();
  const entry = quotaMap.get(ip) || { count: 0, date: today };
  entry.count++;
  quotaMap.set(ip, entry);
  return PREMIUM_LIMIT - entry.count;
}

// // /// /

function getCacheKey(q) {
  return q.toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').trim();
}

const CACHE_TTL = 30 * 60 * 1000;
const CACHE_MAX = 100;

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

// // /// /

async function searchWeb(query) {
  const serperKey = getSerperKey();
  try {
    const res = await fetch(SERPER_URL, {
      method: 'POST',
      headers: { 'X-API-KEY': serperKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ q: query })
    });
    if (!res.ok) return null;
    const data = await res.json();
    let results = [];
    if (data.knowledgeGraph)
      results.push(`[KG] ${data.knowledgeGraph.title}: ${data.knowledgeGraph.description}${data.knowledgeGraph.attributes ? '\n' + Object.entries(data.knowledgeGraph.attributes).map(([k,v]) => `${k}: ${v}`).join('\n') : ''}`);
    if (data.organic)
      for (const r of data.organic.slice(0, 5)) results.push(`[${r.title}](${r.link})\n${r.snippet}`);
    if (data.answerBox)
      results.unshift(`[Answer] ${data.answerBox.title}: ${data.answerBox.snippet}`);
    if (data.topStories)
      for (const s of data.topStories.slice(0, 3)) results.push(`[News] ${s.title} - ${s.source}${s.date ? ' ('+s.date+')' : ''}`);
    return results.length ? results.join('\n\n') : null;
  } catch (e) { return null; }
}

async function callGemini(payload) {
  const geminiUrl = getGeminiURL();
  const res = await fetch(geminiUrl, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.text();
    if (res.status === 429) throw new Error('RATE_LIMITED');
    throw new Error(`${res.status}: ${err.slice(0,200)}`);
  }
  return res.json();
}

// // /// /

function loadArticles() {
  const dir = path.join(process.cwd(), 'articles', 'posts');
  const articles = [];
  if (!fs.existsSync(dir)) return articles;
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json'))) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
      articles.push({ title: a.title, slug: a.slug, ticker: a.ticker, sector: a.sector, date: a.date || '', summary: a.summary || '' });
    } catch(e) {}
  }
  return articles;
}

// // /// /

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const ip = getClientIP(req);
  console.log(`Pulse from ${ip}: "${req.body?.question?.slice(0,60)}..."`);

  try {
    const { question } = req.body;
    if (!question || question.trim().length < 3)
      return res.status(400).json({ error: 'Ask a meaningful question.' });

    const cacheKey = getCacheKey(question);
    const cached = cacheGet(cacheKey);
    if (cached) return res.status(200).json(cached);

    const articles = loadArticles();
    const articleContext = articles.sort((a,b) => new Date(b.date)-new Date(a.date))
      .filter(a => a.title && a.date)
      .map(a => `[${a.ticker}] ${a.title} (${a.sector}, ${(a.date||'').slice(0,10)})\n${a.summary}`)
      .join('\n---\n');

    // STEP 1: Answer using Gemini's knowledge + article context
    const freePrompt = `You are Pulse, the AI assistant on The Signal (readthesignal.net) — a market intelligence site covering AI, defense, space, cybersecurity, and mega-cap stocks.

TONE: Direct, punchy, conversational. Use **bold** for key numbers. Keep answers under 250 words. Be helpful about ANY topic — you're not limited to stocks.

RULES:
- Answer the user's question directly using your knowledge. You can talk about anything.
- If the question relates to stocks, companies, or markets, reference relevant Signal articles below as sources when applicable.
- If you don't know something, say so honestly.
- NEVER fabricate stock prices, earnings data, or financial figures — if you're unsure, say "check live data" instead of guessing.

The Signal's recent articles (for context, use when relevant):
${articleContext.slice(0, 15000)}`;

    const freePayload = {
      systemInstruction: { parts: [{ text: freePrompt }] },
      contents: [{ role: 'user', parts: [{ text: question }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 1024 },
      tools: [{ googleSearch: {} }]
    };

    let freeData, freeAnswer = '';
    try {
      freeData = await callGemini(freePayload);
      if (freeData.candidates?.[0]?.content?.parts) {
        freeAnswer = freeData.candidates[0].content.parts.map(p => p.text || '').join('');
      }
    } catch (e) {
      freeAnswer = '';
    }

    // Return free answer if we got one
    if (freeAnswer) {
      const sources = [];
      for (const a of articles) {
        if (freeAnswer.toLowerCase().includes(a.ticker?.toLowerCase()) && !sources.find(s => s.ticker === a.ticker)) {
          sources.push({ title: a.title, slug: a.slug, ticker: a.ticker });
          if (sources.length >= 3) break;
        }
      }
      const result = { answer: freeAnswer, sources, tier: sources.length ? 'free' : 'free' };
      cacheSet(cacheKey, result);
      return res.status(200).json(result);
    }

    // STEP 2: Needs premium (web search). Check quota.
    const { remaining, used } = checkQuota(ip);

    if (remaining <= 0) {
      const covered = ['NVDA','AMD','AVGO','PLTR','RKLB','RDW','LMT','RTX','GOOGL','META','MSFT','AMZN','TSLA','CRWV','MRVL','CRWD','AXON'];
      return res.status(200).json({
        answer: `You've used all 5 premium web searches today. Premium gives me access to live prices, earnings, and news.\n\n**Free questions I can answer right now:**\nAsk me about any of our covered stocks: ${covered.slice(0,5).join(', ')} and more.\n\n*Your quota resets tomorrow.*`,
        sources: [],
        tier: 'free',
        quota: { remaining: 0, used: PREMIUM_LIMIT }
      });
    }

    // Use quota
    const newRemaining = useQuota(ip);

    // Fire Serper search
    const webResults = await searchWeb(question);

    const webSection = webResults
      ? `Web Search Results (live data):\n${webResults}`
      : 'Web search returned no results. Rely on the article library and your training data.';

    const premiumPrompt = `You are Pulse, AI research assistant for The Signal (AI, defense, space, cyber stocks).

TONE: Direct, punchy, data-driven. Use **bold** for key numbers. Keep answers under 300 words.

You have LIVE WEB SEARCH RESULTS below. Use them for real-time data (prices, earnings, news).
Also reference The Signal's article library when relevant.

${webSection}

The Signal articles:\n${articleContext.slice(0, 12000)}`;

    const premiumPayload = {
      systemInstruction: { parts: [{ text: premiumPrompt }] },
      contents: [{ role: 'user', parts: [{ text: question }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 2048 }
    };

    const data = await callGemini(premiumPayload);
    let answer = '';
    if (data.candidates?.[0]?.content?.parts) {
      answer = data.candidates[0].content.parts.map(p => p.text || '').join('');
    }

    const sources = [];
    for (const a of articles) {
      if (answer.includes(a.ticker) && !sources.find(s => s.ticker === a.ticker)) {
        sources.push({ title: a.title, slug: a.slug, ticker: a.ticker });
        if (sources.length >= 3) break;
      }
    }

    const result = { answer, sources, tier: 'premium', quota: { remaining: newRemaining, used: used + 1 } };
    cacheSet(cacheKey, result);
    return res.status(200).json(result);

  } catch (error) {
    const isRate = error.message === 'RATE_LIMITED';
    const errMsg = error.message || String(error);
    console.error('Pulse error:', isRate ? 'RATE_LIMITED' : errMsg);
    return res.status(200).json({
      answer: isRate
        ? "Rate limited. Give me a moment and try again."
        : `I hit a processing issue. (${errMsg.slice(0, 80)})`,
      sources: [],
      tier: 'error'
    });
  }
}
