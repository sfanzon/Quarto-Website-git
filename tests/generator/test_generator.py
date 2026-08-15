from support import GeneratorTestCase
from sitegen.generator import generate_site


class GeneratorTests(GeneratorTestCase):
    def test_generates_complete_deterministic_output(self):
        fixture_root = self.temporary_directory()

        for relative_directory in (
            "assets/img/notes",
            "data",
            "includes",
            "news",
            "notes",
        ):
            (fixture_root / relative_directory).mkdir(parents=True)

        (fixture_root / "assets/img/notes/example.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"/>',
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
        for filename, record_id in (
            ("presentations_talks.bib", "talk"),
            ("presentations_posters.bib", "poster"),
            ("presentations_institutional.bib", "institutional"),
        ):
            (fixture_root / "data" / filename).write_text(
                f"""@misc{{{record_id},
  title = {{A generated presentation}},
  year = {{2025}},
  date = {{1 Jan 2025}},
  venue = {{Test University}},
  event_title = {{Test event}}
}}
""",
                encoding="utf-8",
            )
        for filename, record_id in (
            ("supervision_master.bib", "master"),
            ("supervision_undergraduate.bib", "undergraduate"),
        ):
            (fixture_root / "data" / filename).write_text(
                f"""@misc{{{record_id},
  title = {{A generated supervision project}},
  year = {{2025/26}},
  venue = {{Test University}},
  abstract = {{A generated abstract.}}
}}
""",
                encoding="utf-8",
            )
        (fixture_root / "data/teaching.yml").write_text(
            """- id: course
  role: lecturer
  title: A generated course
  year: '2025'
  yearacademic: 2025/26
  venue: Test University
- id: tutorial
  role: tutor
  title: A generated tutorial
  year: '2025'
  yearacademic: 2025/26
  venue: Test University
""",
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
            "includes/home-news.html",
            "includes/news-all.html",
            "includes/publications-all.html",
            "includes/presentations.html",
            "includes/supervision.html",
            "includes/teaching-list.html",
        }

        generate_site(site_root=fixture_root)
        first_run = {
            path: (fixture_root / path).read_bytes()
            for path in expected_outputs
        }
        generate_site(site_root=fixture_root)
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
            generate_site(site_root=fixture_root)
        after_failed_run = {
            path: (fixture_root / path).read_bytes()
            for path in expected_outputs
        }
        self.assertEqual(second_run, after_failed_run)

        self.assertIn(b"Generated update", first_run["includes/home-news.html"])
        self.assertIn(
            b"A deterministic publication",
            first_run["includes/publications-all.html"],
        )
        self.assertIn(b"2025/26", first_run["includes/teaching-list.html"])
        self.assertIn(b"Generated update", first_run["includes/news-all.html"])
