"""Publication validation and normalization."""

import html
import re

from .bibtex import read_bibtex_entries


PUBLICATION_WEBSITE_FIELDS = {
    'category', 'abbr', 'selected', 'preprint', 'arxiv', 'abstract', 'pdf', 'code', 'slides',
    'poster', 'video', 'explainer', 'bibtex_show', 'author+an', 'altmetric',
    'dimensions', 'google_scholar_id', 'scopus', 'sjr', 'themes',
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
    year = html.escape(entry['year'])
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
    seen_ids = set()
    for record in records:
        missing = sorted(field for field in required if not record.get(field))
        if missing:
            raise ValueError(
                f'Publication {record.get("id", "<unknown>")} is missing required '
                f'BibTeX fields: {", ".join(missing)}'
            )
        if record['id'] in seen_ids:
            raise ValueError(
                f'{path.name} has duplicate publication id: {record["id"]}'
            )
        seen_ids.add(record['id'])
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
        record['themes'] = [
            theme.strip()
            for theme in record.get('themes', '').split(';')
            if theme.strip()
        ][:2]
        record['bibtex'] = publication_bibtex(record)
        publications.append(record)
    return publications
