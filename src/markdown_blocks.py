from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.splitlines()
    if not lines or all(line.strip() == "" for line in lines):
        return BlockType.PARAGRAPH
    # Heading: starts with 1-6 # followed by a space
    if len(lines) == 1 and lines[0].lstrip().startswith("#"):
        import re
        if re.match(r"^#{1,6} ", lines[0]):
            return BlockType.HEADING
    # Code block: starts and ends with ```
    if lines[0].strip().startswith("```") and lines[-1].strip().endswith("```"):
        return BlockType.CODE
    # Quote block: every line starts with >
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE
    # Unordered list: every line starts with "- "
    if all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    # Ordered list: every line starts with incrementing number + ". "
    if all(line.lstrip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    # Default: paragraph
    return BlockType.PARAGRAPH