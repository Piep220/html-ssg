import unittest
from textnode import TextNode, TextType
from markdown_converter import *


class TestMarkdownConverter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and **bold text**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_multiple_delimiters_out_of_order(self):
        node = TextNode("`code block` and **bold text** and _italic text_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code block`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_adjacent_delimiters(self):
        node = TextNode("`code1``code2`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_with_empty_content(self):
        node = TextNode("``", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_with_text_before_and_after(self):
        node = TextNode("before `code` after", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("before ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_with_spaces_inside(self):
        node = TextNode("**bold text** and **more bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("more bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_with_special_characters(self):
        node = TextNode("This is `code!@#` and **bold$%^**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code!@#", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold$%^", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_multiple_delimiters_out_of_order_no_space(self):
        node = TextNode("`code block`and**bold text**and_italic text_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("code block", TextType.CODE),
            TextNode("and", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode("and", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block and **bold text**", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("split_nodes_delimiter: Unmatched delimiter found" in str(context.exception))

    def test_text_with_empty_string(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_no_delimiter(self):
        node = TextNode("This is text without delimiters", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [TextNode("This is text without delimiters", TextType.NORMAL)]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_only_delimiters(self):   
        node = TextNode("`**`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("**", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

class TestLinkAndImageConverter(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_markdown_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_markdown_two_url(self):
        text ="This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_two_images_no_space(self):
        text = "This is text with a![rick roll](https://i.imgur.com/aKaOqIh.gif)and![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_markdown_two_url_no_space(self):
        text ="This is text with a link[to boot dev](https://www.boot.dev)and[to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text without images"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(
            "This is text without links"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_empty_string(self):
        text = ""
        self.assertListEqual([], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_no_delimiter(self):
        text = "This is text without delimiters"
        self.assertListEqual([], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_only_delimiters(self):
        text = "[**](**)"
        self.assertListEqual([('**', '**')], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_only_delimiters2(self):
        text = "![**](**)"
        self.assertListEqual([], extract_markdown_links(text))
        self.assertListEqual([('**', '**')], extract_markdown_images(text))

    def test_extract_markdown_unmatched_delimiter(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

class SplitNodeLinkAndImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_long_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_node = TextNode(text, TextType.NORMAL)
        link_check = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), This is text with a link ", TextType.NORMAL, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" and ", TextType.NORMAL, None), 
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            TextNode(" and some more text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL, None), 
        ]
        image_check = [
            TextNode("This is text with a ", TextType.NORMAL, None), 
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.NORMAL, None), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(", This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text ", TextType.NORMAL, None), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(split_nodes_link(test_node), link_check)
        self.assertListEqual(split_nodes_image(test_node), image_check)

    def test_long_text_many(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_node = TextNode(text, TextType.NORMAL)
        link_check = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), This is text with a link ", TextType.NORMAL, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" and ", TextType.NORMAL, None), 
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            TextNode(" and some more text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL, None), 
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), This is text with a link ", TextType.NORMAL, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" and ", TextType.NORMAL, None), 
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            TextNode(" and some more text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL, None), 
        ]
        image_check = [
            TextNode("This is text with a ", TextType.NORMAL, None), 
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.NORMAL, None), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(", This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text ", TextType.NORMAL, None), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is text with a ", TextType.NORMAL, None), 
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.NORMAL, None), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(", This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text ", TextType.NORMAL, None), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(split_nodes_link([test_node, test_node]), link_check)
        self.assertListEqual(split_nodes_image([test_node, test_node]), image_check)

    def test_empty(self):
        text = ""
        test_node = TextNode(text, TextType.NORMAL)
        link_check = []
        image_check = []
        self.assertListEqual(split_nodes_link(test_node), link_check)
        self.assertListEqual(split_nodes_image(test_node), image_check)

    def test_none(self):
        text = None
        test_node = TextNode(text, TextType.NORMAL)
        link_check = []
        image_check = []
        self.assertListEqual(split_nodes_link(test_node), link_check)
        self.assertListEqual(split_nodes_image(test_node), image_check)

    def test_text_only(self):
        text = "just some text"
        test_node = TextNode(text, TextType.NORMAL)
        link_check = [
            TextNode(text, TextType.NORMAL)
        ]
        image_check = [
            TextNode(text, TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_link(test_node), link_check)
        self.assertListEqual(split_nodes_image(test_node), image_check)

    def test_link_and_image_adjacent(self):
        node = TextNode("![img](url)![img2](url2)[link](url3)", TextType.NORMAL)
        expected_images = [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode("[link](url3)", TextType.NORMAL)
        ]
        expected_links = [
            TextNode("![img](url)![img2](url2)", TextType.NORMAL),
            TextNode("link", TextType.LINK, "url3")
        ]
        self.assertListEqual(split_nodes_image(node), expected_images)
        self.assertListEqual(split_nodes_link(node), expected_links)

    def not_test_link_inside_image_alt_text(self):
        #not testing for nested expressions
        node = TextNode("![alt [link](url)](imgurl)", TextType.NORMAL)
        # Should treat as a single image, not as a link
        expected_images = [
            TextNode("alt [link](url)", TextType.IMAGE, "imgurl")
        ]
        expected_links = [
            TextNode("![alt [link](url)](imgurl)", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_image(node), expected_images)
        self.assertListEqual(split_nodes_link(node), expected_links)

    def not_test_image_inside_link_text(self):
        #not testing for nested expressions
        node = TextNode("[![alt](imgurl)](linkurl)", TextType.NORMAL)
        # Should treat as a single link, not as an image
        expected_links = [
            TextNode("![alt](imgurl)", TextType.LINK, "linkurl")
        ]
        expected_images = [
            TextNode("[![alt](imgurl)](linkurl)", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_link(node), expected_links)
        self.assertListEqual(split_nodes_image(node), expected_images)

    def test_link_and_image_with_escaped_brackets(self):
        node = TextNode(r"This is a link \[notalink](url) and !\[notanimage](img)", TextType.NORMAL)
        expected_links = [
            TextNode(r"This is a link \[notalink](url) and !\[notanimage](img)", TextType.NORMAL)
        ]
        expected_images = [
            TextNode(r"This is a link \[notalink](url) and !\[notanimage](img)", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_link(node), expected_links)
        self.assertListEqual(split_nodes_image(node), expected_images)

    def not_test_link_and_image_with_nested_parentheses(self):
        #not testing for nested expressions
        node = TextNode("![alt](img(url)) and [text](url(more))", TextType.NORMAL)
        expected_images = [
            TextNode("alt", TextType.IMAGE, "img(url)"),
            TextNode(" and [text](url(more))", TextType.NORMAL)
        ]
        expected_links = [
            TextNode("![alt](img(url)) and ", TextType.NORMAL),
            TextNode("text", TextType.LINK, "url(more)")
        ]
        self.assertListEqual(split_nodes_image(node), expected_images)
        self.assertListEqual(split_nodes_link(node), expected_links)

if __name__ == '__main__':
    unittest.main()
