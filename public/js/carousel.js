// carousel.js — Drives the Signal Highlights card carousel
// Works with data-carousel wrapper containing data-carousel-track + prev/next/dots
(function() {
  document.addEventListener('DOMContentLoaded', () => {
    const wrappers = document.querySelectorAll('[data-carousel]');
    wrappers.forEach(initCarousel);
  });

  function initCarousel(wrapper) {
    const track = wrapper.querySelector('[data-carousel-track]');
    const cards = track?.querySelectorAll('.detail-card-link');
    if (!track || !cards?.length) return;

    const prevBtn = wrapper.querySelector('[data-carousel-prev]');
    const nextBtn = wrapper.querySelector('[data-carousel-next]');
    const dotsContainer = wrapper.querySelector('[data-carousel-dots]');

    let currentIdx = 0;
    const total = cards.length;

    // Build dots
    if (dotsContainer) {
      dotsContainer.innerHTML = '';
      for (let i = 0; i < total; i++) {
        const dot = document.createElement('span');
        dot.className = 'detail-carousel-dot' + (i === 0 ? ' active' : '');
        dot.setAttribute('data-dot', i);
        dot.addEventListener('click', () => goTo(i));
        dotsContainer.appendChild(dot);
      }
    }

    function goTo(idx) {
      if (idx < 0) idx = total - 1;
      if (idx >= total) idx = 0;
      currentIdx = idx;

      // Slide track
      const cardWidth = cards[0].offsetWidth;
      const gap = 16; // match CSS gap
      track.style.transform = `translateX(-${idx * (cardWidth + gap)}px)`;

      // Update dots
      if (dotsContainer) {
        dotsContainer.querySelectorAll('.detail-carousel-dot').forEach((d, i) => {
          d.classList.toggle('active', i === idx);
        });
      }

      // Update prev/next visibility
      if (prevBtn) prevBtn.style.visibility = idx === 0 ? 'hidden' : 'visible';
      if (nextBtn) nextBtn.style.visibility = idx === total - 1 ? 'hidden' : 'visible';
    }

    if (prevBtn) prevBtn.addEventListener('click', () => goTo(currentIdx - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => goTo(currentIdx + 1));

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    track.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    track.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const diff = touchStartX - touchEndX;
      if (Math.abs(diff) > 50) {
        goTo(currentIdx + (diff > 0 ? 1 : -1));
      }
    });

    // Initial state
    goTo(0);
  }
})();
