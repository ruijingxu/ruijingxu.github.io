from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.icons = []
        self.headings = []
        self._heading = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "link" and "icon" in attributes.get("rel", "").split():
            self.icons.append(attributes.get("href"))
        if tag in {"h2", "h3"}:
            self._heading = [tag, ""]

    def handle_data(self, data):
        if self._heading is not None:
            self._heading[1] += data

    def handle_endtag(self, tag):
        if self._heading is not None and tag == self._heading[0]:
            self.headings.append((tag, " ".join(self._heading[1].split())))
            self._heading = None


class AcademicHomepageTest(unittest.TestCase):
    def setUp(self):
        page_path = ROOT / "index.html"
        if not page_path.exists():
            self.fail("index.html must exist")
        self.html = page_path.read_text(encoding="utf-8")
        self.parser = PageParser()
        self.parser.feed(self.html)

    def test_identity_and_research_are_published(self):
        required_copy = (
            "Ruijing Xu",
            "National University of Singapore",
            "robotics and embodied AI",
            "tactile sensing",
            "contact-rich manipulation",
            "research assistant and internship opportunities",
        )
        for text in required_copy:
            with self.subTest(text=text):
                self.assertIn(text, self.html)

    def test_contact_and_profile_links_are_correct(self):
        required_links = {
            "mailto:raexuu@outlook.com",
            "data/RuijingXu-CV.pdf",
            "https://github.com/RaeXuu",
            "https://www.linkedin.com/in/ruijing-xu-a932b3323/",
        }
        self.assertTrue(required_links.issubset(set(self.parser.links)))

    def test_local_assets_exist_and_portrait_is_accessible(self):
        local_links = [
            value
            for value in self.parser.links
            if not value.startswith(("http://", "https://", "mailto:"))
        ]
        local_images = [image["src"] for image in self.parser.images]
        for relative_path in local_links + local_images + ["stylesheet.css"]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

        portrait = next(
            image
            for image in self.parser.images
            if image.get("src") == "images/RuijingXu.jpg"
        )
        self.assertEqual(portrait.get("alt"), "Portrait of Ruijing Xu")

    def test_reference_personal_content_is_not_published(self):
        prohibited_copy = (
            "Jon Barron",
            "jonbarron@gmail.com",
            "Jonathan T. Barron",
            "Image Generators are Generalist Vision Learners",
        )
        for text in prohibited_copy:
            with self.subTest(text=text):
                self.assertNotIn(text, self.html)

    def test_favicon_is_declared_and_resolves_locally(self):
        self.assertEqual(self.parser.icons, ["images/favicon.svg"])
        self.assertTrue((ROOT / self.parser.icons[0]).is_file())

    def test_experience_is_organized_into_distinct_sections(self):
        section_headings = [
            text for level, text in self.parser.headings if level == "h2"
        ]
        self.assertEqual(
            section_headings,
            ["Research", "Internship Experience", "Project Experience"],
        )

        entry_headings = [
            text for level, text in self.parser.headings if level == "h3"
        ]
        self.assertEqual(
            entry_headings,
            [
                "Learning Visuo-Tactile Perception for Contact-rich Robotic Manipulation",
                "Swancor PrimeBOT",
                "Senad Robotics Co., Ltd",
                "Edge AI-based Heart Sound Diagnosis System",
            ],
        )


if __name__ == "__main__":
    unittest.main()
