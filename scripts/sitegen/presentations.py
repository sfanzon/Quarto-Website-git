"""Presentation record loading, validation and archive rendering."""

import html

from .bibtex import read_bibtex_entries


PRESENTATION_TYPES = (
    ('talk', 'talks', 'Academic Talks', 'talk'),
    ('poster', 'posters', 'Poster Presentations', 'poster'),
    ('institutional', 'institutional', 'Institutional Presentations', 'institutional'),
)
REQUIRED_FIELDS = ('id', 'title', 'year', 'date', 'venue', 'event_title')


def load_presentations(site_root):
    """Load the canonical BibTeX records, tagged with their archive type."""
    records = []
    for kind, source_name, _, _ in PRESENTATION_TYPES:
        path = site_root / f'data/presentations_{source_name}.bib'
        for record in read_bibtex_entries(path):
            missing = [field for field in REQUIRED_FIELDS if not record.get(field)]
            if missing:
                raise ValueError(
                    f'{path.name} record {record.get("id", "<unknown>")} is missing '
                    + ', '.join(missing)
                )
            record['type'] = kind
            records.append(record)
    ids = [record['id'] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Presentation record IDs must be unique across all types')
    return records


def _presentation_link(record, field, label, icon, asset=False):
    value = record.get(field)
    if not value:
        return ''
    href = value if value.startswith(('http://', 'https://', '/')) else f'/assets/pdf/{value}' if asset else value
    return (
        f'<a class="paper-action" href="{html.escape(href, quote=True)}" '
        f'role="button"><i class="fa-solid {icon}"></i> {label}</a>'
    )


def render_presentations_archive(records):
    """Render type and year groups from presentation records."""
    sections = []
    for kind, _, heading, anchor in PRESENTATION_TYPES:
        typed = [record for record in records if record['type'] == kind]
        groups = []
        for year in sorted({record['year'] for record in typed}, reverse=True):
            entries = []
            for record in [item for item in typed if item['year'] == year]:
                invitation = '<span class="invited-marker" aria-label="Invited contribution">✉</span> ' if record.get('invited') == 'true' else ''
                actions = ''.join([
                    '<button class="paper-action abstract-toggle" type="button">Abstract</button>' if record.get('abstract') else '',
                    _presentation_link(record, 'event_link', 'Event', 'fa-calendar-days'),
                    _presentation_link(record, 'venue_link', 'Venue', 'fa-location-dot'),
                    _presentation_link(record, 'slides', 'Slides', 'fa-display', asset=True),
                    _presentation_link(record, 'poster', 'Poster', 'fa-image', asset=True),
                    _presentation_link(record, 'video', 'Video', 'fa-video'),
                ])
                abstract = f'<div class="abstract hidden"><p>{record["abstract"]}</p></div>' if record.get('abstract') else ''
                entries.append(f'''<div class="row publication-entry" id="{html.escape(record['id'], quote=True)}">
  <div class="col col-sm-2 abbr"><abbr class="badge rounded w-100">{html.escape(record.get('abbr', ''))}</abbr></div>
  <div class="col-sm-8">
    <div class="talk_title">{invitation}{html.escape(record['title'])}</div>
    <div class="conference_title"><em>{html.escape(record['event_title'])}</em></div>
    <div class="conference_venue">{html.escape(record['venue'])}, {html.escape(record['date'])}</div>
    <div class="links archive-actions">{actions}</div>{abstract}
  </div>
</div>''')
            groups.append(f'<h2 class="year archive-year">{html.escape(year)}</h2>\n' + '\n'.join(entries))
        spacing = ' archive-section-heading--spacious' if kind == 'poster' else ''
        sections.append(f'<a id="{anchor}"><h3 class="archive-section-heading{spacing}"><b>{heading}</b></h3></a>\n' + '\n'.join(groups))
    rendered = '<div class="publications">\n' + '\n'.join(sections) + '\n</div>'
    # Markdown treats four-space-indented include lines as code blocks.
    return '\n'.join(line.lstrip() for line in rendered.splitlines())
