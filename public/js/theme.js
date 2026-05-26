// Theme toggle for article pages — light/dark mode
(function() {
  const STORAGE_KEY = 'signal-theme';

  function getPreferredTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return 'dark';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Apply saved theme on load
  applyTheme(getPreferredTheme());

  // Expose toggle globally for inline onclick
  window.toggleTheme = toggleTheme;
})();
