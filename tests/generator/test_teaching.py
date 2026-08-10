from support import GeneratorTestCase
from sitegen.teaching import load_teaching, teaching_years


class TeachingTests(GeneratorTestCase):
    def test_canonical_yaml_requires_complete_unique_role_tagged_records(self):
        source = self.write_fixture(
            """- id: course
  role: lecturer
  title: Example
  venue: Test University
  year: '2025'
  yearacademic: 2025/26
""",
            "teaching.yml",
        )
        self.assertEqual(load_teaching(source)[0]["id"], "course")

        source.write_text("- id: incomplete\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing required"):
            load_teaching(source)

        source.write_text(
            """- id: course
  role: assistant
  title: Example
  venue: Test University
  year: '2025'
  yearacademic: 2025/26
""",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "invalid role"):
            load_teaching(source)

    def test_years_are_validated_and_sorted(self):
        courses = [
            {"id": "new", "yearacademic": "2025/26"},
            {"id": "old", "yearacademic": "2020/21"},
        ]
        self.assertEqual(
            teaching_years(courses, "teaching.bib"),
            ["2025/26", "2020/21"],
        )
        with self.assertRaisesRegex(ValueError, "missing yearacademic"):
            teaching_years([{"id": "missing"}], "teaching.bib")
        with self.assertRaisesRegex(ValueError, "invalid yearacademic"):
            teaching_years(
                [{"id": "invalid", "yearacademic": "2025"}],
                "teaching.bib",
            )
        with self.assertRaisesRegex(ValueError, "non-consecutive"):
            teaching_years(
                [{"id": "invalid", "yearacademic": "2025/27"}],
                "teaching.bib",
            )
