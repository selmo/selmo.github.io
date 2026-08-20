#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""성가집 수록곡 목록을 성가집별 데이터 파일로 추출.

주의: 번호 필드는 num 이다. YAML 1.1 은 no/yes 를 boolean 으로 읽으므로
     키 이름에 no 를 쓰면 false 로 파싱된다.

성가집마다 파일을 나눈다:
- _data/yahure.yml     <- resources/야훼이레-수록곡목록-3판.xlsx (총괄 시트)
- _data/haneulbada.yml <- resources/하늘바다.md

표시 항목은 번호·곡명·작사/작곡자·구분으로 한정한다(가사는 담지 않는다).
"""
import openpyxl, re, unicodedata, io

XLSX = "resources/야훼이레-수록곡목록-3판.xlsx"
HB_MD = "resources/하늘바다.md"
OUT_YH = "_data/yahure.yml"
OUT_HB = "_data/haneulbada.yml"


def nfc(s):
    return unicodedata.normalize("NFC", str(s)).strip() if s else ""


def esc(v):
    if v is None or v == "":
        return '""'
    if isinstance(v, int):
        return str(v)
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


# 원본 xlsx 에 작사·작곡자가 비어 있는 곡의 보완.
#   value = (author, source)
# source 는 근거. 확실한 것만 넣고, 출처가 엇갈리는 곡은 아래 AUTHOR_DISPUTED 로.
# 원본 xlsx 를 고치면 여기서 지워도 된다.
AUTHOR_FIX = {
    269: ("Edward Shippen Barnes", "프랑스 전통 캐롤 'Angels We Have Heard on High' 편곡"),
}

# 출처가 엇갈려 확정하지 못한 곡. 데이터에는 반영하지 않고 기록만 남긴다.
# 원본 xlsx 를 고칠 때 참고용.
AUTHOR_DISPUTED = {
    632: "아무 것도 너를 — 떼제(자크 베르티에) 설과 김정희 수녀 설이 엇갈림",
}


# ---------- 야훼이레 ----------
def load_yahure():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["총괄"]
    items = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        num = r[1]
        if not isinstance(num, int) or not r[3]:
            continue
        items.append({
            "no": num,
            "title": nfc(r[3]),
            "title_en": nfc(r[4]),
            "author": nfc(r[5]),          # 작사·작곡자
            "season": nfc(r[2]) if isinstance(r[2], str) else "",  # 대림/성탄/사순 …
            "tradition": nfc(r[10]),      # 가톨릭 / 개신교 …
            "first_ed": r[8] if isinstance(r[8], int) else None,   # 1판 번호
        })
    for it in items:
        if not it["author"] and it["no"] in AUTHOR_FIX:
            it["author"], it["author_src"] = AUTHOR_FIX[it["no"]]
    items.sort(key=lambda x: x["no"])
    return items


# ---------- 하늘바다 ----------
def load_haneulbada():
    text = open(HB_MD, encoding="utf-8").read()
    mass, titles = [], {}
    section = part = None
    for ln in text.split("\n"):
        h2 = re.match(r"^##\s+〈(.+?)〉", ln)
        if h2:
            section, part = h2.group(1), None
            continue
        h3 = re.match(r"^###\s+○\s+(.+?)\s*$", ln)
        if h3:
            part = h3.group(1).strip()
            continue
        row2 = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$", ln)
        row4 = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$", ln)

        if section == "미사곡" and part and row2 and not row4:
            mass.append({"no": int(row2.group(1)), "part": part,
                         "author": nfc(row2.group(2))})
        elif section and "제목별" in section and row4:
            a_no, a_t, b_no, b_t = row4.groups()
            titles[int(a_no)] = nfc(a_t)
            titles[int(b_no)] = nfc(b_t)

    mass.sort(key=lambda x: x["no"])
    songs = [{"no": n, "title": t} for n, t in sorted(titles.items())]
    return mass, songs


def norm_title(s):
    """곡명 비교용 정규화 (공백·문장부호 제거)."""
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"[\s·・,\.\'\"’‘“”\(\)\[\]!?~\-—]", "", s).lower()


def fill_from_yahure(hb_songs, yh):
    """하늘바다 원본에는 작곡가가 없다. 곡명이 같은 야훼이레 곡에서 가져온다.
    동명이곡이 있으면 어느 쪽인지 알 수 없으므로 건너뛴다."""
    by_title = {}
    for i in yh:
        if i["author"]:
            by_title.setdefault(norm_title(i["title"]), []).append(i)
    filled = 0
    for s in hb_songs:
        cands = by_title.get(norm_title(s["title"]), [])
        if len(cands) == 1:
            s["author"] = cands[0]["author"]
            s["author_src"] = f"야훼이레 {cands[0]['no']}"
            filled += 1
    return filled


def main():
    yh = load_yahure()
    hb_mass, hb_songs = load_haneulbada()
    filled = fill_from_yahure(hb_songs, yh)

    # ---- 야훼이레 ----
    out = io.StringIO()
    out.write("# 야훼이레 3판 수록곡 (scripts/gen_songbooks.py 로 생성)\n")
    out.write("# 원본: resources/야훼이레-수록곡목록-3판.xlsx (총괄 시트)\n")
    out.write("#\n")
    out.write("# 번호 필드는 num. YAML 1.1 은 no/yes 를 boolean 으로 읽는다.\n")
    out.write("# 번호·곡명·작사/작곡자만 담는다(가사는 포함하지 않는다).\n\n")
    out.write("items:\n")
    for it in yh:
        out.write(f'  - num: {it["no"]}\n')
        out.write(f'    title: {esc(it["title"])}\n')
        if it["title_en"]:
            out.write(f'    title_en: {esc(it["title_en"])}\n')
        out.write(f'    author: {esc(it["author"])}\n')
        if it.get("author_src"):
            out.write(f'    author_src: {esc(it["author_src"])}\n')
        if it["season"]:
            out.write(f'    season: {esc(it["season"])}\n')
        if it["tradition"]:
            out.write(f'    tradition: {esc(it["tradition"])}\n')
        if it["first_ed"]:
            out.write(f'    first_ed: {it["first_ed"]}\n')
    open(OUT_YH, "w", encoding="utf-8").write(out.getvalue())

    # ---- 하늘바다 ----
    out = io.StringIO()
    out.write("# 하늘바다(가톨릭 어린이 찬양집) 수록곡 (scripts/gen_songbooks.py 로 생성)\n")
    out.write("# 원본: resources/하늘바다.md\n")
    out.write("#\n")
    out.write("#   mass  : 미사곡 — 전례 파트별 (번호, 파트, 작곡/편곡)\n")
    out.write("#   songs : 그 외 수록곡 — 번호순\n\n")
    out.write("mass:\n")
    for it in hb_mass:
        out.write(f'  - num: {it["no"]}\n')
        out.write(f'    part: {esc(it["part"])}\n')
        out.write(f'    author: {esc(it["author"])}\n')
    out.write("\nsongs:\n")
    for it in hb_songs:
        out.write(f'  - num: {it["no"]}\n')
        out.write(f'    title: {esc(it["title"])}\n')
        if it.get("author"):
            out.write(f'    author: {esc(it["author"])}\n')
            out.write(f'    author_src: {esc(it["author_src"])}\n')
    open(OUT_HB, "w", encoding="utf-8").write(out.getvalue())

    from collections import Counter
    print(f"야훼이레 {len(yh)}곡 (번호 {yh[0]['no']}–{yh[-1]['no']}) -> {OUT_YH}")
    print("  구분:", dict(Counter(i["tradition"] for i in yh if i["tradition"])))
    blank = [i for i in yh if not i["author"]]
    print(f"  작사/작곡 미상: {len(blank)}곡", end="")
    print(f" (보완 {len(AUTHOR_FIX)}곡 적용)" if AUTHOR_FIX else "")
    if AUTHOR_DISPUTED:
        print("  ※ 출처가 엇갈려 미확정 — 원본 xlsx 확인 필요:")
        for n, why in sorted(AUTHOR_DISPUTED.items()):
            print(f"     {n}: {why}")
    print(f"하늘바다 미사곡 {len(hb_mass)} · 일반곡 {len(hb_songs)} -> {OUT_HB}")
    print(f"  일반곡 작곡가: 야훼이레에서 {filled}곡 채움, "
          f"{len(hb_songs) - filled}곡 미상")


if __name__ == "__main__":
    main()
