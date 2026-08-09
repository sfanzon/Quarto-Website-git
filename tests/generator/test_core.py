import yaml

from support import GeneratorTestCase
from sitegen.core import read_front_matter


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
