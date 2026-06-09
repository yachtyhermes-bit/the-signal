// tts.js — Text-to-speech for article pages
// Fetches audio via Google Translate TTS proxy (/api/tts/)
// Free, no API key required

(function() {
  const articleBody = document.querySelector('.article-body');
  if (!articleBody) return;

  let playing = false;
  let audio = null;
  let currentChunkIdx = -1;
  let rate = 1.0;

  // ─── Collect paragraph texts ───
  function getParagraphs() {
    const els = articleBody.querySelectorAll('p, h2, h3, li');
    return Array.from(els)
      .map(el => el.textContent.trim())
      .filter(t => t.length > 20);
  }

  // ─── Split paragraphs into API-friendly chunks ───
  function buildChunks(paragraphs, maxLen = 500) {
    const chunks = [];
    let chunk = '';
    for (const p of paragraphs) {
      if (chunk.length + p.length + 2 > maxLen && chunk) {
        chunks.push(chunk.trim());
        chunk = '';
      }
      chunk += (chunk ? ' ' : '') + p;
    }
    if (chunk.trim()) chunks.push(chunk.trim());
    return chunks;
  }

  // ─── Inject sleek Listen pill button ───
  function injectButton() {
    const meta = document.querySelector('.article-meta');
    if (!meta || document.querySelector('.tts-bar')) return;

    const bar = document.createElement('div');
    bar.className = 'tts-bar';
    bar.style.cssText = 'display:flex;align-items:center;margin:18px 0 14px;';

    const btn = document.createElement('button');
    btn.id = 'ttsListenBtn';
    btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg><span style="margin-left:7px">Listen</span>`;
    btn.style.cssText = 'display:inline-flex;align-items:center;background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;border:none;border-radius:24px;padding:10px 20px;font-family:Inter,sans-serif;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s;box-shadow:0 2px 12px rgba(99,102,241,0.25);letter-spacing:-0.01em;';
    btn.setAttribute('aria-label', 'Listen to article');
    btn.addEventListener('mouseenter', () => { btn.style.boxShadow = '0 4px 20px rgba(99,102,241,0.4)'; btn.style.transform = 'translateY(-1px)'; });
    btn.addEventListener('mouseleave', () => { btn.style.boxShadow = '0 2px 12px rgba(99,102,241,0.25)'; btn.style.transform = 'none'; });
    btn.addEventListener('click', () => {
      if (playing) { stopAudio(); }
      else { startPlayback(); }
    });

    bar.appendChild(btn);
    meta.insertAdjacentElement('afterend', bar);
  }

  // ─── Inject floating controller ───
  function injectController() {
    if (document.getElementById('ttsController')) return;
    const ctrl = document.createElement('div');
    ctrl.id = 'ttsController';
    ctrl.className = 'tts-controller';
    ctrl.innerHTML = `<div class="tts-ctrl-inner">
      <button class="tts-ctrl-btn tts-ctrl-play" id="ttsPlayBtn" aria-label="Play">▶</button>
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

  // ─── Update button state ───
  function updateBtn(state) {
    const btn = document.getElementById('ttsListenBtn');
    if (!btn) return;
    if (state === 'playing') {
      btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg><span style="margin-left:7px">Pause</span>`;
      btn.style.background = 'linear-gradient(135deg,#ef4444,#dc2626)';
    } else if (state === 'loading') {
      btn.innerHTML = `<span style="margin-left:7px">Loading…</span>`;
      btn.style.background = 'linear-gradient(135deg,#6366f1,#4f46e5)';
    } else {
      btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg><span style="margin-left:7px">Listen</span>`;
      btn.style.background = 'linear-gradient(135deg,#6366f1,#4f46e5)';
    }
  }

  function updateProgress() {
    const chunks = buildChunks(getParagraphs());
    const bar = document.getElementById('ttsProgressBar');
    const label = document.getElementById('ttsLabel');
    if (bar) bar.style.width = chunks.length ? ((currentChunkIdx + 1) / chunks.length * 100) + '%' : '0%';
    if (label) label.textContent = `${currentChunkIdx + 1} / ${chunks.length}`;
  }

  // ─── Playback ───
  async function startPlayback() {
    if (playing) return;
    playing = true;
    injectController();
    document.getElementById('ttsController').classList.add('visible');
    document.body.classList.add('tts-active');

    const paragraphs = getParagraphs();
    const chunks = buildChunks(paragraphs);
    updateBtn('loading');

    try {
      for (let i = 0; i < chunks.length && playing; i++) {
        currentChunkIdx = i;
        updateProgress();
        updateBtn('playing');

        const playBtn = document.getElementById('ttsPlayBtn');
        const pauseBtn = document.getElementById('ttsPauseBtn');
        if (playBtn) playBtn.style.display = '';
        if (pauseBtn) pauseBtn.style.display = 'none';

        audio = new Audio(`/api/tts/?text=${encodeURIComponent(chunks[i])}`);
        audio.playbackRate = rate;
        document.getElementById('ttsLabel').textContent = `${i + 1} / ${chunks.length}`;

        try {
          await new Promise((resolve, reject) => {
            audio.onended = resolve;
            audio.onerror = () => reject(new Error('Audio load failed'));
            audio.play().catch(reject);
          });
        } catch (e) {
          // Continue to next chunk on error
          console.warn('TTS chunk failed:', e.message);
        }
      }
    } finally {
      stopAudio();
    }
  }

  function stopAudio() {
    playing = false;
    if (audio) {
      audio.pause();
      audio.src = '';
      audio = null;
    }
    updateBtn('stopped');
    const ctrl = document.getElementById('ttsController');
    if (ctrl) {
      ctrl.classList.remove('visible');
      setTimeout(() => ctrl.remove(), 400);
    }
    document.body.classList.remove('tts-active');
    currentChunkIdx = -1;
  }

  // ─── Init ───
  document.addEventListener('DOMContentLoaded', () => {
    injectButton();
  });
})();
