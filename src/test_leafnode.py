import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leafnode_creation(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.props, {"class": "text"})
        self.assertIsNone(node.children)

    def test_leafnode_to_html_with_props(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello, world!</p>')

    def test_leafnode_to_html_without_props(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')

    def test_leafnode_to_html_no_tag(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), 'Hello, world!')

    def test_leafnode_no_value_raises_error(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode(tag="p")
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")

    def test_leafnode_repr(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "text"})
        expected_repr = ("HTMLNode:\n"
                         "tag: p\n"
                         "value: Hello, world!\n"
                         "props: {'class': 'text'}\n")
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()
