import unittest
from textnode import TextNode, TextType
from block_converter import *


class MarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    def test_none(self):
        md = None
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, None)
    def test_markdown_to_blocks_lots_of_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items

# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.





- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"

            ],
        )

    def test_markdown_to_blocks_excessive_whitespace(self):
        #both tabs and spaces
        md = """
        This is **bolded** paragraph

              This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    

- This is a list
- with items   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class BlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("## Another Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("### 3 Another Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("#### 4 Another Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("##### 5 Another Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("###### 6 Another Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("####### 7 Another Heading"), BlockType.PARA) # Too many #
        self.assertEqual(block_to_block_type("#"), BlockType.PARA)  # Only hash, not a headin
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```print('hi')```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code\nline2\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```"), BlockType.PARA)  # Only backtick
    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\nNot a quote"), BlockType.PARA)
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type("- item 1\nitem 2"), BlockType.PARA)
        self.assertEqual(block_to_block_type("- item 1"), BlockType.UNORDERED)
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), BlockType.ORDERED)
        self.assertEqual(block_to_block_type("1. item 1\n3. item 2"), BlockType.PARA)
        self.assertEqual(block_to_block_type("1. item 1"), BlockType.ORDERED)
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a paragraph."), BlockType.PARA)
        self.assertEqual(block_to_block_type(""), BlockType.PARA)
        self.assertEqual(block_to_block_type("   "), BlockType.PARA)
        self.assertEqual(block_to_block_type(None), None)

class MarkdownToHTMLNode(unittest.TestCase):
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

        
if __name__ == '__main__':
    unittest.main()
