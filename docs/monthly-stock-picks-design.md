# Monthly Stock Picks — Design & Implementation Plan

## 1. Overview

A new **"Monthly Stock Picks"** section for The Signal homepage that displays the current month's curated stock picks (6 stocks) alongside an embedded YouTube video. The design follows The Signal's dark theme: `#06060e` background, blue/purple gradient accents (`#3b82f6` → `#8b5cf6`), clean modern cards with subtle glow effects.

---

## 2. Homepage Placement

**Recommended position:** After **Signal Highlights** (detail-stocks-section) and before **Community Trading (Hive)** section.

**Resulting layout:**
```
Hero → Featured Article (1) → Ask Pulse → GRID_1 (4) → Trending Stocks
  → Scorecards → GRID_2 (6) → Signal Highlights
  → **MONTHLY PICKS**  ← NEW
  → Community Trading (Hive) → GRID_3 (8) → Newsletter → GRID_4 (11)
```

**Rationale:**
- Signal Highlights shows live market data → Monthly Picks shows curation/opinion → Hive shows community trading
- This is a natural editorial feature that lives between "hot right now" (Highlights) and "community content" (Hive)
- It occupies the "premium editorial" slot — high visibility without competing with Hero/Featured

---

## 3. Data Model

### Storage: `articles/monthly-picks/YYYY-MM.json`

Each month gets its own JSON file. The build pipeline scans this directory and picks the latest month.

```json
{
  "year": 2025,
  "month": 7,
  "published": "2025-07-01",
  "title": "July 2025 Stock Picks",
  "subtitle": "Our top 6 picks for the month ahead",
  "youtubeUrl": "https://youtu.be/ojgfFCSsWKg",
  "youtubeEmbed": "https://www.youtube.com/embed/ojgfFCSsWKg",
  "youtubeTitle": "July 2025 Monthly Stock Picks | The Signal",
  "description": "This month we're bullish on AI infrastructure, defense contracts, and space expansion. Here are our 6 top stock picks for July 2025.",
  "picks": [
    {
      "ticker": "PLTR",
      "name": "Palantir Technologies",
      "reason": "AIP platform gaining enterprise traction with 40%+ revenue growth and expanding government contracts.",
      "sector": "ai",
      "sentiment": "bullish",
      "priceTarget": "$195",
      "currentPrice": "$162.45"
    },
    {
      "ticker": "RKLB",
      "name": "Rocket Lab USA",
      "reason": "Neutron launch vehicle on track for 2026 debut and expanding space systems revenue.",
      "sector": "space",
      "sentiment": "bullish",
      "priceTarget": "$45",
      "currentPrice": "$32.80"
    },
    {
      "ticker": "AVGO",
      "name": "Broadcom Inc.",
      "reason": "VMware integration driving margin expansion and AI networking chip demand surging.",
      "sector": "ai",
      "sentiment": "bullish",
      "priceTarget": "$520",
      "currentPrice": "$460.80"
    },
    {
      "ticker": "AXON",
      "name": "Axon Enterprise",
      "reason": "Recurring cloud revenue growing 50%+ and expanding TASER adoption internationally.",
      "sector": "defense",
      "sentiment": "bullish",
      "priceTarget": "$850",
      "currentPrice": "$720.50"
    },
    {
      "ticker": "KTOS",
      "name": "Kratos Defense & Security",
      "reason": "Drone systems and hypersonic test vehicles seeing increased DoD contract flow.",
      "sector": "defense",
      "sentiment": "bullish",
      "priceTarget": "$40",
      "currentPrice": "$28.15"
    },
    {
      "ticker": "SOFI",
      "name": "SoFi Technologies",
      "reason": "Path to GAAP profitability clear with member growth accelerating and lending margins expanding.",
      "sector": "fintech",
      "sentiment": "bullish",
      "priceTarget": "$22",
      "currentPrice": "$16.90"
    }
  ]
}
```

