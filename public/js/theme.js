// Theme toggle for article pages — light/dark mode
// Synced with nav bar switch checkbox and localStorage
(function() {
  'use strict';

  var STORAGE_KEY = 'signal-theme';
  var checkbox = document.getElementById('themeToggleInput');

  function getPreferredTheme() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return 'dark';
  }

  function applyTheme(theme, updateCheckbox) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    if (checkbox && updateCheckbox !== false) {
      checkbox.checked = (theme === 'light');
    }
  }

  function toggleTheme() {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Apply saved theme on load
  var savedTheme = getPreferredTheme();
  applyTheme(savedTheme);

  // Sync checkbox with current theme
  if (checkbox) {
    checkbox.checked = (savedTheme === 'light');
    checkbox.addEventListener('change', function() {
      applyTheme(this.checked ? 'light' : 'dark', false);
    });
  }

  // Expose toggle globally for other UI elements
  window.toggleTheme = toggleTheme;
})();
