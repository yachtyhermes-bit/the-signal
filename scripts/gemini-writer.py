#!/usr/bin/env python3
"""One-shot article writer for The Signal.

The prose is written by Gemini 3.8 Flash in a SINGLE call with a small, fixed context
(house style + research brief). This replaces the old design where the premium model was the
orchestrator and therefore re-sent a growing agent context on every turn — that burned ~1M
tokens per edition to produce ~2,500 tokens of article.

Usage:
  python3 scripts/gemini-writer.py <brief.md> <out.md>
  python3 scripts/gemini-writer.py <brief.md> --dry-run     # print prompt + cost estimate, no call

Output format it asks the model for:
  TITLE: ...
  SUBTITLE: ...
  SUMMARY: ...
  ---BODY---
  <markdown body>

Falls back to gemini-2.5-flash if the primary model errors or returns empty.
"""
import json, os, pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
STYLE = ROOT / 'scripts' / 'writer-style.md'
ENV = pathlib.Path.home() / '.hermes' / 'profiles' / 'yachty' / '.env'
API = 'https://openrouter.ai/api/v1/chat/completions'
PRICES = {  # $ per 1M tokens, OpenRouter list prices
    'google/gemini-3.8-flash': (0.75, 3.75),
    'google/gemini-2.5-flash': (0.30, 2.50),
}
MAX_TOKENS = 8000


def api_key():
    key = os.environ.get('OPENROUTER_API_KEY')
    if key:
        return key
    if ENV.exists():
        for line in ENV.read_text().splitlines():
            m = re.match(r'\s*(?:export\s+)?OPENROUTER_API_KEY\s*=\s*(.+)\s*$', line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    sys.exit('FAIL: OPENROUTER_API_KEY not found (env or profile .env)')


SYSTEM = """You are the writer for The Signal (readthesignal.net). You write ONE article from a
verified research brief. Follow the house style below exactly.

Return ONLY this, with no preamble and no code fences:

TITLE: <one institutional line, subject + event + angle>
SUBTITLE: <one line, the specific hook>
SUMMARY: <two sentences, plain, no price levels>
---BODY---
<the article body in Markdown, using ## for section headings>

Start the body with the opening paragraphs — do not repeat the title as a heading. Never invent a
number, a quotation, or a source: everything must come from the brief. If the brief lacks something
the style asks for, write around it rather than inventing it.

LENGTH: aim for 1,500-1,900 words. Break the body into 4-7 sections using ## headings (short, plain,
no numbering). Always include a dedicated bear-case section. Ending on a plain, declarative line —
no summary paragraph, no call to action.

---

HOUSE STYLE
"""


def build_prompt(brief):
    return SYSTEM + STYLE.read_text() + '\n\n---\n\nRESEARCH BRIEF\n' + brief


def call(model, prompt, key):
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.9,
        'max_tokens': MAX_TOKENS,
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://readthesignal.net',
        'X-Title': 'The Signal writer',
    })
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    brief_path, out_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    prompt = build_prompt(brief_path.read_text())

    if '--dry-run' in sys.argv:
        print(f'prompt chars: {len(prompt)} (~{len(prompt)//4} tokens)')
        print(f'est. input cost on 3.8-flash: ${len(prompt)/4/1e6*PRICES["google/gemini-3.8-flash"][0]:.4f}')
        return

    key = api_key()
    for model in ('google/gemini-3.8-flash', 'google/gemini-2.5-flash'):
        try:
            resp = call(model, prompt, key)
        except urllib.error.HTTPError as e:
            print(f'  [writer] {model} HTTP {e.code}: {e.read()[:200]!r}', file=sys.stderr)
            continue
        except Exception as e:
            print(f'  [writer] {model} failed: {e}', file=sys.stderr)
            continue
        text = (resp.get('choices') or [{}])[0].get('message', {}).get('content') or ''
        if not text.strip():
            print(f'  [writer] {model} returned empty, trying next', file=sys.stderr)
            continue
        u = resp.get('usage') or {}
        pin, pout = PRICES[model]
        cost = u.get('prompt_tokens', 0) / 1e6 * pin + u.get('completion_tokens', 0) / 1e6 * pout
        out_path.write_text(text.strip() + '\n')
        words = len(text.split())
        # log spend: this call bypasses Hermes session accounting, so the budget guard reads it here
        try:
            import time as _t
            with open(ROOT / 'data' / 'writer-spend.jsonl', 'a') as lf:
                lf.write(json.dumps({'ts': _t.time(), 'model': model, 'words': words,
                                     'in': u.get('prompt_tokens', 0), 'out': u.get('completion_tokens', 0),
                                     'cost': round(cost, 6)}) + '\n')
        except Exception:
            pass
        print(f'  [writer] {model}: {words} words, '
              f'{u.get("prompt_tokens", 0)} in / {u.get("completion_tokens", 0)} out '
              f'= ${cost:.4f}', file=sys.stderr)
        return
    sys.exit('FAIL: no model produced an article')


if __name__ == '__main__':
    main()
