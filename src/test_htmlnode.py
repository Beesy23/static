import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_repr(self):
		html = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )

		self.assertEqual(
            html.__repr__(),
            "HTMLNode(tag= p, value= What a strange world, children= None, props= {'class': 'primary'})",
			)

	def test_defaults(self):
		html = HTMLNode()

		self.assertEqual(
			"HTMLNode(tag= None, value= None, children= None, props= None)", 
			repr(html)
		)

	def test_values(self):
		html = HTMLNode(
            "div",
            "I wish I could read",
        )
		self.assertEqual(
            html.tag,
            "div",
        )
		self.assertEqual(
            html.value,
            "I wish I could read",
        )
		self.assertEqual(
            html.children,
            None,
        )
		self.assertEqual(
            html.props,
            None,
        )

	def test_props_to_html_with_props(self):
		html = HTMLNode(
			"p", 
			"This is a test", 
			["child1", "child2"], 
			{"href" : "https://www.google.com", "target" : "_blank"}
		)

		self.assertEqual(
			' href="https://www.google.com" target="_blank"', 
			html.props_to_html()
		)

	def test_props_to_html_without_props(self):
		html = HTMLNode(
			"p", 
			"This is a test", 
			["child1", "child2"]
		)

		self.assertEqual(
			"", 
			html.props_to_html()
		)

	def test_to_html_no_children(self):
		leaf = LeafNode("p", "This is a paragraph of text.")

		self.assertEqual(
        	leaf.to_html(),
            "<p>This is a paragraph of text.</p>"
        )
	
	def test_to_html_no_tag(self):
		leaf = LeafNode(None, "Hello World!")

		self.assertEqual(
			leaf.to_html(),
			"Hello World!"
		)

	def test_to_html_parent(self):
		parent = ParentNode(
			"p",
    		[
        		LeafNode("b", "Bold text"),
        		LeafNode(None, "Normal text"),
        		LeafNode("i", "italic text"),
        		LeafNode(None, "Normal text"),
    		],
		)

		self.assertEqual(
			"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", 
			parent.to_html()
		)

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			"<div><span>child</span></div>",
			parent_node.to_html()
		)
		
	def test_to_html_with_granchildren(self):
		grandchild_node = LeafNode("b","grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent = ParentNode("div",[child_node])

		self.assertEqual(
			"<div><span><b>grandchild</b></span></div>",
			parent.to_html()
		)

	def test_no_children_raises_exception(self):
        # Use assertRaises as a context manager
		with self.assertRaises(ValueError):
			ParentNode("p", None).to_html()

if __name__ == "__main__":
	unittest.main()
