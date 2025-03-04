from textnode import *
from htmlnode import *
from func import *

def main():
    md = """
# heading 1

### heading 3

> quote
> is something
> like this
    """

    node = markdown_to_html_node(md)    
    html = node.to_html()
    print(html)

main()
