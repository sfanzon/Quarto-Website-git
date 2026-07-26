from pathlib import Path
from datetime import datetime
import html, json, re, yaml

root=Path(__file__).resolve().parents[1]
pubs = []  # Loaded from data/publications.bib below.
projects=yaml.safe_load((root/'data/projects.yml').read_text())
(root/'data/projects.generated.json').write_text(json.dumps(projects, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
coauthor_urls=yaml.safe_load((root/'data/coauthors.yml').read_text()) or {}

def read_front_matter(path):
    text = path.read_text()
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.DOTALL)
    if not match:
        return {}, text.strip()
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()

def read_bibtex_entries(path):
    """Parse brace-delimited BibTeX entries of any entry type.

    This intentionally supports the subset used by this site while preserving
    nested braces in abstracts, HTML fragments, and LaTeX.
    """
    source = path.read_text()
    records = []
    position = 0
    entry_pattern = re.compile(r'@(\w+)\s*\{', re.IGNORECASE)
    while True:
        match = entry_pattern.search(source, position)
        if not match:
            break
        entry_type = match.group(1).lower()
        start = match.end()
        cursor = start
        depth = 1
        while cursor < len(source) and depth:
            if source[cursor] == '{':
                depth += 1
            elif source[cursor] == '}':
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError(f'Unclosed BibTeX entry in {path.name}')

        record = source[start:cursor - 1]
        if ',' not in record:
            raise ValueError(f'Malformed BibTeX entry in {path.name}')
        key, fields_source = record.split(',', 1)
        fields = {'id': key.strip(), 'entrytype': entry_type}
        field_position = 0
        field_pattern = re.compile(r'([\w-]+)\s*=\s*\{')
        while True:
            field_match = field_pattern.search(fields_source, field_position)
            if not field_match:
                break
            name = field_match.group(1).lower()
            value_start = field_match.end()
            value_cursor = value_start
            value_depth = 1
            while value_cursor < len(fields_source) and value_depth:
                if fields_source[value_cursor] == '{':
                    value_depth += 1
                elif fields_source[value_cursor] == '}':
                    value_depth -= 1
                value_cursor += 1
            if value_depth:
                raise ValueError(f'Unclosed field {name} in {path.name}:{key.strip()}')
            value = fields_source[value_start:value_cursor - 1]
            fields[name] = re.sub(r'\s+', ' ', value).strip()
            field_position = value_cursor
        records.append(fields)
        position = cursor
    return records

PUBLICATION_WEBSITE_FIELDS = {
    'category', 'abbr', 'selected', 'preprint', 'arxiv', 'abstract', 'pdf', 'code', 'slides',
    'poster', 'video', 'explainer', 'bibtex_show', 'author+an', 'altmetric',
    'dimensions', 'contribution', 'google_scholar_id', 'scopus', 'sjr', 'themes',
    'authors', 'periodical', 'badge', 'links', 'bdsk-url-1',
}


def publication_bibtex(entry):
    """Render a clean citation from the same BibTeX record.

    Website-only fields are omitted, so the Copy BibTeX action remains a
    normal reusable citation rather than exposing presentation metadata.
    """
    fields = []
    for name, value in entry.items():
        if name in {'id', 'entrytype'} or name in PUBLICATION_WEBSITE_FIELDS:
            continue
        fields.append(f'  {name} = {{{value}}}')
    joined = ',\n'.join(fields)
    return f'@{entry["entrytype"]}{{{entry["id"]},\n{joined}\n}}'


def publication_venue(entry):
    """Return the standard BibTeX venue field used by the website."""
    for field in ('journal', 'booktitle', 'school', 'institution', 'publisher', 'howpublished'):
        if entry.get(field):
            return entry[field]
    raise ValueError(
        f'Publication {entry.get("id", "<unknown>")} has no standard venue field '
        '(journal, booktitle, school, institution, publisher, or howpublished)'
    )


def format_author_name(name):
    name = name.strip()
    if ',' in name:
        family, given = [part.strip() for part in name.split(',', 1)]
        display = f'{given} {family}'.strip()
    else:
        display = name
    display = html.escape(display)
    if re.search(r'\bSilvio\s+Fanzon\b|\bFanzon,\s*Silvio\b', name, re.IGNORECASE):
        return f'<em>{display}</em>'
    return display


def publication_authors(entry):
    authors = [format_author_name(name) for name in re.split(r'\s+and\s+', entry['author'])]
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return ' and '.join(authors)
    return ', '.join(authors[:-1]) + ' and ' + authors[-1]


def publication_periodical(entry):
    venue = html.escape(publication_venue(entry))
    year = html.escape(entry["year"])
    # Thesis type used to be communicated by the venue pill. Keep that
    # information in the bibliographic metadata now that the pill is gone.
    if entry.get('category') == 'Theses':
        thesis_type = html.escape(entry.get('abbr', 'Thesis'))
        return f'<em>{venue}</em> · {thesis_type} · {year}'
    return f'<em>{venue}</em> · {year}'



def publication_abstract_html(entry):
    """Render an abstract without requiring HTML paragraph tags in BibTeX.

    Plain abstract text is wrapped in one paragraph automatically. Existing
    block-level HTML is preserved for records that intentionally contain
    multiple paragraphs or other markup.
    """
    abstract = entry.get('abstract', '').strip()
    if not abstract:
        return ''
    if re.match(r'^<(?:p|div|ul|ol|blockquote|pre)\b', abstract, re.IGNORECASE):
        return abstract
    return f'<p>{abstract}</p>'

def publication_links(entry):
    links = []
    if entry.get('abstract'):
        links.append({'label': 'Abs', 'href': '', 'kind': 'abstract'})
    links.append({'label': 'Bib', 'href': '', 'kind': 'bibtex'})

    # The arXiv action is controlled only by the explicit `preprint` field.
    # Stored arXiv identifiers remain available on published records but do
    # not create a button unless preprint is exactly true.
    if entry['preprint']:
        arxiv_id = entry.get('arxiv')
        if not arxiv_id:
            raise ValueError(f'Publication {entry["id"]} is marked preprint=true but has no arxiv field')
        arxiv_href = arxiv_id if arxiv_id.startswith(('http://', 'https://')) else f'https://arxiv.org/abs/{arxiv_id}'
        links.append({'label': 'arXiv', 'href': arxiv_href, 'kind': 'link'})
    else:
        # Published records use the ordinary standard BibTeX destination.
        destination = entry.get('html') or entry.get('url')
        if destination and 'arxiv.org' in destination.lower():
            destination = None
        if not destination and entry.get('doi'):
            doi = entry['doi']
            if 'arxiv.org' not in doi.lower():
                destination = doi if doi.startswith(('http://', 'https://')) else f'https://doi.org/{doi}'
        if destination:
            links.append({'label': 'Journal', 'href': destination, 'kind': 'link'})

    for field, label in [
        ('pdf', 'PDF'), ('code', 'Code'), ('slides', 'Slides'),
        ('poster', 'Poster'), ('video', 'Video'),
    ]:
        if entry.get(field):
            links.append({'label': label, 'href': entry[field], 'kind': 'link'})
    return links


def load_publications(path):
    records = read_bibtex_entries(path)
    required = {'category', 'abbr', 'title', 'author', 'year', 'selected', 'preprint'}
    publications = []
    for record in records:
        missing = sorted(field for field in required if not record.get(field))
        if missing:
            raise ValueError(
                f'Publication {record.get("id", "<unknown>")} is missing required '
                f'BibTeX fields: {", ".join(missing)}'
            )
        selected_value = record['selected'].strip().lower()
        if selected_value not in {'true', 'false'}:
            raise ValueError(
                f'Publication {record["id"]} selected must be exactly true or false'
            )
        record['selected'] = selected_value == 'true'
        preprint_value = record['preprint'].strip().lower()
        if preprint_value not in {'true', 'false'}:
            raise ValueError(
                f'Publication {record["id"]} preprint must be exactly true or false'
            )
        record['preprint'] = preprint_value == 'true'
        publication_venue(record)
        record['authors'] = publication_authors(record)
        record['periodical'] = publication_periodical(record)
        record['badge'] = record['abbr']
        record['themes'] = [theme.strip() for theme in record.get('themes', '').split(';') if theme.strip()][:2]
        record['links'] = publication_links(record)
        record['bibtex'] = publication_bibtex(record)
        publications.append(record)
    return publications


pubs = load_publications(root / 'data/publications.bib')

def teaching_link(value, asset=False):
    if value.startswith(('http://', 'https://', '/')):
        return value
    return f'/assets/pdf/{value}' if asset else value

def teaching_actions(course):
    actions = []
    if course.get('abstract'):
        actions.append('<button class="teaching-action abstract-toggle" type="button"><i class="fa-regular fa-file-lines"></i> About</button>')
    links = [
        ('html', 'HTML', 'fa-code', False),
        ('lecturenotes', 'Notes', 'fa-book-open', True),
        ('lectureslides', 'Slides', 'fa-display', False),
        ('revision', 'Revision', 'fa-list-check', False),
        ('webpage', 'Course page', 'fa-arrow-up-right-from-square', False),
        ('canvas', 'Canvas', 'fa-graduation-cap', False),
        ('taster', 'Taster', 'fa-file-pdf', True),
    ]
    for field, label, icon, asset in links:
        if course.get(field):
            value = course[field]
            if field == 'webpage':
                public_url = course.get('url', '')
                if '/blog/' in public_url:
                    value = public_url
                elif value.startswith('/'):
                    value = f'https://www.silviofanzon.com{value}'
            href = teaching_link(value, asset)
            actions.append(
                f'<a class="teaching-action" href="{html.escape(href, quote=True)}"><i class="fa-solid {icon}"></i> {label}</a>'
            )
    return ''.join(actions)

def teaching_section(section_id, heading, courses, years):
    year_sections = []
    for academic_year in years:
        year_courses = [course for course in courses if course.get('yearacademic') == academic_year]
        year_courses.sort(key=lambda course: int(course.get('year', 0)), reverse=True)
        entries = []
        for course in year_courses:
            degree_line = ' · '.join(
                item for item in [course.get('degree'), course.get('courseyear')] if item
            )
            institution = course.get('venue', '')
            meta = ' · '.join(item for item in [institution, degree_line] if item)
            actions = teaching_actions(course)
            actions_html = f'<div class="teaching-actions">{actions}</div>' if actions else ''
            abstract_html = (
                f'<div class="abstract hidden">{course["abstract"]}</div>'
                if course.get('abstract') else ''
            )
            entries.append(f'''<article class="teaching-course publication-entry" id="{html.escape(course['id'], quote=True)}">
              <div class="teaching-course-main">
                <h4>{html.escape(course.get('title', 'Untitled course'))}</h4>
                <p class="teaching-meta">{html.escape(meta)}</p>
                {actions_html}{abstract_html}
              </div>
            </article>''')
        if entries:
            year_sections.append(f'''<section class="teaching-year">
              <h3>{html.escape(academic_year)}</h3>
              <div class="teaching-course-list">{''.join(entries)}</div>
            </section>''')
    return f'''<section class="teaching-role" id="{section_id}">
      <h2>{heading}</h2>
      <div class="teaching-years">{''.join(year_sections)}</div>
    </section>'''

def news_inline_html(text):
    rendered = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    routes = {
        'publications': 'publications.html',
        'teaching': 'teaching.html',
        'presentations': 'presentations.html',
    }
    for old, new in routes.items():
        rendered = re.sub(
            rf'href=(["\'])/{old}/?#',
            rf'href=\1/{new}#',
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
            items = ''.join(f'<li>{news_inline_html(line[2:].strip())}</li>' for line in lines)
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

def load_news():
    items = []
    news_dir = root / 'news'
    if not news_dir.exists():
        raise FileNotFoundError('Missing news/ directory. Add dated Markdown files such as news/2026-03-17.md')
    for path in news_dir.glob('*.md'):
        metadata, body = read_front_matter(path)
        try:
            date = datetime.strptime(path.stem, '%Y-%m-%d').date()
        except ValueError as error:
            raise ValueError(f'News filename must use YYYY-MM-DD: {path.name}') from error
        if body:
            items.append({
                'date': date,
                'metadata': metadata,
                'body': news_body_html(body),
                'title': str(metadata.get('title') or news_summary(body)).strip(),
                'category': str(metadata.get('category') or 'UPDATE').strip().upper(),
            })
    return sorted(items, key=lambda item: item['date'], reverse=True)

def action_icon(label):
    # Journal and arXiv are both official reading destinations, so they share
    # one clean publication icon on the homepage and Publications page.
    m={'HTML':'fa-arrow-up-right-from-square','Journal':'fa-book-open','Journal page':'fa-book-open','arXiv':'fa-book-open','arXiv page':'fa-book-open','Repository':'fa-building-columns','Repository page':'fa-building-columns','Conference':'fa-arrow-up-right-from-square','Conference page':'fa-arrow-up-right-from-square','Book':'fa-book','Book page':'fa-book','External':'fa-arrow-up-right-from-square','External page':'fa-arrow-up-right-from-square','PDF':'fa-file-pdf','Paper':'fa-file-lines','Code':'fa-code','Slides':'fa-display','Poster':'fa-image','Video':'fa-circle-play'}
    return m.get(label,'fa-link')


def publication_paper_href(p):
    """Return the website-hosted PDF, even when the lightweight repo omits the file."""
    return p.get('pdf', '')


def publication_external_link(p):
    """Return the article's official journal page, or arXiv for a preprint."""
    if p.get('preprint'):
        # Prefer an explicit arXiv URL already stored in standard citation fields.
        for field in ('html', 'url', 'doi'):
            value = p.get(field, '')
            if value and 'arxiv.org' in value.lower():
                return ('arXiv', value)
        arxiv_id = p.get('arxiv', '')
        if arxiv_id:
            href = arxiv_id if arxiv_id.startswith(('http://', 'https://')) else f'https://arxiv.org/abs/{arxiv_id}'
            return ('arXiv', href)
        return ('', '')

    destination = p.get('html') or p.get('url')
    doi = p.get('doi', '')

    if p.get('entrytype') == 'article':
        if destination and 'arxiv.org' not in destination.lower():
            return ('Journal', destination)
        if doi and 'arxiv.org' not in doi.lower():
            href = doi if doi.startswith(('http://', 'https://')) else f'https://doi.org/{doi}'
            return ('Journal', href)
        return ('', '')

    # Non-journal records use an accurate official-source label and avoid a
    # duplicate link when their URL is simply the same website-hosted PDF.
    if destination and p.get('pdf') and destination.rstrip('/').endswith(p['pdf'].rstrip('/')):
        destination = ''
    if p.get('entrytype') in {'phdthesis', 'mastersthesis'} and destination:
        return ('Repository', destination)
    if p.get('entrytype') == 'book' and destination:
        return ('Book', destination)
    if destination:
        return ('External', destination)
    return ('', '')


def publication_theme_pills(p):
    if not p.get('themes'):
        return ''
    pills = ''.join(
        f'<span class="publication-theme">{html.escape(theme)}</span>'
        for theme in p['themes']
    )
    return f'<div class="publication-themes" aria-label="Research themes">{pills}</div>'


def homepage_pub_actions(p):
    """Homepage publications use the same compact action hierarchy as the archive."""
    return pub_actions(p, publications_page=True)


def pub_actions(p, toggles=True, publications_page=False):
    """Render a compact publication action hierarchy.

    The full archive keeps PDF, the official journal/arXiv destination,
    Abstract, Cite and Code visible. Presentation material is grouped under
    More so it does not compete with the primary research outputs.
    """
    if not publications_page:
        return homepage_pub_actions(p)

    xs=[]
    paper_href = publication_paper_href(p)
    if paper_href:
        xs.append(
            f'<a class="paper-action publication-primary-action" href="{html.escape(paper_href, quote=True)}"><i class="fa-solid fa-file-pdf"></i> PDF</a>'
        )
    external_label, external_href = publication_external_link(p)
    if external_href:
        xs.append(
            f'<a class="paper-action" href="{html.escape(external_href, quote=True)}"><i class="fa-solid {action_icon(external_label)}"></i> {external_label}</a>'
        )
    if toggles and p.get('abstract'):
        xs.append('<button class="paper-action abstract-toggle" type="button"><i class="fa-regular fa-file-lines"></i> Abstract</button>')
    if toggles:
        xs.append('<button class="paper-action bibtex-toggle" type="button"><i class="fa-solid fa-quote-right"></i> Cite</button>')
    if p.get('explainer'):
        xs.append(
            f'<a class="paper-action" href="{html.escape(p["explainer"], quote=True)}"><i class="fa-solid fa-lightbulb"></i> Explainer</a>'
        )
    if p.get('code'):
        xs.append(
            f'<a class="paper-action" href="{html.escape(p["code"], quote=True)}"><i class="fa-solid {action_icon("Code")}"></i> Code</a>'
        )
    for field, label in (("slides", "Slides"), ("poster", "Poster"), ("video", "Video")):
        if p.get(field):
            xs.append(
                f'<a class="paper-action" href="{html.escape(p[field], quote=True)}"><i class="fa-solid {action_icon(label)}"></i> {label}</a>'
            )

    return ''.join(xs)

COAUTHOR_URLS = coauthor_urls

def publication_side_meta(p):
    """Research-theme labels for the responsive publication rail."""
    return f'<div class="publication-theme-rail">{publication_theme_pills(p)}</div>'


def linked_authors(authors):
    result = authors.replace('<em>Silvio Fanzon</em>', '<span class="author-self">Silvio Fanzon</span>')
    for name, url in COAUTHOR_URLS.items():
        result = result.replace(name, f'<a class="author-link" href="{url}">{name}</a>')
    return result

# Project cards: data/projects.yml is the single source for both the homepage
# and the Projects archive. Keep card actions deliberately limited to the
# project destination plus Code when a real repository is available.
def render_project_card(project):
    labels = ' · '.join(html.escape(label) for label in project.get('labels', [])[:3])
    title = html.escape(project['title'])
    summary = html.escape(project['summary'])
    image = html.escape(project['image'], quote=True)
    href = html.escape(project['href'], quote=True)
    archive_class = ' project-summary-card-archive' if project.get('archived') else ''
    code_link = ''
    if project.get('code'):
        code_href = html.escape(project['code'], quote=True)
        code_link = f'<a href="{code_href}">Code</a>'
    return f'''<article class="home-project-card project-summary-card{archive_class}">
      <div class="home-project-visual"><img src="{image}" alt="Abstract visual for {title}"></div>
      <div class="home-project-copy"><p class="project-labels">{labels}</p><h3>{title}</h3><p>{summary}</p><div class="home-project-actions"><a href="{href}">Read project <span aria-hidden="true">→</span></a>{code_link}</div></div>
    </article>'''



# Long-form project heroes, F1 resource navigation and related-project
# suggestions are rendered at Quarto render-time by filters/project-components.lua.
# That filter reads data/projects.generated.json, which is refreshed above from
# the same data/projects.yml used by the homepage and Projects page cards.

featured_projects=[p for p in projects if p.get('featured') is True][:3]
proj=[render_project_card(p) for p in featured_projects]
project_archive=[render_project_card(p) for p in projects]
# Every publication explicitly marked `selected: true` appears on the
# homepage, in the same order as data/publications.bib.
selected=[p for p in pubs if p.get('selected') is True]
(root/'includes/home-projects.html').write_text('\n'.join(proj))
(root/'includes/projects-portfolio.html').write_text('''<section class="projects-section project-portfolio">
  <div class="section-heading project-page-heading"><div><p class="eyebrow">Selected work</p><span>Projects, implementations and reproducible outputs</span></div></div>
  <div class="projects-card-grid">
''' + '\n'.join(project_archive) + '''
  </div>
</section>''')

home_pub_rows=[]
for p in selected:
    authors=linked_authors(p['authors'])
    side_meta=publication_side_meta(p)
    home_pub_rows.append(f'''<article class="home-publication-row publication-entry" id="home-list-{p['id']}">
      <div class="home-publication-main pub-main"><h3>{p['title']}</h3><div class="paper-meta"><span class="publication-authors">{authors}</span><span class="publication-periodical">{p['periodical']}</span></div><div class="paper-actions">{homepage_pub_actions(p)}</div><div class="abstract hidden">{publication_abstract_html(p)}</div><div class="bibtex hidden"><pre><code>{html.escape(p['bibtex'])}</code></pre></div></div>{side_meta}
    </article>''')
(root/'includes/home-publications-list.html').write_text('\n'.join(home_pub_rows))

# Publications page
publication_categories = list(dict.fromkeys(p['category'] for p in pubs))

allbits=[]
for group in publication_categories:
    rows=[]
    for p in [x for x in pubs if x['category'] == group]:
        authors=linked_authors(p['authors'])
        side_meta=publication_side_meta(p)
        rows.append(f'''<article class="home-publication-row publication-archive-row publication-entry" id="{p['id']}"><div class="home-publication-main pub-main"><h3>{p['title']}</h3><div class="paper-meta"><span class="publication-authors">{authors}</span><span class="publication-periodical">{p['periodical']}</span></div><div class="paper-actions">{pub_actions(p, publications_page=True)}</div><div class="abstract hidden">{publication_abstract_html(p)}</div><div class="bibtex hidden"><pre><code>{html.escape(p['bibtex'])}</code></pre></div></div>{side_meta}</article>''')
    if rows:
        group_id=group.lower().replace(' ','-')
        allbits.append(f'''<section class="publication-category" id="{group_id}"><h2>{group}</h2><div class="publication-category-list">{''.join(rows)}</div></section>''')
(root/'includes/publications-all.html').write_text('\n'.join(allbits))

# Teaching: retain the original BibDesk bibliographies as the single source.
lecturer_courses = read_bibtex_entries(root / 'data/teaching_lecturer.bib')
tutor_courses = read_bibtex_entries(root / 'data/teaching_tutor.bib')
teaching_html = [
    teaching_section(
        'lecturer',
        'Lecturer',
        lecturer_courses,
        ['2025/26', '2024/25', '2023/24', '2022/23', '2020/21', '2019/20'],
    ),
    teaching_section(
        'tutor',
        'Teaching assistant',
        tutor_courses,
        ['2017/18', '2016/17', '2015/16', '2014/15', '2012/13'],
    ),
]
(root / 'includes/teaching-list.html').write_text('\n'.join(teaching_html))

# News: dated Markdown files are the single source for both views.
news = load_news()


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

    search_markup = ""
    empty_markup = ""
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


# Homepage: latest eight only. The News page uses the same component for all items.
# Write Quarto fragments with an explicit raw-HTML fence. This avoids the HTML
# being interpreted as literal text when the fragment is included during render.
def write_news_qmd(path, items, empty_message, searchable=True):
    markup = render_news_component(items, empty_message, searchable=searchable)
    path.write_text(f"```{{=html}}\n{markup}\n```\n", encoding='utf-8')

write_news_qmd(root / 'includes/home-news.qmd', news[:8], 'No recent announcements.', searchable=False)
write_news_qmd(root / 'includes/news-all.qmd', news, 'No announcements yet.')
