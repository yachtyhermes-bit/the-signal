// Pulse AI Research Agent — Floating Chat Bubble + Homepage Inline Section
(function() {
  'use strict';

  let pulseActive = false;

  function init() {
    // Inline Pulse section (homepage) — init separately from floating bubble
    const pulseSection = document.querySelector('.pulse-section');
    if (pulseSection) {
      initInlinePulse(pulseSection);
    }
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

  // ============== FLOATING BUBBLE ==============
  function initFloatingBubble() {
    // Create bubble element
    const bubble = document.createElement('div');
    bubble.className = 'pulse-float-bubble';
    bubble.setAttribute('aria-label', 'Ask Pulse AI');
    bubble.setAttribute('role', 'button');
    bubble.setAttribute('tabindex', '0');
    bubble.innerHTML = '<img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-float-icon">';
    document.body.appendChild(bubble);

    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'pulse-float-overlay';
    overlay.innerHTML = `
      <div class="pulse-float-modal">
        <div class="pulse-float-header">
          <img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-float-avatar">
          <div class="pulse-float-header-text">
            <div class="pulse-float-name">Ask <span class="pulse-gradient">Pulse</span></div>
            <div class="pulse-float-sub">Free daily queries: <span id="pulseQuotaBadge" class="pulse-quota-badge">5 premium</span></div>
          </div>
          <button class="pulse-float-close" aria-label="Close">&times;</button>
        </div>
        <div class="pulse-float-messages" id="pulseFloatMessages">
          <div class="pulse-message pulse-message-bot">
            <img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-message-avatar">
            <div class="pulse-bubble">Hey, I'm <strong>Pulse</strong>. Find me on any page — ask about earnings, stock moves, contracts, or anything in our coverage universe. I search the web for real-time data.</div>
          </div>
        </div>
        <div class="pulse-float-input-area">
          <input type="text" class="pulse-input pulse-float-input" id="pulseFloatInput" placeholder="e.g. What were Nvidia's latest earnings?">
          <button class="pulse-send pulse-float-send" id="pulseFloatSend" aria-label="Send">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    // Toggle modal on bubble click
    let modalOpen = false;
    bubble.addEventListener('click', function() {
      modalOpen = !modalOpen;
      overlay.classList.toggle('pulse-float-open', modalOpen);
      document.body.classList.toggle('pulse-modal-open', modalOpen);
      if (modalOpen) {
        const input = overlay.querySelector('.pulse-float-input');
        if (input) setTimeout(function() { input.focus(); }, 300);
      }
    });

    // Close button
    const closeBtn = overlay.querySelector('.pulse-float-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        modalOpen = false;
        overlay.classList.remove('pulse-float-open');
        document.body.classList.remove('pulse-modal-open');
      });
    }

    // Close on backdrop click
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) {
        modalOpen = false;
        overlay.classList.remove('pulse-float-open');
        document.body.classList.remove('pulse-modal-open');
      }
    });

    // Send / Enter for float modal
    const floatInput = overlay.querySelector('.pulse-float-input');
    const floatSend = overlay.querySelector('.pulse-float-send');
    const floatMessages = overlay.querySelector('.pulse-float-messages');

    if (floatSend && floatInput) {
      floatSend.addEventListener('click', function() {
        askPulse(floatInput.value, floatMessages);
        floatInput.value = '';
      });
      floatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          askPulse(floatInput.value, floatMessages);
          floatInput.value = '';
        }
      });
    }

    // Keyboard shortcut: Ctrl+Shift+P to toggle
    document.addEventListener('keydown', function(e) {
      if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        e.preventDefault();
        bubble.click();
      }
    });

    // Hide bubble on scroll near inline Pulse (to avoid overlap)
    if (document.querySelector('.pulse-section')) {
      let hideTimer = null;
      window.addEventListener('scroll', function() {
        const ps = document.querySelector('.pulse-section');
        if (!ps || modalOpen) return;
        const rect = ps.getBoundingClientRect();
        const viewportH = window.innerHeight;
        // Pulse section is visible — hide bubble
        if (rect.top < viewportH - 100 && rect.bottom > 100) {
          bubble.classList.add('pulse-float-hidden');
        } else {
          bubble.classList.remove('pulse-float-hidden');
        }
      }, { passive: true });
    }
  }

  // ============== API CALL ==============
  async function askPulse(question, messagesEl) {
    if (!question.trim()) return;
    if (!messagesEl) return;

    // Find input/send within the same container
    const container = messagesEl.closest('.pulse-float-modal, .pulse-chat, .pulse-section');
    const inputEl = container ? container.querySelector('.pulse-input') : null;
    const sendBtn = container ? container.querySelector('.pulse-send') : null;

    if (inputEl) inputEl.disabled = true;
    if (sendBtn) sendBtn.disabled = true;

    // Add user message
    addMessage(question, true, messagesEl);

    // Show loading
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'pulse-message pulse-message-bot';
    loadingDiv.innerHTML = '<img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-message-avatar"><div class="pulse-bubble pulse-loading"><span class="pulse-dot"></span><span class="pulse-dot"></span><span class="pulse-dot"></span></div>';
    messagesEl.appendChild(loadingDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    try {
      const res = await fetch('/api/pulse/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await res.json();

      loadingDiv.remove();

      if (data.answer) {
        addMessage(data.answer, false, messagesEl);

        // Update quota badge
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
          const sourcesDiv = document.createElement('div');
          sourcesDiv.className = 'pulse-sources';
          sourcesDiv.innerHTML = '<div class="pulse-sources-title">Sources:</div>' +
            data.sources.map(function(s) {
              return '<a href="/article/' + s.slug + '" class="pulse-source-link">' + s.ticker + ' &mdash; ' + escapeHtml(s.title.slice(0, 60)) + '</a>';
            }).join('');
          messagesEl.appendChild(sourcesDiv);
          messagesEl.scrollTop = messagesEl.scrollHeight;
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
    if (inputEl) inputEl.focus();
  }

  // ============== HELPERS ==============
  function addMessage(text, isUser, messagesEl) {
    const div = document.createElement('div');
    div.className = 'pulse-message ' + (isUser ? 'pulse-message-user' : 'pulse-message-bot');
    if (!isUser) {
      div.innerHTML = '<img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-message-avatar"><div class="pulse-bubble">' + formatText(text) + '</div>';
    } else {
      div.innerHTML = '<div class="pulse-bubble pulse-bubble-user">' + escapeHtml(text) + '</div>';
    }
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
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
