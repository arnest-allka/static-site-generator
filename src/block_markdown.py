import re
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    new_blocks = [block.strip() for block in new_blocks]
    new_blocks = [block for block in new_blocks if block]
    return new_blocks

def block_to_block_type(block):
    heading = re.findall(r'^(#{1,6})\s+(.*)', block)
    
    if heading:
        return block_type_heading
    elif block[:3] == '```' and block[len(block)-3:] == '```': 
        return block_type_code
    else:
        count = 0
        block_type = ''
        lines = block.split('\n')
        for i, line in enumerate(lines):
            if line[0] == '>':
                block_type = block_type_quote
                count += 1
            elif line[:2] == '* ' or line[:2] == '- ':
                block_type = block_type_ulist
                count += 1
            elif line[:3] == f"{i+1}. ":
                block_type = block_type_olist
                count += 1
        if count == len(lines):
            return block_type
        else:
            return block_type_paragraph
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    elif block_type == block_type_heading:
        return heading_to_html_node(block)
    elif block_type == block_type_code:
        return code_to_html_node(block)
    elif block_type == block_type_olist:
        return olist_to_html_node(block)
    elif block_type == block_type_ulist:
        return ulist_to_html_node(block)
    elif block_type == block_type_quote:
        return quote_to_html_node(block)
    else:
        raise ValueError("Invalid block type")
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []        
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
        
def paragraph_to_html_node(block):
    lines = block.split('\n')
    paragraph = ' '.join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level+=1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}") 
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode('code', children)
    return ParentNode('pre', [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode('li', children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode('li', children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    print(content)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
