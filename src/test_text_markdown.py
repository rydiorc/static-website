import unittest

from textnode import TextNode, TextType
from func import *

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        #print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

This is another paragraph with _italic_ text and `code` here

This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        #print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_blocktype(self):
        md = """
Normal Paragraph

- UL item 1
- UL item 2

> Quote 1
> Quote 2
"""
        blocks = markdown_to_blocks(md)
        types = []
        for b in blocks:
            types.append(block_to_block_type(b))
        self.assertEqual(types, [BlockType.PARAGRAPH, BlockType.UNORDERED_LIST, BlockType.QUOTE])
    
    def test_blocktype2(self):
        md = """
```CODE Paragraph```

1. OL item 1
2. OL item 2

1. OL #2

### Heading 1

##### Heading 2
"""
        blocks = markdown_to_blocks(md)
        types = []
        for b in blocks:
            types.append(block_to_block_type(b))
        self.assertEqual(types, [BlockType.CODE, BlockType.ORDERED_LIST, BlockType.ORDERED_LIST, BlockType.HEADING, BlockType.HEADING])
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_ul_ol(self):
        md = """
- item 1
- item 2

1. item 1
2. item 2
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li></ul><ol><li>item 1</li><li>item 2</li></ol></div>",
        )
    
    def test_quote_head(self):
        md = """
# heading 1

### heading 3

> quote
> is something
> like this
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>heading 1</h1><h3>heading 3</h3><blockquote>quote is something like this</blockquote></div>",
        )

if __name__ == "__main__":
    unittest.main()