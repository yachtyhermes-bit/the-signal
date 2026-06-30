// The Signal — Rocket Lab-style Drawer Navigation
(function() {
  var btn = document.getElementById('hamburgerToggle');
  var drawer = document.getElementById('drawer');
  var overlay = document.getElementById('drawerOverlay');
  var closeBtn = document.getElementById('drawerClose');
  var main = document.getElementById('drawerMain');
  var sub = document.getElementById('drawerSub');

  function openDrawer() {
    if (drawer) drawer.classList.add('open');
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer() {
    if (drawer) drawer.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
    // Reset sub-drawer
    if (main) main.classList.remove('hidden');
    if (sub) sub.classList.remove('active');
  }
  window.openDrawer = openDrawer;
  window.closeDrawer = closeDrawer;

  window.openSubDrawer = function() {
    if (main) main.classList.add('hidden');
    if (sub) sub.classList.add('active');
  };
  window.closeSubDrawer = function() {
    if (main) main.classList.remove('hidden');
    if (sub) sub.classList.remove('active');
  };

  // Desktop dropdown
  window.toggleDropdown = function(e) {
    e.stopPropagation();
    var dd = document.getElementById('sectorsDropdown');
    if (dd) dd.classList.toggle('open');
  };

  // Bind events
  if (btn && drawer && overlay) {
    btn.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });
    // Close dropdown on outside click
    document.addEventListener('click', function(e) {
      var dd = document.getElementById('sectorsDropdown');
      if (dd && dd.classList.contains('open') && !dd.contains(e.target)) {
        dd.classList.remove('open');
      }
    });
  }
})();
