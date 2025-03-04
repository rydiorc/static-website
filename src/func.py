from htmlnode import *
from textnode import *

import re

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    QUOTE = "QUOTE"
    CODE = "CODE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new = []
    for node in old_nodes:
        
        if node.text_type is not TextType.TEXT or node.text.find(delimiter) < 0:
            new.append(node)
            continue
        
        if node.text.count(delimiter) < 2:
            raise Exception("that's invalid Markdown syntax.")
        
        split = node.text.split(delimiter, maxsplit=2)        
        split[0] = TextNode(split[0], TextType.TEXT, None)
        split[1] = TextNode(split[1], text_type, None)
        split[2] = TextNode(split[2], TextType.TEXT, None)
        new.extend(split)

    return new

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\]]*)\]\(([^)]*)\)", text)
    return matches    

def split_nodes_image(old_nodes):
    new = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new.append(node)
            continue
        
        for i in range(len(matches)):
            image_alt = matches[i][0]
            image_link = matches[i][1]
            if i == 0:
                sections = node.text.split(f"![{image_alt}]({image_link})", 1)
            else:
                sections = sections[1].split(f"![{image_alt}]({image_link})", 1)
            #print(sections)            
            new.append(TextNode(sections[0], TextType.TEXT, None))
            new.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            if(i+1 == len(matches) and len(sections) > 1 and sections[1] != ""):
                new.append(TextNode(sections[1], TextType.TEXT, None))
    return new

def split_nodes_link(old_nodes):
    new = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new.append(node)
            continue             
        for i in range(len(matches)):
            link_alt = matches[i][0]
            link = matches[i][1]
            if i == 0:
                sections = node.text.split(f"[{link_alt}]({link})", 1)
            else:
                sections = sections[1].split(f"[{link_alt}]({link})", 1)            
            new.append(TextNode(sections[0], TextType.TEXT, None))
            new.append(TextNode(link_alt, TextType.LINK, link))
            if(i+1 == len(matches) and len(sections) > 1 and sections[1] != ""):
                new.append(TextNode(sections[1], TextType.TEXT, None))
    return new

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)    
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(filter(lambda s: s != "", list(map(lambda s: s.strip(), blocks))))
    return blocks

def block_to_block_type(block):
    matches = re.findall(r"(#{1,6}) \w+", block)
    if len(matches) > 0:
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.find("\n"):
        lines = block.split("\n")
    else:
        lines = block
    if len(list(filter(lambda a: a.startswith(">"), lines))) == len(lines):
        return BlockType.QUOTE
    if len(list(filter(lambda a: a.startswith("- "), lines))) == len(lines):
        return BlockType.UNORDERED_LIST
    is_list = True
    if len(lines) > 1:
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                is_list = False
    else:
        if not lines[0].startswith("1. "):
            is_list = False
    if is_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_node(block, blocktype):
    tag = None
    use_func = True
    match blocktype:
        case BlockType.PARAGRAPH:
            tag = "p"
            text = block.replace("\n", " ")
        case BlockType.CODE:
            tag = "pre"            
            lines = block.replace("```", "").split("\n")
            lines = list(filter(lambda a: not a.isspace() and a != "", lines))
            
            text = ""
            for l in lines:
                text += l.strip() + "\n"            
            node = TextNode(text, TextType.CODE)
            children = [node.text_node_to_html_node()]
            use_func = False
        case BlockType.UNORDERED_LIST:
            tag = "ul"
            items = block.replace("- ", "").split("\n")
            children = []
            for i in items:
                node = LeafNode("li", i)
                children.append(node)
            use_func = False
        case BlockType.ORDERED_LIST:
            tag = "ol"
            items = block.split("\n")
            children = []
            for i in items:
                node = LeafNode("li", i[3:])
                children.append(node)
            use_func = False
        case BlockType.QUOTE:
            tag = "blockquote"
            text = block.replace("> ", "").replace("\n", " ")
        case BlockType.HEADING:
            size = block.count("#")
            tag = f"h{size}"
            text = block.replace("#", "").lstrip()
    if use_func:
        children = text_to_textnodes(text)
        children = list(map(lambda a: a.text_node_to_html_node(), children))
    parent = ParentNode(tag, children)
    return parent

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for b in blocks:
        btype = block_to_block_type(b)
        nodes.append(block_to_node(b, btype))
    html = ParentNode("div", nodes)
    return html