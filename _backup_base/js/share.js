// Share functionality for article pages — handles copy link
(function() {
  'use strict';
  document.addEventListener('DOMContentLoaded', function() {
    var copyBtn = document.getElementById('copyLinkBtn');
    if (!copyBtn) return;
    copyBtn.addEventListener('click', function() {
      var url = this.getAttribute('data-url');
      if (!url) return;
      navigator.clipboard.writeText(url).then(function() {
        var fb = document.getElementById('copyFeedback');
        if (fb) {
          fb.style.display = 'inline';
          setTimeout(function() { fb.style.display = 'none'; }, 1500);
        }
      }).catch(function() {
        // Fallback for older browsers
        var input = document.createElement('input');
        input.value = url;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        document.body.removeChild(input);
        var fb = document.getElementById('copyFeedback');
        if (fb) {
          fb.style.display = 'inline';
          setTimeout(function() { fb.style.display = 'none'; }, 1500);
        }
      });
    });
  });
})();
