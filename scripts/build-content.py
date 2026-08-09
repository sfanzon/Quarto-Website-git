import json, yaml

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
from sitegen.portfolio import (
    load_featured_notes,
    render_featured_note,
    render_project_card,
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
