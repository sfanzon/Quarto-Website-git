from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
import html, json, re, yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def is_external_reference(value):
    """Return whether a reference is intentionally outside this repository."""
    if not isinstance(value, str):
        return False
    return bool(re.match(r'^(?:https?:|mailto:|tel:|data:|javascript:|//)', value.strip(), re.I))


def local_reference_path(value, base=None, site_root=None):
    """Resolve a generated/local URL to its source or rendered file.

    Quarto URLs are checked against the source tree before rendering: an HTML
    route may legitimately correspond to a .qmd source file.
    """
    if not isinstance(value, str) or not value.strip() or is_external_reference(value):
        return None
    site_root = site_root or DEFAULT_ROOT
    path = urlsplit(value.strip()).path
    candidate = site_root / path.lstrip('/') if path.startswith('/') else (base or site_root) / path
    candidates = [candidate]
    if candidate.is_dir():
        candidates.extend([candidate / 'index.html', candidate / 'index.qmd'])
    if candidate.suffix.lower() == '.html':
        candidates.append(candidate.with_suffix('.qmd'))
    if candidate.name == 'index.html':
        candidates.append(candidate.with_name('index.qmd'))
    return next((item for item in candidates if item.is_file()), candidate)


def validate_local_assets(projects, publications, teaching_courses, site_root=None):
    """Validate repository references and return external links skipped.

    Local references fail together so a single build reports every broken
    source value. External URLs are deliberately non-blocking and are returned
    separately for an audit summary; no network requests are made here.
    """
    site_root = site_root or DEFAULT_ROOT
    missing = []
    external = []

    def check(value, label, base=None, asset_prefix=None):
        if not isinstance(value, str) or not value.strip():
            return
        value = value.strip()
        if is_external_reference(value):
            external.append((label, value))
            return
        generated = f'/{asset_prefix.strip("/")}/{value.lstrip("/")}' if asset_prefix else value
        target = local_reference_path(generated, base=base, site_root=site_root)
        if target is None or not target.is_file():
            missing.append(f'{label}: {value} (expected {target})')

    for project in projects:
        project_id = project.get('id', '<unknown project>')
        check(project.get('image'), f'project {project_id} image')
        project_href = project.get('href')
        check(project_href, f'project {project_id} href')
        project_base = (
            site_root / Path(urlsplit(project_href or '').path).parent
            if project_href else site_root
        )
        article = project.get('article') or {}
        for resource in article.get('resources') or []:
            check(resource.get('href'), f'project {project_id} resource {resource.get("label", "<unnamed>")}')
        for view in article.get('views') or []:
            check(view.get('href'), f'project {project_id} view {view.get("id", "<unnamed>")}', base=project_base)
        for field in ('code', 'download', 'zip', 'pdf', 'slides', 'poster'):
            if field in project:
                check(project[field], f'project {project_id} {field}')

    for publication in publications:
        publication_id = publication.get('id', '<unknown publication>')
        for field in ('pdf', 'slides', 'poster', 'explainer', 'code', 'video'):
            if field in publication:
                check(publication[field], f'publication {publication_id} {field}')

    for source_name, courses in teaching_courses:
        for course in courses:
            course_id = course.get('id', '<unknown course>')
            for field in ('html', 'lecturenotes', 'lectureslides', 'revision', 'webpage', 'canvas', 'taster'):
                value = course.get(field)
                if not value:
                    continue
                # Teaching course pages beginning with / are rewritten by
                # teaching_actions() to the canonical public site URL.
                if field == 'webpage' and str(value).startswith('/'):
                    external.append((f'{source_name} {course_id} {field}', value))
                    continue
                asset_prefix = 'assets/pdf' if field in {'lecturenotes', 'taster'} else None
                check(value, f'{source_name} {course_id} {field}', asset_prefix=asset_prefix)

    if missing:
        raise ValueError('Local asset validation failed:\n- ' + '\n- '.join(missing))
    return external

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

        # BibTeX declarations are not content records. In particular,
        # @string entries commonly appear before teaching and publication
        # records and must not be validated as if they were courses.
        if entry_type in {'string', 'preamble', 'comment'}:
            position = cursor
            continue

        record = source[start:cursor - 1]
        if ',' not in record:
            raise ValueError(f'Malformed BibTeX entry in {path.name}')
        key, fields_source = record.split(',', 1)
        fields = {'id': key.strip(), 'entrytype': entry_type}
        field_position = 0
        field_pattern = re.compile(r'([\w-]+)\s*=\s*', re.IGNORECASE)
        while True:
            field_match = field_pattern.search(fields_source, field_position)
            if not field_match:
                break
            name = field_match.group(1).lower()
            value_start = field_match.end()
            while value_start < len(fields_source) and fields_source[value_start].isspace():
                value_start += 1

            if value_start >= len(fields_source):
                raise ValueError(f'Missing value for field {name} in {path.name}:{key.strip()}')

            opening = fields_source[value_start]
            if opening == '{':
                value_cursor = value_start + 1
                value_depth = 1
                while value_cursor < len(fields_source) and value_depth:
                    if fields_source[value_cursor] == '{':
                        value_depth += 1
                    elif fields_source[value_cursor] == '}':
                        value_depth -= 1
                    value_cursor += 1
                if value_depth:
                    raise ValueError(f'Unclosed field {name} in {path.name}:{key.strip()}')
                value = fields_source[value_start + 1:value_cursor - 1]
            elif opening == '"':
                value_cursor = value_start + 1
                escaped = False
                while value_cursor < len(fields_source):
                    char = fields_source[value_cursor]
                    if char == '"' and not escaped:
                        break
                    escaped = char == '\\' and not escaped
                    if char != '\\':
                        escaped = False
                    value_cursor += 1
                if value_cursor >= len(fields_source):
                    raise ValueError(f'Unclosed field {name} in {path.name}:{key.strip()}')
                value = fields_source[value_start + 1:value_cursor]
                value_cursor += 1
            else:
                comma = fields_source.find(',', value_start)
                value_cursor = len(fields_source) if comma == -1 else comma
                value = fields_source[value_start:value_cursor].strip()

            fields[name] = re.sub(r'\s+', ' ', value).strip()
            field_position = value_cursor
        records.append(fields)
        position = cursor
    return records

