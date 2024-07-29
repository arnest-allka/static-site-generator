import unittest

from block_markdown import block_to_block_type, markdown_to_blocks

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

class TestMarkdownBlockTypes(unittest.TestCase):

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), 'heading')

        block = "## This is a level 2 heading"
        self.assertEqual(block_to_block_type(block), 'heading')

        block = "###### This is a level 6 heading"
        self.assertEqual(block_to_block_type(block), 'heading')

    def test_code_block(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), 'code')

        block = "```\nAnother code block\n```"
        self.assertEqual(block_to_block_type(block), 'code')

    def test_quote_block(self):
        block = "> This is a quote block"
        self.assertEqual(block_to_block_type(block), 'quote')

        block = "> Another quote block\n> With multiple lines"
        self.assertEqual(block_to_block_type(block), 'quote')

    def test_unordered_list(self):
        block = "* This is an unordered list item"
        self.assertEqual(block_to_block_type(block), 'unordered_list')

        block = "- This is another unordered list item"
        self.assertEqual(block_to_block_type(block), 'unordered_list')

        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), 'unordered_list')

        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), 'unordered_list')

    def test_ordered_list(self):
        block = "1. This is an ordered list item"
        self.assertEqual(block_to_block_type(block), 'ordered_list')

        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), 'ordered_list')

        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), 'ordered_list')

    def test_paragraph(self):
        block = "This is a paragraph of text."
        self.assertEqual(block_to_block_type(block), 'paragraph')

        block = "This is a paragraph with multiple lines.\nIt should still be considered a paragraph."
        self.assertEqual(block_to_block_type(block), 'paragraph')

if __name__ == "__main__":
    unittest.main()