import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://example.org")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        expected_repr = "TextNode(This is a text node, bold, http://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        expected_repr = "TextNode(This is a text node, bold, http://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        expected_repr = "TextNode(This is a text node, bold, http://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        expected_repr = "TextNode(This is a text node, bold, http://example.com)"
        self.assertEqual(repr(node), expected_repr)
        
    def test_repr_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        expected_repr = "TextNode(This is a text node, bold, http://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_different_text_type_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        expected_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_different_text_type_none_different(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        expected_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected_repr)
        
    def test_repr_different_text_type_none_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        expected_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()