// carousel.js — Drives the Signal Highlights card carousel
// Uses CSS scroll-snap for smooth native scrolling
(function(){
  'use strict';

  var carousels = document.querySelectorAll('[data-carousel]');
  if (!carousels.length) return;

  var AUTOPLAY_DELAY = 5000;

  function initCarousel(wrap) {
    var track = wrap.querySelector('[data-carousel-track]');
    var prevBtn = wrap.querySelector('[data-carousel-prev]');
    var nextBtn = wrap.querySelector('[data-carousel-next]');
    var dotsEl = wrap.querySelector('[data-carousel-dots]');
    if (!track) return;

    var cards = track.querySelectorAll('.detail-card-link');
    var total = cards.length;
    if (total < 2) return;

    var current = 0;
    var autoplayTimer = null;
    var isScrolling = false;

    // Build dots
    var dots = [];
    for (var i = 0; i < total; i++) {
      var dot = document.createElement('button');
      dot.className = 'detail-carousel-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('data-index', i);
      dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      dot.addEventListener('click', (function(idx) {
        return function() { goTo(idx); };
      })(i));
      dotsEl.appendChild(dot);
      dots.push(dot);
    }

    function getCardWidth() {
      if (cards.length === 0) return 340;
      var cardW = cards[0].offsetWidth;
      var gapStr = window.getComputedStyle(track).gap;
      var gapPx = gapStr === 'normal' ? 16 : parseFloat(gapStr) || 16;
      return cardW + gapPx;
    }

    function updateDots() {
      for (var i = 0; i < dots.length; i++) {
        dots[i].classList.toggle('active', i === current);
      }
    }

    function goTo(index) {
      if (index < 0) index = 0;
      if (index >= total) index = total - 1;
      if (index === current) return;

      current = index;
      var slideW = getCardWidth();
      track.scrollTo({ left: current * slideW, behavior: 'smooth' });
      updateDots();
      resetAutoplay();
    }

    function next() {
      if (current < total - 1) {
        goTo(current + 1);
      } else {
        goTo(0);
      }
    }

    function prev() {
      if (current > 0) {
        goTo(current - 1);
      } else {
        goTo(total - 1);
      }
    }

    function startAutoplay() {
      stopAutoplay();
      autoplayTimer = setInterval(next, AUTOPLAY_DELAY);
    }

    function stopAutoplay() {
      if (autoplayTimer) {
        clearInterval(autoplayTimer);
        autoplayTimer = null;
      }
    }

    function resetAutoplay() {
      startAutoplay();
    }

    // Sync current index from scroll position
    function syncIndex() {
      var scrollLeft = track.scrollLeft;
      var slideW = getCardWidth();
      if (slideW <= 0) return;
      var idx = Math.round(scrollLeft / slideW);
      if (idx < 0) idx = 0;
      if (idx >= total) idx = total - 1;
      if (idx !== current) {
        current = idx;
        updateDots();
        resetAutoplay();
      }
    }

    // Event listeners
    prevBtn.addEventListener('click', prev);
    nextBtn.addEventListener('click', next);

    // Track scroll position — uses passive scroll for smooth native feel
    track.addEventListener('scroll', syncIndex, { passive: true });

    wrap.addEventListener('mouseenter', stopAutoplay);
    wrap.addEventListener('mouseleave', startAutoplay);

    // Keyboard accessibility
    wrap.setAttribute('tabindex', '0');
    wrap.setAttribute('role', 'region');
    wrap.setAttribute('aria-label', 'Signal Highlights carousel');
    wrap.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowLeft') { prev(); e.preventDefault(); }
      if (e.key === 'ArrowRight') { next(); e.preventDefault(); }
    });

    // Recalculate scroll position on resize
    var resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        var slideW = getCardWidth();
        track.scrollTo({ left: current * slideW, behavior: 'auto' });
      }, 150);
    });

    // Init
    updateDots();
    startAutoplay();
  }

  for (var i = 0; i < carousels.length; i++) {
    initCarousel(carousels[i]);
  }
})();
