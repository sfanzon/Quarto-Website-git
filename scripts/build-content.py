from datetime import datetime
import html, json, yaml

from sitegen.bibtex import read_bibtex_entries
from sitegen.core import (
    DEFAULT_ROOT,
    is_external_reference,
    local_reference_path,
    read_front_matter,
    validate_local_assets,
)
from sitegen.news import (
    display_news_date,
    load_news,
    news_body_html,
    news_inline_html,
    news_summary,
    render_news_component,
    render_news_qmd,
)
from sitegen.publications import (
    PUBLICATION_WEBSITE_FIELDS,
    action_icon,
    format_author_name,
    linked_authors,
    load_publications,
    pub_actions,
    publication_abstract_html,
    publication_authors,
    publication_bibtex,
    publication_external_link,
    publication_paper_href,
    publication_periodical,
    publication_side_meta,
    publication_theme_pills,
    publication_venue,
    render_publication_entry,
)
from sitegen.teaching import (
    ACADEMIC_YEAR_PATTERN,
    teaching_actions,
    teaching_link,
    teaching_section,
    teaching_years,
)


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