### JSON Schema Validation:

```json
{
  "type": "object",
  "required": ["year", "month", "title", "youtubeEmbed", "picks"],
  "properties": {
    "year": {"type": "integer", "minimum": 2025},
    "month": {"type": "integer", "minimum": 1, "maximum": 12},
    "published": {"type": "string", "format": "date"},
    "title": {"type": "string"},
    "subtitle": {"type": "string"},
    "youtubeUrl": {"type": "string", "format": "uri"},
    "youtubeEmbed": {"type": "string", "format": "uri"},
    "youtubeTitle": {"type": "string"},
    "description": {"type": "string"},
    "picks": {
      "type": "array",
      "minItems": 6,
      "maxItems": 6,
      "items": {
        "type": "object",
        "required": ["ticker", "name", "reason", "sector", "sentiment"],
        "properties": {
          "ticker": {"type": "string", "pattern": "^[A-Z]{1,5}$"},
          "name": {"type": "string"},
          "reason": {"type": "string", "maxLength": 200},
          "sector": {"type": "string"},
          "sentiment": {"type": "string", "enum": ["bullish", "bearish", "neutral"]},
          "priceTarget": {"type": "string"},
          "currentPrice": {"type": "string"}
        }
      }
    }
  }
}
```

---

## 4. HTML Structure

The section is injected by build.js at a new `<!-- MONTHLY_PICKS -->` placeholder.

```html
<section class="monthly-picks-section">
  <!-- Background glow effect -->
  <div class="monthly-picks-bg"></div>

  <div class="monthly-picks-inner">
    <!-- Section Header -->
    <div class="monthly-picks-header">
      <div class="monthly-picks-badge">
        <span class="monthly-picks-badge-dot"></span>
        Monthly Picks
      </div>
      <h2 class="monthly-picks-title">Our <span class="monthly-picks-gradient">Top Picks</span> for <span class="monthly-picks-month">July 2025</span></h2>
      <p class="monthly-picks-desc">6 curated stocks hand-picked by The Signal editorial team — video analysis included.</p>
    </div>

    <div class="monthly-picks-layout">
      <!-- LEFT: Video Player -->
      <div class="monthly-picks-video">
        <div class="monthly-picks-video-wrapper">
          <iframe
            src="https://www.youtube.com/embed/ojgfFCSsWKg"
            title="July 2025 Monthly Stock Picks | The Signal"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            loading="lazy"
          ></iframe>
        </div>
        <div class="monthly-picks-video-caption">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z"/>
          </svg>
          Watch the full breakdown
        </div>
      </div>

      <!-- RIGHT: 6 Stock Picks Grid -->
      <div class="monthly-picks-grid">
        <div class="monthly-pick-card">
          <div class="monthly-pick-rank">1</div>
          <div class="monthly-pick-body">
            <div class="monthly-pick-top">
              <span class="monthly-pick-ticker">PLTR</span>
              <span class="monthly-pick-sentiment bullish">▲ Bullish</span>
            </div>
            <div class="monthly-pick-name">Palantir Technologies</div>
            <p class="monthly-pick-reason">AIP platform gaining enterprise traction with 40%+ revenue growth and expanding government contracts.</p>
            <div class="monthly-pick-targets">
              <span class="monthly-pick-target"><span class="target-label">Target</span> $195</span>
              <span class="monthly-pick-current"><span class="target-label">Current</span> $162.45</span>
            </div>
          </div>
        </div>
        <!-- ... repeat for 6 picks ... -->
      </div>
    </div>

    <!-- Past months archive link -->
    <div class="monthly-picks-footer">
      <a href="/monthly-picks/" class="monthly-picks-archive-link">
        View Past Months →
      </a>
    </div>
  </div>
</section>
```

### Stock Card Variations:

**Standard card (desktop/tablet):** Each pick is a compact card with numbered rank, ticker, sentiment badge, company name, one-line reason, and price targets.

