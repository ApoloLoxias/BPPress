import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph" # paragraph
    HEADING = "heading" # [#]{1-6} heading text
    CODE = "code" # ```code```
    QUOTE = "quote" # >first line\n>second line
    UNORDERED_LIST = "unordered list" # - first line \n- second line
    ORDERED_LIST = "ordered list" # 1. first line\n2. second line



def markdown_to_blocks(markdown: str) -> str:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return blocks



def block_to_block_type(block: str) -> BlockType:
    if re.match(r"[#]{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block[-3:] == "```":
        return BlockType.CODE
    lines = block.split("\n")
    for blocktype, starting_string, condition in [(BlockType.QUOTE, ">", True), (BlockType.UNORDERED_LIST, "- ", True), (BlockType.ORDERED_LIST, r"\d\. ", False)]:
        tmp = 0
        for line in lines:
            if not re.match(starting_string, line):
                tmp += 1
        if tmp == 0 and (condition or lines[0].startswith("1. ")):
            return blocktype
    return BlockType.PARAGRAPH
    


