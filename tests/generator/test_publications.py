from support import GeneratorTestCase
from sitegen.publications import load_publications


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
