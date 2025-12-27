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



def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    match delimiter:
        case "**":
            inside_text_type = TextType.BOLD
        case "_":
            inside_text_type = TextType.ITALIC
        case "`":
            inside_text_type = TextType.CODE
        case _:
            raise ValueError("Delimiter not implemented")
    if text_type not in [
        TextType.PLAIN_TEXT,
        TextType.BOLD,
        TextType.ITALIC,
        TextType.CODE,
    ]:
        raise ValueError(f"TextType {text_type} not implemented")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type:
            new_nodes.append(node)
            continue
        else:
            new_texts = node.text.split(delimiter)
            if len(new_texts) % 2 == 0:
                raise Exception("Invalid markdown syntax")
            for i in range(0, len(new_texts)):
                new_text = new_texts[i]
                if new_text == "":
                    continue
                if i % 2 == 0:
                    new_text_type = node.text_type
                else:
                    new_text_type = inside_text_type
                new_node = TextNode(text=new_text, text_type=new_text_type)
                new_nodes.append(new_node)
    return new_nodes