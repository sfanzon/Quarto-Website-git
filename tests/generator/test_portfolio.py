from support import GeneratorTestCase
from sitegen.portfolio import (
    load_featured_notes,
    render_featured_note,
    render_project_card,
)


class PortfolioTests(GeneratorTestCase):
    def test_project_card_renders_valid_yaml_data(self):
        project = {
            "title": "Example project",
            "summary": "A test project.",
            "image": "assets/img/projects/example.svg",
            "href": "projects/example/index.html",
            "labels": ["Testing"],
        }
        rendered = render_project_card(project)
        self.assertIn("Example project", rendered)
        self.assertIn("assets/img/projects/example.svg", rendered)

    def test_featured_notes_are_validated_sorted_and_rendered(self):
        fixture_root = self.temporary_directory()
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
            template.format(
                title="Second",
                description="Second note.",
                day=20,
                image="second.svg",
                alt="Second visual",
                order=2,
            ),
            encoding="utf-8",
        )
        (notes_dir / "first.qmd").write_text(
            template.format(
                title="First",
                description="First note.",
                day=21,
                image="first.svg",
                alt="First visual",
                order=1,
            ),
            encoding="utf-8",
        )

        notes = load_featured_notes(notes_dir, site_root=fixture_root)
        self.assertEqual([note["title"] for note in notes], ["First", "Second"])
        self.assertEqual(notes[0]["href"], "/notes/first.html")
        self.assertEqual(notes[0]["image_url"], "/assets/img/notes/first.svg")
        rendered = render_featured_note(notes[0])
        self.assertIn("First note.", rendered)
        self.assertIn('alt="First visual"', rendered)
