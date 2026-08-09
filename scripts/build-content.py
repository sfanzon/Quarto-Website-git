from sitegen.bibtex import read_bibtex_entries
from sitegen.core import (
    DEFAULT_ROOT,
    is_external_reference,
    local_reference_path,
    read_front_matter,
    validate_local_assets,
)
from sitegen.generator import generate_site
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
    generate_site(site_root=site_root)


if __name__ == '__main__':
    main()
