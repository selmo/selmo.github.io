---
title: "하늘바다 수록곡 목록"
updated: 2026-08-20
---

# 하늘바다 수록곡 목록

가톨릭 어린이 찬양집 **하늘바다**의 수록곡 색인입니다. 번호·곡명·작곡/편곡자만 정리했으며, 악보와 가사는 담고 있지 않습니다.

{% assign mass = site.data.haneulbada.mass %}
{% assign songs = site.data.haneulbada.songs %}

**미사곡 {{ mass.size }}곡 · 그 외 {{ songs.size }}곡**

---

## 미사곡 — 전례 순서별

{% assign parts = "성호경,자비송,대영광송,화답송,복음환호송,사도신경,보편지향기도,거룩하시도다,거양성체,신앙의 신비여,아멘,주님의 기도,주님께 나라와,평화의 인사,하느님의 어린양,영광송" | split: "," %}

{% for p in parts %}
{% assign items = mass | where: "part", p %}
{% if items.size > 0 %}
### {{ p }}

| 번호 | 작곡 · 편곡 |
|---:|:---|
{% for m in items -%}
| {{ m.num }} | {{ m.author }} |
{% endfor %}

{% endif %}
{% endfor %}

---

## 그 외 수록곡 — 번호순

<div class="sb-filter" id="sb-filter">
  <input type="search" id="sb-q" placeholder="곡명 · 번호 검색…" aria-label="수록곡 검색">
  <span class="sb-count" id="sb-count" aria-live="polite"></span>
</div>

<div class="songbook-table" markdown="1">

| 번호 | 곡명 | 작곡 · 편곡 |
|---:|:---|:---|
{% for s in songs -%}
| <span class="row-meta" data-search="{{ s.num }} {{ s.title | downcase }} {% if s.author %}{{ s.author | downcase }}{% endif %}"></span>{{ s.num }} | {{ s.title }} | {% if s.author %}{{ s.author }}<br><sub>{{ s.author_src }}</sub>{% else %}—{% endif %} |
{% endfor %}

</div>

<script src="{{ '/assets/js/songbook-filter.js' | relative_url }}" defer></script>

---

## 참고

- 이 목록은 `resources/하늘바다.md`에서 자동 생성됩니다(`scripts/gen_songbooks.py`).
- 미사곡은 전례 순서(성호경 → 자비송 → … → 영광송)를 따랐고, 그 외 곡은 번호순입니다.
- 하늘바다 원본 목차에는 작곡가가 없습니다. 곡명이 같은 [야훼이레](Yahure.md) 수록곡에서 가져왔고, 출처를 함께 표기했습니다. 동명이곡이 있어 어느 곡인지 확정할 수 없으면 `—`로 두었습니다.
- 곡의 저작권은 각 작사·작곡자와 저작권자에게 있습니다. 성가집 사용은 발행처의 안내를 따라 주세요.

## 관련 페이지

- [야훼이레 3판 수록곡 목록](Yahure.md) — 가톨릭 청년 성가집
- [성가집 비교 (Songbooks)](../ccm/Songbooks.md) — 어린이·청소년·청년 성가집 비교
- [최태형 · OnE 악보](Scores.md)
