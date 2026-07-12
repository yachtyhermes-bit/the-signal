// tts.js — Jenny voice audio player with seek/scrub controls
// Pre-generated Jenny audio from R2, Google TTS fallback

(function() {
  const articleBody = document.querySelector('.article-body');
  if (!articleBody) return;

  let playing = false;
  let audio = null;
  let rate = 1.0;
  let updateInterval = null;

  function getSlug() {
    const m = window.location.pathname.match(/\/article\/([^/]+)/);
    return m ? m[1] : null;
  }

  function getFullText() {
    const els = articleBody.querySelectorAll('p, h2, h3, li');
    return Array.from(els)
      .map(el => el.textContent.trim())
      .filter(t => t.length > 10)
      .join('. ');
  }

  function fmtTime(secs) {
    if (!secs || !isFinite(secs)) return '0:00';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  // ─── Inject Listen pill ───
  function injectButton() {
    const meta = document.querySelector('.article-meta');
    if (!meta || document.querySelector('.tts-bar')) return;

    const bar = document.createElement('div');
    bar.className = 'tts-bar';
    bar.style.cssText = 'display:flex;align-items:center;margin:18px 0 14px;';

    const btn = document.createElement('button');
    btn.id = 'ttsListenBtn';
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg><span style="margin-left:7px">Listen</span>';
    btn.style.cssText = 'display:inline-flex;align-items:center;background:linear-gradient(135deg,#ec4899,#db2777);color:#fff;border:none;border-radius:24px;padding:10px 20px;font-family:Inter,sans-serif;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s;box-shadow:0 2px 12px rgba(236,72,153,0.25);letter-spacing:-0.01em;';
    btn.setAttribute('aria-label', 'Listen to article');
    btn.addEventListener('mouseenter', () => { btn.style.boxShadow = '0 4px 20px rgba(236,72,153,0.4)'; btn.style.transform = 'translateY(-1px)'; });
    btn.addEventListener('mouseleave', () => { btn.style.boxShadow = '0 2px 12px rgba(236,72,153,0.25)'; btn.style.transform = 'none'; });
    btn.addEventListener('click', () => {
      if (playing) { stopAudio(); }
      else { startPlayback(); }
    });

    bar.appendChild(btn);
    meta.insertAdjacentElement('afterend', bar);
  }

  // ─── Floating controller with seek/scrub ───
  function injectController() {
    if (document.getElementById('ttsController')) return;
    const ctrl = document.createElement('div');
    ctrl.id = 'ttsController';
    ctrl.className = 'tts-controller';
    ctrl.innerHTML = '<div class="tts-ctrl-inner">' +
      '<button class="tts-ctrl-btn" id="ttsBackBtn" aria-label="Rewind 15s">↺</button>' +
      '<button class="tts-ctrl-btn tts-ctrl-play" id="ttsPlayBtn" aria-label="Play">▶</button>' +
      '<button class="tts-ctrl-btn" id="ttsFwdBtn" aria-label="Forward 15s">↻</button>' +
      '<span class="tts-ctrl-time" id="ttsCurTime">0:00</span>' +
      '<div class="tts-ctrl-progress" id="ttsProgressWrap">' +
        '<div class="tts-ctrl-bar" id="ttsProgressBar"></div>' +
        '<input type="range" class="tts-ctrl-scrub" id="ttsScrubber" min="0" max="100" value="0" step="0.1">' +
      '</div>' +
      '<span class="tts-ctrl-time" id="ttsDuration">0:00</span>' +
      '<button class="tts-ctrl-btn" id="ttsSpeedBtn" aria-label="Speed">1×</button>' +
      '<button class="tts-ctrl-btn" id="ttsStopBtn" aria-label="Stop">■</button>' +
    '</div>';
    document.body.appendChild(ctrl);

    // Play/pause toggle
    const playBtn = document.getElementById('ttsPlayBtn');
    playBtn.addEventListener('click', () => {
      if (!audio) return;
      if (audio.paused) { audio.play().catch(() => {}); playBtn.textContent = '⏸'; }
      else { audio.pause(); playBtn.textContent = '▶'; }
    });

    // Rewind 15s
    document.getElementById('ttsBackBtn').addEventListener('click', () => {
      if (audio) { audio.currentTime = Math.max(0, audio.currentTime - 15); }
    });

    // Forward 15s
    document.getElementById('ttsFwdBtn').addEventListener('click', () => {
      if (audio) { audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 15); }
    });

    // Stop
    document.getElementById('ttsStopBtn').addEventListener('click', stopAudio);

    // Speed cycle
    document.getElementById('ttsSpeedBtn').addEventListener('click', () => {
      const speeds = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
      const idx = speeds.indexOf(rate);
      rate = speeds[(idx + 1) % speeds.length];
      document.getElementById('ttsSpeedBtn').textContent = rate + '×';
      if (audio) audio.playbackRate = rate;
    });

    // Scrub bar — drag to seek
    const scrub = document.getElementById('ttsScrubber');
    let scrubbing = false;
    scrub.addEventListener('input', () => {
      if (audio && audio.duration) {
        scrubbing = true;
        audio.currentTime = (scrub.value / 100) * audio.duration;
      }
    });
    scrub.addEventListener('change', () => { scrubbing = false; });
  }

  function updateProgress() {
    if (!audio || !audio.duration) return;
    const scrub = document.getElementById('ttsScrubber');
    const bar = document.getElementById('ttsProgressBar');
    const curTime = document.getElementById('ttsCurTime');
    if (scrub && !scrub.matches(':active')) {
      const pct = (audio.currentTime / audio.duration) * 100;
      scrub.value = pct;
      if (bar) bar.style.width = pct + '%';
    }
    if (curTime) curTime.textContent = fmtTime(audio.currentTime);
  }

  function updateBtn(state) {
    const btn = document.getElementById('ttsListenBtn');
    if (!btn) return;
    if (state === 'playing') {
      btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg><span style="margin-left:7px">Pause</span>';
      btn.style.background = 'linear-gradient(135deg,#ef4444,#dc2626)';
    } else if (state === 'loading') {
      btn.innerHTML = '<span style="margin-left:7px">Loading…</span>';
      btn.style.background = 'linear-gradient(135deg,#ec4899,#db2777)';
    } else {
      btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg><span style="margin-left:7px">Listen</span>';
      btn.style.background = 'linear-gradient(135deg,#ec4899,#db2777)';
    }
  }

  async function startPlayback() {
    if (playing) return;
    playing = true;
    injectController();
    const ctrl = document.getElementById('ttsController');
    ctrl.classList.add('visible');
    document.body.classList.add('tts-active');
    updateBtn('loading');

    const slug = getSlug();
    const text = getFullText();

    try {
      const params = new URLSearchParams();
      params.set('text', text.substring(0, 5000));
      if (slug) params.set('slug', slug);

      const resp = await fetch('/api/tts/?' + params.toString());
      if (!resp.ok) throw new Error('TTS failed');

      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      audio = new Audio(url);
      audio.playbackRate = rate;

      const backend = resp.headers.get('X-TTS-Backend') || 'unknown';
      const durEl = document.getElementById('ttsDuration');
      updateBtn('playing');
      document.getElementById('ttsPlayBtn').textContent = '⏸';
      document.getElementById('ttsCurTime').textContent = '0:00';

      audio.addEventListener('loadedmetadata', () => {
        if (durEl) durEl.textContent = fmtTime(audio.duration);
      });

      audio.addEventListener('ended', () => stopAudio());
      audio.addEventListener('error', () => {
        console.warn('Audio playback error');
        stopAudio();
      });

      // Progress updates
      updateInterval = setInterval(updateProgress, 250);

      await audio.play();
    } catch (e) {
      console.error('TTS error:', e.message);
      updateBtn('stopped');
      stopAudio();
    }
  }

  function stopAudio() {
    playing = false;
    if (updateInterval) { clearInterval(updateInterval); updateInterval = null; }
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
  }

  document.addEventListener('DOMContentLoaded', () => {
    injectButton();
  });
})();
