// 성가집 수록곡 목록 필터 — 검색 / 구분
// 각 행 첫 셀에 숨겨둔 <span class="row-meta" data-search data-tradition>을 읽어 걸러낸다.
// 야훼이레(구분 필터 있음)와 하늘바다(없음) 양쪽에서 같은 스크립트를 쓴다.
(function () {
  var filter = document.getElementById('sb-filter');
  if (!filter) return;

  var q = document.getElementById('sb-q');
  var tradSel = document.getElementById('sb-tradition');   // 하늘바다에는 없다
  var count = document.getElementById('sb-count');

  var rows = [];
  document.querySelectorAll('.songbook-table tbody tr').forEach(function (tr) {
    var meta = tr.querySelector('.row-meta');
    if (!meta) return;
    rows.push({
      tr: tr,
      search: meta.getAttribute('data-search') || '',
      tradition: meta.getAttribute('data-tradition') || ''
    });
  });
  if (rows.length === 0) return;

  function apply() {
    var term = (q.value || '').trim().toLowerCase();
    var trad = tradSel ? tradSel.value : '';
    var shown = 0;

    rows.forEach(function (r) {
      var ok = (!term || r.search.indexOf(term) !== -1) &&
               (!trad || r.tradition === trad);
      r.tr.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });

    count.textContent = (term || trad)
      ? shown + ' / ' + rows.length + '곡'
      : rows.length + '곡';
  }

  q.addEventListener('input', apply);
  if (tradSel) tradSel.addEventListener('change', apply);
  apply();
})();
