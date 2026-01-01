from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from blockmd import markdown_to_blocks, BlockType, block_to_block_type
from inlinemd import text_to_text_nodes


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise Exception("text_node is not of a valid TextType")
    
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(tag=None, value=text_node.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text, props=None)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text, props=None)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})



def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_types = [block_to_block_type(block) for block in blocks]
    block_nodes = []
    for block, block_type in zip(blocks, block_types):
        match block_type:
            case BlockType.PARAGRAPH:
                tag = "p"
            case BlockType.HEADING:
                tag = f"h{len(block)-len(block.strip("#"))}"
            case BlockType.QUOTE:
                tag = "blockquote"
            case BlockType.CODE:
                tag = "code" # Need to nest inside "pre"
            case BlockType.UNORDERED_LIST:
                tag = "ul"
            case BlockType.ORDERED_LIST:
                tag = "ol"

        if tag == "code":
            block_nodes.append(
                ParentNode(
                    tag="pre",
                    children=[
                        LeafNode(tag="code", value=block)
                    ],
                    props=None,
                ),
            )

        else:
            nodes = text_to_text_nodes(block)
            leaves = []
            for node in nodes:
                leaf = text_node_to_html_node(node)
                leaves.append(leaf)
            if leaves:
                html_block = ParentNode(tag=tag, children=leaves, props=None)
                block_nodes.append(html_block)

    return ParentNode(tag="div", children=block_nodes, props=None)


#md = """
#    ```
#    This is text that _should_ remain
#    the **same** even with inline stuff
#    ```
#"""

#node = markdown_to_html_node(md)
#html = node.to_html()
#print(html)

#pnode = ParentNode(div, children: [ParentNode(None, children: [LeafNode(None, This is , None), LeafNode(b, bolded, None), LeafNode(None,  paragraph text in a p tag here, None)], None), ParentNode(None, children: [LeafNode(None, This is another paragraph with , None), LeafNode(i, italic, None), LeafNode(None,  text and , None), LeafNode(code, code, None), LeafNode(None,  here, None)], None)], None)
#html = pnode.to_html
#print(html)