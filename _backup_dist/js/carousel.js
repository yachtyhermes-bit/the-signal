(function() {
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
    var isAnimating = false;

    // Build dots
    var dots = [];
    for (var i = 0; i < total; i++) {
      var dot = document.createElement('button');
      dot.className = 'detail-carousel-dot';
      dot.setAttribute('data-index', i);
      dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      dot.addEventListener('click', function(idx) {
        return function() { goTo(idx); };
      }(i));
      dotsEl.appendChild(dot);
      dots.push(dot);
    }

    function getSlideWidth() {
      if (cards.length === 0) return 360;
      // Measure the actual rendered width of the first card
      var cardW = cards[0].offsetWidth;
      // Compute gap from the track's computed gap
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
      if (isAnimating) return;
      if (index < 0) index = 0;
      if (index >= total) index = total - 1;
      if (index === current) return;

      isAnimating = true;
      current = index;
      var slideW = getSlideWidth();
      var offset = current * slideW;

      track.style.transform = 'translateX(-' + offset + 'px)';
      track.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';

      function onEnd() {
        isAnimating = false;
        track.removeEventListener('transitionend', onEnd);
      }
      track.addEventListener('transitionend', onEnd);

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

    // Event listeners
    prevBtn.addEventListener('click', prev);
    nextBtn.addEventListener('click', next);

    wrap.addEventListener('mouseenter', stopAutoplay);
    wrap.addEventListener('mouseleave', startAutoplay);

    // Touch/swipe support
    var touchStartX = 0;
    var touchEndX = 0;
    track.addEventListener('touchstart', function(e) {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoplay();
    }, { passive: true });
    track.addEventListener('touchend', function(e) {
      touchEndX = e.changedTouches[0].screenX;
      var diff = touchStartX - touchEndX;
      if (Math.abs(diff) > 50) {
        if (diff > 0) next();
        else prev();
      }
      startAutoplay();
    }, { passive: true });

    // Keyboard accessibility
    wrap.setAttribute('tabindex', '0');
    wrap.setAttribute('role', 'region');
    wrap.setAttribute('aria-label', 'Signal Highlights carousel');
    wrap.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowLeft') { prev(); e.preventDefault(); }
      if (e.key === 'ArrowRight') { next(); e.preventDefault(); }
    });

    // Recalculate on resize
    var resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        var slideW = getSlideWidth();
        var offset = current * slideW;
        track.style.transition = 'none';
        track.style.transform = 'translateX(-' + offset + 'px)';
        // Force reflow
        track.offsetHeight;
        track.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
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
