---
title: "OnE 악보 다운로드 (Scores)"
---

# OnE 악보 다운로드 (Scores)

OnE 및 관련 작품의 악보(Score · ChordChart · Chorus)를 폴더별로 제공합니다. 각 항목을 클릭하면 PDF가 다운로드됩니다. 아래 목록은 `resources/OnE-Scores/`의 PDF 파일에서 자동 생성됩니다 — 새 악보를 해당 폴더에 추가하면 이 표에 자동으로 표시됩니다.

> ⚠️ **저작권 안내**: 본 페이지에는 본인 작곡분(미사곡 · OnE 밴드 곡) 외에 타인 작곡 곡의 코드 차트(ChordChart)/스코어도 함께 포함되어 있습니다. 타인 곡 악보는 **개인 학습·반주용**으로만 다운로드·사용하시고, 상업적 재배포는 삼가 주세요.

{% comment %} OnE-Scores 경로의 PDF만 추출하여 폴더별로 분류 {% endcomment %}
{% assign all_pdfs = site.static_files | where_exp: "f", "f.extname == '.pdf'" | where_exp: "f", "f.path contains 'OnE-Scores'" %}

{% assign missa = "" | split: "" %}
{% assign one = "" | split: "" %}
{% assign ccm = "" | split: "" %}
{% assign root = "" | split: "" %}
{% for f in all_pdfs %}
  {% if f.path contains '/OnE-Scores/Missa/' %}{% assign missa = missa | push: f %}
  {% elsif f.path contains '/OnE-Scores/OnE/' %}{% assign one = one | push: f %}
  {% elsif f.path contains '/OnE-Scores/CCM/' %}{% assign ccm = ccm | push: f %}
  {% else %}{% assign root = root | push: f %}
  {% endif %}
{% endfor %}

{% assign missa = missa | sort: "name" %}
{% assign one = one | sort: "name" %}
{% assign ccm = ccm | sort: "name" %}
{% assign root = root | sort: "name" %}

**전체 {{ all_pdfs.size }}곡** · 미사곡 {{ missa.size }} · OnE {{ one.size }} · CCM {{ ccm.size }} · 기타 {{ root.size }}

## 미사곡 (Missa)

{% if missa.size > 0 %}
| 악보 | 다운로드 |
|:---|:---:|
{% for f in missa -%}
| {{ f.basename }} | [⬇ PDF]({{ f.path | relative_url }}){: download="" } |
{% endfor %}
{% else %}_등록된 악보가 없습니다._{% endif %}

## OnE 밴드 (OnE)

{% if one.size > 0 %}
| 악보 | 다운로드 |
|:---|:---:|
{% for f in one -%}
| {{ f.basename }} | [⬇ PDF]({{ f.path | relative_url }}){: download="" } |
{% endfor %}
{% else %}_등록된 악보가 없습니다._{% endif %}

## CCM · 번역곡 (CCM)

{% if ccm.size > 0 %}
| 악보 | 다운로드 |
|:---|:---:|
{% for f in ccm -%}
| {{ f.basename }} | [⬇ PDF]({{ f.path | relative_url }}){: download="" } |
{% endfor %}
{% else %}_등록된 악보가 없습니다._{% endif %}

## 일반 악보 (기타)

{% if root.size > 0 %}
| 악보 | 다운로드 |
|:---|:---:|
{% for f in root -%}
| {{ f.basename }} | [⬇ PDF]({{ f.path | relative_url }}){: download="" } |
{% endfor %}
{% else %}_등록된 악보가 없습니다._{% endif %}

---

## 관련 페이지

- [리소스 자료실 (Resources)](../ccm/Resources.md) — 악보 자료 및 웹사이트 링크
- [미사곡 (Mass)](../ccm/Mass.md)
- [최태형 안셀모 작품 목록](../ccm/songs/TaeHyoungChoi.md)