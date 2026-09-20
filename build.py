#!/usr/bin/env python3
"""Builds privacy.html and terms.html from the app's legal Markdown sources.

Run after editing the Markdown in the app repository:
    python3 build.py
"""

import html
import re
from pathlib import Path

SITE_DIR = Path(__file__).parent
LEGAL_DIR = SITE_DIR.parent / "bracket-maker" / "docs" / "legal"

PAGES = [
    ("privacy-policy.md", "privacy.html", "Privacy Policy"),
    ("terms-of-use.md", "terms.html", "Terms of Use"),
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} · Bracket Maker</title>
    <meta name="description" content="{description}" />
    <link rel="icon" href="/icon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body>
    <header class="page-header">
      <a class="brand" href="/">
        <img class="brand-mark" src="/icon.svg" width="28" height="28" alt="" />
        <span>Bracket Maker</span>
      </a>
    </header>
    <main>
{content}
    </main>
    <footer class="page-footer">
      <a href="/privacy">Privacy Policy</a>
      <a href="/terms">Terms of Use</a>
      <a href="/">Home</a>
    </footer>
  </body>
</html>
"""

INLINE_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
# Trailing punctuation (a sentence period) must stay outside the link.
BARE_URL = re.compile(r"(?<![\">])(https?://[^\s<),]*[^\s<),.;:])")
BOLD = re.compile(r"\*\*([^*]+)\*\*")


def render_inline(text: str) -> str:
    """Escapes HTML, then restores bold and links."""
    rendered = html.escape(text)
    rendered = INLINE_LINK.sub(r'<a href="\2">\1</a>', rendered)
    rendered = BARE_URL.sub(r'<a href="\1">\1</a>', rendered)
    rendered = BOLD.sub(r"<strong>\1</strong>", rendered)
    return rendered


def render_markdown(markdown: str) -> str:
    """Minimal converter for the subset used in the legal documents."""
    lines = markdown.splitlines()
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            # Single line breaks are kept (the contact block relies on them).
            body = "<br />".join(render_inline(line) for line in paragraph)
            blocks.append(f"<p>{body}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            blocks.append(f"<ul>{items}</ul>")
            list_items.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_list()
        elif stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h2>{render_inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h1>{render_inline(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            flush_paragraph()
            list_items.append(stripped[2:])
        else:
            flush_list()
            paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    return "\n".join(f"      {block}" for block in blocks)


def main() -> None:
    for source_name, output_name, title in PAGES:
        markdown = (LEGAL_DIR / source_name).read_text(encoding="utf-8")
        page = PAGE_TEMPLATE.format(
            title=title,
            description=f"{title} for the Bracket Maker tournament bracket app.",
            content=render_markdown(markdown),
        )
        (SITE_DIR / output_name).write_text(page, encoding="utf-8")
        print(f"{source_name} → {output_name}")


if __name__ == "__main__":
    main()
