#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_data/scores.yml 의 모든 곡을 _data/links.yml 에 자리만 만들어 둔다.

- 이미 links.yml 에 있는 곡의 videos 는 그대로 보존한다(덮어쓰지 않음).
- 새로 추가되는 곡은 videos: [] 로 비워 둔다 -> 나중에 영상 ID만 채우면 된다.
- scores.yml 에서 사라진 곡은 links.yml 에 남겨 두되 주석으로 표시하지 않고
  그대로 둔다(악보가 다시 추가될 수 있고, 링크는 악보와 독립이므로).

정렬은 scores.yml 과 같은 순서(카테고리 -> 미사 파트 -> 작곡가 -> 곡명).
"""
import yaml, io, sys

SCORES = "_data/scores.yml"
LINKS = "_data/links.yml"

CAT_LABEL = {
    "missa": "미사곡",
    "one": "OnE 밴드",
    "ccm": "CCM · 번역곡",
    "root": "그 외",
}
MP_LABEL = {
    "kyrie": "자비송", "gloria": "대영광송", "responsorial_psalm": "화답송",
    "gospel_acclamation": "복음환호송", "prayer_of_faithful": "보편지향기도",
    "sanctus": "거룩하시도다", "mystery": "신앙의 신비여", "amen": "아멘",
    "lords_prayer": "주님의 기도", "agnus": "하느님의 어린양",
    "doxology": "마침영광송·주님께 나라와", "other": "그 외 전례곡",
}


def norm(s):
    return (s or "").replace(" ", "")


def esc(v):
    if v is None:
        return '""'
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def main():
    scores = yaml.safe_load(open(SCORES, encoding="utf-8"))["items"]

    # 기존 links.yml 의 videos 보존: (정규화 제목, 작곡가) -> videos
    existing = {}
    try:
        old = yaml.safe_load(open(LINKS, encoding="utf-8")) or {}
        for L in (old.get("items") or []):
            key = (norm(L.get("title")), L.get("composer") or "")
            if L.get("videos"):
                existing[key] = L["videos"]
    except FileNotFoundError:
        pass

    # scores.yml 의 곡 목록 (group 단위, 등장 순서 유지)
    songs, seen = [], set()
    for it in scores:
        if it["group"] in seen:
            continue
        seen.add(it["group"])
        songs.append(it)

    out = io.StringIO()
    out.write("""# 곡별 영상·음원 링크
#
# scores.yml 의 곡과 (title, composer) 로 연결된다.
#   title    : scores.yml 의 title 과 같은 표기. 공백은 무시하고 비교하므로
#              "주님 제 소리를" 과 "주님제소리를" 은 같은 곡으로 취급된다.
#   composer : 동명이곡 구분용. 비워 두면 제목이 같은 모든 곡에 붙는다.
#
# videos 에 아래 형식으로 채워 넣으면 악보 페이지 '영상' 열에 나타난다.
#   videos:
#     - id: 32Co73wBjxA      # 유튜브 영상 ID — watch?v= 뒤의 11자만
#       title: 마침영광송 아멘 118번
#       by: 캐톨릭 뮤직        # 연주자·채널 (선택)
#       note: 2019년 실황      # 부가 설명 (선택)
#
# videos: [] 인 곡은 아직 영상이 없다는 뜻이며, 페이지에는 '—' 로 표시된다.
#
# 이 파일은 scripts/gen_links.py 로 곡 목록을 갱신할 수 있다.
# (이미 입력된 videos 는 보존되고, 새 곡만 빈 자리로 추가된다)

items:
""")

    cur_cat = cur_mp = None
    for s in songs:
        # 카테고리 / 미사 파트가 바뀌면 구분 주석
        if s["category"] != cur_cat:
            cur_cat = s["category"]
            cur_mp = None
            out.write(f"\n  # ══════ {CAT_LABEL.get(cur_cat, cur_cat)} ══════\n")
        if cur_cat == "missa" and s["mass_part"] != cur_mp:
            cur_mp = s["mass_part"]
            out.write(f"\n  # ── {MP_LABEL.get(cur_mp, cur_mp)} ──\n")

        key = (norm(s["title"]), s["composer"] or "")
        vids = existing.get(key)

        out.write(f'  - title: {esc(s["title"])}\n')
        out.write(f'    composer: {esc(s["composer"])}\n')
        if vids:
            out.write("    videos:\n")
            for v in vids:
                out.write(f'      - id: {esc(v.get("id"))}\n')
                out.write(f'        title: {esc(v.get("title"))}\n')
                if v.get("by"):
                    out.write(f'        by: {esc(v["by"])}\n')
                if v.get("note"):
                    out.write(f'        note: {esc(v["note"])}\n')
        else:
            out.write("    videos: []\n")

    open(LINKS, "w", encoding="utf-8").write(out.getvalue())

    kept = sum(1 for s in songs if existing.get((norm(s["title"]), s["composer"] or "")))
    print(f"곡 {len(songs)}개 기록 · 기존 영상 보존 {kept}곡")
    orphan = set(existing) - {(norm(s["title"]), s["composer"] or "") for s in songs}
    if orphan:
        print("※ scores.yml 에 없어 빠진 항목(영상 데이터 손실 주의):")
        for t, c in sorted(orphan):
            print(f"   - {t} / {c or '(작곡가 없음)'}")


if __name__ == "__main__":
    main()
