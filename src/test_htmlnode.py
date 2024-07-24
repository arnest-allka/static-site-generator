import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_no_arguments(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_arguments(self):
        children = [HTMLNode(tag='p', value='child')]
        props = {'class': 'main'}
        node = HTMLNode(tag='div', value='parent', children=children, props=props)
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'parent')
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        props = {'class': 'main', 'id': 'unique'}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), 'class="main" id="unique" ')

    def test_repr_no_arguments(self):
        node = HTMLNode()
        expected_repr = "HTMLNode:\n"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_arguments(self):
        children = [HTMLNode(tag='p', value='child')]
        props = {'class': 'main'}
        node = HTMLNode(tag='div', value='parent', children=children, props=props)
        expected_repr = "HTMLNode:\ntag: div\nvalue: parent\nchildren: [HTMLNode:\ntag: p\nvalue: child\n]\nprops: {'class': 'main'}\n"
        self.assertEqual(repr(node), expected_repr)

if __name__ == '__main__':
    unittest.main()
