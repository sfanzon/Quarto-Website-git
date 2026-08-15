"""Project metadata loading and validation."""

import yaml

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
