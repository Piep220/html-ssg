import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("tag")
        node2 = HTMLNode("tag")
        self.assertEqual(node, node2)

    def test_neq_tag(self):
        node = HTMLNode("tag")
        node2 = HTMLNode("tag2")
        self.assertNotEqual(node, node2)



    def test_neq_value(self):
        node = HTMLNode("tag", "value")
        node2 = HTMLNode("tag", "value2")
        self.assertNotEqual(node, node2)
    def test_neq_children(self):
        node = HTMLNode("tag", "value", ["child1"])
        node2 = HTMLNode("tag", "value", ["child2"])
        self.assertNotEqual(node, node2)
    def test_neq_props(self):
        node = HTMLNode("tag", "value", ["child1"], {"key": "value"})
        node2 = HTMLNode("tag", "value", ["child1"], {"key": "value2"})
        self.assertNotEqual(node, node2)
    def test_repr(self):
        node = HTMLNode("tag", "value", ["child1"], {"key": "value"})
        expected_repr = "HTMLNode(tag, value, ['child1'], {'key': 'value'})"
        self.assertEqual(repr(node), expected_repr)
    def test_repr_none(self):
        node = HTMLNode("tag", "value", None, None)
        expected_repr = "HTMLNode(tag, value, None, None)"
        self.assertEqual(repr(node), expected_repr)
    def test_repr_different_tag(self):
        node = HTMLNode("tag", "value", ["child1"], {"key": "value"})
        expected_repr = "HTMLNode(tag, value, ['child1'], {'key': 'value'})"
        self.assertEqual(repr(node), expected_repr)
    def test_repr_different_value(self):
        node = HTMLNode("tag", "value", ["child1"], {"key": "value"})
        expected_repr = "HTMLNode(tag, value, ['child1'], {'key': 'value'})"
        self.assertEqual(repr(node), expected_repr)
    def test_repr_different_children(self):
        node = HTMLNode("tag", "value", ["child1"], {"key": "value"})
        expected_repr = "HTMLNode(tag, value, ['child1'], {'key': 'value'})"
        self.assertEqual(repr(node), expected_repr)
 


    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com","target": "_blank",})
        to_html = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), to_html)

    def test_props_to_html_single_value(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com",})
        to_html = " href=\"https://www.google.com\""
        self.assertEqual(node.props_to_html(), to_html)

    def test_props_to_html_no_value(self):
        node = HTMLNode(None, None, None, {})
        to_html = ""
        self.assertEqual(node.props_to_html(), to_html)