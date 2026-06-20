#!/usr/bin/env python3
"""Extract bodyHtml content from saved The Signal article HTML files."""
import re
import html as html_module

files = [
    ("article1_servicenow.html", "ServiceNow AI Agent Enterprise Moat"),
    ("article2_sofi.html", "SoFi Fintech Profits"),
    ("article3_palantir.html", "Palantir AIP Defense Contracts"),
    ("article4_amd.html", "AMD MI400 AI Chip Underdog"),
    ("article5_tsmc.html", "TSMC Advanced Chip Monopoly"),
]

for filename, title in files:
    print(f"\n{'='*80}")
    print(f"ARTICLE: {title}")
    print(f"{'='*80}")
    try:
        with open(filename, 'r') as f:
            html = f.read()
        
        # Try to find bodyHtml in embedded JSON (Next.js page props pattern)
        match = re.search(r'"bodyHtml":"((?:[^"\\]|\\.)*)"', html)
        if match:
            raw = match.group(1)
            # Unescape JSON string escaping
            raw = raw.replace('\\n', '\n').replace('\\t', '\t').replace('\\/', '/')
            raw = re.sub(r'\\(.)', r'\1', raw)
            # Decode HTML entities
            text = html_module.unescape(raw)
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Collapse whitespace
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = text.strip()
            print(text[:8000])
        else:
            # Fallback: look for article content in HTML
            m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
            if m:
                text = re.sub(r'<[^>]+>', '', m.group(1))
                text = re.sub(r'\n{3,}', '\n\n', text)
                print(text[:8000])
            else:
                # Try to find any meaningful content in script data
                m2 = re.search(r'__NEXT_DATA__.*?({.*?}).*?</script>', html, re.DOTALL)
                if m2:
                    print("Found Next.js data block (unparsed):")
                    print(m2.group(0)[:2000])
                else:
                    print("NO bodyHtml OR article tag found. First 2000 chars of HTML:")
                    print(html[:2000])
    except Exception as e:
        print(f"ERROR: {e}")
