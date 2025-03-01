from htmlnode import *
from textnode import *
import re

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
    
