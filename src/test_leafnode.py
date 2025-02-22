import sys
import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_value_error(self):
        node = LeafNode("p", None)
        try:
            node.props_to_html()
        except:
            self.assertEqual(sys.exception(), ValueError)
            

    def test_tag_none(self):
        node = LeafNode(None, "This is a text node")
        self.assertEqual(node.to_html(), "This is a text node")

    def test_children_none(self):        
        node = LeafNode("p", "This is a text node")
        self.assertEqual(node.children, None)


if __name__ == "__main__":
    unittest.main()