import unittest

from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_block(self):
        markdown = "# This is a heading"
        expected = ["# This is a heading"]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_multiple_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_leading_and_trailing_whitespace(self):
        markdown = """  # This is a heading  

This is a paragraph of text.  

* This is a list item  
"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text.",
            "* This is a list item"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_excessive_newlines(self):
        markdown = """# Heading 1


# Heading 2"""
        expected = [
            "# Heading 1",
            "# Heading 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_empty_markdown(self):
        markdown = ""
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()