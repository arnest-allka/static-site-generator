import unittest

from textnode import (
    TextNode,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

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

if __name__ == "__main__":
    unittest.main()
