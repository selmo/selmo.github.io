#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""각 페이지 frontmatter 에 updated(마지막 수정일)를 기록한다.

GitHub Pages 레거시 빌드는 jekyll-last-modified-at 을 지원하지 않아
빌드 시점에 파일별 수정 시각을 알 수 없다. 그래서 커밋 전에 git 이력에서
날짜를 읽어 frontmatter 에 직접 박아 둔다.

데이터에서 자동 생성되는 페이지(악보·성가집 등)는 페이지 파일 자체보다
데이터 파일이 더 자주 바뀐다. PAGE_DEPS 에 의존 데이터를 적어 두면
페이지와 데이터 중 더 최근 날짜를 쓴다.

사용:
    python3 scripts/stamp_updated.py          # 미리보기
    python3 scripts/stamp_updated.py --write  # 실제 기록
"""
import subprocess, sys, os, re, unicodedata

# 페이지 -> 그 페이지가 렌더에 쓰는 데이터 파일
PAGE_DEPS = {
    "resources/Scores.md":        ["_data/scores.yml", "_data/links.yml"],
    "resources/OnE-Scores.md":    ["_data/scores.yml", "_data/links.yml"],
    "resources/index.md":         ["_data/scores.yml", "_data/songbooks.yml"],
    "resources/Yahure.md":        ["_data/songbooks.yml"],
    "resources/Haneulbada.md":    ["_data/songbooks.yml"],
    "ccm/Articles.md":            ["_data/articles.yml"],
    "ccm/songs/index.md":         ["_data/songs.yml"],
    "ccm/artists/index.md":       ["_data/artists.yml"],
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
        dates = [d for d in [git_date(p)] if d]
        for dep in PAGE_DEPS.get(p, []):
            d = git_date(dep)
            if d:
                dates.append(d)
        if not dates:
            skipped += 1
            continue
        date = max(dates)                      # 페이지·데이터 중 더 최근
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
