from support import GeneratorTestCase
from sitegen.teaching import teaching_years


class TeachingTests(GeneratorTestCase):
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
