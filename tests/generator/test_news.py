from support import GeneratorTestCase
from sitegen.news import load_news, news_inline_html, news_summary


class NewsTests(GeneratorTestCase):
    def test_helpers_validate_dates_and_convert_links(self):
        self.assertIn(
            "/publications/#item",
            news_inline_html('<a href="/publications/#item">Read</a>'),
        )
        self.assertIn(
            "/teaching/#course",
            news_inline_html('<a href="/teaching.html#course">Read</a>'),
        )
        self.assertIn(
            "/presentations/#talk",
            news_inline_html('<a href="/presentations.html#talk">Read</a>'),
        )
        self.assertTrue(news_summary("A short sentence.").endswith("."))

        fixture_root = self.temporary_directory()
        news_dir = fixture_root / "news"
        news_dir.mkdir()
        (news_dir / "not-a-date.md").write_text("Update", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            load_news(site_root=fixture_root)
