---
title: "자료실 (Resources)"
updated: 2026-08-17
---

# 자료실 (Resources)

악보와 성가집 수록곡 색인을 모아둔 곳입니다.

## 악보

### [최태형 · OnE 악보 (Scores)](Scores.md)

최태형 안셀모의 미사곡과 밴드 OnE 활동곡의 악보(PDF)입니다. 곡마다 연주 영상을 함께 볼 수 있습니다.

{% assign pub = site.data.scores.items | where: "public", true %}
{% assign pub_groups = pub | map: "group" | uniq %}
> {{ pub_groups.size }}곡 · {{ pub.size }}개 파일

## 성가집 수록곡 색인

번호·곡명·작사/작곡자만 정리한 목록입니다. 악보와 가사는 담고 있지 않습니다.

### [야훼이레 3판](Yahure.md)

가톨릭 청년 성가집. 곡명·작사/작곡자·번호로 검색할 수 있고, 가톨릭/개신교 구분으로도 걸러집니다.

{% assign yh = site.data.songbooks.yahure %}
{% assign cath = yh | where: "tradition", "가톨릭" %}
{% assign prot = yh | where: "tradition", "개신교" %}
> {{ yh.size }}곡 — 가톨릭 {{ cath.size }} · 개신교 {{ prot.size }}

### [하늘바다](Haneulbada.md)

가톨릭 어린이 찬양집. 미사곡은 전례 순서별로, 그 외 곡은 번호순으로 정리했습니다.

{% assign hm = site.data.songbooks.haneulbada_mass %}
{% assign hs = site.data.songbooks.haneulbada_songs %}
> 미사곡 {{ hm.size }}곡 · 그 외 {{ hs.size }}곡

## 관련 페이지

- [성가집 비교 (Songbooks)](../ccm/Songbooks.md) — 어린이·청소년·청년 성가집 및 해외 미사 경본 비교
- [리소스 자료실 (Resources)](../ccm/Resources.md) — 출판사 카탈로그·교회 문헌 등 외부 링크
- [작곡가·수록곡·성가집 크로스 레퍼런스](../ccm/CrossReference.md)
