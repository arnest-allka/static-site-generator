import unittest
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_parentnode_creation(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        node = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.props, {"class": "parent"})
        self.assertEqual(node.children, [child1, child2])

    def test_parentnode_to_html_with_props(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        node = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})
        expected_html = '<div class="parent"><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_to_html_without_props(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        node = ParentNode(tag="div", children=[child1, child2])
        expected_html = '<div><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_no_tag_raises_error(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        with self.assertRaises(ValueError) as context:
            node = ParentNode(children=[child1, child2])
        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test_parentnode_no_children_raises_error(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="div")
        self.assertEqual(str(context.exception), "All parent nodes must have children")

if __name__ == "__main__":
    unittest.main()
