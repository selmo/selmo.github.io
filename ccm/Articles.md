# 생활성가·가톨릭 CCM·찬양사도 기사 모음 (Articles)

가톨릭 생활성가와 CCM, 그리고 찬양사도 운동에 관한 언론 기사·평론·논문을 한곳에 모은 페이지입니다. 분류는 출처 성격(매체 종류)에 따랐고, 각 섹션 안에서는 최신순으로 정렬됩니다.

- **데이터 출처**: `_data/articles.yml`
- **수집 기준**: 생활성가, 가톨릭 CCM, 찬양사도([가톨릭찬양사도협회](organizations/index.md#찬양사도-협회--협의회)), 청년 미사·전례음악과 직접 연관된 글
- **표기**: 매체명 + 발행일 + 한두 줄 요약. 외부 링크 클릭 시 원문으로 이동합니다.

{% assign items = site.data.articles.items %}
{% if items == nil or items.size == 0 %}

> _아직 등록된 기사가 없습니다._ `_data/articles.yml`에 항목을 추가하면 이곳에 자동으로 표시됩니다.

{% else %}

{% assign types = "catholic_press,general_press,webzine_blog,academic" | split: "," %}
{% assign type_labels = "가톨릭 언론,일반 언론,회지·웹진·블로그,논문·평론" | split: "," %}

{% for t in types %}
  {% assign type_label = type_labels[forloop.index0] %}
  {% assign group = items | where: "source_type", t | sort: "date" | reverse %}
  {% if group.size > 0 %}

## {{ type_label }} ({{ group.size }})

| 제목 | 매체 | 날짜 | 태그 |
|:---|:---|:---:|:---|
{% for a in group -%}
| {% if a.url %}[{{ a.title }}]({{ a.url }}){% else %}{{ a.title }}{% endif %}{% if a.author %}<br><sub>— {{ a.author }}</sub>{% endif %}{% if a.summary %}<br><sub>{{ a.summary }}</sub>{% endif %}{% unless a.verified %}{% if a.url %} <sub>·날짜 근사</sub>{% endif %}{% endunless %} | {{ a.source }} | {{ a.date }} | {% if a.tags %}{% for tag in a.tags %}`{{ tag }}`{% unless forloop.last %} {% endunless %}{% endfor %}{% endif %} |
{% endfor %}

  {% endif %}
{% endfor %}

{% endif %}

---

## 기여 안내

새 기사를 추가하려면 `_data/articles.yml`의 `items:` 배열에 항목을 더하면 됩니다. 예:

```yaml
items:
  - title: 가톨릭 청년 생활성가 30년, 변화와 과제
    url: https://www.catholictimes.org/article/example
    source: 가톨릭신문
    source_type: catholic_press
    date: 2026-04-15
    author: 김기자
    summary: 1990년대 야훼이레 1판 발행부터 현재까지 한국 가톨릭 청년 음악 운동의 흐름을 정리.
    tags: [생활성가, 청년, 야훼이레]
```

`source_type` 값은 네 가지 중 하나입니다: `catholic_press`, `general_press`, `webzine_blog`, `academic`.
