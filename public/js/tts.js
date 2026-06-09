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
  let voicesLoaded = false;

  // ─── Collect paragraphs ───
  function collectParagraphs() {
    // Get all text-containing elements: p, h2, h3, li (but not blockquotes or code)
    const els = articleBody.querySelectorAll('p, h2, h3, li');
    paragraphs = [];
    els.forEach(el => {
      const text = el.textContent.trim();
      if (text.length > 10) { // skip short fragments
        paragraphs.push({ el, text });
      }
    });
  }

  // ─── Inject TTS button into article header ───
  function injectButton() {
    const meta = document.querySelector('.article-meta');
    if (!meta) return;

    const btn = document.createElement('button');
    btn.id = 'ttsListenBtn';
    btn.className = 'tts-listen-btn';
    btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> Listen`;
    btn.setAttribute('aria-label', 'Listen to article');
    btn.title = 'Read this article aloud';

    btn.addEventListener('click', () => {
      if (speaking && !paused) {
        pause();
      } else if (paused) {
        resume();
      } else {
        startReading();
      }
    });

    // Insert after the meta line
    meta.appendChild(document.createTextNode(' · '));
    meta.appendChild(btn);
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

    // Wire controls
    document.getElementById('ttsPlayBtn').addEventListener('click', resume);
    document.getElementById('ttsPauseBtn').addEventListener('click', pause);
    document.getElementById('ttsStopBtn').addEventListener('click', stop);
    document.getElementById('ttsSpeedBtn').addEventListener('click', () => {
      const speeds = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
      const idx = speeds.indexOf(rate);
      rate = speeds[(idx + 1) % speeds.length];
      document.getElementById('ttsSpeedBtn').textContent = rate + '×';
      // Apply to current utterance if speaking
      if (utterance) {
        // Can't change rate mid-utterance; will apply on next paragraph
      }
    });
  }

  function showController() {
    const ctrl = document.getElementById('ttsController');
    if (ctrl) {
      ctrl.classList.add('visible');
      // Add padding to body so content isn't hidden behind the bar
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
      btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Pause`;
      btn.classList.add('tts-active-btn');
    } else if (paused) {
      btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> Resume`;
      btn.classList.add('tts-active-btn');
    } else {
      btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> Listen`;
      btn.classList.remove('tts-active-btn');
    }
  }

  // ─── Find best voice ───
  function findBestVoice() {
    const voices = speechSynthesis.getVoices();
    if (voices.length === 0) return null;

    // Prefer modern English voices in this order
    const prefs = [
      'Google US English',       // Chrome - natural
      'Microsoft David',         // Edge/Windows - decent
      'Microsoft Zira',          // Edge/Windows - female
      'Samantha',                // macOS - natural female
      'Alex',                    // macOS - natural male
      'Karen',                   // macOS - natural
      'Daniel',                  // macOS
      'en-US',
      'en-GB',
    ];

    for (const pref of prefs) {
      const v = voices.find(v => v.name.includes(pref) && v.lang.startsWith('en'));
      if (v) return v;
    }

    // Fallback to any English voice
    return voices.find(v => v.lang.startsWith('en')) || voices[0];
  }

  // ─── Highlight paragraph ───
  function highlightParagraph(idx) {
    // Remove previous highlights
    document.querySelectorAll('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));

    if (idx >= 0 && idx < paragraphs.length) {
      paragraphs[idx].el.classList.add('tts-highlight');
      // Scroll into view smoothly
      paragraphs[idx].el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function updateProgress() {
    const bar = document.getElementById('ttsProgressBar');
    const label = document.getElementById('ttsLabel');
    if (!bar || !label) return;

    const pct = paragraphs.length > 0 ? Math.round((currentParaIdx / paragraphs.length) * 100) : 0;
    bar.style.width = pct + '%';
    label.textContent = currentParaIdx + 1 + ' / ' + paragraphs.length;
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

    const text = paragraphs[idx].text;

    // iOS Safari rate fix: rate/volume must be set BEFORE speak() or they're ignored
    utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = rate;
    utterance.volume = 1;
    utterance.pitch = 1;

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.onend = () => {
      // Move to next paragraph
      readParagraph(idx + 1);
    };

    utterance.onerror = (e) => {
      // 'interrupted' is normal when pausing/stopping
      if (e.error !== 'interrupted' && e.error !== 'canceled') {
        console.warn('TTS error:', e.error);
      }
    };

    speechSynthesis.speak(utterance);
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

  // ─── Controls ───
  function startReading() {
    if (!voicesLoaded) {
      // Voices not loaded yet; try again
      speechSynthesis.getVoices();
      if (!voicesLoaded) {
        // Attempt to prime
        speechSynthesis.onvoiceschanged = () => {
          voicesLoaded = true;
          selectedVoice = findBestVoice();
          startReading();
        };
        return;
      }
    }

    collectParagraphs();
    if (paragraphs.length === 0) return;

    if (!selectedVoice) {
      selectedVoice = findBestVoice();
    }

    speaking = true;
    paused = false;
    injectController();
    showController();

    // Remove highlights from previous runs
    document.querySelectorAll('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));

    readParagraph(0);
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
  function init() {
    // Preload voices
    const voices = speechSynthesis.getVoices();
    if (voices.length > 0) {
      voicesLoaded = true;
      selectedVoice = findBestVoice();
    }
    speechSynthesis.onvoiceschanged = () => {
      voicesLoaded = true;
      selectedVoice = findBestVoice();
    };

    injectButton();
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
