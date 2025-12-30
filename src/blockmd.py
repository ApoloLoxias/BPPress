def markdown_to_blocks(markdown: str) -> str:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return blocks