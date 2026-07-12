// The Signal — Secure Comments System
// Only authenticated users can comment: Google sign-in OR The Hive account
(function() {
  'use strict';

  var container = document.getElementById('commentsContainer');
  if (!container) return;

  var articleSlug = container.getAttribute('data-slug');
  if (!articleSlug) return;

  var API_BASE = '/api/comments';
  var HIVE_API = '/api/hive';
  var FIREBASE_CONFIG = {
    apiKey: "AIzaSyDhlnHXYACuXc0VWk07JEUA9gMQ3CwZ8Eo",
    authDomain: "kalitta-logs.firebaseapp.com",
    projectId: "kalitta-logs"
  };

  var firebaseApp = null;
  var firebaseUser = null;
  var currentUser = null; // { type: 'google'|'hive', displayName, photoURL, uid, token? }

  // ─── Hive auth helpers ───
  function getHiveToken() {
    try { return localStorage.getItem('hive_token'); } catch(e) { return null; }
  }
  function getHiveUser() {
    try {
      var data = localStorage.getItem('hive_user');
      return data ? JSON.parse(data) : null;
    } catch(e) { return null; }
  }

  // ─── Auth state ───
  function resolveCurrentUser(firebaseUserData, callback) {
    // Priority: Hive auth over Google auth
    var hiveToken = getHiveToken();
    var hiveUser = getHiveUser();

    if (hiveToken && hiveUser) {
      // Verify Hive token is still valid
      fetch(HIVE_API + '?action=me&token=' + encodeURIComponent(hiveToken))
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (data.authenticated) {
            currentUser = {
              type: 'hive',
              displayName: data.displayName || hiveUser.displayName,
              photoURL: null,
              uid: data.uid,
              token: hiveToken
            };
            if (callback) callback(currentUser);
            return;
          }
          // Token expired — fall through to Google
          checkFirebaseAuth(callback);
        })
        .catch(function() {
          // Server unreachable — use cached user
          currentUser = {
            type: 'hive',
            displayName: hiveUser.displayName || 'User',
            photoURL: null,
            uid: hiveUser.uid,
            token: hiveToken
          };
          if (callback) callback(currentUser);
        });
    } else if (firebaseUserData) {
      currentUser = {
        type: 'google',
        displayName: firebaseUserData.displayName || firebaseUserData.email || 'Google User',
        photoURL: firebaseUserData.photoURL || null,
        uid: firebaseUserData.uid,
        token: null
      };
      if (callback) callback(currentUser);
    } else {
      currentUser = null;
      if (callback) callback(null);
    }
  }

  function checkFirebaseAuth(callback) {
    if (firebaseApp && firebase.auth) {
      firebase.auth(firebaseApp).onAuthStateChanged(function(user) {
        firebaseUser = user;
        if (user) {
          currentUser = {
            type: 'google',
            displayName: user.displayName || user.email || 'Google User',
            photoURL: user.photoURL || null,
            uid: user.uid,
            token: null
          };
          renderComments();
        }
        if (callback) callback(currentUser);
      });
    }
  }

  // ─── Build threaded tree ───
  function buildTree(comments) {
    var map = {};
    var roots = [];
    comments.forEach(function(c) {
      c.replies = [];
      map[c.id] = c;
    });
    comments.forEach(function(c) {
      if (c.parentId && map[c.parentId]) {
        map[c.parentId].replies.push(c);
      } else {
        roots.push(c);
      }
    });
    roots.sort(function(a, b) { return new Date(a.createdAt) - new Date(b.createdAt); });
    roots.forEach(function(r) {
      r.replies.sort(function(a, b) { return new Date(a.createdAt) - new Date(b.createdAt); });
    });
    return roots;
  }

  function countAll(roots) {
    var n = 0;
    roots.forEach(function(r) { n += 1 + r.replies.length; });
    return n;
  }

  // ─── Render ───
  function avatarColor(username) {
    var hash = 0;
    for (var i = 0; i < username.length; i++) {
      hash = username.charCodeAt(i) + ((hash << 5) - hash);
      hash = hash & hash;
    }
    var h = Math.abs(hash) % 360;
    return 'hsl(' + h + ', 55%, 45%)';
  }

  function render(comments) {
    var roots = buildTree(comments);
    var totalCount = countAll(roots);
    var html = '';

    // Comment form — only show if authenticated
    html += renderAuthSection();

    // Comment list
    html += '<div class="comment-list" id="commentList">';
    if (roots.length === 0) {
      html += '<div class="comment-empty">No comments yet. Sign in to be the first.</div>';
    } else {
      html += '<div class="comment-count">' + totalCount + ' comment' + (totalCount !== 1 ? 's' : '') + '</div>';
      roots.forEach(function(c) {
        html += renderComment(c, 0);
      });
    }
    html += '</div>';

    container.innerHTML = html;
    bindEvents(comments);
  }

  function renderAuthSection() {
    var html = '<div class="comment-form-area" id="commentFormArea">';
    html += '<div class="comment-signin-title">Drop your thesis below.</div>';

    if (currentUser) {
      // Signed in — show comment form
      var photoHtml = currentUser.photoURL
        ? '<img src="' + escAttr(currentUser.photoURL) + '" class="comment-avatar" alt="" width="28" height="28" onerror="this.style.display=\'none\'">'
        : '<div class="comment-avatar-fallback">' + escHtml((currentUser.displayName || 'U')[0].toUpperCase()) + '</div>';

      var badge = currentUser.type === 'google' ? 'Google' : 'The Hive';

      html += '<div class="comment-user-bar">';
      html += photoHtml;
      html += '<span class="comment-user-name">' + escHtml(currentUser.displayName) + '</span>';
      html += '<span class="comment-user-badge">' + badge + '</span>';
      html += '</div>';
      html += '<textarea class="comment-textarea" id="commentTextarea" placeholder="Share your thoughts…" maxlength="2000" rows="3"></textarea>';
      html += '<button class="comment-submit" id="commentSubmitBtn">Post Comment</button>';
    } else {
      // Not signed in — show auth options
      html += '<div class="comment-signin-prompt">';
      html += '<p class="comment-auth-subtitle">Join the conversation</p>';
      html += '<button class="comment-google-btn" id="commentGoogleBtn"><span class="comment-google-icon">G</span> Sign in with Google</button>';
      html += '<button class="comment-hive-btn" id="commentHiveBtn">🐝 Sign in with The Hive</button>';
      html += '</div>';
    }

    html += '</div>';
    return html;
  }

  function renderComment(c, depth) {
    var date = new Date(c.createdAt);
    var timeAgo = getTimeAgo(date);
    var initials = (c.author || '?')[0].toUpperCase();
    var replyCount = c.replies ? c.replies.length : 0;
    var hasReplies = replyCount > 0;
    var indentStyle = depth > 0 ? ' style="margin-left:' + Math.min(depth * 16, 64) + 'px"' : '';

    var html = '';
    html += '<div class="comment-item' + (depth > 0 ? ' comment-threaded' : '') + '"' + indentStyle + ' data-comment-id="' + c.id + '">';
    html += '<div class="comment-item-avatar" style="background:' + avatarColor(c.author) + '">';
    html += '<span class="comment-avatar-letter">' + escHtml(initials) + '</span>';
    html += '</div>';
    html += '<div class="comment-item-body">';
    html += '<div class="comment-item-header">';
    html += '<span class="comment-item-author">' + escHtml(c.author) + '</span>';
    html += '<span class="comment-item-time">' + timeAgo + '</span>';
    if (depth === 0 && hasReplies) {
      html += '<span class="comment-reply-count">' + replyCount + ' repl' + (replyCount !== 1 ? 'ies' : 'y') + '</span>';
    }
    html += '</div>';
    html += '<div class="comment-item-text">' + linkify(escHtml(c.text)) + '</div>';
    html += '<div class="comment-item-actions">';
    var likes = (c.likes || []).length;
    html += '<button class="comment-like-btn" data-id="' + c.id + '">🔥 <span class="comment-like-count">' + (likes > 0 ? likes : '') + '</span></button>';
    if (currentUser) {
      html += '<button class="comment-reply-btn" data-parent="' + c.id + '">Reply</button>';
    }
    html += '</div>';
    // Inline reply form (hidden initially)
    html += '<div class="comment-reply-form" id="replyForm-' + c.id + '" style="display:none">';
    html += '<textarea class="comment-textarea comment-reply-textarea" placeholder="Write a reply…" maxlength="2000" rows="2"></textarea>';
    html += '<div class="comment-reply-actions">';
    html += '<button class="comment-cancel-btn" data-parent="' + c.id + '">Cancel</button>';
    html += '<button class="comment-submit comment-reply-submit" data-parent="' + c.id + '">Reply</button>';
    html += '</div>';
    html += '</div>';
    // Render nested replies
    if (hasReplies) {
      html += '<div class="comment-replies">';
      c.replies.forEach(function(r) {
        html += renderComment(r, depth + 1);
      });
      html += '</div>';
    }
    html += '</div>'; // comment-item-body
    html += '</div>'; // comment-item

    return html;
  }

  function bindEvents(comments) {
    // ─── Google sign-in ───
    var googleBtn = document.getElementById('commentGoogleBtn');
    if (googleBtn) {
      googleBtn.addEventListener('click', function() {
        if (firebaseApp && firebase.auth) {
          var provider = new firebase.auth.GoogleAuthProvider();
          firebase.auth(firebaseApp).signInWithPopup(provider)
            .then(function() {
              // onAuthStateChanged will fire and re-render
            })
            .catch(function(err) {
              if (err.code !== 'auth/popup-closed-by-user') {
                alert('Google sign-in failed: ' + err.message);
              }
            });
        } else {
          alert('Google sign-in not available. Try The Hive sign-in.');
        }
      });
    }

    // ─── Hive sign-in ───
    var hiveBtn = document.getElementById('commentHiveBtn');
    if (hiveBtn) {
      hiveBtn.addEventListener('click', function() {
        // Check if already have a hive session
        var hiveUser = getHiveUser();
        var hiveToken = getHiveToken();
        if (hiveUser && hiveToken) {
          // Re-resolve auth
          resolveCurrentUser(firebaseUser, function() { renderComments(); });
          return;
        }
        // Open hive auth modal
        if (typeof showHiveJoinModal === 'function') {
          showHiveJoinModal('login');
        } else {
          window.location.href = '/hive';
        }
      });
    }

    // ─── Like buttons ───
    document.querySelectorAll('.comment-like-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var commentId = btn.getAttribute('data-id');
        fetch(API_BASE + '?action=like', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ commentId: commentId, token: 'hive-comment-blast-2026' })
        })
        .then(function(r) { return r.json(); })
        .then(function(d) {
          if (d.status === 'success') {
            loadComments(); // refresh to show new count
          }
        })
        .catch(function() {});
      });
    });

    // ─── Top-level submit ───
    var textarea = document.getElementById('commentTextarea');
    var submitBtn = document.getElementById('commentSubmitBtn');
    if (textarea && submitBtn) {
      submitBtn.addEventListener('click', function() {
        submitComment(textarea.value, null, comments);
      });
      textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          submitComment(textarea.value, null, comments);
        }
      });
    }

    // ─── Reply buttons ───
    document.querySelectorAll('.comment-reply-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var parentId = btn.getAttribute('data-parent');
        document.querySelectorAll('.comment-reply-form').forEach(function(f) {
          if (f.id !== 'replyForm-' + parentId) f.style.display = 'none';
        });
        var form = document.getElementById('replyForm-' + parentId);
        if (form) {
          var isVisible = form.style.display !== 'none';
          form.style.display = isVisible ? 'none' : 'block';
          if (!isVisible) {
            var ta = form.querySelector('.comment-reply-textarea');
            if (ta) setTimeout(function() { ta.focus(); }, 50);
          }
        }
      });
    });

    // ─── Cancel reply buttons ───
    document.querySelectorAll('.comment-cancel-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var parentId = btn.getAttribute('data-parent');
        var form = document.getElementById('replyForm-' + parentId);
        if (form) {
          form.style.display = 'none';
          var ta = form.querySelector('.comment-reply-textarea');
          if (ta) ta.value = '';
        }
      });
    });

    // ─── Reply submit buttons ───
    document.querySelectorAll('.comment-reply-submit').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var parentId = btn.getAttribute('data-parent');
        var form = document.getElementById('replyForm-' + parentId);
        if (!form) return;
        var ta = form.querySelector('.comment-reply-textarea');
        if (!ta) return;
        submitComment(ta.value, parentId, comments, function() {
          ta.value = '';
          form.style.display = 'none';
        });
      });
    });
  }

  // ─── Central comment submit ───
  function submitComment(rawText, parentId, comments, onSuccess) {
    if (!currentUser) {
      alert('You must sign in to comment.');
      renderComments();
      return;
    }

    var text = rawText.trim();
    if (!text) return;

    var body = {
      article: articleSlug,
      text: text,
      author: currentUser.displayName,
      photoURL: currentUser.photoURL || null,
      uid: currentUser.uid
    };
    if (parentId) body.parentId = parentId;
    if (currentUser.token) body.token = currentUser.token;

    var btn = document.getElementById('commentSubmitBtn');
    if (btn) { btn.disabled = true; btn.textContent = 'Posting...'; }

    fetch(API_BASE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (btn) { btn.disabled = false; btn.textContent = 'Post Comment'; }
      if (d.status === 'success') {
        comments.push(d.comment);
        render(comments);
        if (onSuccess) onSuccess();
      } else {
        alert(d.error || 'Failed to post comment');
      }
    })
    .catch(function() {
      if (btn) { btn.disabled = false; btn.textContent = 'Post Comment'; }
      alert('Connection error. Try again.');
    });
  }

  function renderComments() {
    loadComments();
  }

  // ─── Load ───
  function loadComments() {
    fetch(API_BASE + '?article=' + encodeURIComponent(articleSlug))
      .then(function(r) { return r.json(); })
      .then(function(d) {
        var comments = d.comments || [];
        render(comments);
      })
      .catch(function() {
        container.innerHTML = '<div class="comment-error">Failed to load comments.</div>';
      });
  }

  // ─── Helpers ───
  function escHtml(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }
  function escAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/\"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function linkify(text) {
    return text.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
  }
  function getTimeAgo(date) {
    var seconds = Math.floor((new Date() - date) / 1000);
    if (seconds < 60) return 'just now';
    var minutes = Math.floor(seconds / 60);
    if (minutes < 60) return minutes + 'm ago';
    var hours = Math.floor(minutes / 60);
    if (hours < 24) return hours + 'h ago';
    var days = Math.floor(hours / 24);
    if (days < 7) return days + 'd ago';
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  // ─── Init ───
  function initFirebaseSDK(callback) {
    // Dynamically load Firebase SDK if not already available
    if (typeof firebase !== 'undefined' && firebase.initializeApp) {
      callback();
      return;
    }

    var loaded = 0;
    function onLoad() {
      loaded++;
      if (loaded === 2) callback();
    }

    var appScript = document.createElement('script');
    appScript.src = 'https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js';
    appScript.onload = onLoad;
    appScript.onerror = function() { onLoad(); };
    document.head.appendChild(appScript);

    var authScript = document.createElement('script');
    authScript.src = 'https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js';
    authScript.onload = onLoad;
    authScript.onerror = function() { onLoad(); };
    document.head.appendChild(authScript);
  }

  function init() {
    initFirebaseSDK(function() {
      // Initialize Firebase
      if (typeof firebase !== 'undefined' && firebase.initializeApp) {
        try {
          firebaseApp = firebase.initializeApp(FIREBASE_CONFIG, 'thesignal-comments');
        } catch(e) {
          // Already initialized
          try { firebaseApp = firebase.app('thesignal-comments'); } catch(e2) { firebaseApp = null; }
        }

        if (firebaseApp && firebase.auth) {
          // Listen for auth state changes
          firebase.auth(firebaseApp).onAuthStateChanged(function(user) {
            firebaseUser = user;
            resolveCurrentUser(user, function() {
              if (document.getElementById('commentsContainer')) {
                loadComments();
              }
            });
          });
          return;
        }
      }

      // No Firebase — just use Hive auth
      resolveCurrentUser(null, function() {
        loadComments();
      });
    });

    // Listen for Hive auth changes (cross-tab)
    window.addEventListener('storage', function(e) {
      if (e.key === 'hive_user' || e.key === 'hive_token') {
        resolveCurrentUser(firebaseUser, function() { loadComments(); });
      }
    });
  }

  init();
})();
