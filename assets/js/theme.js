// Theme + mobile nav toggle. FOUC-free theme init runs inline in <head>; this only wires controls.
(function () {
  var root = document.documentElement;

  // Theme toggle
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var current = root.getAttribute('data-theme') || 'dark';
      var next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });

    // Follow OS changes only if the user hasn't pinned a choice.
    var media = window.matchMedia('(prefers-color-scheme: dark)');
    if (media.addEventListener) {
      media.addEventListener('change', function (e) {
        if (localStorage.getItem('theme')) return;
        root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
      });
    }
  }

  // Mobile navigation toggle
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();