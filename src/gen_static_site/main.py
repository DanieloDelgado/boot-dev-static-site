from gen_static_site.text_node import TextNode


def main():
    node = TextNode("This is some anchor text", "link", "https://example.com")
    print(node)

if __name__ == "__main__":
    main()