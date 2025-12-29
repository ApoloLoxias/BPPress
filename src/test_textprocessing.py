import unittest

from inlinemd import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_text_nodes
)
from textnode import TextType, TextNode
from htmlnode import LeafNode



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



class test_extract_markdown_images(unittest.TestCase):
    def test_images(self):
        self.assertEqual(
            extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

class test_extract_markdown_links(unittest.TestCase):
    def test_links(self):
        self.assertEqual(
            extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

class test_split_nodes_images(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), as well as some trailing text.",
            TextType.PLAIN_TEXT,
        )
        new_nodes2 = split_nodes_images([node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(", as well as some trailing text.", TextType.PLAIN_TEXT)
            ],
            new_nodes2,
        )
        new_nodes3 = split_nodes_images([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(", as well as some trailing text.", TextType.PLAIN_TEXT)
            ],
            new_nodes3
        )

class test_split_nodes_links(unittest.TestCase):
    def split_singleton(self):
        text = TextNode("This is text with a [link](https://boot.dev)", TextType.PLAIN_TEXT)
        output = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(
            split_nodes_links([text]),
            output
        )

    def split_lonely(self):
        text = TextNode("[link](https://boot.dev)", TextType.PLAIN_TEXT)
        output = [TextNode("link", TextType.LINK, url="https:boot.dev")]
        self.assertListEqual(
            split_nodes_links([text]),
            output
        )

    def split_trailing(self):
        text = TextNode("This is text with a [link](https://boot.dev) and some trailing text", TextType.PLAIN_TEXT)
        output = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and some trailing text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(
            split_nodes_links([text]),
            output
        )
        
    def split_multi_link(self):
        text = TextNode ("This is text with a [link](https://boot.dev) and [another link](https://wiki.archlinux.org)", TextType.PLAIN_TEXT)
        output = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TexNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNOde("another link", textType.LINK, "https://wiki.archlinux.org"),
        ]
        self.assertListEqual(
            split_nodes_links([text]),
            output
        )
        
    def split_multi_nodes(self):
        texts = [
            TextNode("This is text with a [link](https://boot.dev)", TextType.PLAIN_TEXT),
            TextNode("[link](https://boot.dev)", TextType.PLAIN_TEXT),
            TextNode("This is text with a [link](https://boot.dev) and some trailing text", TextType.PLAIN_TEXT),
            TextNode ("This is text with a [link](https://boot.dev) and [another link](https://wiki.archlinux.org)", TextType.PLAIN_TEXT),
        ]
        output =[
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("link", TextType.LINK, url="https:boot.dev"),
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and some trailing text", TextType.PLAIN_TEXT),
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TexNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNOde("another link", textType.LINK, "https://wiki.archlinux.org"),
        ]
        self.assertListEqual(
            split_nodes_links(texts),
            output
        )



class test_text_to_text_nodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_text_nodes(text), output)
