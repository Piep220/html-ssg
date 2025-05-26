from enum import Enum
from htmlnode import HTMLNode
from converters import text_node_to_html_node
from textnode import TextType, TextNode
from markdown_converter import text_to_textnodes
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def markdown_to_blocks(markdown):
    if markdown is None: return
    lines = markdown.split("\n\n")
    new_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line != "":
            new_lines.append(clean_line)
    return new_lines

def block_to_block_type(block:str):
    if block is None:
        return None
    if block.startswith("#"):
        if len(block.strip("#")) > 1:
            if len(block) - len(block.lstrip("#")) > 6:
                return BlockType.PARA
            return BlockType.HEAD
    if block.startswith("```") and block.endswith("```"):
        if len(block.strip("`")) > 1:
            return BlockType.CODE
    if block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARA
        return BlockType.QUOTE
    if block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARA
        return BlockType.UNORDERED
    if block.startswith("1. "):
        lines = block.split("\n")
        for i in range(0, len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARA
        return BlockType.ORDERED
    return BlockType.PARA

def text_to_children(text:str):
    match block_to_block_type(text):
        #https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Lists
        case BlockType.PARA:
            return block_convert_para(text)
        case BlockType.HEAD:
            return HTMLNode("h1", text)
        case BlockType.QUOTE:
            return block_convert_quote(text)
        case BlockType.CODE:
            leaf = text_node_to_html_node(TextNode(text[3:-3], TextType.CODE))
            return LeafNode("pre", leaf)
        case BlockType.UNORDERED:
            return HTMLNode("ul", text)
        case BlockType.ORDERED:
            return HTMLNode("ol", text)

def block_convert_para(text:str):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", leaf_nodes)

def block_convert_head(text:str):
    pass

def block_convert_quote(text:str):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return ParentNode("blockquote", text_nodes)

def block_convert_unordered(text:str):
    pass

def block_convert_ordered(text:str):
    pass

def markdown_to_html_node(markdown:str):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(text_to_children(block))

    return ParentNode("div", nodes)