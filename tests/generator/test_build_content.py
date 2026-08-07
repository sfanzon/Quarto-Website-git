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
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            build_content.load_news(site_root=Path(directory.name))

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

    def test_featured_notes_are_validated_sorted_and_rendered(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        fixture_root = Path(directory.name)
        notes_dir = fixture_root / "notes"
        image_dir = fixture_root / "assets" / "img" / "notes"
        notes_dir.mkdir(parents=True)
        image_dir.mkdir(parents=True)
        (image_dir / "first.svg").write_text("<svg/>", encoding="utf-8")
        (image_dir / "second.svg").write_text("<svg/>", encoding="utf-8")
        template = """---
title: "{title}"
description: "{description}"
date: 2026-07-{day}
image: ../assets/img/notes/{image}
image-alt: "{alt}"
featured: true
featured-order: {order}
categories: [AI, Workflow]
---
Body text.
"""
        (notes_dir / "second.qmd").write_text(
            template.format(title="Second", description="Second note.", day=20, image="second.svg", alt="Second visual", order=2),
            encoding="utf-8",
        )
        (notes_dir / "first.qmd").write_text(
            template.format(title="First", description="First note.", day=21, image="first.svg", alt="First visual", order=1),
            encoding="utf-8",
        )
        notes = build_content.load_featured_notes(notes_dir, site_root=fixture_root)
        self.assertEqual([note["title"] for note in notes], ["First", "Second"])
        self.assertEqual(notes[0]["href"], "/notes/first.html")
        self.assertEqual(notes[0]["image_url"], "/assets/img/notes/first.svg")
        rendered = build_content.render_featured_note(notes[0])
        self.assertIn("First note.", rendered)
        self.assertIn('alt="First visual"', rendered)

    def test_local_asset_validation_checks_assets_and_skips_external_urls(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        fixture_root = Path(directory.name)
        (fixture_root / "assets/pdf").mkdir(parents=True)
        (fixture_root / "assets/pdf/notes.pdf").write_bytes(b"pdf")
        (fixture_root / "assets/img").mkdir(parents=True)
        (fixture_root / "assets/img/project.svg").write_text("<svg/>", encoding="utf-8")
        (fixture_root / "projects/demo").mkdir(parents=True)
        (fixture_root / "projects/demo/index.qmd").write_text("# Demo", encoding="utf-8")
        external = build_content.validate_local_assets(
            [{"id": "demo", "image": "assets/img/project.svg", "href": "projects/demo/index.html"}],
            [{"id": "pub", "pdf": "/assets/pdf/notes.pdf", "code": "https://github.com/example/repo"}],
            [("teaching.bib", [{"id": "course", "taster": "notes.pdf", "webpage": "/blog/course"}])],
            site_root=fixture_root,
        )
        self.assertEqual(len(external), 2)

    def test_local_asset_validation_reports_all_missing_references(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, "project demo image") as context:
            build_content.validate_local_assets(
                [{"id": "demo", "image": "missing.svg", "href": "missing.html"}],
                [{"id": "pub", "pdf": "/missing.pdf"}],
                [],
                site_root=Path(directory.name),
            )
        self.assertIn("publication pub pdf", str(context.exception))

    def test_main_generates_complete_deterministic_output(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        fixture_root = Path(directory.name)

        for relative_directory in (
            "assets/img/notes",
            "data",
            "includes",
            "news",
            "notes",
        ):
            (fixture_root / relative_directory).mkdir(parents=True)

        (fixture_root / "assets/img/notes/example.svg").write_text(
            "<svg xmlns=\"http://www.w3.org/2000/svg\"/>",
            encoding="utf-8",
        )
        (fixture_root / "data/projects.yml").write_text(
            """- id: example
  title: Example project
  summary: A generated project card.
  image: https://example.com/project.svg
  href: https://example.com/project
  labels: [Modelling, Software]
  featured: true
""",
            encoding="utf-8",
        )
        (fixture_root / "data/coauthors.yml").write_text(
            "Ada Lovelace: https://example.com/ada\n",
            encoding="utf-8",
        )
        (fixture_root / "data/publications.bib").write_text(
            """@article{example,
  category = {Articles},
  abbr = {JT},
  title = {A deterministic publication},
  author = {Ada Lovelace and Silvio Fanzon},
  year = {2026},
  selected = {true},
  preprint = {false},
  journal = {Journal of Tests},
  abstract = {A generated abstract.}
}
""",
            encoding="utf-8",
        )
        teaching_record = """@misc{course,
  title = {A generated course},
  year = {2025},
  yearacademic = {2025/26},
  venue = {Test University}
}
"""
        (fixture_root / "data/teaching_lecturer.bib").write_text(
            teaching_record,
            encoding="utf-8",
        )
        (fixture_root / "data/teaching_tutor.bib").write_text(
            teaching_record
            .replace("@misc{course,", "@misc{tutorial,")
            .replace("A generated course", "A generated tutorial"),
            encoding="utf-8",
        )
        (fixture_root / "news/2026-07-01.md").write_text(
            """---
title: Generated update
category: Test
---
The generator produced this update.
""",
            encoding="utf-8",
        )
        (fixture_root / "notes/example.qmd").write_text(
            """---
title: Generated note
description: A generated featured note.
date: 2026-07-02
image: ../assets/img/notes/example.svg
image-alt: Generated note visual
featured: true
featured-order: 1
categories: [Testing]
---
Note body.
""",
            encoding="utf-8",
        )

        expected_outputs = {
            "data/projects.generated.json",
            "includes/home-news.qmd",
            "includes/home-notes.html",
            "includes/home-projects.html",
            "includes/home-publications-list.html",
            "includes/news-all.qmd",
            "includes/projects-portfolio.html",
            "includes/publications-all.html",
            "includes/teaching-list.html",
        }

        build_content.main(site_root=fixture_root)
        first_run = {
            path: (fixture_root / path).read_bytes()
            for path in expected_outputs
        }
        build_content.main(site_root=fixture_root)
        second_run = {
            path: (fixture_root / path).read_bytes()
            for path in expected_outputs
        }

        self.assertEqual(first_run, second_run)

        projects_path = fixture_root / "data/projects.yml"
        projects_path.write_text(
            projects_path.read_text(encoding="utf-8").replace(
                "https://example.com/project.svg",
                "missing-project.svg",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "Local asset validation failed"):
            build_content.main(site_root=fixture_root)
        after_failed_run = {
            path: (fixture_root / path).read_bytes()
            for path in expected_outputs
        }
        self.assertEqual(second_run, after_failed_run)

        self.assertIn(b"Example project", first_run["includes/home-projects.html"])
        self.assertIn(b"Generated note", first_run["includes/home-notes.html"])
        self.assertIn(b"A deterministic publication", first_run["includes/publications-all.html"])
        self.assertIn(b"2025/26", first_run["includes/teaching-list.html"])
        self.assertIn(b"Generated update", first_run["includes/news-all.qmd"])


if __name__ == "__main__":
    unittest.main()
