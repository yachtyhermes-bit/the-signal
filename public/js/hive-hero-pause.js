// Hive hero video auto-pause — stops video when scrolled past, resumes in view
(function() {
  'use strict';
  var video = document.querySelector('.hero-video');
  if (!video) return;

  function checkVisibility() {
    var rect = video.getBoundingClientRect();
    var inView = rect.bottom > 0 && rect.top < window.innerHeight;
    if (inView) {
      if (video.paused) video.play().catch(function(){});
    } else {
      if (!video.paused) video.pause();
    }
  }

  // Throttle scroll checks
  var ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        checkVisibility();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // Initial check
  checkVisibility();
})();
