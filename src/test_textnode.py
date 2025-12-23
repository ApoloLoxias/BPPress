import unittest

from textnode import TextNode, TextType

texts = ["", " ", "test text", "different test text"]
texttypes = [TextType.PLAIN_TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE]
urls = ["", "test url", "another test url"]

def generate_valid_nodes(texts: list, texttypes: list, urls: list) -> list:
    output = []
    for text in texts:
        for texttype in texttypes:
            if texttype in [TextType.LINK, TextType.IMAGE]:
                for url in urls:
                    output.append(TextNode(text, texttype, url))
            else:
                output.append(TextNode(text, texttype))
    return output

valid_nodes = generate_valid_nodes(texts, texttypes, urls)

invalid_node_constructors = [
    (1, TextType.PLAIN_TEXT, None),
    ("text", 1, None),
    ("text", TextType.PLAIN_TEXT, "url"),
    ("text", TextType.IMAGE, None),
    ("text", TextType.LINK, None),
    ("text", TextType.LINK, 1),
    ("text", TextType.IMAGE, 1),
]



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        for node1 in valid_nodes:
            for node2 in valid_nodes:
                if valid_nodes.index(node1) == valid_nodes.index(node2):
                    self.assertEqual(node1, node2) 
                else:
                    self.assertNotEqual(node1, node2)
    
    def test_invalid_ndoes(self):
        for args in invalid_node_constructors:
            with self.assertRaises((TypeError, ValueError)):
                TextNode(*args)



if __name__ == "__main__":
    unittest.main()