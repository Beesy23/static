from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	result = []
	for node in old_nodes:
		if node.text_type != TextType.text_type_text.value:
			result.append(node)
			continue
		
		parts = node.text.split(delimiter)
		if len(parts) == 1:
			result.append(node)
			continue
		if len(parts) % 2 == 0:
			raise Exception("Invalid Markdown Syntax, closing delimiter not found!")

		for index, part in enumerate(parts):
			if part == "":
				continue
			if index % 2 == 0:
				result.append(TextNode(part, TextType.text_type_text.value))
			else:
				result.append(TextNode(part, text_type))
	return result

def split_nodes_image(old_nodes):
	result = []
	for node in old_nodes:
		if node.text_type != TextType.text_type_text.value:
			result.append(node)
			continue
		text = node.text
		images = extract_markdown_images(text)
		if len(images) == 0:
			result.append(node)
			continue
		for image in images:
			sections = text.split(f"![{image[0]}]({image[1]})", 1)
			if len(sections) !=2:
				raise Exception("Invalid Markdown Syntax, image closing delimiter not found!")
			if sections[0] != "":
				result.append(TextNode(sections[0], TextType.text_type_text.value))
			result.append(
				TextNode(image[0], TextType.text_type_image.value, image[1])
			)
			text = sections[1]
		if text != "":
			result.append(TextNode(text, TextType.text_type_text.value))
	return result

def split_nodes_link(old_nodes):
	result = []
	for node in old_nodes:
		if node.text_type != TextType.text_type_text.value:
			result.append(node)
			continue
		text = node.text
		links = extract_markdown_links(text)
		if len(links) == 0:
			result.append(node)
			continue
		for link in links:
			sections = text.split(f"[{link[0]}]({link[1]})", 1)
			if len(sections) !=2:
				raise Exception("Invalid Markdown Syntax, link closing delimiter not found!")
			if sections[0] != "":
				result.append(TextNode(sections[0], TextType.text_type_text.value))
			result.append(
				TextNode(link[0], TextType.text_type_link.value, link[1])
			)
			text = sections[1]
		if text != "":
			result.append(TextNode(text, TextType.text_type_text.value))
	return result

def text_to_textnodes(text):
	result = [TextNode(text, TextType.text_type_text.value)]
	result = split_nodes_delimiter(result, "**", TextType.text_type_bold.value)
	result = split_nodes_delimiter(result, "*", TextType.text_type_italic.value)
	result = split_nodes_delimiter(result, "`", TextType.text_type_code.value)
	result = split_nodes_image(result)
	result = split_nodes_link(result)
	return result

import re

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)