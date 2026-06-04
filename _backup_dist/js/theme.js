// Theme toggle — light/dark mode
(function() {
  'use strict';

  var STORAGE_KEY = 'signal-theme';

  function getPreferredTheme() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return 'dark';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    // Update all theme toggle buttons
    var btns = document.querySelectorAll('.theme-toggle-btn');
    for (var i = 0; i < btns.length; i++) {
      btns[i].setAttribute('data-theme-active', theme);
    }
    // Update label text on homepage button
    var targets = document.querySelectorAll('.theme-label-target');
    for (var j = 0; j < targets.length; j++) {
      targets[j].textContent = theme === 'dark' ? 'Light' : 'Dark';
    }
    // Sync article page toggle button icon visibility
    var artBtn = document.getElementById('articleThemeToggle');
    if (artBtn) {
      artBtn.setAttribute('data-theme-active', theme);
    }
  }

  function toggleTheme() {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Wire article page toggle button
  var artToggle = document.getElementById('articleThemeToggle');
  if (artToggle) {
    artToggle.addEventListener('click', function(e) {
      e.preventDefault();
      toggleTheme();
    });
  }

  // Wire homepage toggle button
  var homeToggle = document.getElementById('themeToggleBtn');
  if (homeToggle) {
    homeToggle.addEventListener('click', function(e) {
      e.preventDefault();
      toggleTheme();
    });
  }

  // Apply saved theme on load
  applyTheme(getPreferredTheme());

  // Expose toggle globally for inline onclick handlers
  window.toggleTheme = toggleTheme;
})();
