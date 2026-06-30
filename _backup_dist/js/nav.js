// The Signal — Rocket Lab-style Drawer (mobile hamburger only)
(function() {
  var btn = document.getElementById('hamburgerToggle');
  var drawer = document.getElementById('drawer');
  var overlay = document.getElementById('drawerOverlay');
  var closeBtn = document.getElementById('drawerClose');

  function openDrawer() {
    if (drawer) drawer.classList.add('open');
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer() {
    if (drawer) drawer.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
    var main = document.getElementById('drawerMain');
    var sub = document.getElementById('drawerSub');
    if (main) main.classList.remove('hidden');
    if (sub) sub.classList.remove('active');
  }

  window.openSubDrawer = function() {
    var main = document.getElementById('drawerMain');
    var sub = document.getElementById('drawerSub');
    if (main) main.classList.add('hidden');
    if (sub) sub.classList.add('active');
  };
  window.closeSubDrawer = function() {
    var main = document.getElementById('drawerMain');
    var sub = document.getElementById('drawerSub');
    if (main) main.classList.remove('hidden');
    if (sub) sub.classList.remove('active');
  };

  if (btn && drawer && overlay) {
    btn.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });
  }
})();
