"""Supervision record loading, validation and archive rendering."""

import html

from .bibtex import read_bibtex_entries


SUPERVISION_TYPES = (
    ('master', 'Master Students', 'master'),
    ('undergraduate', 'Undergraduate Students', 'undergraduate'),
)
REQUIRED_FIELDS = ('id', 'title', 'year', 'venue')


def load_supervision(site_root):
    """Load canonical master’s and undergraduate supervision records."""
    records = []
    for kind, _, _ in SUPERVISION_TYPES:
        path = site_root / f'data/supervision_{kind}.bib'
        for record in read_bibtex_entries(path):
            missing = [field for field in REQUIRED_FIELDS if not record.get(field)]
            if missing:
                raise ValueError(
                    f'{path.name} record {record.get("id", "<unknown>")} is missing '
                    + ', '.join(missing)
                )
            record['supervision_type'] = kind
            records.append(record)
    ids = [record['id'] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Supervision record IDs must be unique across all types')
    return records


def render_supervision_archive(records):
    """Render supervision records grouped by degree level and academic year."""
    sections = []
    for kind, heading, anchor in SUPERVISION_TYPES:
        typed = [record for record in records if record['supervision_type'] == kind]
        groups = []
        for year in sorted({record['year'] for record in typed}, reverse=True):
            entries = []
            for record in [item for item in typed if item['year'] == year]:
                programme = f' · {html.escape(record["type"])}' if record.get('type') else ''
                student = f' — {html.escape(record["addendum"])}' if record.get('addendum') else ''
                abstract = (
                    f'<div class="abstract hidden"><p>{html.escape(record["abstract"])}</p></div>'
                    if record.get('abstract') else ''
                )
                actions = (
                    '<div class="links archive-actions">'
                    '<button class="paper-action abstract-toggle" type="button">Abstract</button>'
                    '</div>' if abstract else ''
                )
                entries.append(f'''<div class="row publication-entry" id="{html.escape(record['id'], quote=True)}">
  <div class="col col-sm-2 abbr"></div>
  <div class="col-sm-8">
    <div class="title">{html.escape(record['title'])}{student}</div>
    <div class="periodical">{html.escape(record['venue'])}{programme}</div>
    {actions}{abstract}
  </div>
</div>''')
            groups.append(f'<h2 class="year archive-year">{html.escape(year)}</h2>\n' + '\n'.join(entries))
        spacing = ' archive-section-heading--spacious' if kind == 'undergraduate' else ''
        sections.append(
            f'<a id="{anchor}"><h3 class="archive-section-heading{spacing}"><b>{heading}</b></h3></a>\n'
            + '\n'.join(groups)
        )
    rendered = '<div class="publications">\n' + '\n'.join(sections) + '\n</div>'
    return '\n'.join(line.lstrip() for line in rendered.splitlines())
