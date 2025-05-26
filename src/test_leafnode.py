import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_br(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None).to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("span", "Important!", props={"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Important!</span>')

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("a", "Click me", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click me</a>')

    def test_leaf_to_html_special_characters(self):
        node = LeafNode("strong", "<&>\"'")
        self.assertEqual(node.to_html(), '<strong><&>"\'</strong>')

    def test_leaf_to_html_with_props_and_special_chars(self):
        with self.assertRaises(ValueError):
            LeafNode("img", None, props={"src": "image.jpg", "alt": "<&>\"'"}).to_html()



if __name__ == "__main__":
    unittest.main()