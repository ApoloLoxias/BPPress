from textnode import TextType, TextNode
from htmlnode import LeafNode



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