**Condensed card (mobile):** On smaller screens, the 6 picks stack in a single column with reduced padding.

---

## 5. CSS Design

### Key Design Tokens (matching existing theme):

```css
:root {
  --monthly-accent: linear-gradient(135deg, #3b82f6, #8b5cf6);
  --monthly-glow: rgba(59, 130, 246, 0.08);
  --monthly-card-bg: #0f0f20;
  --monthly-card-border: #181830;
  --monthly-card-hover: #161630;
}
```

### Complete CSS Implementation:

```css
/* ═══════════════════════════════════════════
   MONTHLY STOCK PICKS SECTION
   ═══════════════════════════════════════════ */

.monthly-picks-section {
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px 60px;
  overflow: hidden;
}

/* Background glow */
.monthly-picks-bg {
  position: absolute;
  top: -120px;
  left: 50%;
  transform: translateX(-50%);
  width: 800px;
  height: 600px;
  background: radial-gradient(ellipse at center, rgba(59, 130, 246, 0.04) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.monthly-picks-inner {
  position: relative;
  z-index: 1;
}

/* ── Section Header ── */
.monthly-picks-header {
  text-align: center;
  margin-bottom: 36px;
}

.monthly-picks-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.06));
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.15);
  margin-bottom: 12px;
}

.monthly-picks-badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--green);
  animation: pulseDot 2s ease-in-out infinite;
}

.monthly-picks-title {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.4px;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.3;
}

.monthly-picks-gradient {
  background: linear-gradient(135deg, #3b82f6, #60a5fa, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.monthly-picks-month {
  color: var(--text-primary);
}

.monthly-picks-desc {
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.5;
  max-width: 500px;
  margin: 0 auto;
}

/* ── Two-Column Layout ── */
.monthly-picks-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  align-items: start;
}

/* ── Video Player ── */
.monthly-picks-video {
  position: sticky;
  top: 80px;
}

.monthly-picks-video-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-card);
  border: 1px solid var(--border);
  box-shadow: 0 4px 30px rgba(59, 130, 246, 0.08);
  transition: all 0.3s ease;
}

.monthly-picks-video-wrapper:hover {
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 8px 40px rgba(59, 130, 246, 0.12);
}

.monthly-picks-video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.monthly-picks-video-caption {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  font-size: 12px;
  color: var(--text-muted);
  padding-left: 2px;
}

.monthly-picks-video-caption svg {
  color: #ef4444; /* YouTube red */
  width: 16px;
  height: 16px;
}

/* ── 6 Picks Grid ── */
.monthly-picks-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

/* Individual Pick Card */
.monthly-pick-card {
  display: flex;
  gap: 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  transition: all 0.25s ease;
  cursor: default;
  position: relative;
}

.monthly-pick-card:hover {
  background: var(--bg-card-hover);
  border-color: rgba(59, 130, 246, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.06);
}

/* Rank Number */
.monthly-pick-rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  min-width: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(139, 92, 246, 0.08));
  border: 1px solid rgba(139, 92, 246, 0.15);
  font-size: 12px;
  font-weight: 700;
  color: #a78bfa;
  font-family: 'JetBrains Mono', monospace;
}

/* Card Body */
.monthly-pick-body {
  flex: 1;
  min-width: 0;
}

.monthly-pick-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.monthly-pick-ticker {
  font-family: 'JetBrains Mono', 'SF Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.2px;
}

.monthly-pick-sentiment {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.3px;
  padding: 2px 8px;
  border-radius: 4px;
}

.monthly-pick-sentiment.bullish {
  background: var(--green-dim);
  color: var(--green);
}

.monthly-pick-sentiment.bearish {
  background: var(--red-dim);
  color: var(--red);
}

.monthly-pick-sentiment.neutral {
  background: var(--gold-dim);
  color: var(--gold);
}

.monthly-pick-name {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.monthly-pick-reason {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 8px;
}

.monthly-pick-targets {
  display: flex;
  gap: 14px;
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
}

.monthly-pick-target,
.monthly-pick-current {
  display: flex;
  align-items: center;
  gap: 4px;
}

.monthly-pick-target {
  color: var(--green);
  font-weight: 600;
}

.monthly-pick-current {
  color: var(--text-secondary);
}

.target-label {
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}

/* ── Footer / Archive Link ── */
.monthly-picks-footer {
  text-align: center;
  margin-top: 28px;
}

.monthly-picks-archive-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  padding: 8px 20px;
  border-radius: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  transition: all 0.25s ease;
}

.monthly-picks-archive-link:hover {
  color: var(--accent);
  border-color: rgba(59, 130, 246, 0.3);
  background: var(--bg-card-hover);
  transform: translateY(-1px);
}

/* ═══════════════════════════════════════════
   RESPONSIVE — Tablet (≤1024px)
   ═══════════════════════════════════════════ */
@media (max-width: 1024px) {
  .monthly-picks-layout {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .monthly-picks-video {
    position: static;
  }

  .monthly-picks-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .monthly-picks-title {
    font-size: 24px;
  }
}

/* ═══════════════════════════════════════════
   RESPONSIVE — Mobile (≤768px)
   ═══════════════════════════════════════════ */
@media (max-width: 768px) {
  .monthly-picks-section {
    padding: 0 16px 40px;
  }

  .monthly-picks-header {
    margin-bottom: 24px;
  }

  .monthly-picks-title {
    font-size: 20px;
  }

  .monthly-picks-desc {
    font-size: 13px;
  }

  .monthly-picks-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .monthly-pick-card {
    padding: 12px;
    gap: 12px;
  }

  .monthly-pick-reason {
    -webkit-line-clamp: 2;
  }
}

/* ═══════════════════════════════════════════
   RESPONSIVE — Small Mobile (≤480px)
   ═══════════════════════════════════════════ */
@media (max-width: 480px) {
  .monthly-picks-title {
    font-size: 18px;
  }

  .monthly-pick-card {
    padding: 10px;
    gap: 10px;
  }

  .monthly-pick-rank {
    width: 24px;
    height: 24px;
    min-width: 24px;
    font-size: 10px;
  }

  .monthly-pick-ticker {
    font-size: 13px;
  }

  .monthly-pick-targets {
    flex-direction: column;
    gap: 2px;
  }
}

/* ═══════════════════════════════════════════
   WIDE SCREEN (≥1280px)
   ═══════════════════════════════════════════ */
@media (min-width: 1280px) {
  .monthly-picks-section {
    max-width: 1440px;
    padding: 0 40px 80px;
  }

  .monthly-picks-layout {
    gap: 36px;
  }

  .monthly-picks-title {
    font-size: 32px;
  }
}

@media (min-width: 1600px) {
  .monthly-picks-section { max-width: 1600px; }
}
```

