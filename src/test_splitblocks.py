import unittest

from splitblocks import markdown_to_blocks, block_to_blocktype
from textnode import BlockType

class TestBlockSplitting(unittest.TestCase):
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

    def test_headings(self):
        text1 = "This is not a heading."
        text2 = "# This is heading 1."
        text3 = "## This is heading 2."
        text4 = "### This is heading 3."
        text5 = "#### This is heading 4."
        text6 = "##### This is heading 5."
        text7 = "###### This is heading 6."
        text8 = "####### This is no longer a valid heading."
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text1))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(text2))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(text3))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(text4))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(text5))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(text6))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(text7))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text8))

    def test_code(self):
        text1 = "```This is a boring one line code block```"
        text2 = """```This is a
multiline code block.
Neat, isn't it?```"""
        text3 = "``This is not a code block``"
        text4 = "```This code block is broken``"
        self.assertEqual(BlockType.CODE, block_to_blocktype(text1))
        self.assertEqual(BlockType.CODE, block_to_blocktype(text2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text4))

    def test_quote(self):
        text1 = ">This is a boring one line quote block"
        text2 = """>This is a
>multiline quote block.
>Neat, isn't it?"""
        text3 = "This is not a quote block"
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(text1))
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(text2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text3))

    def test_unordered(self):
        text1 = "- This is a boring one line unordered list block."
        text2 = """- This is a
- multiline unordered list.
- Neat, isn't it?"""
        text3 = "This is not an unordered list."
        self.assertEqual(BlockType.UNORDERED, block_to_blocktype(text1))
        self.assertEqual(BlockType.UNORDERED, block_to_blocktype(text2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text3))

    def test_ordered(self):
        text1 = "1. This is a boring one line ordered list block."
        text2 = """1. This is a
2. multiline ordered list.
3. Neat, isn't it?"""
        text3 = "2. This is not an ordered list."
        text4 = """1. This is also
4. not an ordered list.
3. Sad, isn't it?"""
        self.assertEqual(BlockType.ORDERED, block_to_blocktype(text1))
        self.assertEqual(BlockType.ORDERED, block_to_blocktype(text2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text4))
