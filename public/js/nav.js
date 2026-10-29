// Nav drawer — hamburger toggle, overlay, and stacked sub-drawers (SECTORS, MY ACCOUNT)
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    var btn = document.querySelector('.hamburger-btn');
    var drawer = document.getElementById('drawer');
    var overlay = document.getElementById('drawerOverlay');
    var closeBtn = document.getElementById('drawerClose');

    if (!btn || !drawer || !overlay) return;

    function subs() {
      return drawer.querySelectorAll('.drawer-sub');
    }

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
      if (main) main.classList.remove('hidden');
      subs().forEach(function(s) { s.classList.remove('active'); });
    }

    // Open a sub-panel by id. With no argument, opens the first sub-panel
    // (keeps old inline onclick="openSubDrawer()" markup working).
    window.openSubDrawer = function(id) {
      var main = document.getElementById('drawerMain');
      var list = subs();
      if (!list.length) return;
      var target = id ? document.getElementById(id) : list[0];
      if (!target) target = list[0];
      if (main) main.classList.add('hidden');
      list.forEach(function(s) { s.classList.toggle('active', s === target); });
    };

    window.closeSubDrawer = function() {
      var main = document.getElementById('drawerMain');
      if (main) main.classList.remove('hidden');
      subs().forEach(function(s) { s.classList.remove('active'); });
    };

    btn.addEventListener('click', function() { openDrawer(); });
    overlay.addEventListener('click', function() { closeDrawer(); });
    if (closeBtn) closeBtn.addEventListener('click', function() { closeDrawer(); });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });

    // Close the drawer when a real navigation link is clicked inside it.
    // javascript:void(0) triggers (SECTORS / MY ACCOUNT) must not close it.
    drawer.querySelectorAll('a').forEach(function(a) {
      var href = a.getAttribute('href') || '';
      if (href.indexOf('javascript:') !== 0) {
        a.addEventListener('click', function() { closeDrawer(); });
      }
    });

    // Back button inside the phone's browser closes the drawer before leaving the page
    window.addEventListener('popstate', function() {
      if (drawer.classList.contains('open')) closeDrawer();
    });
  });

})();