---

## 6. Build Pipeline Integration

### Changes to `build.js`:

1. **New placeholder:** `<!-- MONTHLY_PICKS -->` in `_backup_dist/index.html`
2. **New directory scan:** `articles/monthly-picks/*.json`
3. **New function:** `buildMonthlyPicksSection()` — reads latest month file and generates HTML
4. **Inject step:** After Signal Highlights injection, replace `<!-- MONTHLY_PICKS -->` with generated HTML

### Build function pseudocode:

```javascript
function buildMonthlyPicks() {
  const picksDir = path.join(ROOT, 'articles', 'monthly-picks');
  if (!fs.existsSync(picksDir)) return '';

  const files = fs.readdirSync(picksDir)
    .filter(f => f.endsWith('.json'))
    .sort()
    .reverse();

  if (files.length === 0) return '';

  const latest = JSON.parse(fs.readFileSync(path.join(picksDir, files[0]), 'utf8'));

  if (!latest.picks || latest.picks.length === 0) return '';

  // Build video HTML
  const videoHtml = `
    <div class="monthly-picks-video-wrapper">
      <iframe src="${latest.youtubeEmbed}" title="${latest.youtubeTitle || latest.title}"
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen loading="lazy"></iframe>
    </div>
    <div class="monthly-picks-video-caption">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
      Watch the full breakdown
    </div>`;

  // Build pick cards HTML
  let picksHtml = '';
  for (let i = 0; i < latest.picks.length; i++) {
    const p = latest.picks[i];
    const sentimentLabel = p.sentiment === 'bullish' ? '▲ Bullish' : p.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
    const targetHtml = p.priceTarget
      ? `<span class="monthly-pick-target"><span class="target-label">Target</span> ${p.priceTarget}</span>`
      : '';
    const currentHtml = p.currentPrice
      ? `<span class="monthly-pick-current"><span class="target-label">Current</span> ${p.currentPrice}</span>`
      : '';

    picksHtml += `
      <div class="monthly-pick-card">
        <div class="monthly-pick-rank">${i + 1}</div>
        <div class="monthly-pick-body">
          <div class="monthly-pick-top">
            <span class="monthly-pick-ticker">${escapeHtml(p.ticker)}</span>
            <span class="monthly-pick-sentiment ${p.sentiment}">${sentimentLabel}</span>
          </div>
          <div class="monthly-pick-name">${escapeHtml(p.name)}</div>
          <p class="monthly-pick-reason">${escapeHtml(p.reason)}</p>
          <div class="monthly-pick-targets">${targetHtml}${currentHtml}</div>
        </div>
      </div>`;
  }

  const monthDisplay = months[latest.month - 1] + ' ' + latest.year;

  return `
    <section class="monthly-picks-section">
      <div class="monthly-picks-bg"></div>
      <div class="monthly-picks-inner">
        <div class="monthly-picks-header">
          <div class="monthly-picks-badge">
            <span class="monthly-picks-badge-dot"></span>
            Monthly Picks
          </div>
          <h2 class="monthly-picks-title">Our <span class="monthly-picks-gradient">Top Picks</span> for <span class="monthly-picks-month">${monthDisplay}</span></h2>
          <p class="monthly-picks-desc">${escapeHtml(latest.description || '6 curated stocks hand-picked by The Signal editorial team — video analysis included.')}</p>
        </div>
        <div class="monthly-picks-layout">
          <div class="monthly-picks-video">
            ${videoHtml}
          </div>
          <div class="monthly-picks-grid">
            ${picksHtml}
          </div>
        </div>
        ${files.length > 1 ? '<div class="monthly-picks-footer"><a href="/monthly-picks/" class="monthly-picks-archive-link">View Past Months →</a></div>' : ''}
      </div>
    </section>`;
}
```

