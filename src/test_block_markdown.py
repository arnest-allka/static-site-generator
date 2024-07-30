import unittest

from block_markdown import *

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

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()