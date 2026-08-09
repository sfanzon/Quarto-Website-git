from support import GeneratorTestCase
from sitegen.bibtex import read_bibtex_entries


class BibtexTests(GeneratorTestCase):
    def test_parser_handles_nested_quoted_numeric_and_string(self):
        source = """@string{venue = \"Journal\"}
@article{example,
  title = {A {nested} title},
  year = 2025,
  note = \"quoted, value\",
  journal = {Journal of Tests}
}
"""
        record = read_bibtex_entries(
            self.write_fixture(source, "fixture.bib")
        )[0]
        self.assertEqual(record["id"], "example")
        self.assertEqual(record["title"], "A {nested} title")
        self.assertEqual(record["year"], "2025")
        self.assertEqual(record["note"], "quoted, value")
        self.assertEqual(record["journal"], "Journal of Tests")

    def test_parser_rejects_unclosed_entries(self):
        fixture = self.write_fixture(
            "@article{broken,\n title = {x}\n", "fixture.bib"
        )
        with self.assertRaises(ValueError):
            read_bibtex_entries(fixture)
