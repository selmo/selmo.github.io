---
title: "OnE 악보 다운로드 (Scores)"
# 비공개 페이지 — 사이트 내 링크 없이 URL 직접 접근만 허용
sitemap: false
noindex: true
---

# OnE 악보 다운로드 (Scores)

미사곡 · OnE 밴드 · CCM 번역곡 등의 악보(PDF)를 곡 단위로 제공합니다. 같은 곡의 여러 버전(Score · ChordChart · Chorus · 조성별)은 **한 줄에 모아** 표시되며, 각 링크를 클릭하면 해당 PDF가 다운로드됩니다.

- **미사곡**은 전례 순서(자비송 → 대영광송 → … → 마침영광송)대로, 작곡가별로 구분했습니다.
- **그 외 곡**은 곡명 기준으로 정리했으며, 작곡가가 파일에 명시된 경우에만 표기했습니다.
- **성가집 번호**는 [야훼이레 3판](../ccm/Songbooks.md)과 [하늘바다](하늘바다.md)(가톨릭 어린이 찬양집) 수록 번호입니다. 해당 성가집에 실리지 않은 곡은 `—`로 표시됩니다.
- **영상**은 ▶ 를 누르면 이 페이지 안에서 바로 재생됩니다(새 탭에서 열려면 Ctrl/⌘ 누른 채 클릭). 링크는 `_data/links.yml`에서 관리합니다.
- 목록은 `_data/scores.yml`에서 자동 생성됩니다(`scripts/gen_scores.py` → `scripts/match_songbooks.py`).

> ⚠️ **저작권 안내**: 본 페이지에는 본인 작곡분(미사곡 · OnE 밴드 곡) 외에 타인 작곡 곡의 코드 차트(ChordChart)/스코어도 포함되어 있습니다. 타인 곡 악보는 **개인 학습·반주용**으로만 사용하시고, 상업적 재배포는 삼가 주세요.

{% assign all = site.data.scores.items %}
{% assign missa = all | where: "category", "missa" %}
{% assign one = all | where: "category", "one" %}
{% assign ccm = all | where: "category", "ccm" %}
{% assign root = all | where: "category", "root" %}
{% assign groups = all | map: "group" | uniq %}

**전체 {{ groups.size }}곡 · {{ all.size }}개 파일** — 미사곡 {{ missa.size }} · OnE {{ one.size }} · CCM {{ ccm.size }} · 기타 {{ root.size }}

---

## 미사곡 (Missa) — 전례 순서별

{% assign part_keys = "kyrie,gloria,responsorial_psalm,gospel_acclamation,prayer_of_faithful,sanctus,mystery,amen,lords_prayer,agnus,doxology,other" | split: "," %}
{% assign part_names = "자비송 (Kyrie),대영광송 (Gloria),화답송 (Responsorial Psalm),복음환호송 (Gospel Acclamation),보편지향기도 (Prayer of the Faithful),거룩하시도다 (Sanctus),신앙의 신비여 (Mystery of Faith),아멘 (Amen),주님의 기도 (Lord's Prayer),하느님의 어린양 (Agnus Dei),마침영광송·주님께 나라와 (Doxology),그 외 전례곡" | split: "," %}

{% for pk in part_keys %}
  {% assign part_name = part_names[forloop.index0] %}
  {% assign part_items = missa | where: "mass_part", pk %}
  {% if part_items.size > 0 %}
    {% assign part_groups = part_items | map: "group" | uniq %}

### {{ part_name }}

| 곡명  | 작곡  | 야훼이레 | 하늘바다 | 악보  | 영상  |
| :-- | :-- | :--: | :--: | :-- | :-- |
{% for g in part_groups -%}
{% assign gi = part_items | where: "group", g -%}
{% assign first = gi[0] -%}
| {{ first.title }} | {% if first.composer %}{{ first.composer }}{% else %}—{% endif %} | {% if first.yahure %}{{ first.yahure }}{% else %}—{% endif %} | {% if first.haneulbada %}{{ first.haneulbada }}{% else %}—{% endif %} | {% for s in gi %}[⬇ {{ s.label }}]({{ s.url | relative_url }}){: download="" }{% unless forloop.last %}<br>{% endunless %}{% endfor %} | {% assign vkey = first.title | remove: " " %}{% assign vmatch = "" %}{% for L in site.data.links.items %}{% assign lkey = L.title | remove: " " %}{% if lkey == vkey %}{% if L.composer == nil or L.composer == "" or L.composer == first.composer %}{% assign vmatch = L %}{% break %}{% endif %}{% endif %}{% endfor %}{% if vmatch != "" %}{% for v in vmatch.videos %}<a class="yt" href="https://www.youtube.com/watch?v={{ v.id }}" data-yt="{{ v.id }}" target="_blank" rel="noopener">▶ {{ v.title }}</a>{% if v.by %}<br><sub>{{ v.by }}</sub>{% endif %}{% unless forloop.last %}<br>{% endunless %}{% endfor %}{% else %}—{% endif %} |
{% endfor %}

  {% endif %}
{% endfor %}

---

## OnE 밴드 (OnE)

{% assign one_groups = one | map: "group" | uniq %}

