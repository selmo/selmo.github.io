// Articles 클라이언트 사이드 필터 — 검색 / 연도 / 태그
// 각 표 행의 첫 셀에 숨겨둔 <span class="row-meta" data-year data-tags data-search>를 읽어 필터링한다.
(function () {
  var filter = document.getElementById('articles-filter');
  if (!filter) return;

  var search = document.getElementById('af-search');
  var yearSel = document.getElementById('af-year');
  var tagSel = document.getElementById('af-tag');
  var count = document.getElementById('af-count');

  // 표 행 메타 수집
  var rows = [];
  document.querySelectorAll('.main-content table').forEach(function (table) {
    table.querySelectorAll('tbody tr').forEach(function (tr) {
      var meta = tr.querySelector('.row-meta');
      if (!meta) return;
      rows.push({
        tr: tr,
        year: meta.getAttribute('data-year') || '',
        tags: (meta.getAttribute('data-tags') || ''),
        search: (meta.getAttribute('data-search') || '')
      });
    });
  });

  if (rows.length === 0) return;

  // 드롭다운 옵션 동적 생성
  var yearSet = {};
  var tagSet = {};
  rows.forEach(function (r) {
    if (r.year) yearSet[r.year] = 1;
    r.tags.split(',').forEach(function (t) { if (t) tagSet[t] = 1; });
  });
  Object.keys(yearSet).sort().reverse().forEach(function (y) {
    var o = document.createElement('option');
    o.value = y; o.textContent = y;
    yearSel.appendChild(o);
  });
  Object.keys(tagSet).sort().forEach(function (t) {
    var o = document.createElement('option');
    o.value = t; o.textContent = t;
    tagSel.appendChild(o);
  });

  function apply() {
    var q = (search.value || '').toLowerCase().trim();
    var y = yearSel.value;
    var tg = tagSel.value;
    var visible = 0;
    rows.forEach(function (r) {
      var ok = true;
      if (q && r.search.indexOf(q) === -1) ok = false;
      if (y && r.year !== y) ok = false;
      if (tg && (',' + r.tags + ',').indexOf(',' + tg + ',') === -1) ok = false;
      r.tr.style.display = ok ? '' : 'none';
      if (ok) visible++;
    });
    count.textContent = visible + ' / ' + rows.length + '건 표시';
  }

  search.addEventListener('input', apply);
  yearSel.addEventListener('change', apply);
  tagSel.addEventListener('change', apply);
  apply();
})();