import html
import re
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def read_front_matter(path):
    import yaml
    text = path.read_text()
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.DOTALL)
    if not match:
        return {}, text.strip()
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()


def is_safe_url(url):
    """Validate that a URL uses a safe scheme and is not protocol-relative or pseudo-protocol."""
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    if url.startswith('//'):
        return False
    if url.startswith('/') and not url.startswith('//'):
        return True
    lower = url.lower()
    if lower.startswith(('https://', 'http://', 'mailto:')):
        return True
    return False


TAG_RE = re.compile(r'(</?[a-zA-Z][^>]*>)')
ALLOWED_SIMPLE = {'b', 'strong', 'em', 'i', 'code', 'p'}


def sanitize_html(text):
    """Sanitize inline HTML, preserving safe formatting and anchor tags while neutralizing dangerous tags."""
    if not text or not isinstance(text, str):
        return ''
    tokens = TAG_RE.split(text)
    out = []
    open_a_count = 0
    for token in tokens:
        if not token:
            continue
        if TAG_RE.match(token):
            close_m = re.match(r'^</([a-zA-Z0-9]+)>$', token)
            if close_m:
                tag = close_m.group(1).lower()
                if tag in ALLOWED_SIMPLE:
                    out.append(f'</{tag}>')
                elif tag == 'a' and open_a_count > 0:
                    out.append('</a>')
                    open_a_count -= 1
                else:
                    out.append(html.escape(token))
                continue
            if re.match(r'^<br\s*/?>$', token, re.IGNORECASE):
                out.append('<br>')
                continue
            open_m = re.match(r'^<([a-zA-Z0-9]+)>$', token)
            if open_m:
                tag = open_m.group(1).lower()
                if tag in ALLOWED_SIMPLE:
                    out.append(f'<{tag}>')
                else:
                    out.append(html.escape(token))
                continue
            a_m = re.match(r'^<a\s+([^>]+)>$', token, re.IGNORECASE)
            if a_m:
                href_m = re.search(
                    r'\bhref\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))',
                    a_m.group(1),
                    re.IGNORECASE,
                )
                if href_m:
                    raw_href = href_m.group(1) or href_m.group(2) or href_m.group(3)
                    for route in ('publications', 'teaching', 'research', 'about', 'expertise', 'projects'):
                        raw_href = re.sub(rf'^/{route}(?:\.html|/)?(?=#|$)', f'/{route}/', raw_href)
                    raw_href = re.sub(r'^/presentations(?:\.html|/)?(?=#|$)', '/presentations/', raw_href)
                    if is_safe_url(raw_href):
                        out.append(f'<a href="{html.escape(raw_href, quote=True)}">')
                        open_a_count += 1
                        continue
            out.append(html.escape(token))
        else:
            escaped = html.escape(token, quote=False)
            escaped = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', escaped)
            out.append(escaped)
    while open_a_count > 0:
        out.append('</a>')
        open_a_count -= 1
    return ''.join(out)
