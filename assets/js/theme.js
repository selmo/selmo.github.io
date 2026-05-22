// Theme toggle. FOUC-free init runs inline in <head>; this only wires the button.
(function () {
  var root = document.documentElement;
  var button = document.querySelector('.theme-toggle');
  if (!button) return;

  button.addEventListener('click', function () {
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
})();
