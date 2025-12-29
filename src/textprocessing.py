import re

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



def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    regex = r"!\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)"
    return re.findall(regex, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)"
    return re.findall(regex, text)



def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        text = node.text
        text_type = node.text_type
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        for image in images:
            alt_text = image[0]
            url = image[1]
            new_texts = text.split(f"![{alt_text}]({url})", 1)
            new_text = new_texts[0]
            text = new_texts[1]
            if  new_text:
                new_nodes.append(TextNode(new_text, text_type))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        if text: #This happens only after the last image, avoiding duplication of texts in between 2 images
            new_nodes.append(TextNode(text, text_type))
    return new_nodes
    """
            if len(new_texts) % 2 == 0:W
                raise Exception("Invalid markdown syntax")
            for i in range(0, len(new_texts)):
                new_text = new_texts[i]
                if new_text == "":
                    continue
                if i % 2 == 0:
                    new_text_type = text_type
                    new_node = TextNode(text_type=new_text_type, text=new_text)
                else:
                    new_node = TextNode(
                        text_type=TextType.IMAGE,
                        text=image[0],
                        url=image[1]
                    )
                new_nodes.append(new_node)
    return new_nodes
    """

"""
print(
    split_nodes_images([TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), as well as some trailing text", TextType.PLAIN_TEXT)])
)
"""