import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_assets  # noqa: E402
import indexnow_ping  # noqa: E402
import simpleseo_audit  # noqa: E402


class TestSimpleSEO(unittest.TestCase):
    def test_robots_validation_rejects_nonstandard_directive(self) -> None:
        bad = "User-agent: *\nContent-Signal: search=yes\nAllow: /\n"
        res = simpleseo_audit.validate_robots_txt(bad)
        self.assertFalse(res["valid_rfc9309"])
        self.assertEqual(len(res["invalid_lines"]), 1)

    def test_generated_assets_pass_auditors(self) -> None:
        robots = generate_assets.build_robots_txt("https://www.example.com")
        r_res = simpleseo_audit.validate_robots_txt(robots)
        self.assertTrue(r_res["valid_rfc9309"])
        self.assertEqual(r_res["ai_bots"]["oai-searchbot"], "allowed")

        llms = generate_assets.build_llms_txt(
            "ExampleStudio",
            "https://www.example.com",
            "ExampleStudio builds fast websites and custom web software for growing businesses.",
            [("Services", "/services/", "Core web services and pricing.")],
        )
        l_res = simpleseo_audit.validate_llms_txt(llms)
        self.assertTrue(l_res["valid"])

        catalog = generate_assets.build_ai_catalog(
            "ExampleStudio",
            "example.com",
            "https://www.example.com",
            ["ExampleStudio web design services", "ExampleStudio pricing packages"],
        )
        a_res = simpleseo_audit.validate_ai_catalog(json.dumps(catalog))
        self.assertTrue(a_res["valid"], a_res["errors"])

    def test_audit_html_detects_deprecated_schema_and_missing_img_dims(self) -> None:
        html = """<!doctype html><html lang="en"><head>
        <title>Example Brand | Web Studio</title>
        <meta name="description" content="Fast web development services." />
        <link rel="canonical" href="https://www.example.com/" />
        <script type="application/ld+json">{"@context":"https://schema.org","@type":"HowTo","name":"Demo"}</script>
        </head><body><h1>Hello</h1><img src="/hero.webp" alt="Hero" /></body></html>""".encode("utf-8")
        res = simpleseo_audit.audit_html(html, "https://www.example.com/", {})
        self.assertTrue(res["canonical_matches_final_url"])
        self.assertEqual(res["jsonld"]["deprecated_types"], ["HowTo"])
        self.assertEqual(res["images_missing_dimensions"], ["/hero.webp"])

    def test_indexnow_key_creation_reuses_valid_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pub = Path(tmp)
            key1, path1 = indexnow_ping.resolve_or_create_key(pub, None)
            self.assertEqual(len(key1), 32)
            self.assertTrue(path1.exists())
            key2, path2 = indexnow_ping.resolve_or_create_key(pub, None)
            self.assertEqual(key1, key2)
            self.assertEqual(path1, path2)


if __name__ == "__main__":
    unittest.main()
