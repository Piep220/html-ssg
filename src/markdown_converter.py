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
    # new word split method
    new_nodes = []
    for node in old_nodes:
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