#!/usr/bin/env python3

import argparse
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.resolve()
OUT = ROOT / "out"

SITEMAP = OUT / "sitemap.xml"
ROBOTS = OUT / "robots.txt"

BASE_URL = f"https://khudocmo.github.io/tac-pham/"

# -----------------------
# Collect HTML URLs
# -----------------------

urls = []

for html in OUT.rglob("*.html"):
    rel = html.relative_to(OUT).as_posix()

    if rel == "index.html":
        urls.append(BASE_URL)
    else:
        urls.append(BASE_URL + rel)

# -----------------------
# Write sitemap.xml
# -----------------------

today = date.today().isoformat()

sitemap_lines = []
sitemap_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
sitemap_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for url in sorted(urls):
    sitemap_lines.append("  <url>")
    sitemap_lines.append(f"    <loc>{url}</loc>")
    sitemap_lines.append(f"    <lastmod>{today}</lastmod>")
    sitemap_lines.append("  </url>")

sitemap_lines.append("</urlset>")

SITEMAP.write_text("\n".join(sitemap_lines), encoding="utf-8")

# -----------------------
# Write robots.txt
# -----------------------

robots_text = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}sitemap.xml
"""

ROBOTS.write_text(robots_text, encoding="utf-8")

print(f"sitemap.xml generated: {len(urls)} URLs")
print("robots.txt generated")