| 곡명 | 작곡 | 야훼이레 | 하늘바다 | 악보 | 영상 |
|:---|:---|:---:|:---:|:---|:---|
{% for g in one_groups -%}
{% assign gi = one | where: "group", g -%}
{% assign first = gi[0] -%}
| {{ first.title }} | {% if first.composer %}{{ first.composer }}{% else %}—{% endif %} | {% if first.yahure %}{{ first.yahure }}{% else %}—{% endif %} | {% if first.haneulbada %}{{ first.haneulbada }}{% else %}—{% endif %} | {% for s in gi %}[⬇ {{ s.label }}]({{ s.url | relative_url }}){: download="" }{% unless forloop.last %}<br>{% endunless %}{% endfor %} | {% assign vkey = first.title | remove: " " %}{% assign vmatch = "" %}{% for L in site.data.links.items %}{% assign lkey = L.title | remove: " " %}{% if lkey == vkey %}{% if L.composer == nil or L.composer == "" or L.composer == first.composer %}{% assign vmatch = L %}{% break %}{% endif %}{% endif %}{% endfor %}{% if vmatch != "" %}{% for v in vmatch.videos %}<a class="yt" href="https://www.youtube.com/watch?v={{ v.id }}" data-yt="{{ v.id }}" target="_blank" rel="noopener">▶ {{ v.title }}</a>{% if v.by %}<br><sub>{{ v.by }}</sub>{% endif %}{% unless forloop.last %}<br>{% endunless %}{% endfor %}{% else %}—{% endif %} |
{% endfor %}

---

## CCM · 번역곡 (CCM)

{% assign ccm_groups = ccm | map: "group" | uniq %}

| 곡명 | 작곡 | 야훼이레 | 하늘바다 | 악보 | 영상 |
|:---|:---|:---:|:---:|:---|:---|
{% for g in ccm_groups -%}
{% assign gi = ccm | where: "group", g -%}
{% assign first = gi[0] -%}
| {{ first.title }} | {% if first.composer %}{{ first.composer }}{% else %}—{% endif %} | {% if first.yahure %}{{ first.yahure }}{% else %}—{% endif %} | {% if first.haneulbada %}{{ first.haneulbada }}{% else %}—{% endif %} | {% for s in gi %}[⬇ {{ s.label }}]({{ s.url | relative_url }}){: download="" }{% unless forloop.last %}<br>{% endunless %}{% endfor %} | {% assign vkey = first.title | remove: " " %}{% assign vmatch = "" %}{% for L in site.data.links.items %}{% assign lkey = L.title | remove: " " %}{% if lkey == vkey %}{% if L.composer == nil or L.composer == "" or L.composer == first.composer %}{% assign vmatch = L %}{% break %}{% endif %}{% endif %}{% endfor %}{% if vmatch != "" %}{% for v in vmatch.videos %}<a class="yt" href="https://www.youtube.com/watch?v={{ v.id }}" data-yt="{{ v.id }}" target="_blank" rel="noopener">▶ {{ v.title }}</a>{% if v.by %}<br><sub>{{ v.by }}</sub>{% endif %}{% unless forloop.last %}<br>{% endunless %}{% endfor %}{% else %}—{% endif %} |
{% endfor %}

---

## 그 외 악보 (기타)

{% assign root_groups = root | map: "group" | uniq %}

| 곡명 | 작곡 | 야훼이레 | 하늘바다 | 악보 | 영상 |
|:---|:---|:---:|:---:|:---|:---|
{% for g in root_groups -%}
{% assign gi = root | where: "group", g -%}
{% assign first = gi[0] -%}
| {{ first.title }} | {% if first.composer %}{{ first.composer }}{% else %}—{% endif %} | {% if first.yahure %}{{ first.yahure }}{% else %}—{% endif %} | {% if first.haneulbada %}{{ first.haneulbada }}{% else %}—{% endif %} | {% for s in gi %}[⬇ {{ s.label }}]({{ s.url | relative_url }}){: download="" }{% unless forloop.last %}<br>{% endunless %}{% endfor %} | {% assign vkey = first.title | remove: " " %}{% assign vmatch = "" %}{% for L in site.data.links.items %}{% assign lkey = L.title | remove: " " %}{% if lkey == vkey %}{% if L.composer == nil or L.composer == "" or L.composer == first.composer %}{% assign vmatch = L %}{% break %}{% endif %}{% endif %}{% endfor %}{% if vmatch != "" %}{% for v in vmatch.videos %}<a class="yt" href="https://www.youtube.com/watch?v={{ v.id }}" data-yt="{{ v.id }}" target="_blank" rel="noopener">▶ {{ v.title }}</a>{% if v.by %}<br><sub>{{ v.by }}</sub>{% endif %}{% unless forloop.last %}<br>{% endunless %}{% endfor %}{% else %}—{% endif %} |
{% endfor %}

---

## 작곡가별 색인

파일명에 작곡가가 명시된 곡만 표기합니다.

{% assign named = all | where_exp: "s", "s.composer != ''" %}
{% assign composers = named | map: "composer" | uniq | sort %}

| 작곡가 | 수록곡 |
|:---|:---|
{% for c in composers -%}
{% assign cs = named | where: "composer", c -%}
{% assign cg = cs | map: "group" | uniq -%}
| **{{ c }}** ({{ cg.size }}곡) | {% for g in cg %}{% assign gi = cs | where: "group", g %}{{ gi[0].title }}{% unless forloop.last %} · {% endunless %}{% endfor %} |
{% endfor %}

---

## 관련 페이지

- [리소스 자료실 (Resources)](../ccm/Resources.md) — 악보 자료 및 웹사이트 링크
- [미사곡 (Mass)](../ccm/Mass.md)
- [최태형 안셀모 작품 목록](../ccm/songs/TaeHyoungChoi.md)

<script src="{{ '/assets/js/yt-lite.js' | relative_url }}" defer></script>
