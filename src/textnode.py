from enum import Enum



class TextType(Enum):
    PLAIN_TEXT = "plain text" #"Plain text"
    BOLD = "bold" #**Bold text**"
    ITALIC = "italic" #_Italic text_"
    CODE = "code" #`Code text`"
    LINK = "link" #[anchor text](url)"
    IMAGE = "image" #![alt text](url)"



class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str=None) -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not isinstance(text_type, TextType):
            raise TypeError("text_type must be a TextType")

        if text_type == TextType.LINK or text_type == TextType.IMAGE:
            if url is None:
                raise ValueError("Link or image with no url")
            elif not isinstance(url, str):
                raise TypeError("url must be a string for LINK or IMAGE")
        elif url is not None:
            raise ValueError(f"{text_type} does not support url")

        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, text_node: 'TextNode') -> bool:
        return (
            self.text == text_node.text
            and self.text_type == text_node.text_type
            and self.url == text_node.url
        )


    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"