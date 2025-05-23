import re
from textnode import TextNode, TextType


def split_nodes_delimiter_old(old_nodes, delimiter, text_type):
    #Word split logic fails when more than one delimiter type is used
    new_nodes = []
    for old_node in old_nodes:
        # if a node is not text just add to list to return
        if old_node.text_type is not TextType.NORMAL:
            new_nodes.append(old_node)
        # no need for logic if text is blank
        elif old_node.text == "":
            new_nodes.append(old_node)
        else:
            start_delimit, end_delimit = False, False
            new_node_text = ""
            for word in old_node.text.split():
                if word.startswith(delimiter):
                    start_delimit = True
                    if new_node_text != "":
                        #new_node_text += " "
                        new_nodes.append(TextNode(new_node_text,TextType.NORMAL))
                    new_node_text = word.replace(delimiter, "")
                elif word.endswith(delimiter):
                    end_delimit = True
                    if new_node_text != "":
                        new_node_text += " " + word.replace(delimiter, "")
                        new_nodes.append(TextNode(new_node_text, text_type))
                    new_node_text = " "
                else:
                    new_node_text += word + " "
            #if start_delimit is True and end_delimit is False:
            #    raise Exception("split_node_delimit, no end delimit found")
            if new_node_text != "":
                new_node_text = new_node_text[:-1]
                new_nodes.append(TextNode(new_node_text, TextType.NORMAL))
    
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if type(old_nodes) is not list:
        old_nodes = [old_nodes]
    # new word split method
    new_nodes = []
    for node in old_nodes:
        if type(node) is not TextNode or node.text is None or node.text == "": 
            continue
        # just add if already in a typed block
        if node.text_type is not TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        # skip logic when blank
        if node.text == "":
            new_nodes.append(node)

        parts = node.text.split(delimiter)
        # check in delimiters are in pairs
        if len(parts) % 2 == 0:
            raise Exception("split_nodes_delimiter: Unmatched delimiter found")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

"""
node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
"""

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

"""
!\[.*?\]\(.*?\)
!     \[([^\[\]]*)\]\(([^\(\)]*)\)
(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)

img r"!\[([^\[\]].*?)\]\(([^\(\)].*?)\)"
url r"(?<!!)\[([^\[\]].*?)\]\(([^\(\)].*?)\)"
"""


def split_nodes_image(old_nodes):
    if type(old_nodes) is not list:
        old_nodes = [old_nodes]
    new_nodes = []
    link_pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    for node in old_nodes:
        if type(node) is not TextNode or node.text is None or node.text == "": 
            continue
        if node.text_type is not TextType.NORMAL:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in link_pattern.finditer(text):
            # Add text before the link as NORMAL
            if match.start() > last_index:
                before = text[last_index:match.start()]
                if before:
                    new_nodes.append(TextNode(before, TextType.NORMAL))
            # Add the link as LINK
            anchor, url = match.group(1), match.group(2)
            new_nodes.append(TextNode(anchor, TextType.IMAGE, url))
            last_index = match.end()
        # Add any remaining text after the last link
        if last_index < len(text):
            after = text[last_index:]
            if after:
                new_nodes.append(TextNode(after, TextType.NORMAL))
    return new_nodes


def split_nodes_link1(old_nodes):
    if type(old_nodes) is not list:
        old_nodes = [old_nodes]
    # new word split method
    new_nodes = []
    for node in old_nodes:
        if type(node) is not TextNode or node.text is None or node.text == "": 
            continue
        # just add if already in a typed block
        if node.text_type is not TextType.NORMAL:
            new_nodes.append(node)
            continue

        #if no link, skip
        node_link = extract_markdown_links(node.text)
        if extract_markdown_links(node.text) == []:
            new_nodes.append(node)
            continue
        
        # skip logic when blank
        if node.text == "":
            new_nodes.append(node)

        parts = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        #return parts
        i, j = 0, 0
        max_i = len(parts)
        max_j = len(node_link)
        while i < max_i:
            if i > max_i - 1:
                return
            elif parts[i] == "":
                i += 1
            elif parts[i] == node_link[j][0]:
                new_nodes.append(TextNode(parts[i], TextType.LINK, parts[i+1]))
                i += 2
                j += 1
                if j == max_j: j=0
            else:
                new_nodes.append(TextNode(parts[i], TextType.NORMAL))
                i += 1
        return new_nodes

def split_nodes_link(old_nodes):
    if type(old_nodes) is not list:
        old_nodes = [old_nodes]
    new_nodes = []
    link_pattern = re.compile(r"(?<!!)(?<!\\)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    for node in old_nodes:
        if type(node) is not TextNode or node.text is None: 
            continue
        if node.text_type is not TextType.NORMAL:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in link_pattern.finditer(text):
            # Add text before the link as NORMAL
            if match.start() > last_index:
                before = text[last_index:match.start()]
                if before:
                    new_nodes.append(TextNode(before, TextType.NORMAL))
            # Add the link as LINK
            anchor, url = match.group(1), match.group(2)
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            last_index = match.end()
        # Add any remaining text after the last link
        if last_index < len(text):
            after = text[last_index:]
            if after:
                new_nodes.append(TextNode(after, TextType.NORMAL))
    return new_nodes

