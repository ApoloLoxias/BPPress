import unittest

from blockmd import markdown_to_blocks, BlockType, block_to_block_type



class test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



class test_block_to_blocktype(unittest.TestCase):
    def test_block_to_blocktype(self):
        blocks = [
            "Paragrah",
            "### Heading",
            "```Code```",
            ">Quote\n>second line",
            "- Unoredered\n- List",
            "1. Ordered\n2. List",
        ]
        text_types = [
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
        ]
        for block, text_type in zip(blocks, text_types):
            self.assertEqual(block_to_block_type(block), text_type)