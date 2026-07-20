# Mobile (390px) Visual Fix Plan — readthesignal.net

**Author:** Kim-K (CSS/UI Design Expert)
**Target viewport:** 390px (iPhone 12/13/14, Galaxy S23)
**Source CSS:** `/home/chino/thesignal/_backup_dist/css/main.css`
**Source HTML:** `/home/chino/thesignal/_backup_dist/index.html`

---

## Table of Contents

1. [P0 — Broken / Functional Issues](#p0)
2. [P1 — First Impression / Layout Issues](#p1)
3. [P2 — Polish / Refinement](#p2)
4. [Implementation Notes](#notes)

---

<a name="p0"></a>
## P0 — BROKEN / FUNCTIONAL ISSUES (Fix now — these are bugs)

### P0-1: Pulse section has zero bottom padding, touching the section divider below

**Current (broken):**
```css
.featured-pulse-aside .pulse-section {
  margin: 0;
  padding: 20px 20px 0;   /* ← bottom padding = 0 */
  max-width: none;
  border-top: none;
  height: 100%;
  display: flex;
  flex-direction: column;
}
```

**Problem:** `padding-bottom: 0` means the `.pulse-chat` container (which has `border: 1px solid var(--border)`) sits flush against the `.section-divider` below. There's no air gap.

**Fix — Add at line 1351:**
```css
.featured-pulse-aside .pulse-section {
  /* keep existing */
  padding: 20px 20px 16px;  /* ← was 0, now 16px */
}
```

**Alternative** (if you prefer the bottom gap to come from the row itself):
```css
.featured-pulse-row {
  margin: 0 0 32px;  /* ← was 24px */
}
```
But fixing the padding on `.pulse-section` directly is safer and more targeted.

### P0-2: Trending Stocks — 7-row vertical list is too tall on mobile

**Current:**
```css
.trending-list {
  display: flex;
  flex-direction: column;   /* ← 7 items stacked = ~280px */
}
```

**Problem:** At 390px, 7 rows at ~40px each = 280px of content just for the stock list, plus header. This is dominant vertical space.

**Fix — Add inside `@media (max-width: 640px)` (at line 6741):**
```css
@media (max-width: 640px) {
  /* Existing padding/row rules stay */

  /* Show only 4 items, hide rest */
  .trending-list .trending-row:nth-child(n+5) {
    display: none;
  }
}
```

**Alternative A — 2-column grid (better if you want all 7 visible):**
```css
@media (max-width: 640px) {
  .trending-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    flex-direction: row;  /* override column */
  }
  .trending-row {
    border-bottom: 1px solid #161b26;
  }
  .trending-row:nth-child(even) {
    border-left: 1px solid #161b26;
  }
}
```
This renders 7 items as: 2 columns × 4 rows (last row has 1 item). Each row is ~36px, so total = ~144px instead of 280px. **This is the recommended approach.**

**Alternative B — Horizontal scroll:**
```css
@media (max-width: 640px) {
  .trending-list {
    flex-direction: row;
    overflow-x: auto;
    gap: 0;
    -webkit-overflow-scrolling: touch;
  }
  .trending-row {
    flex: 0 0 auto;
    flex-direction: column;
    padding: 8px 14px;
    min-width: 110px;
    border-bottom: none;
    border-right: 1px solid #161b26;
    align-items: flex-start;
    gap: 2px;
  }
}
```

---

<a name="p1"></a>
## P1 — FIRST IMPRESSION / LAYOUT ISSUES (Fix next — visual quality)

### P1-1: Hive Home section is massively oversized on mobile

**Current (no mobile override exists at all):**
```css
.hive-home-inner {
  padding: 40px 36px;
}
.hive-home-headline {
  font-size: clamp(30px, 5vw, 42px);  /* at 390px: ~30px */
  margin: 0 0 16px;
}
.hive-home-desc {
  margin: 0 auto 32px;
  line-height: 1.75;
}
.hive-home-stats {
  gap: 48px;
  margin-bottom: 32px;
}
.hive-home-cta {
  padding: 14px 34px;
}
.hive-home-section {
  margin: 48px auto;
}
```

**Problem:** The hive section is ~500-550px tall on mobile. Way too much for a section that should be compact.

**Fix — Add new media query block for mobile (insert after line 5181 or at line 5240ish):**
```css
@media (max-width: 640px) {
  .hive-home-section {
    margin: 24px auto;
    padding: 0 16px;
  }
  .hive-home-inner {
    padding: 24px 20px;
  }
  .hive-home-badge {
    margin-bottom: 16px;
    font-size: 9px;
    letter-spacing: 2px;
    padding: 5px 14px;
  }
  .hive-home-headline {
    font-size: 22px;
    margin: 0 0 10px;
    line-height: 1.2;
  }
  .hive-home-desc {
    font-size: 12.5px;
    margin: 0 auto 18px;
    line-height: 1.5;
  }
  .hive-home-stats {
    gap: 20px;
    margin-bottom: 18px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-items: center;
  }
  .hive-home-stat {
    min-width: 0;
  }
  .hive-stat-number {
    font-size: 18px;
  }
  .hive-stat-label {
    font-size: 9px;
    letter-spacing: 1.5px;
  }
  .hive-home-actions {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }
  .hive-home-cta {
    padding: 10px 20px;
    font-size: 10px;
    letter-spacing: 1.5px;
    justify-content: center;
    width: 100%;
  }
}
```

This reduces the section from ~550px to ~340px on 390px.

### P1-2: Section dividers use 48px margin — too aggressive on mobile

**Current:**
```css
.section-divider {
  margin: 48px 0;    /* 96px total vertical space per divider */
}
```

**Problem:** Every divider consumes 96px of vertical space. On a 390px viewport that's a huge percentage.

**Fix — Add after the existing `.section-divider` rules (around line 3259):**
```css
@media (max-width: 640px) {
  .section-divider {
    margin: 24px 0;  /* was 48px — half the space */
  }
}
```

### P1-3: Featured article + Pulse section gap on mobile

**Current:**
```css
.featured-pulse-row {
  margin: 0 0 24px;
  padding: 0 16px;
}
```

**Fix — Add to existing `@media (max-width: 768px)` block (at line 1590):**
```css
@media (max-width: 768px) {
  .featured-pulse-row {
    margin: 0 0 8px;    /* was 24px — already handled by section-divider below */
    padding: 0 12px;    /* was 16px */
  }
}
```

The grid already stacks on mobile (`grid-template-columns: 1fr`), so we just need tighter margins.

### P1-4: Trending + Hive side-by-side on mobile (user request)

**User's stated desire**: Make Trending Stocks AND The Hive section smaller so they can sit side by side on mobile.

**Current DOM order:**
```
<section-divider>
<section.trending-section>    ← trending stocks
<section-divider>
<section.scorecard-section>   ← signal scorecard
<detail-stocks-section>        ← signal highlights carousel
<section.hive-home-section>    ← hive
<section-divider>
```

**Problem:** Trending and Hive are separated by Scorecard + Highlights. They can't be side-by-side without DOM reordering.

**Approach A — Dedicated mobile-only wrapper (requires DOM change):**
Wrap both Trending and Hive in a new container after Scorecard:
```html
<section class="trending-hive-mobile-row">
  <section class="trending-section">...</section>
  <section class="hive-home-section">...</section>
</section>
```
Then CSS:
```css
@media (max-width: 640px) {
  .trending-hive-mobile-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    align-items: stretch;
  }
  .trending-hive-mobile-row .trending-section {
    margin: 0;
    padding: 0;
  }
  .trending-hive-mobile-row .hive-home-section {
    margin: 0;
    padding: 0;
  }
}
```
This is the cleanest approach but modifies the HTML.

**Approach B — Target specific sections via existing selectors (no HTML change):**
This won't work cleanly because they're separated by Scorecard in the DOM.

**Approach C — Sidecar layout (no HTML change, CSS only):**
If you can move Hive to appear right after Trending in the HTML (before Scorecard), then:
```css
@media (max-width: 640px) {
  .trending-section {
    float: left;
    width: 48%;
  }
  .hive-home-section {
    float: right;
    width: 48%;
    margin-top: 0;
  }
}
```
But this requires DOM reordering.

**Recommendation:** Approach A with a minimal HTML change. Move `.hive-home-section` up next to `.trending-section` in the DOM, wrapped in a `.trending-hive-mobile-row` container, place it after `.section-divider` that follows Scorecard. This is the cleanest CSS solution.

---

<a name="p2"></a>
## P2 — POLISH / REFINEMENT (Fix when time allows)

### P2-1: Scorecard section inner padding can be tighter on mobile

**Current (already has mobile override):**
```css
@media (max-width: 768px) {
  .scorecard-inner {
    padding: 20px 16px;   /* already tighter than 32px desktop */
  }
}
```

**Suggestion for 390px specifically — Add `@media (max-width: 480px)` block:**
```css
@media (max-width: 480px) {
  .scorecard-inner {
    padding: 14px 12px;
  }
  .scorecard-grid {
    grid-template-columns: 1fr;  /* single column at very small sizes */
  }
}
```

### P2-2: Pulse send button vs input field alignment check

**Current:**
```css
.pulse-input-area {
  display: flex;
  align-items: center;   /* ← centers vertically */
  gap: 8px;
  padding: 10px 16px;
}
.pulse-input {
  flex: 1;
  padding: 6px 0;
  font-size: 13.5px;
  line-height: 1.4;
}
.pulse-send {
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  flex-shrink: 0;
  /* no explicit height or width — defaults to content-based */
}
```

**Assessment:** The send button has `padding: 8px` but no explicit `width`/`height`. The SVG inside is `width="18" height="18"`. So the button is roughly 18+16=34px square. The input has `font-size: 13.5px` with `padding: 6px 0` = roughly 13.5*1.4+12 = ~31px tall. These should be close enough. But the SVG might appear slightly off-center if `line-height` on the button isn't set.

**Fix — Add to ensure perfect alignment:**
```css
.pulse-send {
  width: 34px;
  height: 34px;
}
```

This guarantees the button is a perfect square, and flexbox centers the SVG inside.

### P2-3: Comments section padding reduction on mobile

**Current:**
```css
.comments-section {
  padding: 48px 24px 64px;
}
```

**Fix — Add mobile override (or extend the existing 768px block around line 1589):**
```css
@media (max-width: 640px) {
  .comments-section {
    padding: 24px 16px 32px;  /* was 48px 24px 64px */
  }
}
```

### P2-4: Hive section top margin on mobile — already addressed in P1-1, but double-check

The `.hive-home-section` has `margin: 48px auto`. After P1-1 fix, this becomes `24px auto`. This is consistent with the halved section-divider margin in P1-2.

### P2-5: Trending section lacks margin-bottom

**Current:**
```css
.trending-section {
  max-width: 1280px;
  margin: 0 auto;          /* ← no margin-bottom */
  padding: 0 24px;
}
```

**Problem:** No bottom margin means the `.section-divider` below provides all spacing. This is actually fine since the divider handles it. But if the divider margins are halved (P1-2), consider adding:
```css
@media (max-width: 640px) {
  .trending-section {
    margin: 0 auto 8px;   /* small extra cushion */
  }
}
```

---

<a name="notes"></a>
## Implementation Notes

### File to edit
`/home/chino/thesignal/_backup_dist/css/main.css`

### Summary of all CSS changes

| Issue | Selector | Change | Breakpoint |
|-------|----------|--------|------------|
| P0-1 | `.featured-pulse-aside .pulse-section` | `padding: 20px 20px 16px` | global (line 1351) |
| P0-2a | `.trending-list .trending-row:nth-child(n+5)` | `display: none` | `@media (max-width: 640px)` (line 6741) |
| P0-2b | `.trending-list` | `display: grid; grid-template-columns: 1fr 1fr;` | `@media (max-width: 640px)` (line 6741) |
| P1-1 | `.hive-home-section` | `margin: 24px auto; padding: 0 16px;` | New `@media (max-width: 640px)` |
| P1-1 | `.hive-home-inner` | `padding: 24px 20px;` | same |
| P1-1 | `.hive-home-headline` | `font-size: 22px; margin: 0 0 10px;` | same |
| P1-1 | `.hive-home-desc` | `font-size: 12.5px; margin: 0 auto 18px;` | same |
| P1-1 | `.hive-home-stats` | `gap: 20px; grid-template-columns: 1fr 1fr;` | same |
| P1-1 | `.hive-home-cta` | `padding: 10px 20px; width: 100%;` | same |
| P1-2 | `.section-divider` | `margin: 24px 0;` | New `@media (max-width: 640px)` |
| P1-3 | `.featured-pulse-row` | `margin: 0 0 8px; padding: 0 12px;` | `@media (max-width: 768px)` (line 1590) |
| P1-4 | `.trending-hive-mobile-row` (new wrapper) | `grid-template-columns: 1fr 1fr` | New `@media (max-width: 640px)` |
| P2-1 | `.scorecard-inner` | `padding: 14px 12px;` | New `@media (max-width: 480px)` |
| P2-2 | `.pulse-send` | `width: 34px; height: 34px;` | global (line 1555) |
| P2-3 | `.comments-section` | `padding: 24px 16px 32px;` | New `@media (max-width: 640px)` |

### Estimated height savings per section (390px viewport)

| Section | Current height | After fix | Savings |
|---------|---------------|-----------|---------|
| Featured + Pulse row | ~240px | ~240px (gap fix only) | 0px |
| Section divider | 50px (2px + 48px*2) | 26px (2px + 24px*2) | 24px |
| Trending Stocks | ~310px (7 rows) | ~170px (2-col grid, 7 items) | 140px |
| Section divider | 50px | 26px | 24px |
| Scorecard Section | ~310px | ~280px | 30px |
| Hive Home | ~530px | ~340px | 190px |
| Section divider | 50px | 26px | 24px |
| **Total page height** | **~1540px** | **~1108px** | **~432px saved** |

This puts most content above the fold on a 390px viewport (which is 844px tall in landscape mode).
