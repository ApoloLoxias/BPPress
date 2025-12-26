import unittest

from textprocessing import text_node_to_html_node
from textnode import TextType, TextNode
from htmlnode import LeafNode


test_textnodes = [
    TextNode("Plain text", TextType.PLAIN_TEXT),
    TextNode("Bold text", TextType.BOLD),
    TextNode("Italic text", TextType.ITALIC),
    TextNode("Code text", TextType.CODE),
    TextNode("Anchor text", TextType.LINK, "https://boot.dev"),
    TextNode("Alt text", TextType.IMAGE, "image.png"),
]
test_html_nodes =[
    LeafNode(None, "Plain text"),
    LeafNode("b", "Bold text"),
    LeafNode("i", "Italic text"),
    LeafNode("code", "Code text"),
    LeafNode("a", "Anchor text", {"href":"https://boot.dev"}),
    LeafNode("img", "", {"src":"image.png", "alt":"Alt text"}),
]

class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_htlm(self):
        for inp, o in zip(test_textnodes, test_html_nodes):
            i = text_node_to_html_node(inp)
            self.assertEqual(i.tag, o.tag)
            self.assertEqual(i.value, o.value)
            self.assertEqual(i.children, o.children)
            self.assertEqual(i.props, o.props)