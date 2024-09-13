from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
	text_type_text = "text"
	text_type_bold = "bold"
	text_type_italic = "italic"
	text_type_code = "code"
	text_type_link = "link"
	text_type_image = "image"

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, text_node):
		if self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url:
			return True
		return False
				
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
	
def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.text_type_text.value:
			return LeafNode(None , text_node.text)
		case TextType.text_type_bold.value:
			return LeafNode("b", text_node.text)
		case TextType.text_type_italic.value:
			return LeafNode("i", text_node.text)
		case TextType.text_type_code.value:
			return LeafNode("code",text_node.text)
		case TextType.text_type_link.value:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.text_type_image.value:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise ValueError("Invalid text type")