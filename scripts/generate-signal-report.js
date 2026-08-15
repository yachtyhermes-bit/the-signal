#!/usr/bin/env node
/**
 * Generate Signal Report (Morningstar-style deep research) for a stock
 * Uses financial data + our articles to synthesize structured analysis
 * 
 * Usage: node scripts/generate-signal-report.js NVDA
 */

const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, '..', 'data');
const ARTICLES = path.join(__dirname, '..', 'articles', 'posts');
const FINANCIALS_PATH = path.join(DATA, 'financials.json');

// Load financial data
const financials = JSON.parse(fs.readFileSync(FINANCIALS_PATH, 'utf8'));

// Load all articles mentioning the ticker
function loadRelatedArticles(ticker) {
  const articles = [];
  if (!fs.existsSync(ARTICLES)) return articles;
  
  const files = fs.readdirSync(ARTICLES).filter(f => f.endsWith('.json'));
  for (const file of files) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(ARTICLES, file), 'utf8'));
      const tickerMatch = (a.ticker && a.ticker.toUpperCase() === ticker.toUpperCase()) ||
                          (a.slug && a.slug.toLowerCase().includes(ticker.toLowerCase()));
      if (tickerMatch) {
        articles.push({
          title: a.title,
          summary: a.summary || '',
          date: a.date,
        });
      }
    } catch (_) { /* skip malformed */ }
  }
  articles.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
  return articles.slice(0, 15); // Keep top 15 most recent
}

// Extract key financial metrics
function extractFinancialSummary(fin) {
  const stats = fin.stats || {};
  const analyst = fin.analyst || {};
  const consensus = fin.consensus || {};
  const returns = fin.returns || {};
  const earnings = fin.earnings || [];
  
  return {
    marketCap: stats.marketCap?.fmt || 'N/A',
    revenue: stats.totalRevenue?.fmt || 'N/A',
    netIncome: stats.netIncome?.fmt || 'N/A',
    grossMargin: stats.grossMargins?.fmt || 'N/A',
    operatingMargin: stats.operatingMargins?.fmt || 'N/A',
    freeCashflow: stats.freeCashflow?.fmt || 'N/A',
    totalCash: stats.totalCash?.fmt || 'N/A',
    totalDebt: stats.totalDebt?.fmt || 'N/A',
    peRatio: stats.trailingPE?.fmt || 'N/A',
    forwardPE: stats.forwardPE?.fmt || 'N/A',
    epsGrowth: stats.earningsGrowth?.fmt || 'N/A',
    revenueGrowth: stats.revenueGrowth?.fmt || 'N/A',
    analystTarget: analyst.targetMeanPrice?.fmt || 'N/A',
    analystRating: analyst.recommendationKey || 'N/A',
    consensus: consensus,
    returns: returns,
    recentEarnings: earnings.slice(0, 3),
  };
}

