from gen_static_site.text_node import TextNode, TextType


class TestTextNode:
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        assert node == node2
