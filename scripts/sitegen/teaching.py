"""Teaching record validation and HTML rendering."""

import html
import re


ACADEMIC_YEAR_PATTERN = re.compile(r'^(?P<start>\d{4})/(?P<end>\d{2})$')


def teaching_link(value, asset=False):
    if value.startswith(('http://', 'https://', '/')):
        return value
    return f'/assets/pdf/{value}' if asset else value


def teaching_actions(course):
    actions = []
    if course.get('abstract'):
        actions.append(
            '<button class="teaching-action abstract-toggle" type="button">'
            '<i class="fa-regular fa-file-lines"></i> About</button>'
        )
    links = [
        ('html', 'HTML', 'fa-code', False),
        ('lecturenotes', 'Notes', 'fa-book-open', True),
        ('lectureslides', 'Slides', 'fa-display', False),
        ('revision', 'Revision', 'fa-list-check', False),
        ('webpage', 'Course page', 'fa-arrow-up-right-from-square', False),
        ('canvas', 'Canvas', 'fa-graduation-cap', False),
        ('taster', 'Taster', 'fa-file-pdf', True),
    ]
    for field, label, icon, asset in links:
        if course.get(field):
            value = course[field]
            if field == 'webpage':
                public_url = course.get('url', '')
                if '/blog/' in public_url:
                    value = public_url
                elif value.startswith('/'):
                    value = f'https://www.silviofanzon.com{value}'
            href = teaching_link(value, asset)
            actions.append(
                f'<a class="teaching-action" href="{html.escape(href, quote=True)}">'
                f'<i class="fa-solid {icon}"></i> {label}</a>'
            )
    return ''.join(actions)


def teaching_years(courses, source_name):
    """Return validated academic years in descending chronological order."""
    years = set()
    for course in courses:
        value = str(course.get('yearacademic', '')).strip()
        if not value:
            raise ValueError(
                f'Teaching record {course.get("id", "<unknown>")} in '
                f'{source_name} is missing yearacademic'
            )
        match = ACADEMIC_YEAR_PATTERN.fullmatch(value)
        if not match:
            raise ValueError(
                f'Teaching record {course.get("id", "<unknown>")} in '
                f'{source_name} has invalid yearacademic: {value!r} '
                '(expected YYYY/YY)'
            )
        start = int(match.group('start'))
        expected_end = f'{(start + 1) % 100:02d}'
        if match.group('end') != expected_end:
            raise ValueError(
                f'Teaching record {course.get("id", "<unknown>")} in '
                f'{source_name} has non-consecutive yearacademic: {value!r}'
            )
        years.add(value)
    return sorted(years, key=lambda year: int(year[:4]), reverse=True)


def teaching_section(section_id, heading, courses, years):
    year_sections = []
    for academic_year in years:
        year_courses = [
            course
            for course in courses
            if course.get('yearacademic') == academic_year
        ]
        year_courses.sort(key=lambda course: int(course.get('year', 0)), reverse=True)
        entries = []
        for course in year_courses:
            degree_line = ' · '.join(
                item
                for item in [course.get('degree'), course.get('courseyear')]
                if item
            )
            institution = course.get('venue', '')
            meta = ' · '.join(item for item in [institution, degree_line] if item)
            actions = teaching_actions(course)
            actions_html = (
                f'<div class="teaching-actions">{actions}</div>'
                if actions else ''
            )
            abstract_html = (
                f'<div class="abstract hidden">{course["abstract"]}</div>'
                if course.get('abstract') else ''
            )
            entries.append(f'''<article class="teaching-course publication-entry" id="{html.escape(course['id'], quote=True)}">
              <div class="teaching-course-main">
                <h4>{html.escape(course.get('title', 'Untitled course'))}</h4>
                <p class="teaching-meta">{html.escape(meta)}</p>
                {actions_html}{abstract_html}
              </div>
            </article>''')
        if entries:
            year_sections.append(f'''<section class="teaching-year">
              <h3>{html.escape(academic_year)}</h3>
              <div class="teaching-course-list">{''.join(entries)}</div>
            </section>''')
    return f'''<section class="teaching-role" id="{section_id}">
      <h2>{heading}</h2>
      <div class="teaching-years">{''.join(year_sections)}</div>
    </section>'''
