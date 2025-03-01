import sys
import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode
from main import *

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

    def test_parent_notag(self):
        node = ParentNode(None, "This is a text node")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "tag must have a value")
    
    def test_parent_nochildren(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "children cannot be None")
    
    def test_empty_children(self):
        node = ParentNode("div", [])  # valid tag, empty list
        expected = "<div></div>"
        self.assertEqual(node.to_html(), expected)
    
    def test_parent_printsimple(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        #print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_parent_printnest(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("p", "Second P"),
            ],
        )
        #print(node.to_html())
        self.assertEqual(node.to_html(), "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p>Second P</p></div>")

    def test_text_normal(self):
        text = TextNode("Normal", TextType.TEXT, None)
        node = text.text_node_to_html_node()
        self.assertEqual(node.to_html(), "Normal")

    def test_text_bold(self):
        text = TextNode("Bold text", TextType.BOLD, None)
        node = text.text_node_to_html_node()
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_text_ita(self):
        text = TextNode("text", TextType.ITALIC, None)
        node = text.text_node_to_html_node()
        self.assertEqual(node.to_html(), "<i>text</i>")

    def test_text_code(self):
        text = TextNode("text", TextType.CODE, None)
        node = text.text_node_to_html_node()
        self.assertEqual(node.to_html(), "<code>text</code>")

    def test_text_image(self):
        text = TextNode("text", TextType.IMAGE, "http://mylink.com")
        node = text.text_node_to_html_node()
        self.assertEqual(node.to_html(), '<img alt="text" src="http://mylink.com"></img>')
        
    def test_text_link(self):
        text = TextNode("text", TextType.LINK, "http://mylink.com")
        node = text.text_node_to_html_node()
        self.assertEqual(node.to_html(), '<a href="http://mylink.com">text</a>')


if __name__ == "__main__":
    unittest.main()