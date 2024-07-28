import re
from unittest import result
from leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_types, delimiter, text_type):
    new_nodes = []

    for node in old_types:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
                
        splited_lines = node.text.split(delimiter)

        if len(splited_lines) % 2 == 0:
            raise ValueError("Mismatched delimiter found in text node.")
        
        for i, line in enumerate(splited_lines):
            if i % 2 == 0:
                if line: 
                    new_nodes.append(TextNode(line, text_type_text))
            else:
                new_nodes.append(TextNode(line, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue
        
        for image_alt, url in images:
            link_markdown = f"![{image_alt}]({url})"
            sections = text.split(link_markdown, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], node.text_type))
            new_nodes.append(TextNode(image_alt, text_type_image, url))
            text = sections[1]
        
        if text:
            new_nodes.append(TextNode(text, node.text_type))
            
    return new_nodes 
    
def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue
        
        for link_text, url in links:
            link_markdown = f"[{link_text}]({url})"
            sections = node.text.split(link_markdown, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], node.text_type))
            new_nodes.append(TextNode(link_text, text_type_link, url))
            node.text = sections[1]
        
        if node.text:
            new_nodes.append(TextNode(node.text, node.text_type))
            
    return new_nodes

def text_to_textnode(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    