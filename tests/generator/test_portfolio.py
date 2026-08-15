from support import GeneratorTestCase
from sitegen.portfolio import load_projects


class PortfolioTests(GeneratorTestCase):
    def test_projects_require_unique_ids_and_known_related_projects(self):
        content = """- id: first
  title: First project
  summary: A test project.
  image: first.svg
  href: first.html
  labels: [Testing]
  related: [second]
- id: second
  title: Second project
  summary: Another test project.
  image: second.svg
  href: second.html
  labels: [Testing]
"""
        source = self.write_fixture(content, "projects.yml")
        self.assertEqual([project["id"] for project in load_projects(source)], ["first", "second"])

        source.write_text(content.replace("id: second", "id: first"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate project id"):
            load_projects(source)

        source.write_text(content.replace("related: [second]", "related: [missing]"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unknown related project"):
            load_projects(source)
