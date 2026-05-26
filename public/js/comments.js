// The Signal — Threaded Comments System
// Google sign-in OR guest posting (Reddit-style) with nested replies
(function() {
  'use strict';

  var container = document.getElementById('commentsContainer');
  if (!container) return;

  var articleSlug = container.getAttribute('data-slug');
  if (!articleSlug) return;

  // Guest name from localStorage
  function getGuestName() {
    try { return localStorage.getItem('signal_guest_name') || ''; } catch { return ''; }
  }
  function setGuestName(name) {
    try { localStorage.setItem('signal_guest_name', name); } catch {}
  }

  // ─── Build threaded tree from flat list ───
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
  function render(comments, user) {
    var roots = buildTree(comments);
    var totalCount = countAll(roots);
    var html = '';

    // Comment form
    html += '<div class="comment-form-area" id="commentFormArea">';
    if (user && user.email) {
      html += '<div class="comment-user-bar">';
      if (user.photoURL) {
        html += '<img src="' + escAttr(user.photoURL) + '" class="comment-avatar" alt="" width="28" height="28">';
      } else {
        html += '<div class="comment-avatar comment-avatar-fallback">' + escHtml((user.displayName || user.email || '?')[0]) + '</div>';
      }
      html += '<span class="comment-user-name">' + escHtml(user.displayName || user.email) + '</span>';
      html += '<span class="comment-user-badge">Google</span>';
      html += '</div>';
    } else if (getGuestName()) {
      html += '<div class="comment-user-bar">';
      html += '<div class="comment-avatar comment-avatar-fallback">' + escHtml(getGuestName()[0]) + '</div>';
      html += '<span class="comment-user-name">' + escHtml(getGuestName()) + '</span>';
      html += '<button class="comment-name-btn" id="commentChangeName">Change name</button>';
      html += '</div>';
    } else {
      html += '<div class="comment-user-bar comment-guest-bar">';
      html += '<input type="text" class="comment-name-input" id="commentGuestName" placeholder="Your name (optional)" maxlength="40" autocomplete="name">';
      html += '</div>';
    }
    html += '<textarea class="comment-textarea" id="commentTextarea" placeholder="Share your thoughts…" maxlength="2000" rows="3"></textarea>';
    html += '<button class="comment-submit" id="commentSubmitBtn">Post</button>';
    html += '</div>';

    // Sign in prompt
    if (!user || !user.email) {
      html += '<div class="comment-signin-prompt">';
      html += '<button class="comment-google-btn" id="commentGoogleBtn"><span class="comment-google-icon">G</span> Sign in with Google (optional)</button>';
      html += '<span class="comment-signin-note">Or just enter a name above</span>';
      html += '</div>';
    }

    // Comments list
    html += '<div class="comment-list" id="commentList">';
    if (roots.length === 0) {
      html += '<div class="comment-empty">No comments yet. Be the first to share your thoughts.</div>';
    } else {
      html += '<div class="comment-count">' + totalCount + ' comment' + (totalCount !== 1 ? 's' : '') + '</div>';
      roots.forEach(function(c) {
        html += renderComment(c, user, 0);
      });
    }
    html += '</div>';

    container.innerHTML = html;
    bindEvents(user, comments);
  }

  function renderComment(c, user, depth) {
    var date = new Date(c.createdAt);
    var timeAgo = getTimeAgo(date);
    var initials = (c.author || '?')[0].toUpperCase();
    var replyCount = c.replies ? c.replies.length : 0;
    var hasReplies = replyCount > 0;
    var indentStyle = depth > 0 ? ' style="margin-left:' + Math.min(depth * 16, 64) + 'px"' : '';

    var html = '';
    html += '<div class="comment-item' + (depth > 0 ? ' comment-threaded' : '') + '"' + indentStyle + ' data-comment-id="' + c.id + '">';
    html += '<div class="comment-item-avatar">';
    if (c.photoURL) {
      html += '<img src="' + escAttr(c.photoURL) + '" alt="" width="32" height="32">';
    } else {
      html += '<div class="comment-avatar-fallback sm">' + escHtml(initials) + '</div>';
    }
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
    html += '<button class="comment-reply-btn" data-parent="' + c.id + '">Reply</button>';
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
        html += renderComment(r, user, depth + 1);
      });
      html += '</div>';
    }
    html += '</div>'; // comment-item-body
    html += '</div>'; // comment-item

    return html;
  }

  function bindEvents(user, comments) {
    // ─── Top-level submit ───
    var textarea = document.getElementById('commentTextarea');
    var submitBtn = document.getElementById('commentSubmitBtn');
    if (textarea && submitBtn) {
      submitBtn.addEventListener('click', function() {
        submitComment(textarea.value, null, user, comments);
      });
      textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          submitComment(textarea.value, null, user, comments);
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
        submitComment(ta.value, parentId, user, comments, function() {
          ta.value = '';
          form.style.display = 'none';
        });
      });
    });

    // ─── Change guest name ───
    var changeNameBtn = document.getElementById('commentChangeName');
    if (changeNameBtn) {
      changeNameBtn.addEventListener('click', function() {
        var name = prompt('Enter your display name:');
        if (name && name.trim()) {
          setGuestName(name.trim());
          render(comments, user);
        }
      });
    }

    // ─── Google sign-in button ───
    var googleBtn = document.getElementById('commentGoogleBtn');
    if (googleBtn) {
      googleBtn.addEventListener('click', function() {
        if (typeof firebase !== 'undefined' && firebase.auth) {
          var provider = new firebase.auth.GoogleAuthProvider();
          firebase.auth().signInWithPopup(provider).catch(function(err) {
            if (err.code === 'auth/popup-blocked') {
              firebase.auth().signInWithRedirect(provider);
            }
          });
        }
      });
    }
  }

  // ─── Central comment submit (top-level + reply) ───
  function submitComment(rawText, parentId, user, comments, onSuccess) {
    var text = rawText.trim();
    if (!text) return;

    var author;
    var photoURL = null;
    var uid = null;

    if (user && user.email) {
      author = user.displayName || user.email;
      photoURL = user.photoURL || null;
      uid = user.uid;
    } else {
      var nameInput = document.getElementById('commentGuestName');
      if (nameInput && nameInput.value.trim()) {
        author = nameInput.value.trim();
        setGuestName(author);
      } else {
        var storedName = getGuestName();
        if (storedName) {
          author = storedName;
        } else {
          author = 'Anonymous';
        }
      }
    }

    var body = {
      article: articleSlug,
      text: text,
      author: author,
      photoURL: photoURL,
      uid: uid
    };
    if (parentId) body.parentId = parentId;

    fetch('/api/comments/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (d.status === 'success') {
        comments.push(d.comment);
        // Re-render entirely — safe even if inline form elements are stale
        render(comments, user);
        if (onSuccess) onSuccess();
      } else {
        alert(d.error || 'Failed to post comment');
      }
    })
    .catch(function() {
      alert('Connection error. Try again.');
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

  // ─── Load comments ───
  function load() {
    fetch('/api/comments/?article=' + encodeURIComponent(articleSlug))
      .then(function(r) { return r.json(); })
      .then(function(d) {
        var comments = d.comments || [];
        if (typeof firebase !== 'undefined' && firebase.auth) {
          firebase.auth().onAuthStateChanged(function(firebaseUser) {
            var user = firebaseUser ? {
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              displayName: firebaseUser.displayName,
              photoURL: firebaseUser.photoURL
            } : null;
            render(comments, user);
          });
        } else {
          render(comments, null);
        }
      })
      .catch(function() {
        container.innerHTML = '<div class="comment-error">Failed to load comments.</div>';
      });
  }

  load();
})();
