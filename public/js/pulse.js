// Pulse AI Research Agent — Floating Chat Bubble + Slide-in Overlay
(function() {
  'use strict';

  let overlayEl = null;
  let backdropEl = null;
  let overlayMessages = null;
  let isOpen = false;
  let currentArticleContext = null;
  let conversationHistory = []; // {role: 'user'|'assistant', text: '...'}
  let hasSentFirstMessage = false;

  function init() {
    // Inline Pulse section (homepage) — init separately from floating bubble
    const pulseSection = document.querySelector('.pulse-section');
    if (pulseSection) {
      initInlinePulse(pulseSection);
    }
    // Create the shared slide-in overlay
    createOverlay();
    // Floating bubble — always on, every page
    initFloatingBubble();
  }

  // ============== INLINE PULSE (homepage) ==============
  function initInlinePulse(section) {
    const messagesEl = section.querySelector('.pulse-messages');
    const inputEl = section.querySelector('.pulse-input');
    const sendBtn = section.querySelector('.pulse-send');
    if (!messagesEl || !inputEl || !sendBtn) return;

    sendBtn.addEventListener('click', function() {
      askPulse(inputEl.value, messagesEl);
      inputEl.value = '';
    });
    inputEl.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        askPulse(inputEl.value, messagesEl);
        inputEl.value = '';
      }
    });
  }

  // ============== SHARED OVERLAY (right-sliding panel) ==============
  function createOverlay() {
    // Backdrop
    backdropEl = document.createElement('div');
    backdropEl.className = 'pulse-overlay-bg';
    backdropEl.addEventListener('click', closeOverlay);
    document.body.appendChild(backdropEl);

    // Panel
    overlayEl = document.createElement('div');
    overlayEl.className = 'pulse-overlay';
    overlayEl.innerHTML =
      '<div class="pulse-overlay-header">' +
        '<div class="brand">' +
          '<div class="logo-mark"><img src="/img/logo-hex.jpg" alt="Pulse" style="width:22px;height:22px;border-radius:4px"></div>' +
          '<div><div class="brand-text">Ask <span class="pulse-gradient">Pulse</span></div></div>' +
        '</div>' +
        '<button class="close-btn" id="overlayClose" aria-label="Close">&#x2715;</button>' +
      '</div>' +
      '<div class="pulse-context-banner" id="contextBanner" style="display:none">' +
        '<span>&#x1F4C4;</span>' +
        '<span>Context:</span>' +
        '<span class="badge" id="contextBadge">Article</span>' +
      '</div>' +
      '<div class="pulse-overlay-messages" id="overlayMessages">' +
        '<div class="message assistant">' +
          '<div class="pulse-assistant-header">' +
            '<div class="pulse-brand-icon"><img src="/img/logo-hex.jpg" alt="" style="width:12px;height:12px;border-radius:3px"></div>' +
            '<div class="pulse-brand-name">Ask <span class="pulse-gradient">Pulse</span></div>' +
          '</div>' +
          '<div class="bubble">Hey, I\'m <strong>Pulse</strong>. Ask me about earnings, stock moves, contracts, or anything in our coverage. I search the web for real-time data.</div>' +
        '</div>' +
      '</div>' +
      '<div class="suggestion-chips" id="suggestionChips">' +
        '<span class="suggestion-chip" data-q="What are today&#39;s biggest movers?">&#x1F4C8; Biggest movers today</span>' +
        '<span class="suggestion-chip" data-q="Recent earnings beats?">&#x1F4CA; Recent earnings beats</span>' +
        '<span class="suggestion-chip" data-q="Top defense contracts this week">&#x1F6E1;&#xFE0F; Defense contracts this week</span>' +
      '</div>' +
      '<div class="pulse-overlay-input">' +
        '<div class="input-wrap">' +
          '<input type="text" placeholder="Ask Pulse anything\u2026" id="overlayInput">' +
          '<button class="icon-btn mic" id="overlayMic" title="Voice input">&#x1F3A4;</button>' +
        '</div>' +
        '<button class="btn-send" id="overlaySend" title="Send">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>' +
        '</button>' +
      '</div>';

    document.body.appendChild(overlayEl);

    overlayMessages = overlayEl.querySelector('#overlayMessages');

    // Wire up events
    overlayEl.querySelector('#overlayClose').addEventListener('click', closeOverlay);

    const input = overlayEl.querySelector('#overlayInput');
    const sendBtn = overlayEl.querySelector('#overlaySend');

    sendBtn.addEventListener('click', function() {
      overlaySend(input.value);
      input.value = '';
    });

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        overlaySend(input.value);
        input.value = '';
      }
    });

    // Suggestion chips
    overlayEl.querySelectorAll('.suggestion-chip').forEach(function(chip) {
      chip.addEventListener('click', function() {
        input.value = chip.getAttribute('data-q') || chip.textContent;
        overlaySend(input.value);
        input.value = '';
      });
    });

    // Mic button — real SpeechRecognition with fallback
    overlayEl.querySelector('#overlayMic').addEventListener('click', function() {
      var mic = this;
      var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SR) {
        // No native support
        mic.classList.toggle('active');
        if (!mic.classList.contains('active')) return;
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          alert('Speech recognition is not supported on this browser.');
          mic.classList.remove('active');
          return;
        }
        alert('Voice input is not available. Try Chrome or Edge for speech recognition.');
        mic.classList.remove('active');
        return;
      }
      if (mic._recognizing) {
        mic._recognition.stop();
        return;
      }
      var rec = new SR();
      mic._recognition = rec;
      mic._recognizing = true;
      rec.continuous = false;
      rec.interimResults = true;
      rec.lang = 'en-US';
      mic.classList.add('active');
      rec.start();
      rec.onresult = function(evt) {
        var transcript = '';
        for (var i = evt.resultIndex; i < evt.results.length; i++) {
          transcript += evt.results[i][0].transcript;
        }
        input.value = transcript;
      };
      rec.onend = function() {
        mic.classList.remove('active');
        mic._recognizing = false;
      };
      rec.onerror = function() {
        mic.classList.remove('active');
        mic._recognizing = false;
      };
    });

    // Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && isOpen) closeOverlay();
    });

    // Keyboard shortcut
    document.addEventListener('keydown', function(e) {
      if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        e.preventDefault();
        toggleOverlay();
      }
    });
  }

  function openOverlay(context) {
    if (!overlayEl || !backdropEl) return;
    currentArticleContext = context || null;

    // Show/hide context banner
    var banner = overlayEl.querySelector('#contextBanner');
    var badge = overlayEl.querySelector('#contextBadge');
    if (context && context.title) {
      banner.style.display = 'flex';
      badge.textContent = context.title.slice(0, 50) + (context.title.length > 50 ? '\u2026' : '');
    } else {
      banner.style.display = 'none';
    }

    overlayEl.classList.add('open');
    backdropEl.classList.add('visible');
    isOpen = true;
    document.body.classList.add('pulse-modal-open');

    // [FIX] Explicitly hide floating bubble when chat opens
    var floatBubble = document.querySelector('.pulse-float-bubble');
    if (floatBubble) floatBubble.style.display = 'none';

    // Focus input
    var input = overlayEl.querySelector('#overlayInput');
    // [FIX] No auto-focus — prevents mobile keyboard auto-popup

    // [FIX] Scroll to top so user reads from beginning
    if (overlayMessages) setTimeout(function() {
      overlayMessages.scrollTop = 0;
    }, 50);
  }

  function closeOverlay() {
    if (!overlayEl || !backdropEl) return;
    overlayEl.classList.remove('open');
    backdropEl.classList.remove('visible');
    isOpen = false;
    document.body.classList.remove('pulse-modal-open');

    // [FIX] Show floating bubble again when chat closes
    var floatBubble = document.querySelector('.pulse-float-bubble');
    if (floatBubble) floatBubble.style.display = '';

    // Reset conversation history and restore suggestion chips
    conversationHistory = [];
    hasSentFirstMessage = false;
    var chips = overlayEl.querySelector('#suggestionChips');
    if (chips) chips.style.display = '';
  }

  function toggleOverlay(context) {
    if (isOpen) {
      closeOverlay();
    } else {
      openOverlay(context);
    }
  }

  // ============== FLOATING BUBBLE ==============
  function initFloatingBubble() {
    var bubble = document.createElement('div');
    bubble.className = 'pulse-float-bubble';
    bubble.setAttribute('aria-label', 'Ask Pulse AI');
    bubble.setAttribute('role', 'button');
    bubble.setAttribute('tabindex', '0');
    bubble.innerHTML = '<img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-float-icon">';
    document.body.appendChild(bubble);

    bubble.addEventListener('click', function() {
      toggleOverlay(currentArticleContext);
    });

    // Hide bubble when overlay is open
    var obs = new MutationObserver(function() {
      bubble.style.display = isOpen ? 'none' : '';
    });
    if (overlayEl) obs.observe(overlayEl, { attributes: true, attributeFilter: ['class'] });

    // Hide bubble on scroll near inline Pulse (to avoid overlap)
    if (document.querySelector('.pulse-section')) {
      window.addEventListener('scroll', function() {
        if (!document.querySelector('.pulse-section') || isOpen) return;
        var rect = document.querySelector('.pulse-section').getBoundingClientRect();
        var viewportH = window.innerHeight;
        if (rect.top < viewportH - 100 && rect.bottom > 100) {
          bubble.classList.add('pulse-float-hidden');
        } else {
          bubble.classList.remove('pulse-float-hidden');
        }
      }, { passive: true });
    }
  }

  // ============== PUBLIC API (for article pulse-divider) ==============
  window.pulseOpenPanel = function(context) {
    openOverlay(context);
  };

  window.togglePulseOverlay = function(context) {
    toggleOverlay(context);
  };

  // ============== OVERLAY SEND ==============
  function overlaySend(question) {
    if (!question || !question.trim()) return;
    if (!overlayMessages) return;

    var input = overlayEl.querySelector('#overlayInput');
    var sendBtn = overlayEl.querySelector('#overlaySend');

    if (input) input.disabled = true;
    if (sendBtn) sendBtn.disabled = true;

    // Track in conversation history
    conversationHistory.push({ role: 'user', text: question });

    // Hide suggestion chips after first message
    if (!hasSentFirstMessage) {
      hasSentFirstMessage = true;
      var chips = overlayEl.querySelector('#suggestionChips');
      if (chips) chips.style.display = 'none';
    }

    // Add user message
    addOverlayMessage(question, true);

    // Show loading
    var loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = '<div class="avatar"><img src="/img/logo-hex.jpg" alt="P" style="width:16px;height:16px"></div><div class="bubble"><span class="typing-indicator"><span></span><span></span><span></span></span></div>';
    overlayMessages.appendChild(loadingDiv);
    overlayMessages.scrollTop = overlayMessages.scrollHeight;

    // Build body with conversation history (send last 20 messages)
    var body = { question: question, history: conversationHistory.slice(0, -1).slice(-20) };
    if (currentArticleContext) {
      body.articleContext = currentArticleContext;
    }

    fetch('/api/pulse/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      loadingDiv.remove();
      if (data.answer) {
        // Track assistant response in history
        conversationHistory.push({ role: 'assistant', text: data.answer });
        // Scroll to top so user reads response from the start (like Gemini)

        addOverlayMessageTyped(data.answer, false);
        // Update quota badge
        var badge = document.querySelector('.pulse-float-sub #pulseQuotaBadge');
        if (!badge) badge = document.getElementById('pulseQuotaBadge');
        if (badge && data.quota) {
          badge.textContent = data.quota.remaining + ' premium';
          badge.className = 'pulse-quota-badge ' + (data.quota.remaining > 0 ? 'has' : 'empty');
        }
        if (badge && data.tier === 'free' && !data.quota) {
          badge.textContent = 'free';
          badge.className = 'pulse-quota-badge free';
        }
        // Sources
        if (data.sources && data.sources.length > 0) {
          var sourcesDiv = document.createElement('div');
          sourcesDiv.className = 'pulse-sources';
          var sourcesHtml = '<div class="pulse-sources-title">Sources:</div>';
          for (var si = 0; si < data.sources.length; si++) {
            var s = data.sources[si];
            if (s.url) {
              // Web source — show clean title as clickable link
              sourcesHtml += '<a href="' + s.url + '" target="_blank" rel="noopener" class="pulse-source-link">' +
                escapeHtml(s.title || s.url) + '</a>';
            } else {
              // Fallback: local article source
              sourcesHtml += '<a href="/article/' + s.slug + '" class="pulse-source-link">' + escapeHtml(s.ticker) + ' &mdash; ' + escapeHtml((s.title || '').slice(0, 60)) + '</a>';
            }
          }
          sourcesDiv.innerHTML = sourcesHtml;
          overlayMessages.appendChild(sourcesDiv);
          scrollToLatestResponse();
        }
      } else {
        conversationHistory.push({ role: 'assistant', text: 'Sorry, I ran into an issue. Try rephrasing your question.' });
        addOverlayMessageTyped('Sorry, I ran into an issue. Try rephrasing your question.', false);
      }
    })
    .catch(function() {
      loadingDiv.remove();
      conversationHistory.push({ role: 'assistant', text: 'Connection issue. Please try again.' });
      addOverlayMessageTyped('Connection issue. Please try again.', false);
    })
    .finally(function() {
      if (input) input.disabled = false;
      if (sendBtn) sendBtn.disabled = false;
      // [FIX] No auto-focus after send
    });
  }

  function addOverlayMessage(text, isUser) {
    if (!overlayMessages) return;
    var div = document.createElement('div');
    div.className = 'message ' + (isUser ? 'user' : 'assistant');
    if (!isUser) {
      // Brand header (logo + "Pulse" label) above assistant response
      var headerHtml = '<div class="pulse-assistant-header">' +
        '<div class="pulse-brand-icon"><img src="/img/logo-hex.jpg" alt="" style="width:12px;height:12px;border-radius:3px"></div>' +
        '<div class="pulse-brand-name">Ask <span class="pulse-gradient">Pulse</span></div>' +
        '</div>';
      div.innerHTML = headerHtml + '<div class="bubble">' + formatText(text) + '</div>';
    } else {
      div.innerHTML = '<div class="bubble">' + escapeHtml(text) + '</div>';
    }
    overlayMessages.appendChild(div);
    overlayMessages.scrollTop = overlayMessages.scrollHeight;
  }
  function scrollToLatestResponse() {
    if (!overlayMessages) return;
    var allMessages = overlayMessages.querySelectorAll('.message.assistant');
    if (allMessages.length > 0) {
      var lastMsg = allMessages[allMessages.length - 1];
      var containerTop = overlayMessages.getBoundingClientRect().top;
      var msgTop = lastMsg.getBoundingClientRect().top;
      var offset = msgTop - containerTop + overlayMessages.scrollTop;
      overlayMessages.scrollTop = offset - 10;
    } else {
      scrollToLatestResponse();
    }
  }


  // Instant reveal — shows full response immediately
  function addOverlayMessageTyped(text, isUser) {
    if (!overlayMessages) return;
    var div = document.createElement('div');
    div.className = 'message assistant';
    var headerHtml = '<div class="pulse-assistant-header">' +
      '<div class="pulse-brand-icon"><img src="/img/logo-hex.jpg" alt="" style="width:12px;height:12px;border-radius:3px"></div>' +
      '<div class="pulse-brand-name">Ask <span class="pulse-gradient">Pulse</span></div>' +
      '</div>';
    var formatted = formatText(text);
    div.innerHTML = headerHtml + '<div class="bubble">' + formatted + '</div>';
    overlayMessages.appendChild(div);
    // Scroll to top so user reads from the start (like Gemini)
    overlayMessages.scrollTop = 0;
  }

  // ============== API CALL (for inline pulse) ==============
  async function askPulse(question, messagesEl) {
    if (!question.trim()) return;
    if (!messagesEl) return;

    var container = messagesEl.closest('.pulse-float-modal, .pulse-chat, .pulse-section');
    var inputEl = container ? container.querySelector('.pulse-input') : null;
    var sendBtn = container ? container.querySelector('.pulse-send') : null;

    if (inputEl) inputEl.disabled = true;
    if (sendBtn) sendBtn.disabled = true;

    addMessage(question, true, messagesEl);

    var loadingDiv = document.createElement('div');
    loadingDiv.className = 'pulse-message pulse-message-bot';
    loadingDiv.innerHTML = '<img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-message-avatar"><div class="pulse-bubble pulse-loading"><span class="pulse-dot"></span><span class="pulse-dot"></span><span class="pulse-dot"></span></div>';
    messagesEl.appendChild(loadingDiv);
    messagesEl.scrollTop = 0;

    try {
      var res = await fetch('/api/pulse/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question, articleContext: currentArticleContext })
      });
      var data = await res.json();

      loadingDiv.remove();

      if (data.answer) {
        addMessage(data.answer, false, messagesEl);
        var badge = document.getElementById('pulseQuotaBadge');
        if (badge && data.quota) {
          badge.textContent = data.quota.remaining + ' premium';
          badge.className = 'pulse-quota-badge ' + (data.quota.remaining > 0 ? 'has' : 'empty');
        }
        if (badge && data.tier === 'free' && !data.quota) {
          badge.textContent = 'free';
          badge.className = 'pulse-quota-badge free';
        }

        if (data.sources && data.sources.length > 0) {
          var sourcesDiv = document.createElement('div');
          sourcesDiv.className = 'pulse-sources';
          sourcesDiv.innerHTML = '<div class="pulse-sources-title">Sources:</div>' +
            data.sources.map(function(s) {
              if (s.url) {
                return '<a href="' + s.url + '" target="_blank" rel="noopener" class="pulse-source-link">' +
                  escapeHtml(s.title || s.url) + '</a>';
              }
              return '<a href="/article/' + s.slug + '" class="pulse-source-link">' + s.ticker + ' &mdash; ' + escapeHtml((s.title || '').slice(0, 60)) + '</a>';
            }).join('');
          messagesEl.appendChild(sourcesDiv);
          messagesEl.scrollTop = 0;
        }
      } else {
        addMessage('Sorry, I ran into an issue. Try rephrasing your question.', false, messagesEl);
      }
    } catch (e) {
      loadingDiv.remove();
      addMessage('Connection issue. Please try again.', false, messagesEl);
    }

    if (inputEl) inputEl.disabled = false;
    if (sendBtn) sendBtn.disabled = false;
    // [FIX] No auto-focus
  }

  // ============== HELPERS ==============
  function addMessage(text, isUser, messagesEl) {
    var div = document.createElement('div');
    div.className = 'pulse-message ' + (isUser ? 'pulse-message-user' : 'pulse-message-bot');
    if (!isUser) {
      div.innerHTML = '<img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-message-avatar"><div class="pulse-bubble">' + formatText(text) + '</div>';
    } else {
      div.innerHTML = '<div class="pulse-bubble pulse-bubble-user">' + escapeHtml(text) + '</div>';
    }
    messagesEl.appendChild(div);
    messagesEl.scrollTop = 0;
  }

  function formatText(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/^\s*[-•]\s+/gm, '<span class="pulse-bullet">&bull;</span> ');
    text = text.replace(/\n/g, '<br>');
    return text;
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // Boot
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
