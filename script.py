#!/usr/bin/env python3

import re
import markdown
from pathlib import Path

# ---------------- Paths ----------------

ROOT_DIR = Path(__file__).resolve().parent
INDEX_MD = ROOT_DIR / "index.md"
TEMPLATE_PATH = ROOT_DIR / "template.html"
DOCS_DIR = ROOT_DIR / "docs"
HOMEPAGE_TEMPLATE = ROOT_DIR / "homepage_template.html"

DOCS_DIR.mkdir(exist_ok=True)

# ---------------- Load files ----------------

md_text = INDEX_MD.read_text(encoding="utf-8")
template = TEMPLATE_PATH.read_text(encoding="utf-8")

homepage_content_html = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code"]
)

# ---------------- Regex ----------------

AUTHOR_RE = re.compile(r"^###\s+(.+)", re.MULTILINE)
WORK_RE = re.compile(r"-\s+\[([^\]]+)\]\((./[^)]+)\)")

# ---------------- Parse index.md ----------------

authors = []

for author_match in AUTHOR_RE.finditer(md_text):
    author = author_match.group(1).strip()

    start = author_match.end()
    next_author = AUTHOR_RE.search(md_text, start)
    block = md_text[start: next_author.start() if next_author else None]

    works = WORK_RE.findall(block)
    authors.append((author, works))

# ---------------- Build pages ----------------

for author, works in authors:
    for title, raw_path in works:
        # Normalize path: /nam-cao_song-mon or /nam-cao_song-mon/
        ten_tep = raw_path.strip().lstrip("./").rstrip("/")

        # author_path = phần trước dấu "_"
        author_path = ten_tep.split("_", 1)[0]

        out_dir = DOCS_DIR / ten_tep
        out_dir.mkdir(parents=True, exist_ok=True)

        html = (
            template
            .replace("[title]", title)
            .replace("[author]", author)
            .replace("[author_path]", author_path)
            .replace("[ten-tep]", ten_tep)
        )

        (out_dir / "index.html").write_text(html, encoding="utf-8")

        print(f"✔ Built: {ten_tep}")


homepage_tpl = HOMEPAGE_TEMPLATE.read_text(encoding="utf-8")

homepage_html = (
    homepage_tpl
    .replace("{{title}}", "Danh sách tác phẩm - Khu đọc mở")
    .replace("{{content}}", homepage_content_html)
)

(DOCS_DIR / "index.html").write_text(homepage_html, encoding="utf-8")

print("✔ Built: docs/index.html")
