// tts.js — Text-to-Speech using Microsoft Edge Cloud Jenny voice via /api/tts
// Free, no API key, high-quality voice

(function() {
  'use strict';

  const body = document.querySelector('.article-body');
  if (!body) return;

  // ─── State ───
  let audio = null;
  let playing = false;
  let currentParagraphs = [];
  let currentChunkIdx = -1;
  let totalChunks = 0;
  let rate = 1.0;

  // ─── Collect paragraphs ───
  function collectParagraphs() {
    const els = body.querySelectorAll('p, h2, h3, li');
    currentParagraphs = [];
    els.forEach(el => {
      const text = el.textContent.trim();
      if (text.length > 10) currentParagraphs.push({ el, text });
    });
  }

  // ─── Split into chunks for API ───
  function buildChunks() {
    collectParagraphs();
    const chunks = [];
    let chunk = '';
    const maxLen = 4800;
    for (const p of currentParagraphs) {
      if (chunk.length + p.text.length + 2 > maxLen && chunk) {
        chunks.push(chunk.trim());
        chunk = '';
      }
      chunk += (chunk ? ' ' : '') + p.text;
    }
    if (chunk.trim()) chunks.push(chunk.trim());
    return chunks;
  }

  // ─── Inject Listen bar ───
  function injectButton() {
    const meta = document.querySelector('.article-meta');
    if (!meta) return;
    if (document.querySelector('.tts-bar')) return;

    const bar = document.createElement('div');
    bar.className = 'tts-bar';
    bar.style.cssText = 'display:flex;align-items:center;gap:12px;margin:16px 0 12px;padding:10px 18px;background:var(--bg-card,#1a1a2e);border:1px solid var(--border,#333);border-radius:10px;cursor:pointer;';

    const icon = document.createElement('span');
    icon.textContent = '🔊';
    icon.style.cssText = 'font-size:18px;';

    const label = document.createElement('span');
    label.textContent = 'Listen — Jenny voice (free Edge TTS)';
    label.style.cssText = 'font-family:Inter,sans-serif;font-size:13px;font-weight:500;color:var(--text-secondary,#aaa);flex:1;';

    const btn = document.createElement('button');
    btn.id = 'ttsListenBtn';
    btn.style.cssText = 'display:flex;align-items:center;gap:6px;background:var(--accent,#6366f1);color:#fff;border:none;border-radius:20px;padding:8px 18px;font-family:Inter,sans-serif;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.2s;';
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> Play`;
    btn.setAttribute('aria-label', 'Listen to article');

    bar.appendChild(icon);
    bar.appendChild(label);
    bar.appendChild(btn);

    bar.addEventListener('click', (e) => {
      if (e.target === btn || btn.contains(e.target)) {
        if (playing) { stopAudio(); }
        else { startPlayback(); }
      } else {
        if (playing) { stopAudio(); }
        else { startPlayback(); }
      }
    });

    meta.insertAdjacentElement('afterend', bar);
  }

  // ─── Inject floating controller ───
  function injectController() {
    if (document.getElementById('ttsController')) return;
    const ctrl = document.createElement('div');
    ctrl.id = 'ttsController';
    ctrl.className = 'tts-controller';
    ctrl.innerHTML = `<div class="tts-ctrl-inner">
      <button class="tts-ctrl-btn tts-ctrl-play" id="ttsPlayBtn" aria-label="Play/Pause">▶</button>
      <button class="tts-ctrl-btn tts-ctrl-pause" id="ttsPauseBtn" aria-label="Pause" style="display:none">⏸</button>
      <div class="tts-ctrl-progress"><div class="tts-ctrl-bar" id="ttsProgressBar"></div></div>
      <span class="tts-ctrl-label" id="ttsLabel"></span>
      <button class="tts-ctrl-btn tts-ctrl-speed" id="ttsSpeedBtn" aria-label="Speed">1×</button>
      <button class="tts-ctrl-btn tts-ctrl-stop" id="ttsStopBtn" aria-label="Stop">■</button>
    </div>`;
    document.body.appendChild(ctrl);

    document.getElementById('ttsPlayBtn').addEventListener('click', () => { if (audio) audio.play().catch(() => {}); });
    document.getElementById('ttsPauseBtn').addEventListener('click', () => { if (audio) audio.pause(); });
    document.getElementById('ttsStopBtn').addEventListener('click', stopAudio);
    document.getElementById('ttsSpeedBtn').addEventListener('click', () => {
      const speeds = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
      const idx = speeds.indexOf(rate);
      rate = speeds[(idx + 1) % speeds.length];
      document.getElementById('ttsSpeedBtn').textContent = rate + '×';
      if (audio) audio.playbackRate = rate;
    });
  }

  // ─── Playback ───
  async function startPlayback() {
    const chunks = buildChunks();
    if (!chunks.length) return;
    totalChunks = chunks.length;
    currentChunkIdx = 0;
    playing = true;
    injectController();
    showController();
    updateBtn('loading');
    document.getElementById('ttsLabel').textContent = 'Loading…';
    await playChunks(chunks);
  }

  async function playChunks(chunks) {
    for (let i = 0; i < chunks.length && playing; i++) {
      currentChunkIdx = i;
      updateProgress();
      updateBtn('playing');
      
      const playBtn = document.getElementById('ttsPlayBtn');
      const pauseBtn = document.getElementById('ttsPauseBtn');
      if (playBtn) playBtn.style.display = 'none';
      if (pauseBtn) pauseBtn.style.display = '';

      try {
        const url = `/api/tts?voice=en-US-JennyNeural&rate=%2B5%25&text=${encodeURIComponent(chunks[i])}`;
        audio = new Audio(url);
        audio.playbackRate = rate;
        document.getElementById('ttsLabel').textContent = `${i + 1} / ${chunks.length}`;

        await new Promise((resolve, reject) => {
          audio.onended = () => resolve();
          audio.onerror = () => reject(new Error('Audio load error'));
          audio.play().catch(reject);
        });

        // Highlight current chunk's paragraphs
        highlightChunkParagraphs(i, chunks, currentParagraphs);

      } catch (e) {
        console.warn('TTS chunk failed:', e.message);
        if (playBtn) playBtn.style.display = '';
        if (pauseBtn) pauseBtn.style.display = 'none';
      }
    }
    stopAudio();
  }

  function highlightChunkParagraphs(chunkIdx, chunks, paragraphs) {
    if (!paragraphs.length) return;
    // Remove all highlights
    body.querySelectorAll('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    // Find paragraphs that are in this chunk
    let textPos = 0;
    const chunkText = chunks[chunkIdx];
    for (const p of paragraphs) {
      const start = textPos;
      textPos += p.text.length;
      // If paragraph starts within this chunk, highlight it
      if (start >= chunkText.length) break; // past this chunk — but chunk boundaries don't align
      // Simple: highlight all paragraphs that were in collected order
    }
    // Simpler approach: highlight by index proportion
    const perChunk = Math.ceil(paragraphs.length / chunks.length);
    const start = chunkIdx * perChunk;
    const end = Math.min(start + perChunk, paragraphs.length);
    for (let i = start; i < end; i++) {
      paragraphs[i].el.classList.add('tts-highlight');
      if (i === start) paragraphs[i].el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function updateProgress() {
    if (!totalChunks) return;
    const pct = ((currentChunkIdx + 1) / totalChunks) * 100;
    const bar = document.getElementById('ttsProgressBar');
    if (bar) bar.style.width = pct + '%';
  }

  function updateBtn(state) {
    const btn = document.getElementById('ttsListenBtn');
    if (!btn) return;
    if (state === 'playing') {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Pause`;
      btn.style.background = '#ef4444';
    } else if (state === 'loading') {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/></svg> Loading…`;
      btn.style.background = '#f59e0b';
    } else {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> Play`;
      btn.style.background = 'var(--accent,#6366f1)';
    }
  }

  function showController() {
    const ctrl = document.getElementById('ttsController');
    if (ctrl) ctrl.classList.add('visible');
    document.body.classList.add('tts-active');
  }

  function hideController() {
    const ctrl = document.getElementById('ttsController');
    if (ctrl) ctrl.classList.remove('visible');
    document.body.classList.remove('tts-active');
  }

  function stopAudio() {
    playing = false;
    if (audio) { audio.pause(); audio = null; }
    updateBtn('stopped');
    hideController();
    body.querySelectorAll('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    const playBtn = document.getElementById('ttsPlayBtn');
    const pauseBtn = document.getElementById('ttsPauseBtn');
    if (playBtn) playBtn.style.display = '';
    if (pauseBtn) pauseBtn.style.display = 'none';
  }

  // ─── Init ───
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { injectButton(); injectController(); });
  } else {
    injectButton();
    injectController();
  }
})();