// Generate Signal Report using AI via OpenRouter
async function generateReport(ticker, fin, articles) {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    throw new Error('OPENROUTER_API_KEY environment variable not set');
  }
  
  const company = fin.company || {};
  const finSummary = extractFinancialSummary(fin);
  
  const prompt = `You are a financial analyst writing a deep research report for ${company.name} (${ticker}).

Company: ${company.name}
Sector: ${company.sector || 'N/A'}
Industry: ${company.industry || 'N/A'}
Description: ${(company.description || '').slice(0, 500)}

Financial Summary:
- Market Cap: ${finSummary.marketCap}
- Revenue (TTM): ${finSummary.revenue}
- Net Income: ${finSummary.netIncome}
- Gross Margin: ${finSummary.grossMargin}
- Operating Margin: ${finSummary.operatingMargin}
- Free Cash Flow: ${finSummary.freeCashflow}
- Cash: ${finSummary.totalCash}
- Debt: ${finSummary.totalDebt}
- P/E Ratio: ${finSummary.peRatio}
- Forward P/E: ${finSummary.forwardPE}
- EPS Growth: ${finSummary.epsGrowth}
- Revenue Growth: ${finSummary.revenueGrowth}

Analyst Consensus:
- Rating: ${finSummary.analystRating}
- Price Target: ${finSummary.analystTarget}
- Strong Buy: ${finSummary.consensus.strongBuy || 0}
- Buy: ${finSummary.consensus.buy || 0}
- Hold: ${finSummary.consensus.hold || 0}
- Sell: ${finSummary.consensus.sell || 0}

Recent Returns:
- 1 Year: ${finSummary.returns.oneYear?.fmt || 'N/A'}
- 5 Year: ${finSummary.returns.fiveYear?.fmt || 'N/A'}
- YTD: ${finSummary.returns.ytd?.fmt || 'N/A'}

Recent Earnings:
${finSummary.recentEarnings.map(e => `- ${e.date}: EPS ${e.epsActual || 'N/A'} vs Est ${e.epsEstimate || 'N/A'}`).join('\n')}

Recent Coverage (our articles):
${articles.map(a => `- ${a.title}: ${a.summary}`).join('\n')}

Generate a structured Signal Report in JSON format with these sections:

1. "aiAnalysis" (string): 2-3 sentence summary thesis covering valuation, moat, and outlook
2. "valuation" (object): { fairValue: string, upside: string, moatRating: "Wide"|"Narrow"|"None", uncertaintyRating: "Low"|"Medium"|"High"|"Very High", capitalAllocation: "Exemplary"|"Standard"|"Poor", starRating: 1-5 }
3. "recentPerformance" (object): { latestEarnings: string, revenueGrowth: string, catalysts: string[] }
4. "coreStrengths" (object): { switchingCosts: string, intangibleAssets: string, networkEffects: string, costAdvantage: string, efficientScale: string }
5. "mainRisks" (string[]): 3-4 key risks
6. "bullsSay" (string[]): 3-4 bullish arguments
7. "bearsSay" (string[]): 3-4 bearish arguments
8. "financialHealth" (string): 2-3 sentence assessment of balance sheet strength
9. "analystNote" (string): 1-2 sentence key takeaway
10. "businessStrategy" (string): 2-3 sentence overview of strategic direction and long-term vision

Be specific, data-driven, and balanced. Use the financial data and article context provided. Output ONLY valid JSON.`;

  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'google/gemini-2.5-flash',
      messages: [
        { role: 'user', content: prompt }
      ],
      response_format: { type: 'json_object' },
    }),
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`OpenRouter API error: ${response.status} - ${error}`);
  }
  
  const data = await response.json();
  const text = data.choices[0]?.message?.content || '';
  
  // Extract JSON from response (in case AI adds markdown fences)
  let textOut = text.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
  const jsonMatch = textOut.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error('Failed to parse AI response as JSON');
  }
  try {
    return JSON.parse(jsonMatch[0]);
  } catch (parseErr) {
    // Retry once with the parse error fed back to the model
    const retry = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'google/gemini-2.5-flash',
        messages: [
          { role: 'user', content: prompt },
          { role: 'assistant', content: text },
          { role: 'user', content: `Your previous response was not valid JSON (${parseErr.message}). Return ONLY the corrected JSON object — no markdown, no trailing commas, no commentary.` },
        ],
        response_format: { type: 'json_object' },
      }),
    });
    if (!retry.ok) throw parseErr;
    const retryData = await retry.json();
    const retryText = (retryData.choices[0]?.message?.content || '').replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
    const retryMatch = retryText.match(/\{[\s\S]*\}/);
    if (!retryMatch) throw parseErr;
    return JSON.parse(retryMatch[0]);
  }
}

// Main
async function main() {
  const ticker = process.argv[2];
  if (!ticker) {
    console.error('Usage: node scripts/generate-signal-report.js TICKER');
    process.exit(1);
  }
  
  const fin = financials[ticker];
  if (!fin) {
    console.error(`No financial data found for ${ticker}`);
    process.exit(1);
  }
  
  console.log(`📊 Generating Signal Report for ${ticker}...`);
  
  const articles = loadRelatedArticles(ticker);
  console.log(`  Found ${articles.length} related articles`);
  
  try {
    const report = await generateReport(ticker, fin, articles);
    
    // Add to financials
    financials[ticker].signalReport = report;
    financials[ticker].signalReportGenerated = new Date().toISOString();
    
    // Save
    fs.writeFileSync(FINANCIALS_PATH, JSON.stringify(financials, null, 2));
    
    console.log(`✅ Signal Report generated for ${ticker}`);
    console.log(`   AI Analysis: ${report.aiAnalysis.slice(0, 100)}...`);
    console.log(`   Moat Rating: ${report.valuation.moatRating}`);
    console.log(`   Star Rating: ${'★'.repeat(report.valuation.starRating)}${'☆'.repeat(5 - report.valuation.starRating)}`);
  } catch (error) {
    console.error(`❌ Failed to generate report: ${error.message}`);
    process.exit(1);
  }
}

main();