PUBLICATION_WEBSITE_FIELDS = {
    'category', 'abbr', 'selected', 'preprint', 'arxiv', 'abstract', 'pdf', 'code', 'slides',
    'poster', 'video', 'explainer', 'bibtex_show', 'author+an', 'altmetric',
    'dimensions', 'contribution', 'google_scholar_id', 'scopus', 'sjr', 'themes',
    'authors', 'periodical', 'links', 'bdsk-url-1',
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
        record['themes'] = [theme.strip() for theme in record.get('themes', '').split(';') if theme.strip()][:2]
        record['bibtex'] = publication_bibtex(record)
        publications.append(record)
    return publications


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

ACADEMIC_YEAR_PATTERN = re.compile(r'^(?P<start>\d{4})/(?P<end>\d{2})$')


def teaching_years(courses, source_name):
    """Return validated academic years in descending chronological order."""
    years = set()
    for course in courses:
        value = str(course.get('yearacademic', '')).strip()
        if not value:
            raise ValueError(
                f'Teaching record {course.get("id", "<unknown>")} in '
                f'{source_name} is missing yearacademic'
            )
        match = ACADEMIC_YEAR_PATTERN.fullmatch(value)
        if not match:
            raise ValueError(
                f'Teaching record {course.get("id", "<unknown>")} in '
                f'{source_name} has invalid yearacademic: {value!r} '
                '(expected YYYY/YY)'
            )
        start = int(match.group('start'))
        expected_end = f'{(start + 1) % 100:02d}'
        if match.group('end') != expected_end:
            raise ValueError(
                f'Teaching record {course.get("id", "<unknown>")} in '
                f'{source_name} has non-consecutive yearacademic: {value!r}'
            )
        years.add(value)
    return sorted(years, key=lambda year: int(year[:4]), reverse=True)


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

def load_news(site_root=None):
    site_root = site_root or DEFAULT_ROOT
    items = []
    news_dir = site_root / 'news'
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
    m={'Journal':'fa-book-open','arXiv':'fa-book-open','Repository':'fa-building-columns','Book':'fa-book','External':'fa-arrow-up-right-from-square','Code':'fa-code','Slides':'fa-display','Poster':'fa-image','Video':'fa-circle-play'}
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


def pub_actions(p, toggles=True):
    """Render a compact publication action hierarchy.

    The homepage and full archive use the same visible PDF, official
    destination, citation, explainer and presentation actions.
    """
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

def publication_side_meta(p):
    """Research-theme labels for the responsive publication rail."""
    return f'<div class="publication-theme-rail">{publication_theme_pills(p)}</div>'


def linked_authors(authors, coauthor_urls=None):
    result = authors.replace('<em>Silvio Fanzon</em>', '<span class="author-self">Silvio Fanzon</span>')
    for name, url in (coauthor_urls or {}).items():
        result = result.replace(name, f'<a class="author-link" href="{url}">{name}</a>')
    return result

def render_publication_entry(p, row_id, row_classes, actions, coauthor_urls=None):
    authors = linked_authors(p['authors'], coauthor_urls)
    side_meta = publication_side_meta(p)
    return f'''<article class="{row_classes} publication-entry" id="{html.escape(row_id, quote=True)}"><div class="home-publication-main pub-main"><h3>{p['title']}</h3><div class="paper-meta"><span class="publication-authors">{authors}</span><span class="publication-periodical">{p['periodical']}</span></div><div class="paper-actions">{actions}</div><div class="abstract hidden">{publication_abstract_html(p)}</div><div class="bibtex hidden"><pre><code>{html.escape(p['bibtex'])}</code></pre></div></div>{side_meta}</article>'''

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


def load_featured_notes(notes_dir=None, site_root=None):
    """Load homepage-selected notes from their canonical front matter."""
    site_root = site_root or DEFAULT_ROOT
    notes_dir = notes_dir or site_root / 'notes'
    featured = []
    required = ('title', 'description', 'date', 'image', 'image-alt', 'featured-order')
    for path in sorted(notes_dir.glob('*.qmd')):
        metadata, _ = read_front_matter(path)
        if metadata.get('featured') is not True:
            continue
        missing = [field for field in required if metadata.get(field) in (None, '')]
        if missing:
            raise ValueError(
                f'Featured note {path.name} is missing metadata: {", ".join(missing)}'
            )
        image_path = local_reference_path(
            str(metadata['image']),
            base=path.parent,
            site_root=site_root,
        )
        if image_path is None or not image_path.is_file():
            raise ValueError(
                f'Featured note {path.name} image does not exist: {metadata["image"]}'
            )
        date_value = metadata['date']
        if hasattr(date_value, 'strftime'):
            date_iso = date_value.isoformat()
            date_display = date_value.strftime('%-d %B %Y')
        else:
            try:
                parsed_date = datetime.strptime(str(date_value), '%Y-%m-%d')
            except ValueError as error:
                raise ValueError(
                    f'Featured note {path.name} has invalid date: {date_value!r}'
                ) from error
            date_iso = parsed_date.date().isoformat()
            date_display = parsed_date.strftime('%-d %B %Y')
        featured.append({
            **metadata,
            'href': f'/notes/{path.stem}.html',
            'image_url': '/' + image_path.resolve().relative_to(site_root.resolve()).as_posix(),
            'date_iso': date_iso,
            'date_display': date_display,
        })
    return sorted(featured, key=lambda note: int(note['featured-order']))


def render_featured_note(note):
    categories = ' · '.join(
        html.escape(str(category)) for category in (note.get('categories') or [])[:3]
    )
    href = html.escape(note['href'], quote=True)
    title = html.escape(str(note['title']))
    return f'''<article class="home-note-row">
      <a class="home-note-row-visual" href="{href}" aria-label="Read {title}"><img src="{html.escape(note['image_url'], quote=True)}" alt="{html.escape(str(note['image-alt']), quote=True)}"></a>
      <div class="home-note-row-copy"><div class="home-note-row-meta"><time datetime="{note['date_iso']}">{html.escape(note['date_display'])}</time><span>{categories}</span></div><h3><a href="{href}">{title}</a></h3><p>{html.escape(str(note['description']))}</p><a class="home-note-row-link" href="{href}">Read note <span aria-hidden="true">→</span></a></div>
    </article>'''



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
# Render Quarto fragments with an explicit raw-HTML fence. This avoids the HTML
# being interpreted as literal text when the fragment is included during render.
def render_news_qmd(items, empty_message, searchable=True):
    markup = render_news_component(items, empty_message, searchable=searchable)
    return f"```{{=html}}\n{markup}\n```\n"


def main(site_root=None):
    site_root = site_root or DEFAULT_ROOT
    projects = yaml.safe_load((site_root / 'data/projects.yml').read_text()) or []
    coauthor_urls = yaml.safe_load((site_root / 'data/coauthors.yml').read_text()) or {}
    pubs = load_publications(site_root / 'data/publications.bib')
    featured_notes = load_featured_notes(site_root=site_root)
    lecturer_courses = read_bibtex_entries(site_root / 'data/teaching_lecturer.bib')
    tutor_courses = read_bibtex_entries(site_root / 'data/teaching_tutor.bib')
    news = load_news(site_root=site_root)

    external_assets = validate_local_assets(
        projects,
        pubs,
        [('teaching_lecturer.bib', lecturer_courses), ('teaching_tutor.bib', tutor_courses)],
        site_root=site_root,
    )
    print(f'Asset validation: local references passed; skipped {len(external_assets)} external references.')

    # Long-form project heroes, F1 resource navigation and related-project
    # suggestions are rendered at Quarto render-time by filters/project-components.lua.
    featured_projects = [p for p in projects if p.get('featured') is True][:3]
    project_cards = [render_project_card(p) for p in featured_projects]
    project_archive = [render_project_card(p) for p in projects]
    selected = [p for p in pubs if p.get('selected') is True]
    home_projects_html = '\n'.join(project_cards)
    home_notes_html = '\n'.join(render_featured_note(note) for note in featured_notes)
    projects_portfolio_html = '''<section class="projects-section project-portfolio">
  <div class="section-heading project-page-heading"><div><p class="eyebrow">Selected work</p><span>Projects, implementations and reproducible outputs</span></div></div>
  <div class="projects-card-grid">
''' + '\n'.join(project_archive) + '''
  </div>
</section>'''

    home_pub_rows = [
        render_publication_entry(
            p,
            f"home-list-{p['id']}",
            'home-publication-row',
            pub_actions(p),
            coauthor_urls,
        )
        for p in selected
    ]
    home_publications_html = '\n'.join(home_pub_rows)

    publication_categories = list(dict.fromkeys(p['category'] for p in pubs))
    allbits = []
    for group in publication_categories:
        rows = [
            render_publication_entry(
                p,
                p['id'],
                'home-publication-row publication-archive-row',
                pub_actions(p),
                coauthor_urls,
            )
            for p in pubs
            if p['category'] == group
        ]
        if rows:
            group_id = group.lower().replace(' ', '-')
            allbits.append(
                f'''<section class="publication-category" id="{group_id}"><h2>{group}</h2><div class="publication-category-list">{''.join(rows)}</div></section>'''
            )
    publications_html = '\n'.join(allbits)

    teaching_html = [
        teaching_section(
            'lecturer',
            'Lecturer',
            lecturer_courses,
            teaching_years(lecturer_courses, 'teaching_lecturer.bib'),
        ),
        teaching_section(
            'tutor',
            'Teaching assistant',
            tutor_courses,
            teaching_years(tutor_courses, 'teaching_tutor.bib'),
        ),
    ]
    teaching_list_html = '\n'.join(teaching_html)

    outputs = {
        'data/projects.generated.json': json.dumps(
            projects,
            ensure_ascii=False,
            indent=2,
        ) + '\n',
        'includes/home-projects.html': home_projects_html,
        'includes/home-notes.html': home_notes_html,
        'includes/projects-portfolio.html': projects_portfolio_html,
        'includes/home-publications-list.html': home_publications_html,
        'includes/publications-all.html': publications_html,
        'includes/teaching-list.html': teaching_list_html,
        'includes/home-news.qmd': render_news_qmd(
            news[:8],
            'No recent announcements.',
            searchable=False,
        ),
        'includes/news-all.qmd': render_news_qmd(news, 'No announcements yet.'),
    }
    for relative_path, content in outputs.items():
        (site_root / relative_path).write_text(content, encoding='utf-8')


if __name__ == '__main__':
    main()
