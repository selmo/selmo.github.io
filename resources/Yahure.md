---
title: "야훼이레 3판 수록곡 목록"
updated: 2024-01-05
---

# 야훼이레 3판 수록곡 목록

가톨릭 청년 성가집 **야훼이레 3판**의 수록곡 색인입니다. 번호·곡명·작사/작곡자만 정리했으며, 악보와 가사는 담고 있지 않습니다.

{% assign yh = site.data.yahure.items %}
{% assign cath = yh | where: "tradition", "가톨릭" %}
{% assign prot = yh | where: "tradition", "개신교" %}

**전체 {{ yh.size }}곡** — 가톨릭 {{ cath.size }} · 개신교 {{ prot.size }} · 그 외 {{ yh.size | minus: cath.size | minus: prot.size }}

<div class="sb-filter" id="sb-filter">
  <input type="search" id="sb-q" placeholder="곡명 · 작사/작곡자 · 번호 검색…" aria-label="수록곡 검색">
  <select id="sb-tradition" aria-label="구분 필터">
    <option value="">전체 구분</option>
    <option value="가톨릭">가톨릭</option>
    <option value="개신교">개신교</option>
  </select>
  <span class="sb-count" id="sb-count" aria-live="polite"></span>
</div>

<div class="songbook-table" markdown="1">

| 번호 | 곡명 | 작사 · 작곡 | 구분 |
|---:|:---|:---|:---:|
{% for s in yh -%}
| <span class="row-meta" data-tradition="{{ s.tradition }}" data-search="{{ s.num }} {{ s.title | downcase }} {% if s.title_en %}{{ s.title_en | downcase }} {% endif %}{{ s.author | downcase }}"></span>{{ s.num }} | {{ s.title }}{% if s.title_en %}<br><sub>{{ s.title_en }}</sub>{% endif %} | {{ s.author }}{% if s.author_src %}<br><sub>{{ s.author_src }}</sub>{% endif %} | {% if s.tradition %}<sub>{{ s.tradition }}</sub>{% endif %} |
{% endfor %}

</div>

<script src="{{ '/assets/js/songbook-filter.js' | relative_url }}" defer></script>

---

## 참고

- 이 목록은 `resources/야훼이레-수록곡목록-3판.xlsx`에서 자동 생성됩니다(`scripts/gen_songbooks.py`).
- 곡의 저작권은 각 작사·작곡자와 저작권자에게 있습니다. 성가집 사용은 발행처의 안내를 따라 주세요.

## 관련 페이지

- [하늘바다 수록곡 목록](Haneulbada.md) — 가톨릭 어린이 찬양집
- [성가집 비교 (Songbooks)](../ccm/Songbooks.md) — 어린이·청소년·청년 성가집 비교
- [최태형 · OnE 악보](Scores.md)
