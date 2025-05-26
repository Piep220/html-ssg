from pprint import pprint
# Imports from project files
from textnode import TextNode, TextType
from markdown_converter import *
from block_converter import *



def main():
    print("hello world")
    #test_TextNode = TextNode("test text", "link", "http://www.google.com")
    #print(test_TextNode)
    #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #test = extract_markdown_images(text)
    #print(test)
    #print(type(test))
    #print(type(test[0]))
    #text = "This is text with a [link](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev)"
    #print(extract_markdown_links(text))
    #node = TextNode(
    #    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text",
    #    TextType.NORMAL,
    #)
    #print(re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))
    #print(split_nodes_link([node]))
    #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #test = extract_markdown_images(text)
    #print(test)
    #node = TextNode(
    #    "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg),This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
    #    TextType.NORMAL,
    #)
    #print(split_nodes_image([node]))
    #print(type(node))
    #print(type([node]))
    #text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #pprint(text_to_textnodes("None"))
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


- This is the first list item in a list block     
- This is a list item
- This is another list item      
"""
    #test = markdown_to_blocks(markdown)
    #pprint(markdown)
    #print(type(test), len(test))
    #print(test)
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    #print(md)
    #print("<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
    #pprint(markdown_to_html_node(md))
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    #print("###########################")
    #print(md)
    #print("<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
    #test = markdown_to_html_node(md).to_html()
    #print(test)
    #for node in test.children:
    #    print(type(node))

main()

