from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextType, TextNode
from markdown_converter import text_to_textnodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, f"href=\"{text_node.url}\"")
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            #return LeafNode("img", "", f"src=\"{text_node.url}\" alt=\"{text_node.text}\"")
        #case _:
        #    return ValueError("invalid text type for text to html conversion")
        

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

def block_to_html_node(text:str):
    match block_to_block_type(text):
        #https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Lists
        case BlockType.PARA:
            return block_convert_para(text)
        case BlockType.HEAD:
            return block_convert_head(text)
        case BlockType.QUOTE:
            return block_convert_quote(text)
        case BlockType.CODE:
            return block_convert_code(text)
        case BlockType.UNORDERED:
            return block_convert_unordered(text)
        case BlockType.ORDERED:
            return block_convert_ordered(text)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text:str):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_convert_para(text:str):
    lines = text.split("\n")
    para = " ".join(lines)
    children = text_to_children(para)
    return ParentNode("p", children)

def block_convert_head(text:str):
    level = 0
    for char in text:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(text):
        raise ValueError(f"invalid heading level: {level}")
    children = text_to_children(text[level + 1 :])
    return ParentNode(f"h{level}", children)

def block_convert_code(text:str):
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("invalid code block")
    trimmed_text = text[3:-3]
    if trimmed_text.startswith("\n"):
        trimmed_text = trimmed_text[1:]
    leaf = text_node_to_html_node(TextNode(trimmed_text, TextType.NORMAL))
    child = ParentNode("code", [leaf])
    return ParentNode("pre", [child])

def block_convert_quote(text:str):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(content))

def block_convert_unordered(text:str):
    html_items = []
    for line in text.split("\n"):
        children = text_to_children(line[2:])
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_convert_ordered(text:str):
    html_items = []
    for line in text.split("\n"):
        children = text_to_children(line[3:])
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def markdown_to_html_node(markdown:str):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        nodes.append(html_node)
    return ParentNode("div", nodes, None)