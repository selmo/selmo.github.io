---
title: "곡 정보 및 해설 (Songs)"
updated: 2026-08-11
---

# 곡 정보 및 해설 (Songs)

번역곡, 번안곡 및 주요 작품들에 대한 해설입니다. 각 곡은 원곡 정보, 작곡가, 수록 성가집을 포함합니다. 아래 목록은 `_data/songs.yml`에서 자동 생성됩니다 — 새 곡은 YAML에 항목을 추가하면 이 표에 자동으로 표시됩니다.

{% assign songs = site.data.songs.items %}
{% assign translations = songs | where: "type", "translation" %}
{% assign adaptations = songs | where: "type", "adaptation" %}
{% assign originals = songs | where: "type", "original" %}

## 번역곡 — 원곡 작곡가별

| 곡명 (한국어) | 원곡 | 작곡가 | 야훼이레 번호 | 페이지 |
|:---|:---|:---|:---:|:---|
{% for s in translations -%}
| {{ s.title_ko }} | {{ s.title_en }} | {{ s.composer }}{% if s.co_composer %} ({{ s.co_composer }} 공동){% endif %} | {% if s.yahure_number %}#{{ s.yahure_number }}{% else %}-{% endif %} | [→]({{ s.file }}.md) |
{% endfor %}

## 번안곡

| 곡명 (한국어) | 원곡 | 번안 | 페이지 |
|:---|:---|:---|:---|
{% for s in adaptations -%}
| {{ s.title_ko }} | {{ s.title_en }} | {{ s.composer }} | [→]({{ s.file }}.md) |
{% endfor %}

## 창작곡 — 작곡가별 카탈로그

| 작곡가 | 수록곡 | 성가집 | 페이지 |
|:---|:---|:---|:---|
{% for s in originals -%}
| {{ s.composer }} | {% if s.note %}{{ s.note }}{% endif %} | 야훼이레 | [→]({{ s.file }}.md) |
{% endfor %}

## 빠른 검색 — 작곡가 → 곡

> "수록곡" 열은 이 사이트에 **개별 페이지가 있는 곡**입니다. 전체 카탈로그(야훼이레 전 수록곡 포함)는 [작곡가·수록곡·성가집 크로스 레퍼런스](../CrossReference.md)를 참조하세요.

| 작곡가 | 수록곡 (한국어 제목) | 곡 페이지 |
|:---|:---|:---|
{% assign by_composer = translations | group_by: "composer" -%}
{% for g in by_composer -%}
| {{ g.name }} | {% for it in g.items %}{{ it.title_ko }}{% unless forloop.last %}, {% endunless %}{% endfor %} | {% for it in g.items %}[{{ it.file }}]({{ it.file }}.md){% unless forloop.last %} · {% endunless %}{% endfor %} |
{% endfor %}

## 관련 항목

- [작곡가·수록곡·성가집 크로스 레퍼런스](../CrossReference.md) — 전체 작곡가-곡-성가집 관계 그래프
- [아티스트 목록](../artists/index.md) — 작곡가 프로필
- [어린이·청소년·청년 성가집 비교](../Songbooks.md)
- [외국 원곡 매핑](../CrossReference.md#외국-원곡--한국어-번역-매핑)