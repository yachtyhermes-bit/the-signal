// Hero background video loader.
// The <video> ships with preload="none" and a poster, so the first paint costs ~69KB
// instead of the full loop. This decides whether to fetch the loop at all.
(function() {
  'use strict';

  var v = document.querySelector('video.hero-video');
  if (!v) return;

  var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var slowLink = /(^|-)2g$/.test(conn.effectiveType || '') || conn.effectiveType === 'slow-2g';

  // Respect the user's data and motion preferences: leave the poster in place.
  if (conn.saveData === true || slowLink || reduceMotion) return;

  var src = window.matchMedia('(max-width: 640px)').matches
    ? v.getAttribute('data-src-mobile')
    : v.getAttribute('data-src-desktop');

  if (!src) return;

  v.addEventListener('error', function() {
    v.removeAttribute('src');
    v.load();
  });

  v.src = src;
  var playing = v.play();
  if (playing && playing.catch) playing.catch(function() { /* autoplay blocked: poster stays */ });
})();
