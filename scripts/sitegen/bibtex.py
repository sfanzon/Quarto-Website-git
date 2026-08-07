"""BibTeX parsing for publication and teaching source records."""

import re


def read_bibtex_entries(path):
    """Parse brace-delimited BibTeX entries of any entry type.

    This intentionally supports the subset used by this site while preserving
    nested braces in abstracts, HTML fragments, and LaTeX.
    """
    source = path.read_text()
    records = []
    position = 0
    entry_pattern = re.compile(r'@(\w+)\s*\{', re.IGNORECASE)
    while True:
        match = entry_pattern.search(source, position)
        if not match:
            break
        entry_type = match.group(1).lower()
        start = match.end()
        cursor = start
        depth = 1
        while cursor < len(source) and depth:
            if source[cursor] == '{':
                depth += 1
            elif source[cursor] == '}':
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError(f'Unclosed BibTeX entry in {path.name}')

        # BibTeX declarations are not content records. In particular,
        # @string entries commonly appear before teaching and publication
        # records and must not be validated as if they were courses.
        if entry_type in {'string', 'preamble', 'comment'}:
            position = cursor
            continue

        record = source[start:cursor - 1]
        if ',' not in record:
            raise ValueError(f'Malformed BibTeX entry in {path.name}')
        key, fields_source = record.split(',', 1)
        fields = {'id': key.strip(), 'entrytype': entry_type}
        field_position = 0
        field_pattern = re.compile(r'([\w-]+)\s*=\s*', re.IGNORECASE)
        while True:
            field_match = field_pattern.search(fields_source, field_position)
            if not field_match:
                break
            name = field_match.group(1).lower()
            value_start = field_match.end()
            while value_start < len(fields_source) and fields_source[value_start].isspace():
                value_start += 1

            if value_start >= len(fields_source):
                raise ValueError(
                    f'Missing value for field {name} in {path.name}:{key.strip()}'
                )

            opening = fields_source[value_start]
            if opening == '{':
                value_cursor = value_start + 1
                value_depth = 1
                while value_cursor < len(fields_source) and value_depth:
                    if fields_source[value_cursor] == '{':
                        value_depth += 1
                    elif fields_source[value_cursor] == '}':
                        value_depth -= 1
                    value_cursor += 1
                if value_depth:
                    raise ValueError(
                        f'Unclosed field {name} in {path.name}:{key.strip()}'
                    )
                value = fields_source[value_start + 1:value_cursor - 1]
            elif opening == '"':
                value_cursor = value_start + 1
                escaped = False
                while value_cursor < len(fields_source):
                    char = fields_source[value_cursor]
                    if char == '"' and not escaped:
                        break
                    escaped = char == '\\' and not escaped
                    if char != '\\':
                        escaped = False
                    value_cursor += 1
                if value_cursor >= len(fields_source):
                    raise ValueError(
                        f'Unclosed field {name} in {path.name}:{key.strip()}'
                    )
                value = fields_source[value_start + 1:value_cursor]
                value_cursor += 1
            else:
                comma = fields_source.find(',', value_start)
                value_cursor = len(fields_source) if comma == -1 else comma
                value = fields_source[value_start:value_cursor].strip()

            fields[name] = re.sub(r'\s+', ' ', value).strip()
            field_position = value_cursor
        records.append(fields)
        position = cursor
    return records
