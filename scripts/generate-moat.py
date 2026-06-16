#!/usr/bin/env python3
"""
Morningstar-Style 5-Factor Economic Moat Assessment
========================
Evaluates a company's economic moat using Morningstar's framework:
  1. Switching Costs – how hard/expensive to switch to a competitor?
  2. Intangible Assets – patents, brands, regulatory advantages
  3. Network Effect – product more valuable as more users join
  4. Cost Advantage – can produce cheaper than competitors?
  5. Efficient Scale – market naturally supports few players

Outputs a structured JSON assessment to stdout.

Usage:
  python3 scripts/generate-moat.py NVDA
  python3 scripts/generate-moat.py NVDA > data/moat-NVDA.json
"""

import json
import sys
import os

# Paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
FINANCIALS_PATH = os.path.join(DATA_DIR, "financials.json")

# ─── Industry benchmarks for context ─────────────────────────
# These are approximate industry averages used for relative scoring
INDUSTRY_BENCHMARKS = {
    "Semiconductors": {
        "gross_margin_avg": 0.50,       # ~50% industry average
        "gross_margin_top": 0.65,       # top quartile
        "rd_to_revenue_avg": 0.12,      # ~12% R&D/revenue for semis
        "rd_to_revenue_top": 0.20,      # top quartile
        "market_share_threshold": 0.40, # 40% share → concentrated
        "op_margin_avg": 0.25,          # ~25% operating margin avg
    },
    "Technology": {
        "gross_margin_avg": 0.55,
        "gross_margin_top": 0.70,
        "rd_to_revenue_avg": 0.10,
        "rd_to_revenue_top": 0.18,
        "market_share_threshold": 0.30,
        "op_margin_avg": 0.20,
    },
    "Software—Application": {
        "gross_margin_avg": 0.70,
        "gross_margin_top": 0.85,
        "rd_to_revenue_avg": 0.15,
        "rd_to_revenue_top": 0.25,
        "market_share_threshold": 0.25,
        "op_margin_avg": 0.25,
    },
    "Software—Infrastructure": {
        "gross_margin_avg": 0.68,
        "gross_margin_top": 0.82,
        "rd_to_revenue_avg": 0.16,
        "rd_to_revenue_top": 0.28,
        "market_share_threshold": 0.25,
        "op_margin_avg": 0.22,
    },
}

# ─── Default benchmarks for unknown industries ───────────────
DEFAULT_BENCHMARKS = {
    "gross_margin_avg": 0.40,
    "gross_margin_top": 0.55,
    "rd_to_revenue_avg": 0.05,
    "rd_to_revenue_top": 0.12,
    "market_share_threshold": 0.35,
    "op_margin_avg": 0.15,
}


