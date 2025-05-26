import unittest
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from block_converter import text_node_to_html_node


class TestConverters(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children, [])

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children, [])

    def test_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children, [])

    def test_code(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children, [])

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, 'href="https://example.com"')
        self.assertEqual(html_node.children, [])
        
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://example.com/image.png', 'alt': 'This is an image'})
        self.assertEqual(html_node.children, [])

    def test_no_text(self):
        node = TextNode("", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children, [])


if __name__ == '__main__':
    unittest.main()
