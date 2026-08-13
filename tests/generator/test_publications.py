from pathlib import Path

from support import GeneratorTestCase
from sitegen.publications import load_publications
from sitegen.publication_rendering import pub_actions, render_publication_archive


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class PublicationTests(GeneratorTestCase):
    def test_validation_rejects_missing_fields_and_invalid_flags(self):
        missing = "@article{id, title = {Title}}"
        with self.assertRaisesRegex(ValueError, "missing required"):
            load_publications(self.write_fixture(missing, "publications.bib"))

        invalid = """@article{id,
  category = {Articles}, abbr = {A}, title = {Title}, author = {Author},
  year = {2025}, selected = {maybe}, preprint = {false}, journal = {Journal}
}"""
        with self.assertRaisesRegex(ValueError, "selected"):
            load_publications(self.write_fixture(invalid, "publications.bib"))

    def test_validation_rejects_missing_venue(self):
        source = """@article{id,
  category = {Articles}, abbr = {A}, title = {Title}, author = {Author},
  year = {2025}, selected = {false}, preprint = {false}
}"""
        with self.assertRaisesRegex(ValueError, "venue"):
            load_publications(self.write_fixture(source, "publications.bib"))

    def test_validation_rejects_duplicate_ids(self):
        source = """@article{duplicate,
  category = {Articles}, abbr = {A}, title = {First}, author = {Author},
  year = {2025}, selected = {false}, preprint = {false}, journal = {Journal}
}
@article{duplicate,
  category = {Articles}, abbr = {A}, title = {Second}, author = {Author},
  year = {2024}, selected = {false}, preprint = {false}, journal = {Journal}
}"""
        with self.assertRaisesRegex(ValueError, "duplicate publication id"):
            load_publications(self.write_fixture(source, "publications.bib"))

    def test_contribution_metadata_and_publication_links(self):
        publications = load_publications(REPOSITORY_ROOT / "data/publications.bib")
        marked = {
            publication["id"]
            for publication in publications
            if publication["contribution"]
        }
        self.assertEqual(marked, {
            "2026-Fry-Fan-Aus-Bri",
            "2025-Fry-Aus-Fan",
            "2024-Fry-Bri-Fan",
            "2021-ISMRM",
        })
        self.assertTrue(all(
            "contribution" not in publication["bibtex"]
            for publication in publications
        ))

        f1 = next(
            publication
            for publication in publications
            if publication["id"] == "2024-Fry-Bri-Fan"
        )
        actions = pub_actions(f1)
        self.assertIn(
            'href="/assets/pdf/journal/2024-Fry-Bri-Fan.pdf" '
            'target="_blank" rel="noopener noreferrer"',
            actions,
        )
        self.assertIn(
            'href="https://doi.org/10.1016/j.econlet.2024.111671" '
            'target="_blank" rel="noopener noreferrer"',
            actions,
        )
        self.assertIn(
            'href="https://github.com/sfanzon/F1-Paper-Code" '
            'target="_blank" rel="noopener noreferrer"',
            actions,
        )
        self.assertIn('href="/projects/f1-time-rank-duality/"', actions)
        self.assertNotIn('href="/projects/f1-time-rank-duality/" target=', actions)

        archive = render_publication_archive(publications, {})
        self.assertIn('id="journal-publications"', archive)
        self.assertIn('id="journal"', archive)
        self.assertIn('class="publication-contribution-marker"', archive)
