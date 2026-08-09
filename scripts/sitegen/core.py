"""Shared site root and source-loading utilities."""

import re
from pathlib import Path

import yaml


DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def read_front_matter(path):
    text = path.read_text()
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.DOTALL)
    if not match:
        return {}, text.strip()
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()
