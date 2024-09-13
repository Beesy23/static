import unittest

from textnode import TextNode, TextType
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
            node = TextNode("This is **bold** text", TextType.text_type_text.value)
            result = split_nodes_delimiter([node], "**", TextType.text_type_bold.value)

            self.assertListEqual(result, [
                TextNode("This is ", "text"), 
                TextNode("bold", "bold"),
                TextNode(" text", "text")
                ]
            )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is *italic* text", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "*", TextType.text_type_italic.value)

        self.assertListEqual(result, [
            TextNode("This is ", "text"), 
            TextNode("italic", "italic"),
            TextNode(" text", "text")
            ]
        )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "`", TextType.text_type_code.value)

        self.assertListEqual(result, [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
            ]
        )

    def test_split_nodes_delimiter_bold_empty(self):
        node = TextNode("**Bold** ** ** text", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "**", TextType.text_type_bold.value)
                
        self.assertListEqual(result, [
            TextNode("Bold", "bold"), 
            TextNode(" ", "text"),
            TextNode(" ", "bold"),
            TextNode(" text", "text")
            ]
        )

    def test_split_nodes_delimiter_italic_empty(self):
        node = TextNode("*Italic* * * text", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "*", TextType.text_type_italic.value)
                
        self.assertListEqual(result, [
            TextNode("Italic", "italic"), 
            TextNode(" ", "text"),
            TextNode(" ", "italic"),
            TextNode(" text", "text")
            ]
        )

    def test_split_nodes_delimiter_bold_multiword(self):    
        node = TextNode("This is text with a **bolded word** and **another**", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "**", TextType.text_type_bold.value)

        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded word", "bold"),
                TextNode(" and ", "text"),
                TextNode("another", "bold"),
            ],
            result,
        )

    def test_split_nodes_delimiter_italic_multiword(self):    
        node = TextNode("This is text with a *italic word* and *another*", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "*", TextType.text_type_italic.value)

        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("italic word", "italic"),
                TextNode(" and ", "text"),
                TextNode("another", "italic"),
            ],
            result,
        )

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("**Bold** and *italic*", TextType.text_type_text.value)
        result = split_nodes_delimiter([node], "**", TextType.text_type_bold.value)
        result = split_nodes_delimiter(result, "*", TextType.text_type_italic.value)

        self.assertListEqual(
            [
                TextNode("Bold", "bold"),
                TextNode(" and ", "text"),
                TextNode("italic", "italic"),
            ],
            result,
        )

    def test_split_node_delimiter_without_closing(self):
        node = TextNode("Invalid **bold text", TextType.text_type_text.value)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.text_type_bold.value)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        self.assertEqual(
            extract_markdown_images(text), [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        self.assertEqual(
            extract_markdown_links(text),[
                ("to boot dev", "https://www.boot.dev"), 
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text_type_text.value,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_type_text.value),
                TextNode("image", TextType.text_type_image.value, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            result,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.text_type_text.value,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_type_text.value),
                TextNode("link", TextType.text_type_link.value, "https://boot.dev"),
                TextNode(" and ", TextType.text_type_text.value),
                TextNode("another link", TextType.text_type_link.value, "https://blog.boot.dev"),   
                TextNode(" with text that follows", TextType.text_type_text.value),             
            ],
            result,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)

        self.assertListEqual([
            TextNode("This is ", TextType.text_type_text.value),
            TextNode("text", TextType.text_type_bold.value),
            TextNode(" with an ", TextType.text_type_text.value),
            TextNode("italic", TextType.text_type_italic.value),
            TextNode(" word and a ", TextType.text_type_text.value),
            TextNode("code block", TextType.text_type_code.value),
            TextNode(" and an ", TextType.text_type_text.value),
            TextNode("obi wan image", TextType.text_type_image.value, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.text_type_text.value),
            TextNode("link", TextType.text_type_link.value, "https://boot.dev"),
            ], 
            text_nodes 
        )


if __name__ == "__main__":
    unittest.main()