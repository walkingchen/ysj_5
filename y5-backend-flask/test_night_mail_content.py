import unittest

from night_mail_content import (
    DAILY_SURVEY_LINKS,
    build_night_mail_content,
    build_night_mail_subject,
)


class NightMailContentTest(unittest.TestCase):
    def test_each_day_uses_its_own_survey_link(self):
        self.assertEqual(len(DAILY_SURVEY_LINKS), 8)

        for day, link in DAILY_SURVEY_LINKS.items():
            with self.subTest(day=day):
                content = build_night_mail_content(day, 1.25)
                self.assertIn(f'href="{link}"', content)
                self.assertIn(f">{link}</a>", content)
                self.assertIn("earned $1.25", content)

    def test_subject_contains_current_day(self):
        self.assertEqual(
            build_night_mail_subject(6),
            "Chattera Night Mail and Daily Survey - DAY 6",
        )

    def test_unknown_day_is_rejected(self):
        with self.assertRaises(KeyError):
            build_night_mail_content(9, 0)


if __name__ == "__main__":
    unittest.main()
