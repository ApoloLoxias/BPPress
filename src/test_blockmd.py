import unittest

from blockmd import(
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    MD_Block,
) 



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

class test_MD_Block(unittest.TestCase):
    def test_MD_Block(self):
        blocks = [
            """

    This is **bolded** paragraph
    text in a p    
    tag here

            """,
            "### Heading  \n",
            "```Code```",
            ">Quote\n>second line",
            "- Unoredered\n- List",
            "1. Ordered\n2. List",
        ]
        texts = [
            "This is **bolded** paragraph text in a p tag here",
            "Heading",
            None,
            None,
            None,
            None,
        ]
        text_types = [
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
        ]
        tags = [
            "p",
            "h3",
            "code",
            "blockquote",
            "ul",
            "ol"
        ]
        md_blocks = [MD_Block(block) for block in blocks]
        md_block_types = [md_block.block_type for md_block in md_blocks]
        md_block_tags = [md_block.tag for md_block in md_blocks]
        md_block_texts = [md_block.text for md_block in md_blocks]
        map(self.assertEqual, md_block_types, text_types)
        map(self.assertEqual, md_block_tags, tags)
        map(self.assertEqual, md_block_texts, texts)

    def test_malformed_heading(self):
        malformed_headings = [
            "#Heading"
            "######## Heading"
            "# Heading \nNew line"
        ]
        for malformed_heading in malformed_headings:
            md_block = MD_Block("Hi")
            md_block.block = malformed_heading
            md_block.block_type = BlockType.HEADING
            with self.assertRaises(ValueError):
                md_block.normalize_block()