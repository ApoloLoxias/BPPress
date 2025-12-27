import unittest

from textprocessing import text_node_to_html_node, split_nodes_delimiter
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

test_splitables = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_not_splitables = [TextNode("Some **incorrectly formated markdown", TextType.PLAIN_TEXT)]
test_splited_plain_bold = [
    TextNode("Some ", TextType.PLAIN_TEXT),
    TextNode("bold text", TextType.BOLD),
    TextNode(" inside some ", TextType.PLAIN_TEXT),
    TextNode("plain text", TextType.BOLD),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_plain_italic = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some ", TextType.PLAIN_TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" text ", TextType.PLAIN_TEXT),
    TextNode("inside", TextType.ITALIC),
    TextNode(" some ", TextType.PLAIN_TEXT),
    TextNode("plain", TextType.ITALIC),
    TextNode(" text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_plain_code = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some ", TextType.PLAIN_TEXT),
    TextNode("code", TextType.CODE),
    TextNode(" inside some ", TextType.PLAIN_TEXT),
    TextNode("plain text", TextType.CODE),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE)
]
test_splited_bold_italic = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some ", TextType.BOLD),
    TextNode("italic text", TextType.ITALIC),
    TextNode(" inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_bold_code = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some ", TextType.BOLD),
    TextNode("code", TextType.CODE),
    TextNode(" inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_italic_bold = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some ", TextType.ITALIC),
    TextNode("bold text", TextType.BOLD),
    TextNode(" inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_italic_code = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some ", TextType.ITALIC),
    TextNode("code", TextType.CODE),
    TextNode(" inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_code_bold = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some ", TextType.CODE),
    TextNode("bold text", TextType.BOLD),
    TextNode(" inside code", TextType.CODE),
    TextNode("Some _italic text_ inside code", TextType.CODE),
]
test_splited_code_italic = [
    TextNode("Some **bold text** inside some **plain text**", TextType.PLAIN_TEXT),
    TextNode("Some _italic_ text _inside_ some _plain_ text", TextType.PLAIN_TEXT),
    TextNode("Some `code` inside some `plain text`", TextType.PLAIN_TEXT),
    TextNode("Some _italic text_ inside bold text", TextType.BOLD),
    TextNode("Some `code` inside bold text", TextType.BOLD),
    TextNode("Some **bold text** inside italic text", TextType.ITALIC),
    TextNode("Some `code` inside italic text", TextType.ITALIC),
    TextNode("Some **bold text** inside code", TextType.CODE),
    TextNode("Some ", TextType.CODE),
    TextNode("italic text", TextType.ITALIC),
    TextNode(" inside code", TextType.CODE),
]

class test_split_nodes_delimiter(unittest.TestCase):
    def test_plain_text_bold(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "**", TextType.PLAIN_TEXT),
            test_splited_plain_bold
        )
    def test_plain_text_italic(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "_", TextType.PLAIN_TEXT),
            test_splited_plain_italic
        )
    def test_plain_text_code(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "`", TextType.PLAIN_TEXT),
            test_splited_plain_code
        )
    def test_bold_italic(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "_", TextType.BOLD),
            test_splited_bold_italic
        )
    def test_bold_code(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "`", TextType.BOLD),
            test_splited_bold_code
        )
    def test_italic_bold(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "**", TextType.ITALIC),
            test_splited_italic_bold
        )
    def test_italic_code(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "`", TextType.ITALIC),
            test_splited_italic_code
        )
    def test_code_bold(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "**", TextType.CODE),
            test_splited_code_bold
        )
    def test_code_italic(self):
        self.assertEqual(
            split_nodes_delimiter(test_splitables, "_", TextType.CODE),
            test_splited_code_italic
        )
    def test_invalid_input(self):
        self.assertRaises(
            ValueError,
            split_nodes_delimiter,
            test_splitables, "**", TextType.IMAGE
        )
        self.assertRaises(
        ValueError,
        split_nodes_delimiter,
        test_splitables, "*", TextType.PLAIN_TEXT
        )
        self.assertRaises(
        Exception,
        split_nodes_delimiter,
        test_not_splitables, "**", TextType.PLAIN_TEXT
        )