### Injection point in build.js:

```javascript
// After Signal Highlights injection (line ~508):
indexHtml = indexHtml.replace('SIGNAL_HIGHLIGHTS_PLACEHOLDER', cardsHtml);

// NEW: Inject Monthly Picks
const monthlyPicksHtml = buildMonthlyPicks();
indexHtml = indexHtml.replace('<!-- MONTHLY_PICKS -->', monthlyPicksHtml);
```

---

## 7. Placeholder in Index.html

Insert `<!-- MONTHLY_PICKS -->` in `_backup_dist/index.html` between the Signal Highlights/Hive section and the `<!-- GRID_3 -->` section:

```html
  <!-- GRID_2 -->
  <section class="detail-stocks-section">...</section>
  <section class="hive-home-section">...</section>
  <!-- MONTHLY_PICKS -->        ← NEW PLACEHOLDER
  <!-- GRID_3 -->
```

Current insertion point (between line 326's hive section end and `<!-- GRID_3 -->` on line 327):

```html
  <!-- GRID_2 -->
  ...
</div></section><section class="hive-home-section" id="hiveHomeSection">...</section>
  <!-- MONTHLY_PICKS -->
  <!-- GRID_3 -->
```

---

## 8. Archive Page (Optional Future)

A `/monthly-picks/` archive page listing all past months in a timeline layout. Each entry shows month title, a thumbnail of the video, and links to the YouTube video. This is optional for v1 — the archive link on the homepage section can link to `/monthly-picks/` which would be a static section listing all JSON files in the directory.

---

## 9. Implementation Steps (Ordered)

### Step 1: Create data directory + first data file
- Create `articles/monthly-picks/`
- Create `articles/monthly-picks/2025-07.json` with the first month's data

### Step 2: Add placeholder to homepage template
- Edit `_backup_dist/index.html`
- Insert `<!-- MONTHLY_PICKS -->` between Hive section and `<!-- GRID_3 -->`

### Step 3: Add CSS to main stylesheet
- Append the Monthly Picks CSS block to `_backup_dist/css/main.css`
- Covers all responsive breakpoints (mobile → tablet → desktop → wide)

### Step 4: Extend build.js
- Add `buildMonthlyPicks()` function
- Add import of the picks directory
- Add injection after Signal Highlights section
- Update the build summary output

### Step 5: Build & verify
- Run `node build.js`
- Verify the generated `dist/index.html` has the new section
- Check responsive layout at mobile, tablet, desktop widths
- Verify YouTube iframe loads and plays correctly

### Step 6: Future months
- Each month: create a new `YYYY-MM.json` in `articles/monthly-picks/`
- Rebuild — the section auto-picks the latest file

---

## 10. Design Mockup (Text-based)

```
┌──────────────────────────────────────────────────────┐
│  ┌────────────────────────────────────────────────┐  │
│  │    ● Monthly Picks                              │  │
│  │    Our Top Picks for July 2025                  │  │
│  │    6 curated stocks hand-picked by The Signal   │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐  │
│  │                      │  │  ┌──┐                 │  │
│  │   ┌──────────────┐   │  │  │ 1│ PLTR ▲ Bullish │  │
│  │   │              │   │  │  └──┘ Palantir Tech. │  │
│  │   │   YouTube    │   │  │      AIP platform... │  │
│  │   │    Embed     │   │  │      Target $195     │  │
│  │   │  (16:9)      │   │  │      Current $162    │  │
│  │   └──────────────┘   │  ├──────────────────────┤  │
│  │   ▶ Watch the full   │  │  ┌──┐                 │  │
│  │     breakdown        │  │  │ 2│ RKLB ▲ Bullish │  │
│  │                      │  │  └──┘ Rocket Lab USA │  │
│  └──────────────────────┘  │      Neutron launch  │  │
│                             │      Target $45      │  │
│  ┌────────────────────────┐ │      Current $32     │  │
│  │ View Past Months →     │ ├──────────────────────┤  │
│  └────────────────────────┘ │  ┌──┐  ...and so on  │  │
│                             │  │ 3│ through 6 picks│  │
│                             └──────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 11. Summary

| Aspect | Decision |
|--------|----------|
| **Placement** | After Signal Highlights, before Community Trading (Hive) |
| **Layout** | 2-column: left = sticky video, right = 2×3 grid of stock cards |
| **Data format** | `articles/monthly-picks/YYYY-MM.json` |
| **Pick count** | Exactly 6 per month |
| **Video** | YouTube embed (16:9 iframe) |
| **Design** | Matches Signal theme: dark bg, blue/purple gradients, monospace tickers, sentiment badges |
| **Build integration** | Placeholder `<!-- MONTHLY_PICKS -->` injected by build.js |
| **Responsive** | Tablet: stacks vertically, Mobile: 1-column picks, Small mobile: compact |
| **Archive** | Link to `/monthly-picks/` for browsing past months (future) |
