import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_initialization(self):
        node = HTMLNode(tag="div", value="Some content", children=[], props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Some content")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_initialization_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html().strip(), 'class="container" id="main"')

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="p", value="Some text", children=None, props={"style": "color:red;"})
        expected_repr = "HTMLNode(p, Some text, children: None, {'style': 'color:red;'})"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_children(self):
        child_node = HTMLNode(tag="span", value="Child")
        node = HTMLNode(tag="div", value=None, children=[child_node], props={"class": "container"})
        expected_repr = f"HTMLNode(div, None, children: [{repr(child_node)}], {{'class': 'container'}})"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_props(self):
        node = HTMLNode(tag="div", value="No props", children=[], props=None)
        expected_repr = "HTMLNode(div, No props, children: [], None)"
        self.assertEqual(repr(node), expected_repr)

    def test_not_implemented_to_html(self):
        node = HTMLNode(tag="div", value="Some content", children=[], props={"class": "container"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
