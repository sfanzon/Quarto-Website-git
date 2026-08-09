"""Top-level site content-generation orchestration."""

import json

import yaml

from .bibtex import read_bibtex_entries
from .core import DEFAULT_ROOT, validate_local_assets
from .news import load_news, render_news_qmd
from .portfolio import load_featured_notes, render_featured_note, render_project_card
from .publications import load_publications, pub_actions, render_publication_entry
from .teaching import teaching_section, teaching_years


def generate_site(site_root=None):
    """Generate every data-derived include after validating all source data."""
    site_root = site_root or DEFAULT_ROOT
    projects = yaml.safe_load((site_root / 'data/projects.yml').read_text()) or []
    coauthor_urls = yaml.safe_load((site_root / 'data/coauthors.yml').read_text()) or {}
    publications = load_publications(site_root / 'data/publications.bib')
    featured_notes = load_featured_notes(site_root=site_root)
    lecturer_courses = read_bibtex_entries(
        site_root / 'data/teaching_lecturer.bib'
    )
    tutor_courses = read_bibtex_entries(
        site_root / 'data/teaching_tutor.bib'
    )
    news = load_news(site_root=site_root)

    external_assets = validate_local_assets(
        projects,
        publications,
        [
            ('teaching_lecturer.bib', lecturer_courses),
            ('teaching_tutor.bib', tutor_courses),
        ],
        site_root=site_root,
    )
    print(
        'Asset validation: local references passed; '
        f'skipped {len(external_assets)} external references.'
    )

    # Long-form project heroes, resource navigation and related-project
    # suggestions are rendered at Quarto render-time by the project filter.
    featured_projects = [
        project
        for project in projects
        if project.get('featured') is True
    ][:3]
    project_cards = [render_project_card(project) for project in featured_projects]
    project_archive = [render_project_card(project) for project in projects]
    selected_publications = [
        publication
        for publication in publications
        if publication.get('selected') is True
    ]
    home_projects_html = '\n'.join(project_cards)
    home_notes_html = '\n'.join(
        render_featured_note(note)
        for note in featured_notes
    )
    projects_portfolio_html = '''<section class="projects-section project-portfolio">
  <div class="section-heading project-page-heading"><div><p class="eyebrow">Selected work</p><span>Projects, implementations and reproducible outputs</span></div></div>
  <div class="projects-card-grid">
''' + '\n'.join(project_archive) + '''
  </div>
</section>'''

    home_publication_rows = [
        render_publication_entry(
            publication,
            f"home-list-{publication['id']}",
            'home-publication-row',
            pub_actions(publication),
            coauthor_urls,
        )
        for publication in selected_publications
    ]
    home_publications_html = '\n'.join(home_publication_rows)

    publication_categories = list(dict.fromkeys(
        publication['category']
        for publication in publications
    ))
    publication_sections = []
    for group in publication_categories:
        rows = [
            render_publication_entry(
                publication,
                publication['id'],
                'home-publication-row publication-archive-row',
                pub_actions(publication),
                coauthor_urls,
            )
            for publication in publications
            if publication['category'] == group
        ]
        if rows:
            group_id = group.lower().replace(' ', '-')
            publication_sections.append(
                f'''<section class="publication-category" id="{group_id}"><h2>{group}</h2><div class="publication-category-list">{''.join(rows)}</div></section>'''
            )
    publications_html = '\n'.join(publication_sections)

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
        'includes/teaching-list.html': '\n'.join(teaching_html),
        'includes/home-news.qmd': render_news_qmd(
            news[:8],
            'No recent announcements.',
            searchable=False,
        ),
        'includes/news-all.qmd': render_news_qmd(
            news,
            'No announcements yet.',
        ),
    }
    for relative_path, content in outputs.items():
        (site_root / relative_path).write_text(content, encoding='utf-8')
