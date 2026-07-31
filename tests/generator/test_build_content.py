import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "build-content.py"
spec = importlib.util.spec_from_file_location("build_content", SCRIPT)
build_content = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_content)


class BuildContentTests(unittest.TestCase):
    def write_fixture(self, content, name="fixture.txt"):
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / name
        path.write_text(content, encoding="utf-8")
        self.addCleanup(directory.cleanup)
        return path

    def test_front_matter_valid_and_missing(self):
        valid = self.write_fixture("---\ntitle: Example\n---\nBody")
        metadata, body = build_content.read_front_matter(valid)
        self.assertEqual(metadata, {"title": "Example"})
        self.assertEqual(body, "Body")
        plain = self.write_fixture("Plain body")
        self.assertEqual(build_content.read_front_matter(plain), ({}, "Plain body"))

    def test_front_matter_malformed_yaml_fails(self):
        invalid = self.write_fixture("---\ntitle: [broken\n---\nBody")
        with self.assertRaises(yaml.YAMLError):
            build_content.read_front_matter(invalid)

    def test_bibtex_parser_handles_nested_quoted_numeric_and_string(self):
        source = """@string{venue = \"Journal\"}
@article{example,
  title = {A {nested} title},
  year = 2025,
  note = \"quoted, value\",
  journal = {Journal of Tests}
}
"""
        record = build_content.read_bibtex_entries(self.write_fixture(source, "fixture.bib"))[0]
        self.assertEqual(record["id"], "example")
        self.assertEqual(record["title"], "A {nested} title")
        self.assertEqual(record["year"], "2025")
        self.assertEqual(record["note"], "quoted, value")
        self.assertEqual(record["journal"], "Journal of Tests")

    def test_bibtex_parser_rejects_unclosed_entries(self):
        with self.assertRaises(ValueError):
            build_content.read_bibtex_entries(self.write_fixture("@article{broken,\n title = {x}\n"))

    def test_publication_validation_rejects_missing_fields_and_invalid_flags(self):
        missing = "@article{id, title = {Title}}"
        with self.assertRaisesRegex(ValueError, "missing required"):
            build_content.load_publications(self.write_fixture(missing, "publications.bib"))
        invalid = """@article{id,
  category = {Articles}, abbr = {A}, title = {Title}, author = {Author},
  year = {2025}, selected = {maybe}, preprint = {false}, journal = {Journal}
}"""
        with self.assertRaisesRegex(ValueError, "selected"):
            build_content.load_publications(self.write_fixture(invalid, "publications.bib"))

    def test_publication_validation_rejects_missing_venue(self):
        source = """@article{id,
  category = {Articles}, abbr = {A}, title = {Title}, author = {Author},
  year = {2025}, selected = {false}, preprint = {false}
}"""
        with self.assertRaisesRegex(ValueError, "venue"):
            build_content.load_publications(self.write_fixture(source, "publications.bib"))

    def test_teaching_years_are_validated_and_sorted(self):
        courses = [{"id": "new", "yearacademic": "2025/26"}, {"id": "old", "yearacademic": "2020/21"}]
        self.assertEqual(build_content.teaching_years(courses, "teaching.bib"), ["2025/26", "2020/21"])
        with self.assertRaisesRegex(ValueError, "missing yearacademic"):
            build_content.teaching_years([{"id": "missing"}], "teaching.bib")
        with self.assertRaisesRegex(ValueError, "invalid yearacademic"):
            build_content.teaching_years([{"id": "invalid", "yearacademic": "2025"}], "teaching.bib")
        with self.assertRaisesRegex(ValueError, "non-consecutive"):
            build_content.teaching_years([{"id": "invalid", "yearacademic": "2025/27"}], "teaching.bib")

    def test_news_helpers_validate_dates_and_convert_links(self):
        self.assertIn("/publications.html#item", build_content.news_inline_html('<a href="/publications/#item">Read</a>'))
        self.assertTrue(build_content.news_summary("A short sentence.").endswith("."))
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        invalid_news = Path(directory.name) / "news"
        invalid_news.mkdir()
        (invalid_news / "not-a-date.md").write_text("Update", encoding="utf-8")
        original_root = build_content.root
        build_content.root = Path(directory.name)
        try:
            with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                build_content.load_news()
        finally:
            build_content.root = original_root

    def test_project_card_renders_valid_yaml_data(self):
        project = {
            "title": "Example project",
            "summary": "A test project.",
            "image": "assets/img/projects/example.svg",
            "href": "projects/example/index.html",
            "labels": ["Testing"],
        }
        rendered = build_content.render_project_card(project)
        self.assertIn("Example project", rendered)
        self.assertIn("assets/img/projects/example.svg", rendered)


if __name__ == "__main__":
    unittest.main()
