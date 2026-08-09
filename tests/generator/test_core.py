import yaml

from support import GeneratorTestCase
from sitegen.core import read_front_matter, validate_local_assets


class CoreTests(GeneratorTestCase):
    def test_front_matter_valid_and_missing(self):
        valid = self.write_fixture("---\ntitle: Example\n---\nBody")
        metadata, body = read_front_matter(valid)
        self.assertEqual(metadata, {"title": "Example"})
        self.assertEqual(body, "Body")

        plain = self.write_fixture("Plain body")
        self.assertEqual(read_front_matter(plain), ({}, "Plain body"))

    def test_front_matter_malformed_yaml_fails(self):
        invalid = self.write_fixture("---\ntitle: [broken\n---\nBody")
        with self.assertRaises(yaml.YAMLError):
            read_front_matter(invalid)

    def test_local_asset_validation_checks_assets_and_skips_external_urls(self):
        fixture_root = self.temporary_directory()
        (fixture_root / "assets/pdf").mkdir(parents=True)
        (fixture_root / "assets/pdf/notes.pdf").write_bytes(b"pdf")
        (fixture_root / "assets/img").mkdir(parents=True)
        (fixture_root / "assets/img/project.svg").write_text(
            "<svg/>", encoding="utf-8"
        )
        (fixture_root / "projects/demo").mkdir(parents=True)
        (fixture_root / "projects/demo/index.qmd").write_text(
            "# Demo", encoding="utf-8"
        )

        external = validate_local_assets(
            [
                {
                    "id": "demo",
                    "image": "assets/img/project.svg",
                    "href": "projects/demo/index.html",
                }
            ],
            [
                {
                    "id": "pub",
                    "pdf": "/assets/pdf/notes.pdf",
                    "code": "https://github.com/example/repo",
                }
            ],
            [
                (
                    "teaching.bib",
                    [
                        {
                            "id": "course",
                            "taster": "notes.pdf",
                            "webpage": "/blog/course",
                        }
                    ],
                )
            ],
            site_root=fixture_root,
        )
        self.assertEqual(len(external), 2)

    def test_local_asset_validation_reports_all_missing_references(self):
        fixture_root = self.temporary_directory()
        with self.assertRaisesRegex(ValueError, "project demo image") as context:
            validate_local_assets(
                [{"id": "demo", "image": "missing.svg", "href": "missing.html"}],
                [{"id": "pub", "pdf": "/missing.pdf"}],
                [],
                site_root=fixture_root,
            )
        self.assertIn("publication pub pdf", str(context.exception))
