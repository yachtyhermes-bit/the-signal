const express = require('express');
const path = require('path');
const fs = require('fs');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const app = express();
const PORT = process.env.PORT || 3004;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Load articles index
function loadArticles() {
  try {
    const index = JSON.parse(fs.readFileSync(path.join(__dirname, 'articles', 'index.json'), 'utf8'));
    return index.sort((a, b) => new Date(b.date) - new Date(a.date));
  } catch { return []; }
}

function loadPrices() {
  try {
    return JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'prices.json'), 'utf8'));
  } catch { return {}; }
}

function loadTickerArticles(ticker) {
  const dir = path.join(__dirname, 'articles', ticker.toUpperCase());
  try {
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));
    return files.map(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')))
      .sort((a, b) => new Date(b.date) - new Date(a.date));
  } catch { return []; }
}

// Static pages
app.get('/', (req, res) => {
  const articles = loadArticles();
  const prices = loadPrices();
  res.render('pages/index', { articles: articles.slice(0, 30), prices, allArticles: articles });
});

app.get('/ticker/:symbol', (req, res) => {
  const symbol = req.params.symbol.toUpperCase();
  const articles = loadTickerArticles(symbol);
  const prices = loadPrices();
  const price = prices[symbol] || null;
  const allArticles = loadArticles();
  res.render('pages/ticker', { symbol, articles, price, prices, allArticles });
});

app.get('/sector/:name', (req, res) => {
  const sectors = {
    'ai': ['NVDA', 'AMD', 'AVGO', 'MRVL', 'TSM', 'ASML', 'MU', 'CBRS'],
    'cyber': ['CRWD', 'PANW', 'FTNT', 'ZS', 'S', 'CHKP', 'CYBR', 'TENB'],
    'defense': ['LMT', 'RTX', 'NOC', 'GD', 'LHX', 'KTOS', 'AVAV', 'PL'],
    'space': ['RKLB', 'RDW', 'LUNR', 'ASTS'],
    'mega-cap': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA'],
    'ai-software': ['PLTR', 'CRWD', 'DDOG', 'SNOW', 'NOW', 'NET', 'AI'],
    'all': []
  };
  const tickers = sectors[name.toLowerCase()] || [];
  const allArticles = loadArticles();
  const articles = tickers.length > 0
    ? allArticles.filter(a => tickers.includes(a.ticker))
    : allArticles;
  const prices = loadPrices();
  res.render('pages/sector', { name: name.toUpperCase(), articles, prices, tickers, allArticles });
});

app.get('/article/:slug', (req, res) => {
  const slug = req.params.slug;
  try {
    const article = JSON.parse(fs.readFileSync(path.join(__dirname, 'articles', 'posts', `${slug}.json`), 'utf8'));
    const prices = loadPrices();
    const allArticles = loadArticles();
    res.render('pages/article', { article, prices, allArticles });
  } catch {
    res.status(404).render('pages/404');
  }
});

app.get('/api/articles.json', (req, res) => {
  const articles = loadArticles();
  res.json(articles);
});

// Pulse AI Research Agent API
app.post('/api/pulse', async (req, res) => {
  try {
    const { question } = req.body;
    if (!question || question.trim().length < 3) {
      return res.status(400).json({ error: 'Please ask a meaningful question.' });
    }

    // Load articles
    const articlesDir = path.join(__dirname, 'articles', 'posts');
    const articles = [];
    if (fs.existsSync(articlesDir)) {
      const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.json'));
      for (const file of files) {
        try {
          const article = JSON.parse(fs.readFileSync(path.join(articlesDir, file), 'utf8'));
          articles.push({
            title: article.title,
            slug: article.slug,
            ticker: article.ticker,
            sector: article.sector,
            date: article.date,
            tags: article.tags || [],
            summary: article.summary,
            bodyText: (article.bodyHtml || '').replace(/<[^>]*>/g, '').slice(0, 3000)
          });
        } catch(e) {}
      }
    }
    articles.sort((a, b) => new Date(b.date) - new Date(a.date));

    const genAI = new GoogleGenerativeAI('AIzaSyDLpweLQTfZkdlpCtarQOnRX36Uiza3fiQ');
    const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash', tools: [{ googleSearch: {} }] });

    const articleContext = articles.map(a =>
      `[${a.ticker}] ${a.title} (${a.sector}, ${a.date.slice(0,10)})\nSummary: ${a.summary}\nBody excerpt: ${a.bodyText.slice(0, 1500)}`
    ).join('\n\n---\n\n');

    const systemPrompt = `You are Pulse, an AI research assistant for The Signal — covering AI, defense, space, cybersecurity, and mega-cap stocks.

You have TWO capabilities:
1. **Web Search** — You can search Google in real-time for current earnings, stock data, SEC filings, news, and any financial information. USE THIS whenever users ask about real-time or recent data.
2. **Article Library** — The Signal's analysis articles below. Reference these when relevant but don't limit yourself to them.

Your tone: Direct, punchy, data-driven (AXON style). Bold key numbers. Cite sources clearly. If you search the web, mention that you did.

The Signal's article library (for reference):
${articleContext.slice(0, 20000)}`;

    const result = await model.generateContent([
      { text: systemPrompt },
      { text: `User question: ${question}` }
    ]);

    let answer = '';
    try { answer = result.response.text(); } catch (e) {
      try {
        const parts = result.response.candidates?.[0]?.content?.parts || [];
        answer = parts.map(p => p.text || '').join('\n');
      } catch(e2) { answer = ''; }
    }

    // Find sources from articles
    const sources = [];
    for (const a of articles) {
      if (answer.includes(a.ticker) || answer.includes(a.title.slice(0, 30))) {
        sources.push({ title: a.title, slug: a.slug, ticker: a.ticker });
        if (sources.length >= 3) break;
      }
    }

    return res.json({ answer, sources });
  } catch (error) {
    console.error('Pulse API error:', error.message);
    return res.json({
      answer: 'I hit a processing limit — try asking that in a different way.',
      sources: []
    });
  }
});

app.get('/sitemap.xml', (req, res) => {
  const articles = loadArticles();
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  xml += '  <url><loc>https://thesignal.market/</loc><priority>1.0</priority></url>\n';
  for (const a of articles) {
    xml += `  <url><loc>https://thesignal.market/article/${a.slug}</loc><lastmod>${a.date}</lastmod><priority>0.8</priority></url>\n`;
  }
  xml += '</urlset>';
  res.header('Content-Type', 'application/xml');
  res.send(xml);
});

app.get('/rss', (req, res) => {
  const articles = loadArticles();
  let rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>The Signal — Market Intelligence</title>
  <link>https://thesignal.market/</link>
  <description>AI, defense, space, cyber &amp; tech stock intelligence</description>
  <atom:link href="https://thesignal.market/rss" rel="self" type="application/rss+xml"/>`;
  for (const a of articles.slice(0, 50)) {
    rss += `
  <item>
    <title><![CDATA[${a.title}]]></title>
    <link>https://thesignal.market/article/${a.slug}</link>
    <description><![CDATA[${a.summary}]]></description>
    <pubDate>${new Date(a.date).toUTCString()}</pubDate>
    <guid>https://thesignal.market/article/${a.slug}</guid>
  </item>`;
  }
  rss += '\n</channel>\n</rss>';
  res.header('Content-Type', 'application/rss+xml');
  res.send(rss);
});

app.listen(PORT, () => {
  console.log(`📡 The Signal running on http://localhost:${PORT}`);
});
