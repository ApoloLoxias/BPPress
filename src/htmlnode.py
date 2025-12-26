class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list['HTMLNode']=None, props: dict=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError


    def props_to_html(self) -> str:
        if not self.props:
            return ""
        output = f""
        for k, v in self.props.items():
            output += f'  {k}="{v}"'
        return output
    

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self) -> str:
        if not self.value:
            raise ValueError("A LeafNode requires a value")
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], props: dict=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)


    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("A ParentNode requires a tag")
        if not self.children:
            raise ValueError("A ParentNode requires children")

        inner_string = f""
        for child in self.children:
            inner_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_string}</{self.tag}>"


    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"