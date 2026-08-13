"""Local-reference resolution and source asset validation."""

import re
from pathlib import Path
from urllib.parse import urlsplit

from .core import DEFAULT_ROOT


def is_external_reference(value):
    """Return whether a reference is intentionally outside this repository."""
    if not isinstance(value, str):
        return False
    return bool(
        re.match(
            r'^(?:https?:|mailto:|tel:|data:|javascript:|//)',
            value.strip(),
            re.I,
        )
    )


def local_reference_path(value, base=None, site_root=None):
    """Resolve a generated/local URL to its source or rendered file.

    Quarto URLs are checked against the source tree before rendering: an HTML
    route may legitimately correspond to a .qmd source file.
    """
    if not isinstance(value, str) or not value.strip() or is_external_reference(value):
        return None
    site_root = site_root or DEFAULT_ROOT
    path = urlsplit(value.strip()).path
    candidate = (
        site_root / path.lstrip('/')
        if path.startswith('/')
        else (base or site_root) / path
    )
    candidates = [candidate]
    if path.startswith('/'):
        route = path.strip('/')
        astro_pages = site_root / 'astro' / 'src' / 'pages'
        if route:
            candidates.extend([
                astro_pages / f'{route}.astro',
                astro_pages / route / 'index.astro',
            ])
        else:
            candidates.append(astro_pages / 'index.astro')
    if candidate.is_dir():
        candidates.extend([candidate / 'index.html', candidate / 'index.qmd'])
    if candidate.suffix.lower() == '.html':
        candidates.append(candidate.with_suffix('.qmd'))
    if candidate.name == 'index.html':
        candidates.append(candidate.with_name('index.qmd'))
    return next((item for item in candidates if item.is_file()), candidate)


def validate_local_assets(projects, publications, teaching_courses, site_root=None):
    """Validate repository references and return external links skipped.

    Local references fail together so a single build reports every broken
    source value. External URLs are deliberately non-blocking and are returned
    separately for an audit summary; no network requests are made here.
    """
    site_root = site_root or DEFAULT_ROOT
    missing = []
    external = []

    def check(value, label, base=None, asset_prefix=None):
        if not isinstance(value, str) or not value.strip():
            return
        value = value.strip()
        if is_external_reference(value):
            external.append((label, value))
            return
        generated = (
            f'/{asset_prefix.strip("/")}/{value.lstrip("/")}'
            if asset_prefix else value
        )
        target = local_reference_path(
            generated,
            base=base,
            site_root=site_root,
        )
        if target is None or not target.is_file():
            missing.append(f'{label}: {value} (expected {target})')

    for project in projects:
        project_id = project.get('id', '<unknown project>')
        check(project.get('image'), f'project {project_id} image')
        project_href = project.get('href')
        check(project_href, f'project {project_id} href')
        project_base = (
            site_root / Path(urlsplit(project_href or '').path).parent
            if project_href else site_root
        )
        article = project.get('article') or {}
        for resource in article.get('resources') or []:
            check(
                resource.get('href'),
                f'project {project_id} resource {resource.get("label", "<unnamed>")}',
            )
        for view in article.get('views') or []:
            check(
                view.get('href'),
                f'project {project_id} view {view.get("id", "<unnamed>")}',
                base=project_base,
            )
        for field in ('code', 'download', 'zip', 'pdf', 'slides', 'poster'):
            if field in project:
                check(project[field], f'project {project_id} {field}')

    for publication in publications:
        publication_id = publication.get('id', '<unknown publication>')
        for field in ('pdf', 'slides', 'poster', 'explainer', 'code', 'video'):
            if field in publication:
                check(publication[field], f'publication {publication_id} {field}')

    for source_name, courses in teaching_courses:
        for course in courses:
            course_id = course.get('id', '<unknown course>')
            for field in (
                'html',
                'lecturenotes',
                'lectureslides',
                'revision',
                'webpage',
                'canvas',
                'taster',
            ):
                value = course.get(field)
                if not value:
                    continue
                # Teaching course pages beginning with / are rewritten by
                # teaching_actions() to the canonical public site URL.
                if field == 'webpage' and str(value).startswith('/'):
                    external.append((f'{source_name} {course_id} {field}', value))
                    continue
                asset_prefix = (
                    'assets/pdf'
                    if field in {'lecturenotes', 'taster'} else None
                )
                check(
                    value,
                    f'{source_name} {course_id} {field}',
                    asset_prefix=asset_prefix,
                )

    if missing:
        raise ValueError('Local asset validation failed:\n- ' + '\n- '.join(missing))
    return external
