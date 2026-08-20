#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""각 페이지 frontmatter 에 updated(마지막 수정일)를 기록한다.

GitHub Pages 레거시 빌드는 jekyll-last-modified-at 을 지원하지 않아
빌드 시점에 파일별 수정 시각을 알 수 없다. 그래서 커밋 전에 날짜를 읽어
frontmatter 에 직접 박아 둔다.

날짜는 '내용이 실제로 바뀐 시점'이어야 한다. 원본 종류에 따라 소스가 다르다:

  - 원본 자료(PDF 악보, xlsx 등): 파일시스템 mtime.
    저장소에 늦게 올린 파일은 커밋일이 실제 수정일과 크게 어긋난다.
    (예: 야훼이레 xlsx — 수정 2024-01-05, 커밋 2026-05-22)
  - 손으로 쓴 문서(.md, 수작업 데이터): git 커밋일.
    편집할 때마다 mtime 이 바뀌므로 checkout 만 해도 갱신되어 믿을 수 없다.

사용:
    python3 scripts/stamp_updated.py          # 미리보기
    python3 scripts/stamp_updated.py --write  # 실제 기록
"""
import subprocess, sys, os, re, glob as globmod
from datetime import date as _date

# 페이지가 실제로 의존하는 원본.
#   glob:  파일시스템 mtime 중 가장 최근 (원본 자료 — PDF·xlsx 등)
#   git:   git 커밋일 (손으로 쓴 문서·수작업 데이터)
PAGE_DEPS = {
    "resources/Scores.md": [
        ("glob", "resources/OnE-Scores/**/*.pdf"),   # 악보 원본
        ("git", "_data/links.yml"),                  # 영상 링크는 수작업
    ],
    "resources/OnE-Scores.md": [
        ("glob", "resources/OnE-Scores/**/*.pdf"),
        ("git", "_data/links.yml"),
    ],
    "resources/index.md": [
        ("glob", "resources/OnE-Scores/**/*.pdf"),
        ("glob", "resources/야훼이레-수록곡목록-3판.xlsx"),
        ("git", "resources/하늘바다.md"),
    ],
    # 성가집 목차 페이지는 각자 자기 원본만 본다 (_data/yahure.yml,
    # _data/haneulbada.yml 은 그 원본에서 생성되므로 따로 적지 않는다)
    "resources/Yahure.md": [
        ("glob", "resources/야훼이레-수록곡목록-3판.xlsx"),
    ],
    "resources/Haneulbada.md": [
        ("git", "resources/하늘바다.md"),
    ],
    "ccm/Articles.md":      [("git", "_data/articles.yml")],
    "ccm/songs/index.md":   [("git", "_data/songs.yml")],
    "ccm/artists/index.md": [("git", "_data/artists.yml")],
}


def git_date(path):
    """파일의 마지막 커밋일 (YYYY-MM-DD). 이력이 없으면 None."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=format:%Y-%m-%d", "--", path],
            capture_output=True, text=True, check=True).stdout.strip()
        return out or None
    except subprocess.CalledProcessError:
        return None


def mtime_date(pattern):
    """glob 패턴에 걸리는 파일들의 mtime 중 가장 최근 (YYYY-MM-DD)."""
    paths = globmod.glob(pattern, recursive=True)
    if not paths:
        return None
    newest = max(os.path.getmtime(p) for p in paths)
    return _date.fromtimestamp(newest).isoformat()


def dep_date(kind, target):
    return mtime_date(target) if kind == "glob" else git_date(target)


def tracked_pages():
    out = subprocess.run(["git", "ls-files", "-z", "*.md"],
                         capture_output=True, check=True).stdout
    files = [f.decode("utf-8") for f in out.split(b"\0") if f]
    # _layouts, _includes 등 언더스코어 디렉터리와 README 는 페이지가 아니다
    return [f for f in files
            if not f.startswith("_") and os.path.basename(f) not in ("README.md",)]


def stamp(path, date, write):
    """frontmatter 의 updated 를 date 로 맞춘다. 바뀌면 True."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    if not text.startswith("---\n"):
        return False, "frontmatter 없음"

    end = text.find("\n---", 4)
    if end == -1:
        return False, "frontmatter 미종료"

    head, body = text[4:end], text[end:]

    m = re.search(r"^updated:.*$", head, re.M)
    if m:
        if m.group(0) == f"updated: {date}":
            return False, "변경 없음"
        new_head = head[:m.start()] + f"updated: {date}" + head[m.end():]
    else:
        new_head = head.rstrip("\n") + f"\nupdated: {date}\n"
        new_head = new_head.rstrip("\n")

    if write:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("---\n" + new_head + body)
    return True, date


def main():
    write = "--write" in sys.argv
    pages = tracked_pages()

    changed = skipped = 0
    for p in pages:
        deps = PAGE_DEPS.get(p)
        if deps:
            # 데이터에서 생성되는 페이지: 원본이 바뀐 날이 곧 내용이 바뀐 날.
            # 페이지 파일의 커밋일은 쓰지 않는다 — 템플릿 손질이나 이 스크립트가
            # 남긴 updated 갱신까지 '내용 수정'으로 잡히기 때문이다.
            dates = [d for d in (dep_date(k, t) for k, t in deps) if d]
        else:
            dates = [d for d in [git_date(p)] if d]
        if not dates:
            skipped += 1
            continue
        date = max(dates)
        ok, msg = stamp(p, date, write)
        if ok:
            changed += 1
            if p in PAGE_DEPS:
                print(f"  {p} -> {date} (데이터 반영)")
        elif msg not in ("변경 없음",):
            print(f"  ! {p}: {msg}")
            skipped += 1

    print(f"\n페이지 {len(pages)}개 · 기록 {changed} · 건너뜀 {skipped}")
    if not write:
        print("미리보기입니다. 실제 기록하려면 --write 를 붙이세요.")


if __name__ == "__main__":
    main()
