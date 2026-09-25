#!/usr/bin/env node
/**
 * render-smoke.mjs — "does this page actually PAINT?" check for the key pages of readthesignal.net.
 *
 * Why this exists:
 *   /hive/boardroom/ returned HTTP 200 for weeks while rendering a blank page. The whole site
 *   content was nested inside <div id="searchOverlay"> (opacity:0; visibility:hidden;
 *   position:fixed) because the search overlay's close button was missing </svg></button>.
 *   Nothing painted and the document collapsed to a single viewport, so the page could not even
 *   scroll. A status-code check can never see that; only rendering can.
 *
 * What it does: drives headless Chromium over CDP, loads each page, and fails a page when
 *   - the HTTP status is not 200,
 *   - the document is not taller than the viewport (the collapsed-page signature),
 *   - content is trapped inside a hidden overlay container (#searchOverlay, #drawer, ...),
 *   - a watched element is invisible (opacity/visibility),
 *   - a required text marker is missing from the RENDERED text,
 *   - a required element count is not met (e.g. leaderboard rows),
 *   - the page logged an uncaught exception or a same-origin console error.
 *
 * Usage:  node scripts/render-smoke.mjs [--origin https://readthesignal.net] [--json /tmp/out.json]
 * Exit:   0 = all pages healthy, 1 = at least one page failed.
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const args = process.argv.slice(2);
const argOf = (flag, dflt) => {
  const i = args.indexOf(flag);
  return i >= 0 && args[i + 1] ? args[i + 1] : dflt;
};
const ORIGIN = argOf('--origin', 'https://readthesignal.net').replace(/\/$/, '');
const JSON_OUT = argOf('--json', '');
// Ad-hoc single-page mode: --url <path> [--img "<css selector>"] [--min-width 600]
// Handy right after a hero swap: proves the image files really LOAD (naturalWidth > 0),
// not merely that its URL appears in the HTML.
const ADHOC_URL = argOf('--url', '');
const ADHOC_IMG = argOf('--img', '');
const PORT = 9411;

// Pages worth watching, with the evidence that proves each one really rendered.
const PAGES = [
  { url: '/',                            markers: ['the signal', 'terms of service'], watch: ['nav.nav'] },
  { url: '/hive/',                       markers: ['hive'],                          watch: [] },
  { url: '/hive/boardroom/',             markers: ['leaderboard', 'trader'],
    watch: ['#leaderboard'], rows: { selector: '#hiveTableBody tr', min: 4 } },
  { url: '/articles/',                   markers: ['the signal'],                    watch: [] },
  { url: '/article/nvda-hugging-face-acquisition-2026/',
    markers: ['by chino iruke', 'sources'], watch: [], rows: { selector: 'table tr', min: 0 } },
  { url: '/stocks/NVDA/',                markers: ['nvidia'],                        watch: [] },
  { url: '/sector/etfs/',                markers: ['etf'],                           watch: [] },
  { url: '/signal-vs-the-street/',       markers: ['street'],                        watch: [] },
  { url: '/about/',                      markers: ['chino iruke', 'mechanical technician'], watch: [] },
  { url: '/pricing/',                    markers: ['premium'],                        watch: [] },
  { url: '/corrections/',                markers: ['correction'],                     watch: [] },
  { url: '/terms/',                      markers: ['terms'],                          watch: [] },
  { url: '/disclosure/',                 markers: ['disclosure'],                     watch: [] },
];

// Console noise that is not a site defect.
const IGNORE = [/favicon/i, /net::ERR_/i, /analytics|gtag|googletagmanager|doubleclick|clarity|hotjar/i,
                /extension:\/\//i, /AbortError/i, /play\(\) request was interrupted/i];

const HIDDEN_OVERLAY_SELECTOR = '#searchOverlay, #drawer, .search-overlay, .drawer, #drawerOverlay, #searchModal';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function baseUrl() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      if (r.ok) return (await r.json()).webSocketDebuggerUrl;
    } catch {}
    await sleep(500);
  }
  throw new Error('chromium did not expose a DevTools endpoint');
}

function cdpClient(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 0;
    const pending = new Map();
    let handlers = [];
    ws.onerror = (e) => reject(new Error('ws error'));
    ws.onmessage = (e) => {
      const m = JSON.parse(e.data);
      if (m.id && pending.has(m.id)) {
        const { resolve: res } = pending.get(m.id);
        pending.delete(m.id);
        res(m);
      } else if (m.method) {
        for (const h of handlers) h(m);
      }
    };
    ws.onopen = () =>
      resolve({
        send: (method, params = {}) =>
          new Promise((res) => {
            const i = ++id;
            pending.set(i, { resolve: res });
            ws.send(JSON.stringify({ id: i, method, params }));
          }),
        onEvent: (fn) => handlers.push(fn),
        clearHandlers: () => { handlers = []; },
        close: () => ws.close(),
      });
  });
}

async function evaluate(client, expression) {
  const r = await client.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.result && r.result.exceptionDetails) return { error: r.result.exceptionDetails.text };
  return { value: r.result && r.result.result ? r.result.result.value : null };
}

const DIAGNOSTIC = (page) => `(() => {
  const sels = ${JSON.stringify(page.watch || [])};
  const out = { viewportHeight: window.innerHeight, documentHeight: document.documentElement.scrollHeight,
                text: (document.body ? document.body.innerText : '').slice(0, 20000), watch: {}, trapped: [], rows: null };
  for (const s of sels) {
    const el = document.querySelector(s);
    if (!el) { out.watch[s] = 'MISSING'; continue; }
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    out.watch[s] = { display: cs.display, visibility: cs.visibility, opacity: Number(cs.opacity),
                     height: Math.round(r.height), textLen: (el.innerText || '').length };
  }
  // Anything the visitor is meant to read must not live inside a hidden overlay container.
  const probes = document.querySelectorAll('main, section, article, footer, table, #leaderboard, #hiveTableBody');
  for (const el of probes) {
    const holder = el.closest(${JSON.stringify(HIDDEN_OVERLAY_SELECTOR)});
    if (holder && holder !== el) {
      out.trapped.push(holder.id ? '#' + holder.id : (holder.className || holder.tagName).toString().split(' ')[0]);
    }
  }
  out.trapped = Array.from(new Set(out.trapped)).slice(0, 6);
  ${page.rows ? `out.rows = document.querySelectorAll(${JSON.stringify(page.rows && page.rows.selector)}).length;` : ''}
  ${page.image ? `(() => {
    const im = document.querySelector(${JSON.stringify(page.image.selector)});
    out.image = im
      ? { complete: im.complete, naturalWidth: im.naturalWidth, naturalHeight: im.naturalHeight,
          currentSrc: im.currentSrc || im.src }
      : 'MISSING';
  })();` : ''}
  return out;
})()`;

async function checkPage(client, page) {
  const url = ORIGIN + page.url;
  const findings = [];
  let status = 0;
  try {
    const res = await fetch(url, { redirect: 'follow' });
    status = res.status;
  } catch (e) {
    return { url: page.url, status: 0, ok: false, findings: ['unreachable: ' + e.message] };
  }
  if (status !== 200) findings.push(`HTTP ${status}`);

  const errors = [];
  client.clearHandlers();
  client.onEvent((m) => {
    if (m.method === 'Runtime.exceptionThrown') {
      const d = m.params.exceptionDetails;
      const text = ((d.exception && d.exception.description) || d.text || '').split('\n')[0];
      if (text && !IGNORE.some((re) => re.test(text))) errors.push('exception: ' + text);
    }
    if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') {
      const t = (m.params.entry.text || '') + ' ' + (m.params.entry.url || '');
      if (!IGNORE.some((re) => re.test(t))) errors.push('console: ' + t.slice(0, 160));
    }
  });
  await client.send('Network.enable');
  await client.send('Runtime.enable');
  await client.send('Log.enable');
  await client.send('Page.enable');
  await client.send('Page.navigate', { url });
  await sleep(2600);                       // let the page's own JS finish (leaderboard fetch, reveals)

  // scroll through the page so IntersectionObserver content is revealed, then return to the top
  await evaluate(client, `(() => { const h = document.documentElement.scrollHeight; window.scrollTo(0, h / 2); return 1; })()`);
  await sleep(900);
  await evaluate(client, `(() => { window.scrollTo(0, document.documentElement.scrollHeight); return 1; })()`);

  // Data-driven sections (the HIVE leaderboard) fetch after load, so wait for the evidence the
  // page defines instead of guessing a delay - a genuinely broken page simply never satisfies it.
  if (page.rows) {
    const sel = page.rows.selector;
    for (let i = 0; i < 22; i++) {
      await sleep(800);
      const n = (await evaluate(client, `document.querySelectorAll(${JSON.stringify(sel)}).length`)).value;
      if (typeof n === 'number' && n >= page.rows.min) break;
    }
  } else {
    await sleep(1200);
  }

  const diag = (await evaluate(client, DIAGNOSTIC(page))).value;
  if (!diag) {
    findings.push('page produced no DOM state (render failed)');
    return { url: page.url, status, ok: false, findings };
  }

  if (diag.documentHeight <= diag.viewportHeight * 1.15) {
    findings.push(`collapsed page: document ${diag.documentHeight}px vs viewport ${diag.viewportHeight}px (content hidden or trapped)`);
  }
  if (diag.trapped && diag.trapped.length) {
    findings.push(`content inside a hidden overlay container: ${diag.trapped.join(', ')}`);
  }
  for (const [sel, state] of Object.entries(diag.watch || {})) {
    if (state === 'MISSING') { findings.push(`watched element not on the page: ${sel}`); continue; }
    if (state.display === 'none' || state.visibility === 'hidden' || state.opacity < 0.05 || state.height < 4) {
      findings.push(`${sel} is not visible (display:${state.display} visibility:${state.visibility} opacity:${state.opacity} h:${state.height}px)`);
    }
  }
  const text = (diag.text || '').toLowerCase();
  for (const m of page.markers || []) {
    if (!text.includes(m.toLowerCase())) findings.push(`missing expected content: "${m}"`);
  }
  if (page.rows && typeof diag.rows === 'number' && diag.rows < page.rows.min) {
    findings.push(`expected >= ${page.rows.min} rows for ${page.rows.selector}, found ${diag.rows}`);
  }
  if (page.image && page.image.selector) {
    const im = diag.image;
    if (!im || im === 'MISSING') findings.push(`hero image not in the DOM: ${page.image.selector}`);
    else if (!im.complete || !im.naturalWidth) findings.push(`hero image did not load: ${im.currentSrc || '(no src)'}`);
    else if (im.naturalWidth < (page.image.minWidth || 600)) {
      findings.push(`hero image is only ${im.naturalWidth}px wide: ${im.currentSrc}`);
    }
  }
  if (errors.length) findings.push(...errors.slice(0, 3).map((e) => 'js ' + e));

  return { url: page.url, status, ok: findings.length === 0, documentHeight: diag.documentHeight,
           image: diag.image && diag.image !== 'MISSING' ? `${diag.image.naturalWidth}x${diag.image.naturalHeight}` : null,
           findings };
}

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'smoke-'));
  const chrome = spawn('chromium-browser', [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
    '--disable-features=Translate,MediaRouter', '--mute-audio',
    `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, 'about:blank',
  ], { stdio: 'ignore', detached: false });

  let results = [];
  let client;
  try {
    const wsUrl = await baseUrl();
    client = await cdpClient(wsUrl);
    const targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
    const pageTarget = targets.find((t) => t.type === 'page');
    if (pageTarget) client.close();
    // attach to the real page target so navigation affects what we inspect
    const pageWs = pageTarget ? pageTarget.webSocketDebuggerUrl : wsUrl;
    client = await cdpClient(pageWs);

    const pages = ADHOC_URL
      ? [{
          url: ADHOC_URL,
          markers: [],
          watch: [],
          image: ADHOC_IMG ? { selector: ADHOC_IMG, minWidth: Number(argOf('--min-width', '600')) } : null,
        }]
      : PAGES;

    for (const p of pages) {
      try {
        results.push(await checkPage(client, p));
      } catch (e) {
        results.push({ url: p.url, ok: false, findings: ['check crashed: ' + e.message] });
      }
    }
  } catch (e) {
    console.error('render-smoke could not run:', e.message);
    chrome.kill('SIGKILL');
    process.exit(2);
  }

  try { client.close(); } catch {}
  chrome.kill('SIGKILL');
  fs.rmSync(profile, { recursive: true, force: true });

  const failed = results.filter((r) => !r.ok);
  console.log(`render-smoke: ${results.length - failed.length}/${results.length} pages healthy (${ORIGIN})`);
  for (const r of results) {
    if (r.ok) console.log(`  OK    ${r.url}`);
    else console.log(`  FAIL  ${r.url}\n          - ${r.findings.join('\n          - ')}`);
  }
  if (JSON_OUT) {
    try { fs.writeFileSync(JSON_OUT, JSON.stringify({ origin: ORIGIN, at: new Date().toISOString(), results }, null, 1)); } catch {}
  }
  process.exit(failed.length ? 1 : 0);
})();
