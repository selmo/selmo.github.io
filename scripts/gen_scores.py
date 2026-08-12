#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resources/OnE-Scores PDF -> _data/scores.yml 메타데이터 생성.
- path: 파일 시스템 원본(NFD 포함) 그대로 -> relative_url 링크 안전.
- title/composer/mass_part/note: 정제. 작곡가는 파일명에 명시된 경우만.
- group: "{category}-{공백제거 title}-{composer}" 자동 부여 -> 같은 곡 변형이 한 줄에 묶임.
"""
import os, re, unicodedata
from urllib.parse import quote

ROOT = "resources/OnE-Scores"

# 작곡가 후보 (파일명에 명시되는 이름)
COMPOSERS = ["신상옥", "현정수", "최태형", "이종철", "윤남근", "신지은", "이지혜",
             "김용휘", "박정선"]

# 미사 파트 키워드 -> mass_part
MASS_PART_RULES = [
    (r"주님저희에게자비를|주님 저희에게 자비를", "responsorial_psalm"),
    (r"자비송", "kyrie"),
    (r"대영광송", "gloria"),
    (r"복음환호송", "gospel_acclamation"),
    (r"화답송", "responsorial_psalm"),
    (r"신앙의?신비여", "mystery"),
    (r"거룩하시도다", "sanctus"),
    (r"하느님의?어린양", "agnus"),
    (r"주님의?기도|주님의기도", "lords_prayer"),
    (r"주님께나라와", "kingdom"),
    (r"마침영광송", "doxology"),
    (r"보편지향기도", "prayer_of_faithful"),
    (r"아멘", "amen"),
]

# Missa/ 아래 하위 폴더명 -> mass_part (파일명 키워드보다 우선)
# 새 폴더를 만들면 여기에 한 줄 추가하면 된다. 미등록 폴더는 파일명 규칙으로 넘어간다.
FOLDER_PART_MAP = {
    "자비송": "kyrie",
    "대영광송": "gloria",
    "화답송": "responsorial_psalm",
    "복음환호송": "gospel_acclamation",
    "보편지향기도": "prayer_of_faithful",
    "거룩하시도다": "sanctus",
    "신앙의 신비여": "mystery",
    "신앙의신비여": "mystery",
    "아멘": "amen",
    "주님의 기도": "lords_prayer",
    "주님의기도": "lords_prayer",
    "하느님의 어린양": "agnus",
    "하느님의어린양": "agnus",
    "주님께 나라와": "kingdom",
    "주님께나라와": "kingdom",
    "마침영광송": "doxology",
    "영광송": "doxology",
    "성호경": "sign_of_cross",
    "사도신경": "creed",
    "평화의 인사": "peace",
    "평화의인사": "peace",
    "거양성체": "elevation",
}

# --- 하드코딩 보정 (basename NFC -> {title, composer, mass_part, note, yahure}) ---
# 자동 추출로 부정확한 케이스만. key 는 NFC basename.
CORRECTIONS = {
    # 미사 — 복합/특수
    "신앙의신비여+아멘.pdf": dict(title="신앙의 신비여", composer="최태형", mass_part="mystery", note="아멘 포함"),
    "신앙의신비여(107).pdf": dict(title="신앙의 신비여", composer="최태형", mass_part="mystery"),
    "주님께나라와+하느님의어린양 [신상옥].pdf": dict(title="주님께 나라와", composer="신상옥", mass_part="kingdom", note="하느님의 어린양 포함"),
    "주님께나라와 - 신상옥.pdf": dict(title="주님께 나라와", composer="신상옥", mass_part="kingdom"),
    "복음환호송 + 보편지향기도.pdf": dict(title="복음환호송 + 보편지향기도", composer="", mass_part="gospel_acclamation", note="보편지향기도 포함"),
    "복음환호송-20240704.pdf": dict(title="복음환호송", composer="", mass_part="gospel_acclamation", note="2024-07-04"),
    "복음환호송(9월18일).pdf": dict(title="복음환호송", composer="", mass_part="gospel_acclamation", note="9월 18일"),
    "주님의기도 - 신지은,이지혜.pdf": dict(title="주님의 기도", composer="신지은·이지혜", mass_part="lords_prayer"),
    "주님의기도 (이종철, 어린이미사).pdf": dict(title="주님의 기도", composer="이종철", mass_part="lords_prayer", note="어린이미사"),
    "주님의기도-주님께나라와 [최태형,야훼이레131].pdf": dict(title="주님의 기도", composer="최태형", mass_part="lords_prayer", yahure=131, note="주님께 나라와"),
    "주님의기도-주님께나라와[최태형].pdf": dict(title="주님의 기도", composer="최태형", mass_part="lords_prayer", note="주님께 나라와"),
    "마침영광송-아멘 [최태형,야훼이레118].pdf": dict(title="마침영광송", composer="최태형", mass_part="doxology", yahure=118, note="아멘 포함"),
    "보편지향기도 (어린이미사).pdf": dict(title="보편지향기도", composer="", mass_part="prayer_of_faithful", note="어린이미사"),
    "화답송 - 주님저희에게자비를.pdf": dict(title="화답송 '주님 저희에게 자비를'", composer="", mass_part="responsorial_psalm"),
    "주님저희에게자비를.pdf": dict(title="주님 저희에게 자비를", composer="", mass_part="responsorial_psalm"),
    "삼위일체.pdf": dict(title="삼위일체", composer="", mass_part="other"),
    "오소서성령님저희마음을가득채우시어저희안에사랑의불이타오르게하소서.pdf": dict(title="오소서 성령님", composer="", mass_part="other"),
    "아멘.pdf": dict(title="아멘", composer="", mass_part="amen"),
    # 미사 — 자동 추출로 충분하나 title 띄어쓰기 통일
    "자비송 [신상옥].pdf": dict(title="자비송", composer="신상옥", mass_part="kyrie"),
    "자비송 [최태형,야훼이레9].pdf": dict(title="자비송", composer="최태형", mass_part="kyrie", yahure=9),
    "대영광송 - 신상옥.pdf": dict(title="대영광송", composer="신상옥", mass_part="gloria"),
    "대영광송 [최태형,야훼이레31].pdf": dict(title="대영광송", composer="최태형", mass_part="gloria", yahure=31),
    "신앙의 신비여 [현정수].pdf": dict(title="신앙의 신비여", composer="현정수", mass_part="mystery"),
    "신앙의 신비여 (신상옥).pdf": dict(title="신앙의 신비여", composer="신상옥", mass_part="mystery"),
    "신앙의신비여 [최태형,야훼이레107].pdf": dict(title="신앙의 신비여", composer="최태형", mass_part="mystery", yahure=107),
    "거룩하시도다 - 신상옥 [075].pdf": dict(title="거룩하시도다", composer="신상옥", mass_part="sanctus", yahure=75),
    "거룩하시도다 [최태형,야훼이레81].pdf": dict(title="거룩하시도다", composer="최태형", mass_part="sanctus", yahure=81),
    "하느님의어린양 - 신상옥 [165].pdf": dict(title="하느님의 어린양", composer="신상옥", mass_part="agnus", yahure=165),
    "하느님의어린양 [최태형,야훼이레170].pdf": dict(title="하느님의 어린양", composer="최태형", mass_part="agnus", yahure=170),
    "하느님의어린양 [최태형][170].pdf": dict(title="하느님의 어린양", composer="최태형", mass_part="agnus", yahure=170),
    # OnE
    "주의사랑과권능으로.pdf": dict(title="주의 사랑과 권능으로", composer="윤남근"),
    "나일어나.pdf": dict(title="나 일어나", composer="Mike Ash"),
    "나 일어나.pdf": dict(title="나 일어나", composer="Mike Ash"),
    "돌아가리라.pdf": dict(title="돌아가리라", composer="Bill Batstone"),
    # OnE — 김용휘 작곡
    "기적.pdf": dict(title="기적", composer="김용휘"),
    "처음과 같이.pdf": dict(title="처음과 같이", composer="김용휘"),
    "처음과같이.pdf": dict(title="처음과 같이", composer="김용휘"),
    # OnE — 박정선 작곡
    "나의하루.pdf": dict(title="나의 하루", composer="박정선"),
    "나의 하루.pdf": dict(title="나의 하루", composer="박정선"),
    # OnE — 최태형 작곡 (파일명에 작곡가 미표기, 작곡자 확인분)
    "섬-DAY!.pdf": dict(title="섬-DAY!", composer="최태형"),
    "나의 기도가 이루어질 때.pdf": dict(title="나의 기도가 이루어질 때", composer="최태형"),
    "내 영혼아 주님을.pdf": dict(title="내 영혼아 주님을", composer="최태형"),
    "봉헌합니다.pdf": dict(title="봉헌합니다", composer="최태형"),
    "일상.pdf": dict(title="일상", composer="최태형"),
    "주님당신께맡기나이다.pdf": dict(title="주님 당신께 맡기나이다", composer="최태형"),
    "주님제소리를들으소서.pdf": dict(title="주님 제 소리를 들으소서", composer="최태형"),
    "주님 제 소리를 들으소서.pdf": dict(title="주님 제 소리를 들으소서", composer="최태형"),
    "주님평화안에서.pdf": dict(title="주님 평화 안에서", composer="최태형"),
    "하나되게 하소서.pdf": dict(title="하나되게 하소서", composer="최태형"),
    "하나되어.pdf": dict(title="하나되어", composer="최태형"),
    # CCM — title 띄어쓰기 / note
    "주품에 816 - Full Score.pdf": dict(title="주품에 품으소서", yahure=816),
    "우리를 위해 [We are the reason].pdf": dict(title="우리를 위해", note="We are the reason"),
    "주님사랑노래해(Testify to love).pdf": dict(title="주님 사랑 노래해", note="Testify to love"),
    "주없이살수없네(Can't live a day).pdf": dict(title="주 없이 살 수 없네", note="Can't live a day"),
    "호산나 (Hosanna).pdf": dict(title="호산나", note="Hosanna"),
    "내가천사의말한다해도 (with Piano).pdf": dict(title="내가 천사의 말한다 해도", note="with Piano"),
    "약할때강함되시네 648 - Full Score.pdf": dict(title="약할 때 강함 되시네", yahure=648),
    "내이름아시죠 [야훼이레,450].pdf": dict(title="내 이름 아시죠", yahure=450),
    "나의모습나의소유 [야훼이레,416].pdf": dict(title="나의 모습 나의 소유", yahure=416),
    "말씀하시면 [야훼이레, 514].pdf": dict(title="말씀하시면", yahure=514),
    "내맘에오시는주.pdf": dict(title="내 맘에 오시는 주"),
    "이시간너의맘속에.pdf": dict(title="이 시간 너의 맘속에"),
    "이시간너의맘속에 [야훼이레710] - Full Score.pdf": dict(title="이 시간 너의 맘속에", yahure=710),
    "나의가장낮은마음 [412].pdf": dict(title="나의 가장 낮은 마음", yahure=412),
    "나의가장낮은마음 [야훼이레412] - Full Score.pdf": dict(title="나의 가장 낮은 마음", yahure=412),
    "사랑은하느님에게서오는것이니.pdf": dict(title="사랑은 하느님에게서 오는 것이니"),
    "사랑은하느님에게서오는것이니 - Full Score.pdf": dict(title="사랑은 하느님에게서 오는 것이니"),
    "사랑한다는말은.pdf": dict(title="사랑한다는 말은"),
    "사랑한다는말은(1page) - Full Score.pdf": dict(title="사랑한다는 말은", note="1page"),
    "아버지뜻대로 [야훼이레633] - Full Score.pdf": dict(title="아버지 뜻대로", yahure=633),
    "야곱의축복.pdf": dict(title="야곱의 축복"),
    "야곱의축복 [야훼이레640] - Full Score.pdf": dict(title="야곱의 축복", yahure=640),
    "오주여나의마음이.pdf": dict(title="오 주여 나의 마음이"),
    "오주여나의마음이(1page) - Full Score.pdf": dict(title="오 주여 나의 마음이", note="1page"),
    "주님은나의목자[야훼이레768] - Full Score.pdf": dict(title="주님은 나의 목자", yahure=768),
    "주품에품으소서.pdf": dict(title="주품에 품으소서"),
    "주여 나를 받으소서 [야훼이레, 797] - Full Score.pdf": dict(title="주여 나를 받으소서", yahure=797),
    "오셔서다스리소서.pdf": dict(title="오셔서 다스리소서"),
    # (OnE 곡의 제목 정제·작곡가 지정은 모두 위 OnE 블록에 모아둠 — 여기서 중복 지정 금지)
    # 루트
    "주여나를받으소서 [야훼이레, 797].pdf": dict(title="주여 나를 받으소서", yahure=797),
    "글로리아높으신이의탄생.pdf": dict(title="글로리아 높으신 이의 탄생"),
    "그분께로한걸음씩.pdf": dict(title="그분께로 한 걸음씩"),
    "아름다운세상.pdf": dict(title="아름다운 세상"),
    "하느님의말씀은.pdf": dict(title="하느님의 말씀은"),
    "주님달링주님허니.pdf": dict(title="주님 달링 주님 허니"),
    # 재배치 후 파일명 (- Full Score 접미사가 빠진 형태)
    "나의가장낮은마음 [야훼이레412].pdf": dict(title="나의 가장 낮은 마음", yahure=412),
    "나의모습나의소유 [야훼이레416].pdf": dict(title="나의 모습 나의 소유", yahure=416),
    "사랑한다는말은(1page).pdf": dict(title="사랑한다는 말은", note="1page"),
    "오주여나의마음이(1page).pdf": dict(title="오 주여 나의 마음이", note="1page"),
    "이시간너의맘속에 [야훼이레710].pdf": dict(title="이 시간 너의 맘속에", yahure=710),
    "주님은나의목자[야훼이레768].pdf": dict(title="주님은 나의 목자", yahure=768),
    "야곱의축복 [야훼이레640].pdf": dict(title="야곱의 축복", yahure=640),
    "주여 나를 받으소서 [야훼이레797].pdf": dict(title="주여 나를 받으소서", yahure=797),
    # Eres Tu — 번안하여 '주님의 기도'로 불린다 (야훼이레 129, Juan Carlos Calderon)
    "Eres Tu [Bass].pdf": dict(title="주님의 기도", composer="Juan Carlos Calderon",
                               mass_part="lords_prayer", yahure=129, note="Eres Tu 번안"),
    "Eres Tu.pdf": dict(title="주님의 기도", composer="Juan Carlos Calderon",
                        mass_part="lords_prayer", yahure=129, note="Eres Tu 번안"),
}

def category_of(rel):
    if "/Missa/" in rel: return "missa"
    if "/OnE/" in rel: return "one"
    if "/CCM/" in rel: return "ccm"
    return "root"

def subdir_of(rel):
    """카테고리 폴더(Missa/OnE/CCM) 바로 아래의 하위 폴더명. 없으면 "".

    resources/OnE-Scores/Missa/화답송/foo.pdf -> "화답송"
    resources/OnE-Scores/Missa/foo.pdf        -> ""
    """
    parts = rel.replace(os.sep, "/").split("/")
    try:
        i = parts.index("OnE-Scores")
    except ValueError:
        return ""
    rest = parts[i + 1:-1]          # 카테고리 폴더부터 파일 직전까지
    return rest[1] if len(rest) >= 2 else ""

def type_of(bn):
    if bn.startswith("[Score]"): return "score"
    if bn.startswith("[ChordChart]"): return "chordchart"
    if bn.startswith("[Chorus]"): return "chorus"
    return "score"

def mass_part_of(nfc_bn, subdir=""):
    """미사 파트 판정. 폴더명(subdir)이 파트를 지정하면 그것이 우선.

    Missa/ 아래 하위 폴더명은 작성자가 명시한 분류이므로 파일명 키워드보다 신뢰도가 높다
    (예: 화답송/[Score] 내 영혼아 주님을.pdf — 파일명에 파트 키워드가 없음).
    """
    if subdir:
        part = FOLDER_PART_MAP.get(unicodedata.normalize("NFC", subdir).strip())
        if part:
            return part
    for pat, part in MASS_PART_RULES:
        if re.search(pat, nfc_bn):
            return part
    return ""

def strip_prefix(bn):
    s = bn
    for pfx in ["[Score][미사곡] ", "[Score][미사곡]", "[Score] ", "[Score]",
                "[ChordChart] ", "[ChordChart]", "[Chorus] ", "[Chorus]",
                "[미사곡] ", "[미사곡]"]:
        if s.startswith(pfx):
            s = s[len(pfx):]
            break
    return s

def extract_yahure(bn):
    m = re.search(r"야훼이레\s*,?\s*(\d{1,4})", bn)
    if m: return int(m.group(1))
    m = re.search(r"\[(\d{2,4})\]", bn)
    if m: return int(m.group(1))
    m = re.search(r"\s(\d{3})\s", bn)
    if m: return int(m.group(1))
    return None

def extract_key(bn):
    m = re.search(r"\(([^)]*Key)\)", bn)
    if m: return m.group(1)
    if "[Bass]" in bn: return "Bass"
    m = re.search(r"Full Score\(([EG])\)", bn)
    if m: return m.group(1)
    return ""

def extract_composer(bn):
    s = strip_prefix(bn)
    # [작곡가,야훼이레NN] 또는 [작곡가]
    m = re.search(r"\[([가-힣]{2,5})(?:\s*,\s*야훼이레\s*\d+)?\]", s)
    if m and m.group(1) in COMPOSERS:
        return m.group(1)
    # - 작곡가 (뒤에 [번호], 공백, (, 끝)
    m = re.search(r"-\s*([가-힣]{2,5})(?=\s|$|\[|\()", s)
    if m and m.group(1) in COMPOSERS:
        return m.group(1)
    # (작곡가 ...) 괄호
    m = re.search(r"\(([가-힣]{2,5})(?:,\s*[가-힣]+)?\s*(?:,\s*)?\)", s)
    if m and m.group(1) in COMPOSERS:
        return m.group(1)
    return ""

def clean_title(bn):
    s = strip_prefix(bn)
    s = re.sub(r"\.pdf$", "", s)
    # 작곡가/야훼이레 괄호 블록 제거
    s = re.sub(r"\s*\[[^\]]*\]\s*", " ", s)
    # - 작곡가
    s = re.sub(r"\s*-\s*(신상옥|현정수|최태형|이종철|윤남근)\s*", " ", s)
    # (부가정보) 제거
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s)
    # Full Score / 1page 접미사
    s = re.sub(r"\s*-\s*Full Score\s*", " ", s)
    s = re.sub(r"\s*\(1page\)\s*", " ", s)
    # 날짜/번호 잔여
    s = re.sub(r"\s*-\s*\d{8}\s*", " ", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s

def extract_note(bn):
    notes = []
    if "어린이미사" in bn: notes.append("어린이미사")
    if "Testify to love" in bn: notes.append("Testify to love")
    if "We are the reason" in bn: notes.append("We are the reason")
    if "Can't live a day" in bn: notes.append("Can't live a day")
    if "Hosanna" in bn: notes.append("Hosanna")
    if "with Piano" in bn: notes.append("with Piano")
    if "(1page)" in bn: notes.append("1page")
    if "Full Score" in bn and not re.search(r"Full Score\([EG]\)", bn):
        pass  # Full Score 자체는 note 아님
    return ", ".join(notes)

def py_escape(v):
    if v is None: return "null"
    if isinstance(v, int): return str(v)
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'

items = []
for root, dirs, files in os.walk(ROOT):
    dirs.sort()
    for f in sorted(files):
        if not f.endswith(".pdf"): continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, ".")
        bn = f
        nfc_bn = unicodedata.normalize("NFC", bn)
        cat = category_of(rel)
        typ = type_of(nfc_bn)
        # Missa/ 아래 하위 폴더명 (예: "화답송") — 파트 분류의 1순위 근거
        subdir = subdir_of(rel)
        folder_part = FOLDER_PART_MAP.get(unicodedata.normalize("NFC", subdir)) if subdir else None
        # 기본 자동 추출 — 반드시 NFC 정규화한 이름으로 한다.
        # macOS 파일시스템은 한글을 NFD(자소 분리)로 저장하기도 하는데, 그대로 쓰면
        # 정규식·CORRECTIONS 매칭이 모두 빗나가 제목이 정제되지 않은 채로 남는다.
        # (path/url 은 실제 파일 접근에 쓰이므로 원본 그대로 유지)
        title = clean_title(nfc_bn)
        composer = extract_composer(nfc_bn)
        yahure = extract_yahure(nfc_bn)
        key = extract_key(nfc_bn)
        mass_part = mass_part_of(nfc_bn, subdir) if cat == "missa" else ""
        note = extract_note(nfc_bn)
        # 하드코딩 보정 (키 = 접두사 제거한 NFC basename)
        corr = CORRECTIONS.get(strip_prefix(nfc_bn))
        if corr:
            title = corr.get("title", title)
            composer = corr.get("composer", composer)
            mass_part = corr.get("mass_part", mass_part)
            if "yahure" in corr: yahure = corr["yahure"]
            if "note" in corr: note = corr["note"]
        # 폴더 분류는 파일명 규칙·CORRECTIONS 어느 쪽보다 우선 (작성자가 직접 지정한 것)
        if folder_part:
            mass_part = folder_part
        # 그룹: 같은 카테고리 내 같은 곡(제목+작곡가) -> 같은 group
        group_key = re.sub(r"\s+", "", title)
        group = f"{cat}-{group_key}-{composer}"
        # 링크 라벨: 같은 곡의 변형을 구분 (Score / ChordChart / Chorus + 키·비고)
        base_label = {"score": "Score", "chordchart": "ChordChart", "chorus": "Chorus"}[typ]
        extras = []
        if key: extras.append(key)
        if "Full Score" in nfc_bn: extras.append("Full")
        if note and note not in ("어린이미사",): extras.append(note)
        label = base_label + (" · " + " · ".join(extras) if extras else "")

        # 마크다운 링크용 URL: 공백/대괄호/한글 퍼센트 인코딩 (경로 구분자 / 는 보존)
        url = "/" + quote(rel, safe="/")

        # 표시용 텍스트 필드는 NFC 로 못박는다 (path/url 은 파일 접근용이라 원본 유지)
        nfc = lambda x: unicodedata.normalize("NFC", x) if isinstance(x, str) else x

        items.append({
            "path": rel, "url": url,
            "title": nfc(title), "composer": nfc(composer),
            "category": cat, "mass_part": mass_part, "type": typ,
            "yahure": yahure, "key": nfc(key), "note": nfc(note),
            "group": nfc(group), "label": nfc(label),
        })

CAT_ORDER = {"missa": 0, "one": 1, "ccm": 2, "root": 3}
# 미사 전례 순서. 마침영광송(doxology)은 성찬기도를 맺는 자리라
# 신앙의 신비여 다음·주님의 기도 앞에 오고, '주님께 나라와'(kingdom)는
# 주님의 기도에 이어지는 별개 항목이다.
MP_ORDER = {"kyrie":0,"gloria":1,"responsorial_psalm":2,"gospel_acclamation":3,
            "prayer_of_faithful":4,"sanctus":5,"mystery":6,"doxology":7,"amen":8,
            "lords_prayer":9,"kingdom":10,"agnus":11,"other":12}
TYPE_ORDER = {"score": 0, "chordchart": 1, "chorus": 2}
items.sort(key=lambda x: (
    CAT_ORDER.get(x["category"], 9),
    MP_ORDER.get(x["mass_part"], 99) if x["mass_part"] else 99,
    (0, x["composer"]) if x["composer"] else (1, ""),
    x["group"],
    TYPE_ORDER.get(x["type"], 9),
))

# 같은 group 안에서 라벨이 중복되면 번호 부여 (Score, Score 2, Score 3 …)
from collections import defaultdict
_by_group = defaultdict(list)
for it in items:
    _by_group[it["group"]].append(it)
for grp in _by_group.values():
    counts = defaultdict(int)
    totals = defaultdict(int)
    for it in grp:
        totals[it["label"]] += 1
    for it in grp:
        if totals[it["label"]] > 1:
            counts[it["label"]] += 1
            if counts[it["label"]] > 1:
                it["label"] = f'{it["label"]} {counts[it["label"]]}'

with open("_data/scores.yml", "w", encoding="utf-8") as out:
    out.write("# OnE-Scores PDF 메타데이터\n")
    out.write("# path = 파일 시스템 원본(NFD 포함 그대로). title/composer/mass_part/group/note 정제됨.\n")
    out.write("# group 이 같으면 같은 곡의 변형(Score/ChordChart/Chorus/키) -> 한 줄에 여러 링크.\n")
    out.write("items:\n")
    for it in items:
        out.write(f'  - path: {py_escape(it["path"])}\n')
        out.write(f'    url: {py_escape(it["url"])}\n')
        out.write(f'    title: {py_escape(it["title"])}\n')
        out.write(f'    composer: {py_escape(it["composer"])}\n')
        out.write(f'    category: {it["category"]}\n')
        out.write(f'    mass_part: {py_escape(it["mass_part"])}\n')
        out.write(f'    type: {it["type"]}\n')
        out.write(f'    yahure: {py_escape(it["yahure"])}\n')
        out.write(f'    key: {py_escape(it["key"])}\n')
        out.write(f'    note: {py_escape(it["note"])}\n')
        out.write(f'    group: {py_escape(it["group"])}\n')
        out.write(f'    label: {py_escape(it["label"])}\n')

# 요약
from collections import Counter
print("총", len(items), "파일")
print("category:", dict(Counter(i["category"] for i in items)))
print("mass_part:", dict(Counter(i["mass_part"] for i in items if i["mass_part"])))
print("composer(명시):", dict(Counter(i["composer"] for i in items if i["composer"])))
print("group 수(고유 곡):", len(set(i["group"] for i in items)))
print("---작곡가 비어있는(미상) 파일 수:", sum(1 for i in items if not i["composer"]))
print("---title 비어있는(정제 실패):", [it["path"] for it in items if not it["title"]])
print()
print("※ 성가집 번호(yahure/haneulbada)는 이 스크립트가 채우지 않습니다.")
print("  이어서 반드시 실행: python3 scripts/match_songbooks.py --write")