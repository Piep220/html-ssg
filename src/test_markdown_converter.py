import unittest
from textnode import TextNode, TextType
from markdown_converter import split_nodes_delimiter


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

    def test_text_with_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block and **bold text**", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("split_nodes_delimiter: Unmatched delimiter found" in str(context.exception))

    def test_text_with_empty_string(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [TextNode("", TextType.NORMAL)]
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



if __name__ == '__main__':
    unittest.main()
