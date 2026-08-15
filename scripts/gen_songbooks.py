#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""성가집 수록곡 목록을 _data/songbooks.yml 로 추출.

주의: 번호 필드는 num 이다. YAML 1.1 은 no/yes 를 boolean 으로 읽으므로
     키 이름에 no 를 쓰면 false 로 파싱된다.

- 야훼이레 3판: resources/야훼이레-수록곡목록-3판.xlsx (총괄 시트)
- 하늘바다(가톨릭 어린이 찬양집): resources/하늘바다.md

표시 항목은 번호·곡명·작사/작곡자·구분으로 한정한다(가사는 담지 않는다).
"""
import openpyxl, re, unicodedata, io

XLSX = "resources/야훼이레-수록곡목록-3판.xlsx"
HB_MD = "resources/하늘바다.md"
OUT = "_data/songbooks.yml"


def nfc(s):
    return unicodedata.normalize("NFC", str(s)).strip() if s else ""


def esc(v):
    if v is None or v == "":
        return '""'
    if isinstance(v, int):
        return str(v)
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


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


def main():
    yh = load_yahure()
    hb_mass, hb_songs = load_haneulbada()

    out = io.StringIO()
    out.write("# 성가집 수록곡 목록 (scripts/gen_songbooks.py 로 생성)\n")
    out.write("#\n")
    out.write("#   yahure     : 야훼이레 3판 — resources/야훼이레-수록곡목록-3판.xlsx\n")
    out.write("#   haneulbada : 하늘바다(가톨릭 어린이 찬양집) — resources/하늘바다.md\n")
    out.write("#\n")
    out.write("# 번호·곡명·작사/작곡자만 담는다(가사는 포함하지 않는다).\n\n")

    out.write("yahure:\n")
    for it in yh:
        out.write(f'  - num: {it["no"]}\n')
        out.write(f'    title: {esc(it["title"])}\n')
        if it["title_en"]:
            out.write(f'    title_en: {esc(it["title_en"])}\n')
        out.write(f'    author: {esc(it["author"])}\n')
        if it["season"]:
            out.write(f'    season: {esc(it["season"])}\n')
        if it["tradition"]:
            out.write(f'    tradition: {esc(it["tradition"])}\n')
        if it["first_ed"]:
            out.write(f'    first_ed: {it["first_ed"]}\n')

    out.write("\nhaneulbada_mass:\n")
    for it in hb_mass:
        out.write(f'  - num: {it["no"]}\n')
        out.write(f'    part: {esc(it["part"])}\n')
        out.write(f'    author: {esc(it["author"])}\n')

    out.write("\nhaneulbada_songs:\n")
    for it in hb_songs:
        out.write(f'  - num: {it["no"]}\n')
        out.write(f'    title: {esc(it["title"])}\n')

    open(OUT, "w", encoding="utf-8").write(out.getvalue())

    from collections import Counter
    print(f"야훼이레 {len(yh)}곡 (번호 {yh[0]['no']}–{yh[-1]['no']})")
    print("  구분:", dict(Counter(i["tradition"] for i in yh if i["tradition"])))
    print(f"하늘바다 미사곡 {len(hb_mass)} · 일반곡 {len(hb_songs)}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
