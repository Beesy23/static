import unittest
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        raw = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
This is the same paragraph on a new line

* This is the first list item in a list block
* This is a list item
* This is another list item"""    
        blocks = markdown_to_blocks(raw)

        self.assertEqual([
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is the same paragraph on a new line",
            """* This is the first list item in a list block\n* This is a list item\n* This is another list item"""
            ],
            blocks
        )

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is the same paragraph on a new line"
        result = block_to_block_type(block)

        self.assertEqual(result, paragraph)

    def test_block_to_block_type_heading(self):
        block1 = "# This is a heading"
        block2 = "## This is a heading"
        block3 = "### This is a heading"
        block4 = "#### This is a heading"
        block5 = "##### This is a heading"
        block6 = "###### This is a heading"
        block7 = "####### This is not a heading"
        result1 = block_to_block_type(block1)
        result2 = block_to_block_type(block2)
        result3 = block_to_block_type(block3)
        result4 = block_to_block_type(block4)
        result5 = block_to_block_type(block5)
        result6 = block_to_block_type(block6)
        result7 = block_to_block_type(block7)
        
        self.assertEqual(result1, heading)
        self.assertEqual(result2, heading)
        self.assertEqual(result3, heading)
        self.assertEqual(result4, heading)
        self.assertEqual(result5, heading)
        self.assertEqual(result6, heading)
        self.assertNotEqual(result7, heading)

    def test_block_to_block_type_code(self):
        block = "```This is a block of code```"
        result = block_to_block_type(block)
        
        self.assertEqual(result, code)

    def test_block_to_block_type_quote(self):
        block = ">This is the first line of a qoute\n>This is the second line\n>This is the last line of the quote"
        result = block_to_block_type(block)
        
        self.assertEqual(result, quote)

    def test_block_to_block_type_unordered_list(self):
        block1 = "* This is the first item of an unordered list\n* This is the second item\n* This is the last item of an unordered list"
        result1 = block_to_block_type(block1)
        block2 = "- This is the first item of an unordered list\n- This is the second item\n- This is the last item of an unordered list"
        result2 = block_to_block_type(block2)
        block3 = "- This is the first item of an unordered list\n* This is the second item\n- This is the last item of an unordered list"
        result3 = block_to_block_type(block3)

        self.assertEqual(result1, unordered_list)
        self.assertEqual(result2, unordered_list)
        self.assertEqual(result3, unordered_list)

    def test_block_to_block_type_ordered_list(self):
        block1 = "1. This is the first item of an ordered list\n2. This is the second item\n3. This is the last item of an ordered list"
        result1 = block_to_block_type(block1)
        block2 = "1. This is the first item of an ordered list\n3. This is the second item\n2. This is the last item of an ordered list"
        result2 = block_to_block_type(block2)
        block3 = "1 This is the first item of an ordered list\n2 This is the second item\n3 This is the last item of an ordered list"
        result3 = block_to_block_type(block3)

        self.assertEqual(result1, ordered_list)
        self.assertNotEqual(result2, ordered_list)
        self.assertNotEqual(result3, ordered_list)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
if __name__ == "__main__":
    unittest.main()