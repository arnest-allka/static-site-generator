import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', 'bold')
        node2 = TextNode('This is a text node', 'bold')
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode('This is a text node', 'bold', 'http://example.com')
        node2 = TextNode('This is a text node', 'bold', 'http://example.com')
        self.assertEqual(node, node2)
        
    def test_eq_not_equal(self):
        node = TextNode('This is a text node', 'bold')
        node2 = TextNode('This is a text node', 'italic')
        self.assertNotEqual(node, node2)
        
    def test_eq_url_not_equal(self):
        node = TextNode('This is a text node', 'bold', 'http://example.com')
        node2 = TextNode('This is a text node', 'bold', 'http://example.org')
        self.assertNotEqual(node, node2)
        
    def test_eq_url_None(self):
        node = TextNode('This is a text node', 'bold', None)
        node2 = TextNode('This is a text node', 'bold', None)
        self.assertEqual(node, node2)
    
if __name__ == "__main__":
    unittest.main()