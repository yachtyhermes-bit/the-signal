// The Signal — Glassmorphism Comments System
// "Drop your thesis below." — Community trading discussion
(function() {
  'use strict';

  // ─── Detect article page ───
  var listEl = document.getElementById('commentsList');
  if (!listEl) return;

  var formEl = document.getElementById('commentForm');
  var nameInput = document.getElementById('commentName');
  var contentInput = document.getElementById('commentContent');
  var parentInput = document.getElementById('commentParentId');
  var countBadge = document.getElementById('commentCount');

  // Extract slug from URL
  var path = window.location.pathname;
  var slug = path.replace(/^\/article\//, '').replace(/\/$/, '');

  if (!slug) return;

  var STORAGE_KEY = 'ts_comments_' + slug;
  var REACTIONS = [
    { emoji: '\u{1F680}', label: 'Bullish' },
    { emoji: '\u{1F48E}', label: 'Diamond Hands' },
    { emoji: '\u{1F525}', label: 'Fire' },
    { emoji: '\u{1F9E0}', label: 'Big Brain' }
  ];

  // Seed personas for new articles
  var PERSONAS = [
    { name: 'WolfOfOakland', take: 'veteran' },
    { name: 'QuantQuinn_', take: 'data' },
    { name: 'MemeStockMamba', take: 'hype' },
    { name: 'BearishBrad', take: 'contrarian' },
    { name: 'MacroMindy', take: 'macro' }
  ];

  var SEED_COMMENTS = {
    veteran: [
      "Been trading this name since $12. This is the same setup I saw in '23 before the 3x. Patience pays.",
      "Charts don't lie. It's forming a beautiful cup and handle on the weekly.",
      "Volume profile says accumulation. Smart money is loading here."
    ],
    data: [
      "Just one number: forward PE of 22 vs sector median of 35. That's all you need to know.",
      "Free cash flow yield at 4.2% — highest it's been in 18 months."
    ],
    hype: [
      "\u{1F680} This is literally the next NVIDIA. Not selling a single share.",
      "LFG \u{1F525} Institutions are sleeping on this. Retail figured it out first."
    ],
    contrarian: [
      "Everyone's bullish. That's exactly when I get nervous. Show me the margin story.",
      "The narrative is priced in. I need to see execution before I add.",
      "Call me crazy but I think the pullback to $140s is the real opportunity nobody's watching."
    ],
    macro: [
      "Rates narrative shifting. If the Fed pauses in September, growth names rip.",
      "Defense budgets aren't going down regardless of who's in office. That's the real tailwind here."
    ]
  };

  // ─── Styles ───
  function injectStyles() {
    if (document.getElementById('ts-comments-css')) return;
    var css = document.createElement('style');
    css.id = 'ts-comments-css';
    css.textContent = [
      '.ts-comments-wrap { margin-top: 8px; }',
      '.ts-comments-title { font-size: 1.15rem; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }',
      '.ts-comments-subtitle { font-size: 0.8rem; color: #94a3b8; margin-bottom: 16px; font-style: italic; }',
      '.ts-comment-card {',
      '  background: rgba(255,255,255,0.04);',
      '  backdrop-filter: blur(12px);',
      '  -webkit-backdrop-filter: blur(12px);',
      '  border: 1px solid rgba(255,255,255,0.08);',
      '  border-radius: 12px;',
      '  padding: 14px 16px;',
      '  margin-bottom: 10px;',
      '  animation: tsFadeIn 0.35s ease-out;',
      '  transition: border-color 0.2s;',
      '}',
      '.ts-comment-card:hover { border-color: rgba(255,255,255,0.14); }',
      '.ts-comment-card.threaded { margin-left: 36px; border-left: 2px solid rgba(99,102,241,0.3); }',
      '@keyframes tsFadeIn { from { opacity:0; transform: translateY(8px); } to { opacity:1; transform: translateY(0); } }',
      '.ts-comment-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }',
      '.ts-comment-avatar {',
      '  width: 28px; height: 28px; border-radius: 50%;',
      '  background: linear-gradient(135deg, #6366f1, #8b5cf6);',
      '  color: #fff; font-size: 0.7rem; font-weight: 700;',
      '  display: flex; align-items: center; justify-content: center;',
      '  flex-shrink: 0;',
      '}',
      '.ts-comment-name { font-weight: 600; font-size: 0.85rem; color: #e2e8f0; }',
      '.ts-comment-time { font-size: 0.7rem; color: #64748b; margin-left: auto; }',
      '.ts-comment-body { font-size: 0.88rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 8px; }',
      '.ts-comment-reactions { display: flex; gap: 4px; flex-wrap: wrap; }',
      '.ts-reaction-btn {',
      '  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06);',
      '  border-radius: 16px; padding: 3px 10px; font-size: 0.78rem;',
      '  color: #94a3b8; cursor: pointer; transition: all 0.2s;',
      '  display: flex; align-items: center; gap: 4px;',
      '}',
      '.ts-reaction-btn:hover { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.3); color: #a5b4fc; }',
      '.ts-reaction-btn.active { background: rgba(99,102,241,0.2); border-color: #6366f1; color: #c7d2fe; }',
      '.ts-reaction-count { font-size: 0.7rem; opacity: 0.8; }',
      '.ts-reply-btn {',
      '  background: none; border: none; color: #6366f1; font-size: 0.75rem;',
      '  cursor: pointer; padding: 2px 6px; border-radius: 4px; transition: background 0.2s;',
      '}',
      '.ts-reply-btn:hover { background: rgba(99,102,241,0.1); }',
      '.ts-reply-form-wrap { margin-top: 8px; display: none; }',
      '.ts-reply-form-wrap.active { display: block; }',
      '.ts-reply-input {',
      '  width: 100%; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1);',
      '  border-radius: 8px; padding: 8px 12px; color: #e2e8f0; font-size: 0.82rem;',
      '  resize: none; min-height: 48px; margin-bottom: 6px;',
      '}',
      '.ts-reply-input:focus { outline: none; border-color: #6366f1; }',
      '.ts-reply-actions { display: flex; gap: 6px; justify-content: flex-end; }',
      '.ts-reply-actions button {',
      '  padding: 4px 14px; border-radius: 6px; font-size: 0.78rem; cursor: pointer; border: none;',
      '  transition: all 0.2s;',
      '}',
      '.ts-reply-cancel { background: rgba(255,255,255,0.06); color: #94a3b8; }',
      '.ts-reply-cancel:hover { background: rgba(255,255,255,0.1); }',
      '.ts-reply-submit { background: #6366f1; color: #fff; }',
      '.ts-reply-submit:hover { background: #4f46e5; }',
      '.ts-reply-submit:disabled { opacity: 0.5; cursor: not-allowed; }',
      '.comment-form {',
      '  background: rgba(255,255,255,0.03);',
      '  backdrop-filter: blur(12px);',
      '  -webkit-backdrop-filter: blur(12px);',
      '  border: 1px solid rgba(255,255,255,0.08);',
      '  border-radius: 12px; padding: 16px; margin-bottom: 20px;',
      '}',
      '.comment-form-label {',
      '  display: block; font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 10px;',
      '}',
      '.comment-input-name, .comment-input-content {',
      '  width: 100%; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1);',
      '  border-radius: 8px; padding: 8px 12px; color: #e2e8f0; font-size: 0.85rem; margin-bottom: 8px;',
      '}',
      '.comment-input-name:focus, .comment-input-content:focus { outline: none; border-color: #6366f1; }',
      '.comment-input-content { min-height: 60px; resize: vertical; }',
      '.comment-form button[type="submit"] {',
      '  background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff;',
      '  border: none; border-radius: 8px; padding: 8px 24px; font-size: 0.85rem; font-weight: 600;',
      '  cursor: pointer; transition: all 0.2s;',
      '}',
      '.comment-form button[type="submit"]:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(99,102,241,0.3); }',
      '.comment-form button[type="submit"]:active { transform: translateY(0); }',
      '.comment-count-badge {',
      '  background: rgba(99,102,241,0.2); color: #a5b4fc;',
      '  font-size: 0.75rem; padding: 2px 10px; border-radius: 12px;',
      '}'
    ].join('\n');
    document.head.appendChild(css);
  }

  // ─── Load comments ───
  function loadComments() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch(e) {}
    return seedComments();
  }

  function seedComments() {
    var shuffled = PERSONAS.sort(function() { return Math.random() - 0.5; });
    var comments = [];
    var used = {};
    var total = Math.floor(Math.random() * 4) + 3;

    for (var i = 0; i < total && i < shuffled.length; i++) {
      var p = shuffled[i];
      var takes = SEED_COMMENTS[p.take];
      var text = takes[Math.floor(Math.random() * takes.length)];
      if (used[text]) continue;
      used[text] = true;
      comments.push({
        id: 'seed_' + Date.now() + '_' + i,
        author: p.name,
        text: text,
        createdAt: new Date(Date.now() - Math.floor(Math.random() * 86400000)).toISOString(),
        reactions: {},
        replies: []
      });
    }
    saveComments(comments);
    return comments;
  }

  function saveComments(comments) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(comments)); } catch(e) {}
  }

  function countAll(comments) {
    var n = 0;
    comments.forEach(function(c) { n += 1 + (c.replies ? c.replies.length : 0); });
    return n;
  }

  // ─── Render ───
  function render(comments) {
    var html = '';
    html += '<div class="ts-comments-title">\u{1F4AC} Drop your thesis below.</div>';
    html += '<div class="ts-comments-subtitle">Community trading discussion \u00B7 ' + countAll(comments) + ' takes</div>';
    html += '<div class="ts-comments-wrap">';
    comments.forEach(function(c) { html += renderCard(c, 0); });
    html += '</div>';
    listEl.innerHTML = html;
    if (countBadge) countBadge.textContent = countAll(comments);
    bindEvents(comments);
  }

  function renderCard(c, depth) {
    var date = new Date(c.createdAt);
    var timeAgo = getTimeAgo(date);
    var initials = (c.author || '?')[0].toUpperCase();
    var cls = depth > 0 ? ' ts-comment-card threaded' : ' ts-comment-card';
    var html = '<div class="' + cls + '" data-id="' + c.id + '">';
    html += '<div class="ts-comment-header">';
    html += '<div class="ts-comment-avatar">' + initials + '</div>';
    html += '<span class="ts-comment-name">' + esc(c.author) + '</span>';
    html += '<span class="ts-comment-time">' + timeAgo + '</span>';
    html += '</div>';
    html += '<div class="ts-comment-body">' + esc(c.text) + '</div>';
    html += '<div class="ts-comment-reactions">';
    REACTIONS.forEach(function(r) {
      var count = (c.reactions && c.reactions[r.emoji]) || 0;
      var active = hasReacted(c, r.emoji) ? ' active' : '';
      html += '<button class="ts-reaction-btn' + active + '" data-react="' + r.emoji + '" data-id="' + c.id + '" title="' + r.label + '">';
      html += '<span>' + r.emoji + '</span>';
      if (count > 0) html += '<span class="ts-reaction-count">' + count + '</span>';
      html += '</button>';
    });
    if (depth < 2) {
      html += '<button class="ts-reply-btn" data-reply="' + c.id + '">\u21A9 Reply</button>';
    }
    html += '</div>';
    if (depth < 2) {
      html += '<div class="ts-reply-form-wrap" id="replyWrap-' + c.id + '">';
      html += '<textarea class="ts-reply-input" placeholder="Add your take..." id="replyInput-' + c.id + '" rows="2"></textarea>';
      html += '<div class="ts-reply-actions">';
      html += '<button class="ts-reply-cancel" data-cancel="' + c.id + '">Cancel</button>';
      html += '<button class="ts-reply-submit" data-submit="' + c.id + '">Reply</button>';
      html += '</div></div>';
    }
    if (c.replies && c.replies.length > 0) {
      c.replies.forEach(function(r) { html += renderCard(r, depth + 1); });
    }
    html += '</div>';
    return html;
  }

  function getReactions() {
    try { return JSON.parse(localStorage.getItem('ts_reactions') || '{}'); } catch(e) { return {}; }
  }

  function hasReacted(comment, emoji) {
    var r = getReactions();
    return !!(r[comment.id] && r[comment.id][emoji]);
  }

  function toggleReaction(commentId, emoji, comments) {
    var r = getReactions();
    if (!r[commentId]) r[commentId] = {};

    function findAndUpdate(list) {
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === commentId) {
          if (!list[i].reactions) list[i].reactions = {};
          if (r[commentId][emoji]) {
            list[i].reactions[emoji] = Math.max(0, (list[i].reactions[emoji] || 1) - 1);
            delete r[commentId][emoji];
          } else {
            list[i].reactions[emoji] = (list[i].reactions[emoji] || 0) + 1;
            r[commentId][emoji] = true;
          }
          return true;
        }
        if (list[i].replies && findAndUpdate(list[i].replies)) return true;
      }
      return false;
    }
    findAndUpdate(comments);
    localStorage.setItem('ts_reactions', JSON.stringify(r));
    saveComments(comments);
    render(comments);
  }

  function bindEvents(comments) {
    listEl.querySelectorAll('.ts-reaction-btn').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        toggleReaction(btn.getAttribute('data-id'), btn.getAttribute('data-react'), comments);
      });
    });
    listEl.querySelectorAll('.ts-reply-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var id = btn.getAttribute('data-reply');
        var wrap = document.getElementById('replyWrap-' + id);
        if (wrap) {
          var isOpen = wrap.classList.contains('active');
          listEl.querySelectorAll('.ts-reply-form-wrap.active').forEach(function(w) { w.classList.remove('active'); });
          if (!isOpen) {
            wrap.classList.add('active');
            var input = document.getElementById('replyInput-' + id);
            if (input) setTimeout(function() { input.focus(); }, 50);
          }
        }
      });
    });
    listEl.querySelectorAll('.ts-reply-cancel').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var id = btn.getAttribute('data-cancel');
        var wrap = document.getElementById('replyWrap-' + id);
        if (wrap) { wrap.classList.remove('active'); }
      });
    });
    listEl.querySelectorAll('.ts-reply-submit').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var id = btn.getAttribute('data-submit');
        var input = document.getElementById('replyInput-' + id);
        if (!input) return;
        var text = input.value.trim();
        if (!text) return;
        btn.disabled = true;
        var reply = {
          id: 'r_' + Date.now(),
          author: nameInput ? nameInput.value.trim() || 'Anonymous' : 'Anonymous',
          text: text,
          createdAt: new Date().toISOString(),
          reactions: {},
          replies: []
        };
        function addReply(list) {
          for (var i = 0; i < list.length; i++) {
            if (list[i].id === id) {
              if (!list[i].replies) list[i].replies = [];
              list[i].replies.push(reply);
              return true;
            }
            if (list[i].replies && addReply(list[i].replies)) return true;
          }
          return false;
        }
        addReply(comments);
        saveComments(comments);
        render(comments);
        btn.disabled = false;
      });
    });
  }

  function submitComment() {
    if (!contentInput) return;
    var text = contentInput.value.trim();
    if (!text) return;
    var author = nameInput ? nameInput.value.trim() || 'Anonymous' : 'Anonymous';
    var comments = loadComments();
    comments.push({
      id: 'c_' + Date.now(),
      author: author,
      text: text,
      createdAt: new Date().toISOString(),
      reactions: {},
      replies: []
    });
    saveComments(comments);
    contentInput.value = '';
    render(comments);
  }

  if (formEl) {
    formEl.addEventListener('submit', function(e) { e.preventDefault(); submitComment(); });
  }

  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function getTimeAgo(date) {
    var diff = new Date() - date;
    var seconds = Math.floor(diff / 1000);
    if (seconds < 60) return 'just now';
    var minutes = Math.floor(seconds / 60);
    if (minutes < 60) return minutes + 'm ago';
    var hours = Math.floor(minutes / 60);
    if (hours < 24) return hours + 'h ago';
    var days = Math.floor(hours / 24);
    if (days < 7) return days + 'd ago';
    var months = Math.floor(days / 30);
    if (months < 12) return months + 'mo ago';
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  injectStyles();
  var comments = loadComments();
  render(comments);
})();
