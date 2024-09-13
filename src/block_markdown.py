import re
from htmlnode import *
from textnode import *
from inline_markdown import *

paragraph = "paragraph"
heading = "heading"
code = "code"
quote = "quote"
unordered_list = "unordered list"
ordered_list = "ordered list"


def markdown_to_blocks(markdown):
    mk_strings = markdown.split("\n\n")
    result = []
    for string in mk_strings:
        if string == "":
            continue
        result.append(string.strip())
    return result

def block_to_block_type(block):
    if block != "":
        lines = block.split("\n")
        # Check for heading
        if re.match(r"^#{1,6} ", block) is not None:
            return heading
        # Check for code
        if block[0:3] == "```" and block[-3:] == "```":
            return code
        # Check for quote
        quote_counter = 0 
        for line in lines:
            if line.strip() and line[0] == ">":
                quote_counter += 1 
            else:
                break
        if quote_counter == len(lines):
            return quote
        # Check for unordered list
        unordered_counter = 0
        for line in lines:
            if re.match(r"[*-] ", line) is not None:
                unordered_counter += 1 
            else:
                break
        if unordered_counter == len(lines):
            return unordered_list
        # Check for ordered list
        ordered_counter = 1
        for line in lines:
            match =  re.match(r"(\d+)\. ", line)
            if match is None:
                break
            number = int(match.group(1))
            if number != ordered_counter:
                break
            ordered_counter += 1
        if ordered_counter == len(lines) + 1:
            return ordered_list
    # If none of the above conditions are met, block is a normal paragraph
    return paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode("div", [block_to_html_node(block) for block in blocks], None)
       
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == paragraph:
        return paragraph_block_to_html_node(block)
    if block_type == heading:
        return heading_block_to_html_node(block)
    if block_type == code:
        return code_block_to_html_node(block)
    if block_type == quote:
        return quote_block_to_html_node(block)
    if block_type == unordered_list:
        return unordered_list_block_to_html_node(block)
    if block_type == ordered_list:
        return ordered_list_block_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children
    
def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    para = " ".join(lines)
    children = text_to_children(para)
    return ParentNode("p", children)

def heading_block_to_html_node(block):
    h_level = len(re.match(r"^(#{1,6}) ", block).group(1))
    children = text_to_children(block[h_level + 1:])
    return ParentNode(f"h{h_level}", children)

def code_block_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    return ParentNode(
        "pre", 
        [ParentNode(
            "code", 
            [text_node_to_html_node(TextNode(block[3:-3], "text"))]
            )
        ]
    )

def quote_block_to_html_node(block):
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    quo = " ".join(lines)
    children = text_to_children(quo)
    return ParentNode("blockquote", children)

def unordered_list_block_to_html_node(block):
    lines = [ParentNode("li",text_to_children(line[2:])) for line in block.split("\n")]
    return ParentNode("ul", lines)

def ordered_list_block_to_html_node(block):
    lines = [ParentNode("li",text_to_children(line[3:])) for line in block.split("\n")]
    return ParentNode("ol", lines)
