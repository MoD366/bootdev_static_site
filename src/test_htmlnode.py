import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNodes(unittest.TestCase):
    def test_link(self):
        node = HTMLNode("a", "important link", None, {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://google.com" target="_blank"')

    def test_inlinestyle(self):
        node = HTMLNode("p", "This is bold text", None, {"color": "red", "bgcolor": "black"})
        self.assertEqual(node.props_to_html(),' color="red" bgcolor="black"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_link(self):
        node = LeafNode("a", "important link", {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://google.com" target="_blank">important link</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_two_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1,child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("i", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2 = ParentNode("u", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1,child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b></span><u><i>grandchild2</i></u></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")