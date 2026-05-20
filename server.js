const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3004;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
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
  res.render('pages/index', { articles: articles.slice(0, 30), prices });
});

app.get('/ticker/:symbol', (req, res) => {
  const symbol = req.params.symbol.toUpperCase();
  const articles = loadTickerArticles(symbol);
  const prices = loadPrices();
  const price = prices[symbol] || null;
  res.render('pages/ticker', { symbol, articles, price, prices });
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
  res.render('pages/sector', { name: name.toUpperCase(), articles, prices, tickers });
});

app.get('/article/:slug', (req, res) => {
  const slug = req.params.slug;
  try {
    const article = JSON.parse(fs.readFileSync(path.join(__dirname, 'articles', 'posts', `${slug}.json`), 'utf8'));
    const prices = loadPrices();
    res.render('pages/article', { article, prices });
  } catch {
    res.status(404).render('pages/404');
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
