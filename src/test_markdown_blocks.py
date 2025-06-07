import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Not a heading if more than 6 hashes
        self.assertEqual(block_to_block_type("####### Not heading"), BlockType.PARAGRAPH)
        # Not a heading if no space after hashes
        self.assertEqual(block_to_block_type("##Heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        code = "```\ndef foo():\n    return 1\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        # Not code if only starts or ends with ```
        self.assertEqual(block_to_block_type("```\nnot closed"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("not opened\n```"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        # Not a quote if one line doesn't start with >
        not_quote = "> This is a quote\nNot a quote"
        self.assertEqual(block_to_block_type(not_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)
        # Not unordered if one line doesn't start with -
        not_ul = "- item 1\nitem 2"
        self.assertEqual(block_to_block_type(not_ul), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)
        # Not ordered if numbers are not sequential
        not_ol = "1. first\n3. second"
        self.assertEqual(block_to_block_type(not_ol), BlockType.PARAGRAPH)
        # Not ordered if not starting at 1
        not_ol2 = "2. first\n3. second"
        self.assertEqual(block_to_block_type(not_ol2), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
