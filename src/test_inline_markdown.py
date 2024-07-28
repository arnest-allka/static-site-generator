import unittest
from inline_markdown import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", "text")
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        result_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_bold_delimiter(self):
        node = TextNode("This is **bold** text", "text")
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]
        result_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_italic_delimiter(self):
        node = TextNode("This is *italic* text", "text")
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text"),
        ]
        result_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_mismatched_delimiter(self):
        node = TextNode("This is text with a `mismatched code block", "text")
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", "code")
        self.assertEqual(str(context.exception), "Mismatched delimiter found in text node.")

    def test_no_text_nodes(self):
        node1 = TextNode("Not to split", "bold")
        node2 = TextNode("Another node", "italic")
        result_nodes = split_nodes_delimiter([node1, node2], "`", "code")
        self.assertEqual(result_nodes, [node1, node2])

    def test_empty_text_node(self):
        node = TextNode("", "text")
        expected_nodes = []
        result_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(result_nodes, expected_nodes)

    def test_multiple_delimiters(self):
        node = TextNode("Mix `code` and **bold**", "text")
        intermediate_nodes = split_nodes_delimiter([node], "`", "code")
        expected_nodes = [
            TextNode("Mix ", "text"),
            TextNode("code", "code"),
            TextNode(" and **bold**", "text"),
        ]
        self.assertEqual(intermediate_nodes, expected_nodes)
        
        final_nodes = split_nodes_delimiter(intermediate_nodes, "**", "bold")
        final_expected_nodes = [
            TextNode("Mix ", "text"),
            TextNode("code", "code"),
            TextNode(" and ", "text"),
            TextNode("bold", "bold"),
        ]
        self.assertEqual(final_nodes, final_expected_nodes)

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images_basic(self):
        text = "Here is an image ![alt text](http://example.com/image.jpg)"
        expected = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = ("Here is an image ![alt text](http://example.com/image.jpg) "
                "and another ![another image](http://example.com/another.jpg)")
        expected = [
            ("alt text", "http://example.com/image.jpg"),
            ("another image", "http://example.com/another.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_edge_cases(self):
        text = ("![empty alt]() ![](http://example.com/image.jpg) "
                "![alt with spaces](http://example.com/with spaces.jpg)")
        expected = [
            ("empty alt", ""),
            ("", "http://example.com/image.jpg"),
            ("alt with spaces", "http://example.com/with spaces.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_basic(self):
        text = "Here is a link [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = ("Here is a link [link text](http://example.com) "
                "and another [another link](http://example.com/another)")
        expected = [
            ("link text", "http://example.com"),
            ("another link", "http://example.com/another")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_none(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_edge_cases(self):
        text = ("[empty text]() [](http://example.com) "
                "[link with spaces](http://example.com/with spaces)")
        expected = [
            ("empty text", ""),
            ("", "http://example.com"),
            ("link with spaces", "http://example.com/with spaces")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_image_basic(self):
        node = TextNode("Here is an image ![alt text](http://example.com/image.jpg)", "text")
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here is an image ", "text"),
            TextNode("alt text", "image", "http://example.com/image.jpg")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode("![first](http://example.com/first.jpg) and ![second](http://example.com/second.jpg)", "text")
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", "image", "http://example.com/first.jpg"),
            TextNode(" and ", "text"),
            TextNode("second", "image", "http://example.com/second.jpg")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_none(self):
        node = TextNode("This text has no images.", "text")
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_edge_cases(self):
        node = TextNode("![empty alt]() ![](http://example.com/image.jpg) ![alt with spaces](http://example.com/with spaces.jpg)", "text")
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("empty alt", "image", ""),
            TextNode(" ", "text"),
            TextNode("", "image", "http://example.com/image.jpg"),
            TextNode(" ", "text"),
            TextNode("alt with spaces", "image", "http://example.com/with spaces.jpg")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_basic(self):
        node = TextNode("Here is a link [link text](http://example.com)", "text")
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here is a link ", "text"),
            TextNode("link text", "link", "http://example.com")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode("[first link](http://example.com/first) and [second link](http://example.com/second)", "text")
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first link", "link", "http://example.com/first"),
            TextNode(" and ", "text"),
            TextNode("second link", "link", "http://example.com/second")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_none(self):
        node = TextNode("This text has no links.", "text")
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_edge_cases(self):
        node = TextNode("[empty link]() [](http://example.com) [link with spaces](http://example.com/with spaces)", "text")
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("empty link", "link", ""),
            TextNode(" ", "text"),
            TextNode("", "link", "http://example.com"),
            TextNode(" ", "text"),
            TextNode("link with spaces", "link", "http://example.com/with spaces")
        ]
        self.assertEqual(new_nodes, expected)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnode(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()