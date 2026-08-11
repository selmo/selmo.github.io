---
title: "아티스트 및 작곡가 (Artists & Composers)"
---

# 아티스트 및 작곡가 (Artists & Composers)

가톨릭 성가 및 CCM 작곡가들에 대한 정보입니다. 아래 목록은 `_data/artists.yml`에서 자동 생성됩니다 — 새 아티스트는 YAML에 항목을 추가하면 자동으로 표시됩니다.

{% assign artists = site.data.artists.items %}
{% assign koreans = artists | where: "category", "korean" %}
{% assign mass = artists | where: "category", "mass_composer" %}
{% assign reps = artists | where: "category", "representative" %}
{% assign taize = artists | where: "category", "taize_focolare" %}
{% assign ecumenical = artists | where: "category", "ecumenical" %}
{% assign folk = artists | where: "category", "folk" %}

## 한국 가톨릭 작곡가 (Korean Catholic Composers)

{% for a in koreans %}
* {% if a.file %}**[{{ a.name_ko }} ({{ a.name_en }})]({{ a.file }}.md)**{% else %}**{{ a.name_ko }}** ({{ a.name_en }}){% endif %}
  {% if a.description %}* {{ a.description }}{% endif %}{% if a.works %} 대표곡: {{ a.works }}{% endif %}
{% endfor %}

## 해외 가톨릭 아티스트 (Global Catholic Artists)

### 미사곡 작곡가 (Mass Setting Composers)

{% for a in mass %}
* **[{{ a.name_ko }} ({{ a.name_en }})]({{ a.file }}.md)**
  * {{ a.description }}
{% endfor %}

### 대표곡 중심 아티스트

{% for a in reps %}
* **[{{ a.name_ko }} ({{ a.name_en }})]({{ a.file }}.md)**
  {% if a.description %}* {{ a.description }}{% endif %}{% if a.works %} 대표곡: {{ a.works }}{% endif %}
{% endfor %}

## 떼제 & 포콜라레 (Taizé & Focolare)

{% for a in taize %}
* **[{{ a.name_ko }} ({{ a.name_en }})]({{ a.file }}.md)**
  * {{ a.description }}
{% endfor %}

## 에큐메니칼 & 현대 워십 (Ecumenical & Modern Worship)

야훼이레 성가집에 수록된, 가톨릭 전례에서도 자주 불리는 개신교 및 에큐메니칼 아티스트들입니다.

{% for a in ecumenical %}
* {% if a.file %}**[{{ a.name_ko }} ({{ a.name_en }})]({{ a.file }}.md)**{% else %}**{{ a.name_ko }}** ({{ a.name_en }}){% endif %}{% if a.works %} ('{{ a.works }}'){% endif %}
{% endfor %}

## 포크 & 기타 (Folk & Others)

{% for a in folk %}
* **[{{ a.name_ko }} ({{ a.name_en }})]({{ a.file }}.md)**
  * 대표곡: {{ a.works }}
{% endfor %}

---

**관련 페이지**:
* [최태형 안셀모 작품 목록](../songs/TaeHyoungChoi.md)
* [곡 정보 및 해설 (Songs)](../songs/index.md)
* [한국청년대회 (Korea Youth Day, KYD)](../organizations/KoreaYouthDay.md)
* [청소년 주일](../organizations/KoreanYouthSunday.md)
* [젊은이 성령축제 HYD](../organizations/HolyspiritYouthDay.md)
* [청소년·대학생·국제행사 가이드](../organizations/YouthAndYoungAdultGuide.md)
* [청소년·청년 운동 비교표](../organizations/YouthMovementsComparison.md)
* [청소년·청년 운동과 레퍼토리 대응표](../organizations/YouthRepertoireMap.md)