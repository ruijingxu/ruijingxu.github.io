from html.parser import HTMLParser
from pathlib import Path
import struct
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

    def test_favicon_displays_rae(self):
        favicon = (ROOT / "images/favicon.svg").read_text(encoding="utf-8")
        self.assertIn('aria-label="RAE"', favicon)
        self.assertIn(">RAE</text>", favicon)

    def test_availability_uses_light_pink_highlight_without_left_border(self):
        stylesheet = (ROOT / "stylesheet.css").read_text(encoding="utf-8")
        self.assertIn('<p class="availability">', self.html)
        self.assertIn(".availability", stylesheet)
        self.assertIn("background-color: #fff1f4;", stylesheet)
        self.assertNotIn("border-left:", stylesheet)

    def test_organization_logos_link_to_official_websites(self):
        expected = {
            "images/nus-logo.svg": "https://www.nus.edu.sg/",
            "images/njust-logo.webp": "https://www.njust.edu.cn/",
            "images/upc-logo.png": "https://www.upc.edu/es",
            "images/primebot-logo.jpeg": "https://www.primebot.cn/",
            "images/senad-logo.webp": "https://www.senadvision.com/",
        }
        for image_path, website in expected.items():
            with self.subTest(image_path=image_path):
                self.assertTrue((ROOT / image_path).is_file())
                self.assertIn(f'href="{website}"', self.html)
                self.assertIn(f'src="{image_path}"', self.html)
        stylesheet = (ROOT / "stylesheet.css").read_text(encoding="utf-8")
        self.assertIn(".organization-logo", stylesheet)

    def test_organization_names_carry_links_and_primebot_identifies_agibot(self):
        for website, name in (
            ("https://www.primebot.cn/", "Swancor PrimeBOT"),
            ("https://www.senadvision.com/", "Senad Robotics Co., Ltd"),
            ("https://www.nus.edu.sg/", "National University of Singapore"),
            ("https://www.njust.edu.cn/", "Nanjing University of Science and Technology"),
            ("https://www.upc.edu/es", "Universitat Politècnica de Catalunya"),
        ):
            with self.subTest(name=name):
                self.assertIn(f'h3><a href="{website}"', self.html)
                self.assertIn(f">{name}</a>", self.html)
        self.assertIn(
            'href="https://www.agibot.com.cn/"',
            self.html,
        )
        self.assertIn("(subsidiary of AGIBOT)", self.html)
        stylesheet = (ROOT / "stylesheet.css").read_text(encoding="utf-8")
        self.assertIn("width: 70px;", stylesheet)
        self.assertIn("height: 70px;", stylesheet)

    def test_edge_ai_project_has_a_logo(self):
        self.assertTrue((ROOT / "images/edge-ai-logo.png").is_file())
        self.assertIn(
            '<img class="organization-logo" src="images/edge-ai-logo.png" alt="Edge AI project logo">',
            self.html,
        )
        png_header = (ROOT / "images/edge-ai-logo.png").read_bytes()
        self.assertEqual(png_header[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", png_header[16:24]), (512, 512))

    def test_msc_dissertation_has_a_gelsight_logo(self):
        self.assertTrue((ROOT / "images/gelsight-mini.png").is_file())
        self.assertIn(
            '<img class="organization-logo" src="images/gelsight-mini.png" alt="GelSight mini logo">',
            self.html,
        )

    def test_experience_is_organized_into_distinct_sections(self):
        section_headings = [
            text for level, text in self.parser.headings if level == "h2"
        ]
        self.assertEqual(
            section_headings,
            [
                "Research",
                "Project",
                "Internship",
                "Education",
            ],
        )

        entry_headings = [
            text for level, text in self.parser.headings if level == "h3"
        ]
        self.assertEqual(
            entry_headings,
            [
                "Learning Visuo-Tactile Perception for Contact-rich Robotic Manipulation",
                "Edge AI-based Heart Sound Diagnosis System",
                "Swancor PrimeBOT (subsidiary of AGIBOT)",
                "Senad Robotics Co., Ltd",
                "National University of Singapore",
                "Nanjing University of Science and Technology",
                "Universitat Politècnica de Catalunya",
            ],
        )

        for education_detail in (
            "M.Sc. in Electrical Engineering · Aug 2026-Jun 2027",
            "B.Eng. in Electronic and Information Engineering · Sep 2022-Jun 2026",
            "Exchange Student in Electrical Engineering · Sep 2024-Jan 2025",
        ):
            with self.subTest(education_detail=education_detail):
                self.assertIn(education_detail, self.html)


if __name__ == "__main__":
    unittest.main()
