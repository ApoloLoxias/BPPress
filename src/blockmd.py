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
    

class MD_Block:
    def __init__(self, block:str) -> None:
        self.block = block
        self.block_type = block_to_block_type(self.block)
        self.tag = self.get_tag()
        self.text = self.normalize_block()
        if self.block_type == BlockType.CODE:
            self.preformat()

    def get_tag(self) -> str:
        match self.block_type:
            case BlockType.PARAGRAPH:
                tag = "p"
            case BlockType.HEADING:
                tag = f"h{len(self.block)-len(self.block.strip("#"))}"
            case BlockType.QUOTE:
                tag = "blockquote"
            case BlockType.CODE:
                tag = "code" # Need to nest inside "pre"
            case BlockType.UNORDERED_LIST:
                tag = "ul"
            case BlockType.ORDERED_LIST:
                tag = "ol"
        return tag

    def normalize_block(self) -> str:
        match self.block_type:
            case BlockType.PARAGRAPH:
                text = self.normalize_paragraph()
            case BlockType.HEADING:
                text = self.normalize_heading()
            case BlockType.QUOTE:
                text = self.normalize_quote()
            case BlockType.CODE:
                text = self.normalize_code() # Need to nest inside "pre"
            case BlockType.UNORDERED_LIST:
                text = self.normalize_ul()
            case BlockType.ORDERED_LIST:
                text = self.normalize_ol()
        return text

    def normalize_paragraph(self) -> str:
        text = self.block.strip()
        text = text.split("\n")
        text = [t.strip() for t in text]
        text = " ".join(text)
        return text

    def normalize_heading(self) -> str:
        if (
            len(self.block)-len(self.block.strip("#")) not in range(1, 7)
            or self.block.lstrip("#")[0] != " "
            or re.search(r"\n+.", self.block)
        ):
            raise ValueError("malformated heading block")
        text = self.block.lstrip("#")
        text = self.block[1:]
        text = self.block.rstrip()
        return text

    def normalize_quote(self) -> str:
        text = self.block.split("\n")
        for line in text:
            line = line[1:]
            line.strip()
        text = "\n".join(text)
        text.strip()
        return text

    def normalize_code(self) -> str:
        text = self.block[3:-3]
        text = text.lstrip("\n")
        text = text.rstrip()

    def normalize_ul(self) -> str:
        text = self.block.strip()
        text = self.block.split("\n")
        for line in text:
            line = line[1:]
            line = line.strip()
        text = "\n".join(text)
        return text

    def normalize_ol(self) -> str:
        return self.normalize_ul()

    def preformat(self):
        pass


"""md = "# Heading \nNew line"

md_block = MD_Block(md)
print(re.search(r"\n+.", "# Heading \nNew line"))"""