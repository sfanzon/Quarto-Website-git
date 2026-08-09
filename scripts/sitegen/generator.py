"""Top-level site content-generation orchestration."""

import json

import yaml

from .bibtex import read_bibtex_entries
from .core import DEFAULT_ROOT, validate_local_assets
from .news import load_news, render_news_qmd
from .portfolio import (
    load_featured_notes,
    render_featured_note,
    render_featured_projects,
    render_projects_portfolio,
)
from .publications import (
    load_publications,
    render_publication_archive,
    render_selected_publications,
)
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
    home_projects_html = render_featured_projects(projects)
    home_notes_html = '\n'.join(
        render_featured_note(note)
        for note in featured_notes
    )
    projects_portfolio_html = render_projects_portfolio(projects)
    home_publications_html = render_selected_publications(
        publications,
        coauthor_urls,
    )
    publications_html = render_publication_archive(
        publications,
        coauthor_urls,
    )

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
