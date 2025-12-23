import unittest

from htmlnode import HTMLNode
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



if __name__ == "__main__":
    unittest.main()