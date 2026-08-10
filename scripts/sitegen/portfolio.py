"""Project-card and featured-note loading and rendering."""

import html
from datetime import datetime

import yaml

from .assets import local_reference_path
from .core import DEFAULT_ROOT, read_front_matter


PROJECT_REQUIRED_FIELDS = ('id', 'title', 'summary', 'image', 'href', 'labels')


def load_projects(path):
    """Load project metadata used by both generated cards and the Lua filter.

    Project IDs are lookup keys in ``projects.generated.json``.  They must be
    unique so a later record cannot silently replace an earlier project while
    Quarto renders a long-form article.
    """
    projects = yaml.safe_load(path.read_text(encoding='utf-8')) or []
    if not isinstance(projects, list):
        raise ValueError(f'{path.name} must contain a YAML list of projects')

    seen_ids = set()
    for index, project in enumerate(projects, start=1):
        if not isinstance(project, dict):
            raise ValueError(f'{path.name} entry {index} must be a mapping')
        missing = [field for field in PROJECT_REQUIRED_FIELDS if not project.get(field)]
        if missing:
            raise ValueError(
                f'{path.name} entry {index} is missing required field(s): '
                + ', '.join(missing)
            )
        project_id = project['id']
        if project_id in seen_ids:
            raise ValueError(f'{path.name} has duplicate project id: {project_id}')
        seen_ids.add(project_id)
        if not isinstance(project['labels'], list) or not all(
            isinstance(label, str) and label.strip() for label in project['labels']
        ):
            raise ValueError(f'{path.name} project {project_id} labels must be a non-empty list')
        if 'featured' in project and not isinstance(project['featured'], bool):
            raise ValueError(f'{path.name} project {project_id} featured must be true or false')
        if 'related' in project and (
            not isinstance(project['related'], list)
            or not all(isinstance(related_id, str) and related_id for related_id in project['related'])
        ):
            raise ValueError(f'{path.name} project {project_id} related must be a list of project IDs')

    known_ids = {project['id'] for project in projects}
    for project in projects:
        unknown = sorted(set(project.get('related', [])) - known_ids)
        if unknown:
            raise ValueError(
                f'{path.name} project {project["id"]} has unknown related project ID(s): '
                + ', '.join(unknown)
            )
    return projects


def render_project_card(project):
    """Render a project card for the homepage or Projects archive."""
    labels = ' · '.join(
        html.escape(label)
        for label in project.get('labels', [])[:3]
    )
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


def render_featured_projects(projects, limit=3):
    featured = [project for project in projects if project.get('featured') is True]
    return '\n'.join(
        render_project_card(project)
        for project in featured[:limit]
    )


def render_projects_portfolio(projects):
    cards = '\n'.join(render_project_card(project) for project in projects)
    return '''<section class="projects-section project-portfolio">
  <div class="section-heading project-page-heading"><div><p class="eyebrow">Selected work</p><span>Projects, implementations and reproducible outputs</span></div></div>
  <div class="projects-card-grid">
''' + cards + '''
  </div>
</section>'''


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
        missing = [
            field
            for field in required
            if metadata.get(field) in (None, '')
        ]
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
            'image_url': '/' + image_path.resolve().relative_to(
                site_root.resolve()
            ).as_posix(),
            'date_iso': date_iso,
            'date_display': date_display,
        })
    return sorted(featured, key=lambda note: int(note['featured-order']))


def render_featured_note(note):
    categories = ' · '.join(
        html.escape(str(category))
        for category in (note.get('categories') or [])[:3]
    )
    href = html.escape(note['href'], quote=True)
    title = html.escape(str(note['title']))
    return f'''<article class="home-note-row">
      <a class="home-note-row-visual" href="{href}" aria-label="Read {title}"><img src="{html.escape(note['image_url'], quote=True)}" alt="{html.escape(str(note['image-alt']), quote=True)}"></a>
      <div class="home-note-row-copy"><div class="home-note-row-meta"><time datetime="{note['date_iso']}">{html.escape(note['date_display'])}</time><span>{categories}</span></div><h3><a href="{href}">{title}</a></h3><p>{html.escape(str(note['description']))}</p><a class="home-note-row-link" href="{href}">Read note <span aria-hidden="true">→</span></a></div>
    </article>'''
