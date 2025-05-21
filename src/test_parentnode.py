import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span></div>",
        )
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    def test_to_html_with_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_to_html_with_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    def test_to_html_with_special_characters(self):
        child_node = LeafNode("span", "<&>'\"")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><&>\'"</span></div>',
        )
    def test_to_html_with_props_and_special_chars(self):
        child_node = LeafNode("span", "<&>'\"")
        parent_node = ParentNode(
            "div", [child_node], props={"class": "container", "id": "main"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span><&>\'"</span></div>',
        )
    def test_to_html_with_empty_string(self):
        child_node = LeafNode("span", "")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span></span></div>")
    def test_to_html_with_none_value(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_to_html_with_none_value_and_props(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        with self.assertRaises(ValueError):
            parent_node.to_html()
   



if __name__ == "__main__":
    unittest.main()