from textnode import TextType, TextNode



def main() -> None:
    textnode = TextNode("This is some anchor text", TextType.PLAIN_TEXT, "https://www.boot.dev")
    print(textnode)


if __name__ == "__main__":
    main()