from support import GeneratorTestCase
from sitegen.assets import validate_local_assets


class AssetTests(GeneratorTestCase):
    def test_validation_checks_assets_and_skips_external_urls(self):
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
        (fixture_root / "astro/src/pages").mkdir(parents=True)
        (fixture_root / "astro/src/pages/publications.astro").write_text(
            "---\n---", encoding="utf-8"
        )

        external = validate_local_assets(
            [
                {
                    "id": "demo",
                    "image": "assets/img/project.svg",
                    "href": "projects/demo/index.html",
                },
                {
                    "id": "archive",
                    "image": "assets/img/project.svg",
                    "href": "/publications/",
                },
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

    def test_validation_reports_all_missing_references(self):
        fixture_root = self.temporary_directory()
        with self.assertRaisesRegex(ValueError, "project demo image") as context:
            validate_local_assets(
                [{"id": "demo", "image": "missing.svg", "href": "missing.html"}],
                [{"id": "pub", "pdf": "/missing.pdf"}],
                [],
                site_root=fixture_root,
            )
        self.assertIn("publication pub pdf", str(context.exception))
