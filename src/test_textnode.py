import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "text")
        node2 = TextNode("This is a text node", "text")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", "text")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", "text")
        node2 = TextNode("This is a text node2", "text")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "italic", "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", "italic", "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "text", "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node", "text")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode(
            "This is a text node", 
            "link", 
            "https://www.boot.dev"
        )
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(
            html_node.props, 
            {"href": "https://www.boot.dev"}
        )

    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            "This is an image", 
            "image", 
            "https://www.boot.dev"
        )
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

if __name__ == "__main__":
    unittest.main()