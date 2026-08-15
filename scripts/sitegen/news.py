"""News source loading, Markdown conversion, and component rendering."""

import html
import re
from datetime import datetime

from .core import DEFAULT_ROOT, read_front_matter


def news_inline_html(text):
    rendered = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    for route in ('publications', 'teaching', 'research', 'about', 'expertise', 'projects'):
        rendered = re.sub(
            rf'href=(["\'])/{route}(?:\.html|/)?(?=#|\1)',
            rf'href=\1/{route}/',
            rendered,
        )
    rendered = re.sub(
        r'href=(["\'])/presentations(?:\.html|/)?(?=#|\1)',
        r'href=\1/presentations/',
        rendered,
    )
    return rendered


def news_body_html(source):
    blocks = re.split(r'\n\s*\n', source.strip())
    rendered = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if all(line.startswith('- ') for line in lines):
            items = ''.join(
                f'<li>{news_inline_html(line[2:].strip())}</li>'
                for line in lines
            )
            rendered.append(f'<ul>{items}</ul>')
        else:
            rendered.append(f'<p>{news_inline_html(" ".join(lines))}</p>')
    return ''.join(rendered).replace('</ul><ul>', '')


def news_summary(source, limit=142):
    plain = re.sub(r'<[^>]+>', '', source)
    plain = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', plain)
    plain = html.unescape(plain.replace('*', ''))
    plain = re.sub(r'\s+', ' ', plain).strip()
    first = re.split(r'(?<=[.!?])\s+', plain, maxsplit=1)[0]
    if len(first) <= limit:
        return first
    shortened = first[:limit + 1].rsplit(' ', 1)[0]
    return shortened.rstrip(' ,;:') + '…'


def display_news_date(value):
    return value.strftime('%b %Y')


def load_news(site_root=None):
    site_root = site_root or DEFAULT_ROOT
    items = []
    news_dir = site_root / 'news'
    if not news_dir.exists():
        raise FileNotFoundError(
            'Missing news/ directory. Add dated Markdown files such as '
            'news/2026-03-17.md'
        )
    for path in news_dir.glob('*.md'):
        metadata, body = read_front_matter(path)
        try:
            date = datetime.strptime(path.stem, '%Y-%m-%d').date()
        except ValueError as error:
            raise ValueError(
                f'News filename must use YYYY-MM-DD: {path.name}'
            ) from error
        if body:
            items.append({
                'date': date,
                'metadata': metadata,
                'body': news_body_html(body),
                'title': str(metadata.get('title') or news_summary(body)).strip(),
                'category': str(
                    metadata.get('category') or 'UPDATE'
                ).strip().upper(),
            })
    return sorted(items, key=lambda item: item['date'], reverse=True)


def render_news_component(items, empty_message, searchable=True):
    """Render the shared accordion, with search enabled only where requested."""
    rows = []
    for item in items:
        date = item['date']
        rows.append(f"""<details class="news-item" id="news-{date.isoformat()}" data-news-item>
      <summary>
        <time class="news-date" datetime="{date.isoformat()}">{display_news_date(date)}</time>
        <span class="news-category">{html.escape(item['category'])}</span>
        <span class="news-title">{html.escape(item['title'])}</span>
        <span class="news-disclosure" aria-hidden="true"></span>
      </summary>
      <div class="news-body">{item['body']}</div>
    </details>""")

    if not rows:
        rows.append(f'<p class="news-empty">{html.escape(empty_message)}</p>')

    search_markup = ''
    empty_markup = ''
    if searchable:
        search_markup = """<div class="news-tools">
    <label class="news-search">
      <span class="visually-hidden">Search news</span>
      <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
      <input type="search" placeholder="Search updates" autocomplete="off" data-news-search>
    </label>
  </div>"""
        empty_markup = '<p class="news-search-empty" hidden>No news items match your search.</p>'

    return f"""<div class="news-component" data-news-component>
  {search_markup}
  <div class="news-list" data-news-list>
    {''.join(rows)}
    {empty_markup}
  </div>
</div>"""
