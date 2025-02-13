import sys
import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a text node")
        try:
            node.props_to_html()
        except:
            self.assertEqual(sys.exception(), NotImplementedError)
            

    def test_props_none(self):
        node = HTMLNode("p", "This is a text node")
        self.assertEqual(node.props, None)

    def test_children_none(self):
        node = HTMLNode("p", "This is a text node")
        self.assertEqual(node.children, None)


if __name__ == "__main__":
    unittest.main()