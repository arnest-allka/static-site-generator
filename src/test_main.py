import unittest

from main import *

class TestExtractTitle(unittest.TestCase):

    def test_extract_title_single_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_leading_trailing_whitespace(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_multiple_lines(self):
        markdown = """
Some text
# My Title
More text
"""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_no_h1(self):
        markdown = "No header here"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_extract_title_with_other_headers(self):
        markdown = """
## Subheading
# Main Title
### Another subheading
"""
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_extract_title_with_inline_formatting(self):
        markdown = "# This is **bold** and *italic*"
        self.assertEqual(extract_title(markdown), "This is **bold** and *italic*")

if __name__ == "__main__":
    unittest.main()
