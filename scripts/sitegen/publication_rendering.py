"""HTML rendering for normalized publication records."""

import html

from .publications import publication_abstract_html


def action_icon(label):
    # Journal and arXiv are both official reading destinations, so they share
    # one clean publication icon on the homepage and Publications page.
    icons = {
        'Journal': 'fa-book-open',
        'arXiv': 'fa-book-open',
        'Repository': 'fa-building-columns',
        'Book': 'fa-book',
        'External': 'fa-arrow-up-right-from-square',
        'Code': 'fa-code',
        'Slides': 'fa-display',
        'Poster': 'fa-image',
        'Video': 'fa-circle-play',
    }
    return icons.get(label, 'fa-link')


def publication_paper_href(publication):
    """Return the website-hosted PDF, even when the lightweight repo omits the file."""
    return publication.get('pdf', '')


def publication_external_link(publication):
    """Return the article's official journal page, or arXiv for a preprint."""
    if publication.get('preprint'):
        # Prefer an explicit arXiv URL already stored in standard citation fields.
        for field in ('html', 'url', 'doi'):
            value = publication.get(field, '')
            if value and 'arxiv.org' in value.lower():
                return ('arXiv', value)
        arxiv_id = publication.get('arxiv', '')
        if arxiv_id:
            href = (
                arxiv_id
                if arxiv_id.startswith(('http://', 'https://'))
                else f'https://arxiv.org/abs/{arxiv_id}'
            )
            return ('arXiv', href)
        return ('', '')

    destination = publication.get('html') or publication.get('url')
    doi = publication.get('doi', '')

    if publication.get('entrytype') == 'article':
        if destination and 'arxiv.org' not in destination.lower():
            return ('Journal', destination)
        if doi and 'arxiv.org' not in doi.lower():
            href = (
                doi
                if doi.startswith(('http://', 'https://'))
                else f'https://doi.org/{doi}'
            )
            return ('Journal', href)
        return ('', '')

    # Non-journal records use an accurate official-source label and avoid a
    # duplicate link when their URL is simply the same website-hosted PDF.
    if (
        destination
        and publication.get('pdf')
        and destination.rstrip('/').endswith(publication['pdf'].rstrip('/'))
    ):
        destination = ''
    if publication.get('entrytype') in {'phdthesis', 'mastersthesis'} and destination:
        return ('Repository', destination)
    if publication.get('entrytype') == 'book' and destination:
        return ('Book', destination)
    if destination:
        return ('External', destination)
    return ('', '')


def publication_theme_pills(publication):
    if not publication.get('themes'):
        return ''
    pills = ''.join(
        f'<span class="publication-theme">{html.escape(theme)}</span>'
        for theme in publication['themes']
    )
    return f'<div class="publication-themes" aria-label="Research themes">{pills}</div>'


def pub_actions(publication, toggles=True):
    """Render a compact publication action hierarchy.

    The homepage and full archive use the same visible PDF, official
    destination, citation, explainer and presentation actions.
    """
    actions = []
    paper_href = publication_paper_href(publication)
    if paper_href:
        actions.append(
            f'<a class="paper-action publication-primary-action" href="{html.escape(paper_href, quote=True)}"><i class="fa-solid fa-file-pdf"></i> PDF</a>'
        )
    external_label, external_href = publication_external_link(publication)
    if external_href:
        actions.append(
            f'<a class="paper-action" href="{html.escape(external_href, quote=True)}"><i class="fa-solid {action_icon(external_label)}"></i> {external_label}</a>'
        )
    if toggles and publication.get('abstract'):
        actions.append('<button class="paper-action abstract-toggle" type="button"><i class="fa-regular fa-file-lines"></i> Abstract</button>')
    if toggles:
        actions.append('<button class="paper-action bibtex-toggle" type="button"><i class="fa-solid fa-quote-right"></i> Cite</button>')
    if publication.get('explainer'):
        actions.append(
            f'<a class="paper-action" href="{html.escape(publication["explainer"], quote=True)}"><i class="fa-solid fa-lightbulb"></i> Explainer</a>'
        )
    if publication.get('code'):
        actions.append(
            f'<a class="paper-action" href="{html.escape(publication["code"], quote=True)}"><i class="fa-solid {action_icon("Code")}"></i> Code</a>'
        )
    for field, label in (('slides', 'Slides'), ('poster', 'Poster'), ('video', 'Video')):
        if publication.get(field):
            actions.append(
                f'<a class="paper-action" href="{html.escape(publication[field], quote=True)}"><i class="fa-solid {action_icon(label)}"></i> {label}</a>'
            )
    return ''.join(actions)


def publication_side_meta(publication):
    """Research-theme labels for the responsive publication rail."""
    return (
        '<div class="publication-theme-rail">'
        f'{publication_theme_pills(publication)}'
        '</div>'
    )


def linked_authors(authors, coauthor_urls=None):
    result = authors.replace(
        '<em>Silvio Fanzon</em>',
        '<span class="author-self">Silvio Fanzon</span>',
    )
    for name, url in (coauthor_urls or {}).items():
        result = result.replace(name, f'<a class="author-link" href="{url}">{name}</a>')
    return result


def render_publication_entry(
    publication,
    row_id,
    row_classes,
    actions,
    coauthor_urls=None,
):
    authors = linked_authors(publication['authors'], coauthor_urls)
    side_meta = publication_side_meta(publication)
    return f'''<article class="{row_classes} publication-entry" id="{html.escape(row_id, quote=True)}"><div class="home-publication-main pub-main"><h3>{publication['title']}</h3><div class="paper-meta"><span class="publication-authors">{authors}</span><span class="publication-periodical">{publication['periodical']}</span></div><div class="paper-actions">{actions}</div><div class="abstract hidden">{publication_abstract_html(publication)}</div><div class="bibtex hidden"><pre><code>{html.escape(publication['bibtex'])}</code></pre></div></div>{side_meta}</article>'''


def render_selected_publications(publications, coauthor_urls):
    selected = [
        publication
        for publication in publications
        if publication.get('selected') is True
    ]
    return '\n'.join(
        render_publication_entry(
            publication,
            f"home-list-{publication['id']}",
            'home-publication-row',
            pub_actions(publication),
            coauthor_urls,
        )
        for publication in selected
    )


def render_publication_archive(publications, coauthor_urls):
    categories = list(dict.fromkeys(
        publication['category']
        for publication in publications
    ))
    sections = []
    for group in categories:
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
            sections.append(
                f'''<section class="publication-category" id="{group_id}"><h2>{group}</h2><div class="publication-category-list">{''.join(rows)}</div></section>'''
            )
    return '\n'.join(sections)
