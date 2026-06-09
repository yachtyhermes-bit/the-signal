// tts.js — Text-to-speech for article pages (Web Speech API)
// Reads article body aloud with modern voice, visual highlighting, and playback controls

(function () {
  'use strict';

  // Only run on article pages
  const articleBody = document.querySelector('.article-body');
  if (!articleBody) return;

  // ─── State ───
  let speaking = false;
  let paused = false;
  let currentParaIdx = -1;
  let paragraphs = [];
  let utterance = null;
  let rate = 1.0;
  let selectedVoice = null;
  let voicesRetries = 0;

  // ─── Collect paragraphs ───
  function collectParagraphs() {
    const els = articleBody.querySelectorAll('p, h2, h3, li');
    paragraphs = [];
    els.forEach(el => {
      const text = el.textContent.trim();
      if (text.length > 10) {
        paragraphs.push({ el, text });
      }
    });
  }

  // ─── Inject TTS button bar ───
  function injectButton() {
    const meta = document.querySelector('.article-meta');
    if (!meta) return;

    const bar = document.createElement('div');
    bar.style.cssText = 'display:flex;align-items:center;gap:12px;margin:16px 0 12px;padding:10px 18px;background:var(--bg-card,#1a1a2e);border:1px solid var(--border,#333);border-radius:10px;';

    const iconSpan = document.createElement('span');
    iconSpan.innerHTML = '🔊';
    iconSpan.style.cssText = 'font-size:18px;';

    const label = document.createElement('span');
    label.textContent = 'Listen to this article';
    label.style.cssText = 'font-family:Inter,sans-serif;font-size:13px;font-weight:500;color:var(--text-secondary,#aaa);flex:1;';

    const btn = document.createElement('button');
    btn.id = 'ttsListenBtn';
    btn.style.cssText = 'display:flex;align-items:center;gap:6px;background:var(--accent,#6366f1);color:#fff;border:none;border-radius:20px;padding:8px 18px;font-family:Inter,sans-serif;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.2s;';
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> Play`;
    btn.setAttribute('aria-label', 'Listen to article');
    btn.title = 'Read this article aloud';

    // WIRE THE CLICK DIRECTLY — the button must work on first tap
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (speaking && !paused) {
        pause();
      } else if (paused) {
        resume();
      } else {
        startReading();
      }
    });

    bar.appendChild(iconSpan);
    bar.appendChild(label);
    bar.appendChild(btn);
    meta.insertAdjacentElement('afterend', bar);
  }

  // ─── Inject floating controller ───
  function injectController() {
    if (document.getElementById('ttsController')) return;

    const ctrl = document.createElement('div');
    ctrl.id = 'ttsController';
    ctrl.className = 'tts-controller';
    ctrl.innerHTML = `
      <div class="tts-ctrl-inner">
        <button class="tts-ctrl-btn tts-ctrl-play" id="ttsPlayBtn" aria-label="Play/Pause">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        </button>
        <button class="tts-ctrl-btn tts-ctrl-pause" id="ttsPauseBtn" aria-label="Pause" style="display:none">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
        </button>
        <div class="tts-ctrl-progress">
          <div class="tts-ctrl-bar" id="ttsProgressBar"></div>
        </div>
        <span class="tts-ctrl-label" id="ttsLabel">Reading…</span>
        <button class="tts-ctrl-btn tts-ctrl-speed" id="ttsSpeedBtn" aria-label="Speed">1×</button>
        <button class="tts-ctrl-btn tts-ctrl-stop" id="ttsStopBtn" aria-label="Stop">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="4" y="4" width="16" height="16" rx="2"/></svg>
        </button>
      </div>`;

    document.body.appendChild(ctrl);

    document.getElementById('ttsPlayBtn').addEventListener('click', resume);
    document.getElementById('ttsPauseBtn').addEventListener('click', pause);
    document.getElementById('ttsStopBtn').addEventListener('click', stop);
    document.getElementById('ttsSpeedBtn').addEventListener('click', () => {
      const speeds = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
      const idx = speeds.indexOf(rate);
      rate = speeds[(idx + 1) % speeds.length];
      document.getElementById('ttsSpeedBtn').textContent = rate + '×';
    });
  }

  function showController() {
    const ctrl = document.getElementById('ttsController');
    if (ctrl) {
      ctrl.classList.add('visible');
      document.body.classList.add('tts-active');
    }
    updateListenBtn();
  }

  function hideController() {
    const ctrl = document.getElementById('ttsController');
    if (ctrl) {
      ctrl.classList.remove('visible');
      document.body.classList.remove('tts-active');
    }
  }

  function updateListenBtn() {
    const btn = document.getElementById('ttsListenBtn');
    if (!btn) return;
    if (speaking && !paused) {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Pause`;
      btn.style.background = '#ef4444';
    } else if (paused) {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> Resume`;
      btn.style.background = '#f59e0b';
    } else {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> Play`;
      btn.style.background = 'var(--accent,#6366f1)';
    }
  }

  // ─── Find best voice ───
  function findBestVoice() {
    const voices = speechSynthesis.getVoices();
    if (voices.length === 0) return null;

    // Prefer modern English voices in this order
    const prefs = [
      'Google US English',
      'Microsoft David',
      'Microsoft Zira',
      'Samantha',
      'Alex',
      'Karen',
      'Daniel',
    ];

    for (const pref of prefs) {
      const v = voices.find(v => v.name.includes(pref) && v.lang.startsWith('en'));
      if (v) return v;
    }

    // Fallback to any English voice
    return voices.find(v => v.lang.startsWith('en')) || voices[0];
  }

  // ─── Load voices with retry ───
  function loadVoices(callback) {
    // Try immediately
    const voices = speechSynthesis.getVoices();
    if (voices.length > 0) {
      selectedVoice = findBestVoice();
      if (selectedVoice) { callback(); return; }
    }

    // Listen for voiceschanged event
    speechSynthesis.onvoiceschanged = function () {
      if (selectedVoice) return; // already got it
      selectedVoice = findBestVoice();
      if (selectedVoice) { callback(); return; }
    };

    // Retry loop: some mobile browsers never fire onvoiceschanged
    function retry() {
      if (selectedVoice) { callback(); return; }
      if (voicesRetries > 15) {
        // Last resort: use any available voice
        const v = speechSynthesis.getVoices();
        selectedVoice = v.find(x => x.lang.startsWith('en')) || v[0] || null;
        if (selectedVoice) { callback(); return; }
      }
      voicesRetries++;
      const v = speechSynthesis.getVoices();
      if (v.length > 0) {
        selectedVoice = findBestVoice();
        if (selectedVoice) { callback(); return; }
      }
      setTimeout(retry, 200);
    }
    setTimeout(retry, 150);
  }

  // ─── Highlight paragraph ───
  function highlightParagraph(idx) {
    document.querySelectorAll('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    if (idx >= 0 && idx < paragraphs.length) {
      paragraphs[idx].el.classList.add('tts-highlight');
      paragraphs[idx].el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function updateProgress() {
    const bar = document.getElementById('ttsProgressBar');
    const label = document.getElementById('ttsLabel');
    if (!bar || !label) return;
    const pct = paragraphs.length > 0 ? Math.round(((currentParaIdx + 1) / paragraphs.length) * 100) : 0;
    bar.style.width = pct + '%';
    label.textContent = (currentParaIdx + 1) + ' / ' + paragraphs.length;
  }

  function updateControllerButtons() {
    const playBtn = document.getElementById('ttsPlayBtn');
    const pauseBtn = document.getElementById('ttsPauseBtn');
    if (!playBtn || !pauseBtn) return;
    if (speaking && !paused) {
      playBtn.style.display = 'none';
      pauseBtn.style.display = 'flex';
    } else {
      playBtn.style.display = 'flex';
      pauseBtn.style.display = 'none';
    }
  }

  // ─── Read a single paragraph ───
  function readParagraph(idx) {
    if (idx >= paragraphs.length) {
      stop();
      return;
    }

    currentParaIdx = idx;
    highlightParagraph(idx);
    updateProgress();
    updateControllerButtons();

    // Cancel any pending speech first (iOS fix)
    speechSynthesis.cancel();

    const text = paragraphs[idx].text;
    utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = rate;
    utterance.volume = 1;
    utterance.pitch = 1;

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.onend = function () {
      readParagraph(idx + 1);
    };

    utterance.onerror = function (e) {
      if (e.error !== 'interrupted' && e.error !== 'canceled') {
        console.warn('TTS error:', e.error);
        // Try to continue to next paragraph on unknown errors
        setTimeout(() => readParagraph(idx + 1), 300);
      }
    };

    // Chrome bug workaround: sometimes speech stops after ~15s of inactivity
    // Keep a heartbeat
    const heartbeat = setInterval(() => {
      if (!speaking || paused) { clearInterval(heartbeat); return; }
      speechSynthesis.pause();
      speechSynthesis.resume();
    }, 10000);

    utterance.onend = function () {
      clearInterval(heartbeat);
      readParagraph(idx + 1);
    };

    utterance.onerror = function (e) {
      clearInterval(heartbeat);
      if (e.error !== 'interrupted' && e.error !== 'canceled') {
        console.warn('TTS error:', e.error);
        setTimeout(() => readParagraph(idx + 1), 300);
      }
    };

    speechSynthesis.speak(utterance);
  }

  // ─── Controls ───
  function startReading() {
    loadVoices(function () {
      collectParagraphs();
      if (paragraphs.length === 0) return;

      speaking = true;
      paused = false;
      injectController();
      showController();
      readParagraph(0);
    });
  }

  function pause() {
    paused = true;
    speechSynthesis.cancel();
    updateControllerButtons();
    updateListenBtn();
  }

  function resume() {
    if (!speaking) {
      startReading();
      return;
    }
    paused = false;
    updateControllerButtons();
    updateListenBtn();
    readParagraph(currentParaIdx);
  }

  function stop() {
    speaking = false;
    paused = false;
    speechSynthesis.cancel();
    hideController();
    updateListenBtn();
    document.querySelectorAll('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    currentParaIdx = -1;
    utterance = null;
  }

  // ─── Init ───
  // Run as soon as possible
  injectButton();

  // Preload voices in the background
  const voices = speechSynthesis.getVoices();
  if (voices.length > 0) {
    selectedVoice = findBestVoice();
  }
  speechSynthesis.onvoiceschanged = function () {
    if (!selectedVoice) {
      selectedVoice = findBestVoice();
    }
  };
})();
