"""Regression checks for the site's link and resource checker."""
import pathlib
import subprocess
import sys
import tempfile
import unittest


CHECKER = pathlib.Path(__file__).with_name("check.py").resolve()


class CheckTest(unittest.TestCase):
    def check_site(self, files, *, absolute=False):
        with tempfile.TemporaryDirectory(prefix="overalls-site-check-") as directory:
            root = pathlib.Path(directory)
            for name, content in {"site.css": "", **files}.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            return subprocess.run(
                [sys.executable, "-I", str(CHECKER), str(root) if absolute else "."],
                cwd=root,
                capture_output=True,
                text=True,
            )

    def test_healthy_links_and_resources(self):
        files = {
            "index.html": '<a href="other.html#there">other</a>'
                '<a href="docs/#there">docs</a><a href="/other.html#there">root</a>'
                '<a href="space%20page.html#an%20id">escaped</a>'
                '<a href="mailto:hello@example.com">mail</a><a href="tel:+123">call</a>'
                '<a href="https://example.com/">external link</a>'
                '<script src="https://api.ghuntley.com/latest.js"></script>',
            "other.html": '<h1 id="there">Other</h1>',
            "docs/index.html": '<h1 id="there">Docs</h1>',
            "space page.html": '<h1 id="an id">Escaped</h1>',
        }
        for absolute in (False, True):
            with self.subTest(absolute=absolute):
                result = self.check_site(files, absolute=absolute)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("OK: no problems", result.stdout)

    def test_missing_file_fails(self):
        result = self.check_site({"index.html": '<a href="missing.html">missing</a>'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing missing.html", result.stdout)

    def test_cross_page_anchor_fails_for_relative_and_absolute_roots(self):
        files = {
            "index.html": '<a href="other.html#absent">missing anchor</a>',
            "other.html": '<h1 id="present">Other</h1>',
        }
        for absolute in (False, True):
            with self.subTest(absolute=absolute):
                result = self.check_site(files, absolute=absolute)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("bad anchor other.html#absent", result.stdout)

    def test_directory_anchor_fails(self):
        result = self.check_site({
            "index.html": '<a href="docs/#absent">missing anchor</a>',
            "docs/index.html": '<h1 id="present">Docs</h1>',
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bad anchor docs/#absent", result.stdout)

    def test_directory_without_index_fails(self):
        result = self.check_site({
            "index.html": '<a href="docs/">missing index</a>',
            "docs/asset.txt": "not an index",
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing docs/", result.stdout)

    def test_external_resources_fail(self):
        for source in ("https://external.example/script.js", "//external.example"):
            with self.subTest(source=source):
                result = self.check_site({"index.html": f'<script src="{source}"></script>'})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("external resource " + source, result.stdout)

    def test_http_resources_without_a_parsed_host_fail(self):
        for source in (r"https:\\external.example/script.js", "https:missing.js"):
            with self.subTest(source=source):
                result = self.check_site({"index.html": f'<script src="{source}"></script>'})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unsupported URL " + source, result.stdout)

    def test_non_hyperlink_schemes_fail(self):
        for source in ("file:///outside/script.js", "data:text/javascript,alert(1)"):
            with self.subTest(source=source):
                result = self.check_site({"index.html": f'<script src="{source}"></script>'})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unsupported URL " + source, result.stdout)

    def test_colour_outside_tokens_fails(self):
        result = self.check_site({
            "index.html": "<h1>Test</h1>",
            "site.css": "/* ---- fonts */\nbody { color: #123456; }",
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("colour literal: #123456", result.stdout)

    def test_colour_tokens_and_print_overrides_pass(self):
        result = self.check_site({
            "index.html": "<h1>Test</h1>",
            "site.css": ":root { --text-color: #000; }\n/* ---- fonts */\n"
                "@media print { body { color: #fff; } }",
        })
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_external_css_fails(self):
        result = self.check_site({
            "index.html": "<h1>Test</h1>",
            "site.css": '@import "https://external.example/style.css";',
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("external css", result.stdout)

    def test_existing_site_passes(self):
        root = CHECKER.parents[2]
        result = subprocess.run(
            [sys.executable, "-I", str(CHECKER), "."],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK: no problems", result.stdout)


if __name__ == "__main__":
    unittest.main()
