import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



keys = ["attribute1", "attribute2", "attribute3"]
values = ["value1", "value2", "value3"]

def generate_dicts(keys: list[str], values: list[str]) -> list[dict]:
    output = [{}]
    kvpairs = list(zip(keys, values))
    for k, v in kvpairs:
        dics = []
        for dic in output:
            new_dic = dic.copy()
            new_dic[k] = v
            dics.append(new_dic)
        output.extend(dics)
    return output

dicts = generate_dicts(keys, values)

class TestHTLMNode(unittest.TestCase):
    def test_props_to_html(self):
        for dic in dicts:
          output = HTMLNode(props = dic).props_to_html()
          for k, v in dic.items():
            self.assertIn(f'  {k}="{v}"', output)



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a  href="https://www.google.com">Click me!</a>')
        node = LeafNode("x", "Text", {"k1": "v1", "k2": "v2", "k3": "v3"})
        self.assertEqual(node.to_html(), '<x  k1="v1"  k2="v2"  k3="v3">Text</x>')



class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
        node = ParentNode(None, LeafNode(None, "Text"))
        self.assertRaises(ValueError, node.to_html)
        node = ParentNode("t", None)
        self.assertRaises(ValueError, node.to_html)

        greatgrandchild = LeafNode("t31", "Text31", {"k311":"v311", "k312":"v312"})
        grandchild1 = LeafNode("t1", "Text1", {"k11":"v11", "k12":"v12", "k13":"v13"})
        grandchild2 = LeafNode("t2", "Text2", {"k21":"v21", "k22":"v22"})
        grandchild3 = ParentNode("t3", [greatgrandchild], {"k31":"v31", "k32":"v32"})
        node = ParentNode("t", [grandchild1, grandchild2, grandchild3], {"k1":"v1", "k2":"v2", "k3":"v3", "k4":"v4"})
        self.assertEqual(
            node.to_html(),
            '<t  k1="v1"  k2="v2"  k3="v3"  k4="v4"><t1  k11="v11"  k12="v12"  k13="v13">Text1</t1><t2  k21="v21"  k22="v22">Text2</t2><t3  k31="v31"  k32="v32"><t31  k311="v311"  k312="v312">Text31</t31></t3></t>'
        )



if __name__ == "__main__":
    unittest.main()