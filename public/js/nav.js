// Nav drawer — hamburger toggle, overlay, sector sub-drawer
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    var btn = document.querySelector('.hamburger-btn');
    var drawer = document.getElementById('drawer');
    var overlay = document.getElementById('drawerOverlay');
    var closeBtn = document.getElementById('drawerClose');

    if (!btn || !drawer || !overlay) return;

    function openDrawer() {
      drawer.classList.add('open');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      drawer.classList.remove('open');
      overlay.classList.remove('open');
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

    btn.addEventListener('click', function() { openDrawer(); });
    overlay.addEventListener('click', function() { closeDrawer(); });
    if (closeBtn) closeBtn.addEventListener('click', function() { closeDrawer(); });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });

    // Close drawer when any link is clicked inside it
    drawer.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', function() { closeDrawer(); });
    });
  });

})();
