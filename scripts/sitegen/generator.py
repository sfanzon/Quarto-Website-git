"""Top-level site content-generation orchestration."""

import json

import yaml

from .assets import validate_local_assets
from .core import DEFAULT_ROOT
from .news import load_news, render_news_component
from .portfolio import load_projects
from .publication_rendering import (
    render_publication_archive,
)
from .presentations import load_presentations, render_presentations_archive
from .publications import load_publications
from .supervision import load_supervision, render_supervision_archive
from .teaching import load_teaching, teaching_section, teaching_years


def generate_site(site_root=None):
    """Generate every data-derived include after validating all source data."""
    site_root = site_root or DEFAULT_ROOT
    projects = load_projects(site_root / 'data/projects.yml')
    coauthor_urls = yaml.safe_load((site_root / 'data/coauthors.yml').read_text()) or {}
    publications = load_publications(site_root / 'data/publications.bib')
    presentations = load_presentations(site_root)
    supervision = load_supervision(site_root)
    teaching_courses = load_teaching(site_root / 'data/teaching.yml')
    lecturer_courses = [
        course for course in teaching_courses if course['role'] == 'lecturer'
    ]
    tutor_courses = [
        course for course in teaching_courses if course['role'] == 'tutor'
    ]
    news = load_news(site_root=site_root)

    external_assets = validate_local_assets(
        projects,
        publications,
        [
            ('teaching.yml', teaching_courses),
        ],
        site_root=site_root,
    )
    print(
        'Asset validation: local references passed; '
        f'skipped {len(external_assets)} external references.'
    )

    # Long-form project heroes, resource navigation and related-project
    # suggestions are rendered at Quarto render-time by the project filter.
    publications_html = render_publication_archive(
        publications,
        coauthor_urls,
    )

    teaching_html = [
        teaching_section(
            'lecturer',
            'Lecturer',
            lecturer_courses,
            teaching_years(lecturer_courses, 'teaching.yml'),
        ),
        teaching_section(
            'tutor',
            'Teaching assistant',
            tutor_courses,
            teaching_years(tutor_courses, 'teaching.yml'),
        ),
    ]

    outputs = {
        'data/projects.generated.json': json.dumps(
            projects,
            ensure_ascii=False,
            indent=2,
        ) + '\n',
        'includes/publications-all.html': publications_html,
        'includes/presentations.html': render_presentations_archive(presentations),
        'includes/supervision.html': render_supervision_archive(supervision),
        'includes/teaching-list.html': '\n'.join(teaching_html),
        'includes/home-news.html': render_news_component(
            news[:8],
            'No recent announcements.',
            searchable=False,
        ),
        'includes/news-all.html': render_news_component(
            news,
            'No announcements yet.',
        ),
    }
    for relative_path, content in outputs.items():
        (site_root / relative_path).write_text(content, encoding='utf-8')
