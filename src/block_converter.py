from enum import Enum

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