def load_financials():
    """Load the financials.json data."""
    if not os.path.exists(FINANCIALS_PATH):
        print(f"ERROR: financials.json not found at {FINANCIALS_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(FINANCIALS_PATH, "r") as f:
        return json.load(f)


def get_benchmarks(industry):
    """Get industry benchmarks or defaults."""
    return INDUSTRY_BENCHMARKS.get(industry, DEFAULT_BENCHMARKS)


def safe_get(stats, key, default=None):
    """Safely get a raw value from stats dict."""
    val = stats.get(key)
    if isinstance(val, dict):
        return val.get("raw", default)
    return val if val is not None else default


def assess_switching_costs(fin, stats, benchmarks):
    """
    Switching Costs: How hard is it for customers to switch to a competitor?
    
    Indicators checked:
    - Ecosystem lock-in (CUDA, proprietary platforms)
    - Revenue concentration (high Data Center % suggests platform stickiness)
    - R&D spending (high R&D → specialized products → harder to switch)
    - Operating margins (high margins → pricing power → switching costs)
    """
    score = 1
    evidence = []

    # Check for segment data (NVDA's Data Center dominance = CUDA lock-in)
    segments = fin.get("segmentData", {})
    breakdown = segments.get("breakdown", [])
    if breakdown:
        top_segment = max(breakdown, key=lambda s: s.get("pct", 0))
        top_pct = top_segment.get("pct", 0)
        if top_pct >= 85:
            score = max(score, 5)
            evidence.append(f"dominant segment at {top_pct}% of revenue (deep ecosystem lock-in)")
        elif top_pct >= 65:
            score = max(score, 4)
            evidence.append(f"high segment concentration at {top_pct}% (significant platform stickiness)")
        elif top_pct >= 45:
            score = max(score, 3)
            evidence.append(f"moderate segment concentration at {top_pct}%")
    
    # Operating margins as proxy for pricing power
    op_margin = safe_get(stats, "operatingMargins", 0) or 0
    op_margin_avg = benchmarks.get("op_margin_avg", 0.15)
    if op_margin > op_margin_avg * 2.5:
        score = max(score, 5)
        evidence.append(f"operating margin {op_margin*100:.0f}% vs {op_margin_avg*100:.0f}% industry (extreme pricing power)")
    elif op_margin > op_margin_avg * 1.8:
        score = max(score, 4)
        evidence.append(f"operating margin {op_margin*100:.0f}% well above industry")
    elif op_margin > op_margin_avg * 1.2:
        score = max(score, 3)
        evidence.append(f"operating margin slightly above industry")

    # Gross margins also signal stickiness
    gm = safe_get(stats, "grossMargins", 0) or 0
    if gm > 0.65:
        score = max(score, 4)
        evidence.append(f"gross margins {gm*100:.0f}% indicate premium pricing / low substitution")
    
    if not evidence:
        evidence.append("no strong switching-cost indicators detected")
        score = max(score, 2)

    rationale = "; ".join(evidence[:3])
    return {"name": "Switching Costs", "score": min(score, 5), "rationale": rationale}


def assess_intangible_assets(fin, stats, benchmarks):
    """
    Intangible Assets: Patents, brands, regulatory advantages.
    
    Indicators:
    - R&D spend as % of revenue (proxy for patent/IP investment)
    - R&D spend growth (sustained innovation)
    - Total revenue (larger companies can afford more IP)
    - Gross margins (brand premium)
    """
    score = 1
    evidence = []

    # R&D as % of revenue
    # Check if we can derive R&D from fmpGrowth or income data
    fmp_growth = fin.get("fmpGrowth", [])
    rd_growth = None
    if fmp_growth:
        latest = fmp_growth[0]
        rd_growth = latest.get("rdexpenseGrowth")
    
    # Try to get R&D from income statements (fmpIncome)
    fmp_income = fin.get("fmpIncome", [])
    revenue = safe_get(stats, "totalRevenue", 0) or 0
    
    if fmp_income and revenue:
        latest_income = fmp_income[0]
        rd_expense = latest_income.get("researchAndDevelopmentExpenses", 0)
        if rd_expense and rd_expense > 0:
            rd_pct = rd_expense / revenue if revenue else 0
            rd_avg = benchmarks.get("rd_to_revenue_avg", 0.05)
            rd_top = benchmarks.get("rd_to_revenue_top", 0.12)
            
            if rd_pct > rd_top:
                score = max(score, 5)
                evidence.append(f"R&D at {rd_pct*100:.1f}% of revenue (top-tier innovation spend)")
            elif rd_pct > rd_avg * 1.5:
                score = max(score, 4)
                evidence.append(f"R&D at {rd_pct*100:.1f}% of revenue (above industry)")
            elif rd_pct > rd_avg:
                score = max(score, 3)
                evidence.append(f"R&D spending in line with industry")

    # R&D growth signals sustained innovation
    if rd_growth is not None and rd_growth > 0.30:
        score = max(score, 5)
        evidence.append(f"R&D spending growing at {rd_growth*100:.0f}% YoY (heavy innovation investment)")
    elif rd_growth is not None and rd_growth > 0.15:
        score = max(score, 4)
        evidence.append(f"R&D spending growing at {rd_growth*100:.0f}% YoY")
    elif rd_growth is not None and rd_growth > 0.05:
        score = max(score, 3)

    # Gross margins signal brand power
    gm = safe_get(stats, "grossMargins", 0) or 0
    gm_top = benchmarks.get("gross_margin_top", 0.55)
    if gm > gm_top * 1.05:
        score = max(score, 4)
        evidence.append(f"premium gross margins {gm*100:.0f}% reflect brand/IP power")
    
    # Revenue scale as proxy for IP portfolio size
    rev = safe_get(stats, "totalRevenue", 0) or 0
    if rev > 50e9:  # $50B+
        score = max(score, 4)
        evidence.append(f"large revenue base ({rev/1e9:.0f}B) enables sustained IP investment")

    if not evidence:
        evidence.append("limited intangible asset indicators available")
        score = max(score, 2)

    rationale = "; ".join(evidence[:3])
    return {"name": "Intangible Assets", "score": min(score, 5), "rationale": rationale}


def assess_network_effect(fin, stats, benchmarks):
    """
    Network Effect: Product becomes more valuable as more users join.
    
    Indicators:
    - Platform business model (developer ecosystems, marketplaces)
    - Revenue growth acceleration (flywheel effect)
    - High revenue concentration in platform segment
    - Strong EPS growth (network effects drive operating leverage)
    """
    score = 1
    evidence = []

    # Segment data indicates platform nature
    segments = fin.get("segmentData", {})
    breakdown = segments.get("breakdown", [])
    if breakdown:
        top_segment = max(breakdown, key=lambda s: s.get("pct", 0))
        top_name = top_segment.get("name", "").lower()
        if any(kw in top_name for kw in ["data center", "platform", "cloud", "marketplace", "network"]):
            score = max(score, 4)
            evidence.append(f"platform-centric business ({top_name} at {top_segment['pct']}%)")
    
    # Revenue growth acceleration → network effects
    rev_growth = safe_get(stats, "revenueGrowth", 0) or 0
    fmp_growth = fin.get("fmpGrowth", [])
    
    if rev_growth > 0.50:  # 50%+ revenue growth
        score = max(score, 5)
        evidence.append(f"explosive {rev_growth*100:.0f}% revenue growth (flywheel spinning)")
    elif rev_growth > 0.20:
        score = max(score, 4)
        evidence.append(f"strong {rev_growth*100:.0f}% revenue growth")
    elif rev_growth > 0.10:
        score = max(score, 3)
    
    # Check for accelerating growth (multi-year data)
    if fmp_growth and len(fmp_growth) >= 2:
        rev_g1 = fmp_growth[0].get("revenueGrowth", 0) or 0
        rev_g2 = fmp_growth[1].get("revenueGrowth", 0) or 0
        if rev_g1 > rev_g2 > 0:
            score = max(score, 4)
            evidence.append("accelerating multi-year revenue growth (network effect building)")
    
    # EPS growth (operating leverage from network)
    eps_growth = safe_get(stats, "epsGrowth", 0) or 0
    if eps_growth > 0.50:
        score = max(score, 4)
        evidence.append(f"high EPS growth {eps_growth*100:.0f}% (operating leverage from scale)")

    if not evidence:
        evidence.append("no clear network-effect indicators in available data")
        score = max(score, 2)

    rationale = "; ".join(evidence[:3])
    return {"name": "Network Effect", "score": min(score, 5), "rationale": rationale}


def assess_cost_advantage(fin, stats, benchmarks):
    """
    Cost Advantage: Can the company produce cheaper than competitors?
    
    Indicators:
    - Gross margins vs industry average
    - Operating margins (efficiency)
    - Scale (fixed cost absorption)
    - Free cash flow generation
    """
    score = 1
    evidence = []

    gm = safe_get(stats, "grossMargins", 0) or 0
    gm_avg = benchmarks.get("gross_margin_avg", 0.40)
    
    if gm > gm_avg * 1.5:
        score = max(score, 5)
        evidence.append(f"gross margins {gm*100:.0f}% vs {gm_avg*100:.0f}% industry (massive cost advantage)")
    elif gm > gm_avg * 1.3:
        score = max(score, 4)
        evidence.append(f"gross margins {gm*100:.0f}% well above {gm_avg*100:.0f}% industry")
    elif gm > gm_avg * 1.1:
        score = max(score, 3)
        evidence.append(f"gross margins slightly above industry average")
    elif gm > gm_avg:
        score = max(score, 2)
    
    # Operating margin
    op_margin = safe_get(stats, "operatingMargins", 0) or 0
    op_avg = benchmarks.get("op_margin_avg", 0.15)
    if op_margin > op_avg * 2:
        score = max(score, 5)
        evidence.append(f"operating margin {op_margin*100:.0f}% vs {op_avg*100:.0f}% (extreme efficiency)")
    elif op_margin > op_avg * 1.5:
        score = max(score, 4)
    
    # Revenue scale → cost absorption
    rev = safe_get(stats, "totalRevenue", 0) or 0
    if rev > 100e9:
        score = max(score, 5)
        evidence.append(f"massive scale (${rev/1e9:.0f}B revenue) enables fixed-cost absorption")
    elif rev > 10e9:
        score = max(score, 4)
        evidence.append(f"significant scale (${rev/1e9:.0f}B revenue)")
    
    # FCF generation
    fcf = safe_get(stats, "freeCashflow", 0) or 0
    if rev > 0 and fcf / rev > 0.20:
        score = max(score, 4)
        evidence.append(f"strong free cash flow ({fcf/rev*100:.0f}% of revenue)")

    if not evidence:
        evidence.append("cost position not clearly distinguishable from data")
        score = max(score, 2)

    rationale = "; ".join(evidence[:3])
    return {"name": "Cost Advantage", "score": min(score, 5), "rationale": rationale}


def assess_efficient_scale(fin, stats, benchmarks):
    """
    Efficient Scale: Market naturally supports few players.
    
    Indicators:
    - Market share / dominance in key segment
    - High barriers to entry (capital intensity, tech complexity)
    - High revenue concentration in one segment
    - Limited competition (high margins sustained over time)
    """
    score = 1
    evidence = []

    segments = fin.get("segmentData", {})
    breakdown = segments.get("breakdown", [])
    
    # Dominant segment suggests natural monopoly/duopoly
    if breakdown:
        top_segment = max(breakdown, key=lambda s: s.get("pct", 0))
        top_pct = top_segment.get("pct", 0)
        threshold = benchmarks.get("market_share_threshold", 0.35)
        
        if top_pct >= 85:
            score = max(score, 5)
            evidence.append(f"{top_segment['name']} at {top_pct}% share (near-monopoly position)")
        elif top_pct >= 65:
            score = max(score, 4)
            evidence.append(f"{top_segment['name']} dominance at {top_pct}% revenue share")
        elif top_pct >= threshold * 1.5:
            score = max(score, 3)
            evidence.append(f"majority revenue from one segment ({top_pct}%)")
    
    # Gross margins sustained high → barriers to entry
    gm = safe_get(stats, "grossMargins", 0) or 0
    gm_top = benchmarks.get("gross_margin_top", 0.55)
    if gm > gm_top:
        score = max(score, 5)
        evidence.append(f"premium {gm*100:.0f}% gross margins sustained (high barriers)")
    
    # Revenue scale → capital barriers
    rev = safe_get(stats, "totalRevenue", 0) or 0
    assets = safe_get(stats, "totalAssets", 0) or 0  # might not exist in stats
    
    if rev > 100e9:
        score = max(score, 4)
        evidence.append(f"$100B+ revenue scale creates massive entry barrier")

    # Market cap → incumbent advantage
    mcap = safe_get(stats, "marketCap", 0) or 0
    if mcap > 1e12:
        score = max(score, 4)
    elif mcap > 100e9:
        score = max(score, 3)

    if not evidence:
        evidence.append("insufficient data for efficient scale assessment")
        score = max(score, 2)

    rationale = "; ".join(evidence[:3])
    return {"name": "Efficient Scale", "score": min(score, 5), "rationale": rationale}


def generate_analysis(sources, rating, avg_score):
    """Generate a 2-3 sentence overall assessment."""
    wide_sources = [s for s in sources if s["score"] >= 4]
    narrow_sources = [s for s in sources if s["score"] == 3]
    
    source_names_wide = [s["name"] for s in wide_sources]
    source_names_all = [s["name"] for s in sources]
    
    if rating == "Wide":
        return (
            f"{' and '.join(source_names_wide[:3])} create a durable competitive fortress. "
            f"The company's moat is reinforced by multiple reinforcing factors, making it "
            f"unlikely competitors can erode its position in the next decade."
        )
    elif rating == "Narrow":
        return (
            f"{' and '.join(source_names_wide[:2] or [source_names_all[0]])} provide some competitive protection, "
            f"but not all moat sources are fully developed. The company has defensible advantages "
            f"that should persist for several years but may face erosion over time."
        )
    else:
        return (
            f"No significant moat sources were identified. The company operates in a competitive "
            f"market with limited barriers to entry. It must compete primarily on price and execution."
        )


def assess_moat(symbol):
    """
    Main assessment function. Returns a dict with the moat assessment.
    """
    financials = load_financials()
    fin = financials.get(symbol.upper())
    
    if not fin:
        print(f"ERROR: No data found for ticker {symbol}", file=sys.stderr)
        sys.exit(1)
    
    stats = fin.get("stats", {})
    company = fin.get("company", {})
    industry = company.get("industry", "Technology")
    benchmarks = get_benchmarks(industry)
    
    # Assess each of the 5 Morningstar moat sources
    sources = [
        assess_switching_costs(fin, stats, benchmarks),
        assess_intangible_assets(fin, stats, benchmarks),
        assess_network_effect(fin, stats, benchmarks),
        assess_cost_advantage(fin, stats, benchmarks),
        assess_efficient_scale(fin, stats, benchmarks),
    ]
    
    # Calculate overall rating
    total_score = sum(s["score"] for s in sources)
    avg_score = total_score / len(sources)
    stars = round(avg_score)
    stars = max(1, min(5, stars))  # clamp 1-5
    
    if stars >= 4:
        rating = "Wide"
    elif stars >= 2:
        rating = "Narrow"
    else:
        rating = "None"
    
    # Confidence: based on variance of scores
    scores = [s["score"] for s in sources]
    score_variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
    if score_variance < 0.5:
        confidence = "High"
    elif score_variance < 1.5:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    analysis = generate_analysis(sources, rating, avg_score)
    
    return {
        "symbol": symbol.upper(),
        "industry": industry,
        "rating": rating,
        "stars": stars,
        "confidence": confidence,
        "sources": sources,
        "analysis": analysis,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-moat.py <TICKER>", file=sys.stderr)
        print("  python3 scripts/generate-moat.py NVDA > data/moat-NVDA.json", file=sys.stderr)
        sys.exit(1)
    
    symbol = sys.argv[1]
    result = assess_moat(symbol)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
