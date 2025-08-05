import pytest

from gen_static_site.html_node import HTMLNode
from gen_static_site.parent_node import ParentNode
from gen_static_site.leaf_node import LeafNode
from gen_static_site.conversions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from gen_static_site.text_node import TextNode, TextType


class TestHTMLNode:
    def test_htmlnode_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        assert node.props_to_html() == 'class="container" id="main"'


class TestLeafNode:
    def test_without_value(self):
        node = LeafNode("span", None)
        with pytest.raises(ValueError):
            node.to_html()

    def test_raw_text(self):
        text = "This is a text without a tag."
        assert text == LeafNode(None, text).to_html()

    def test_without_props(self):
        rendered_text = LeafNode("p", "This is a paragraph of text.").to_html()
        assert "<p>This is a paragraph of text.</p>" == rendered_text

    def test_with_props(self):
        rendered_text = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        assert '<a href="https://www.google.com">Click me!</a>' == rendered_text


class TestParentNode:
    def test_without_tag(self):
        with pytest.raises(ValueError):
            ParentNode(None, []).to_html()

    def test_without_children(self):
        with pytest.raises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        assert parent_node.to_html() == "<div><span>child</span></div>"

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        assert  parent_node.to_html() == "<div><span><b>grandchild</b></span></div>"


class TestTextNodeToHTMLNode:
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        assert html_node.to_html() == '<a href="https://example.com">This is a link</a>'


class TestSplitNodesDelimiter:
    def test_split_code_delimiter(self):
        nodes = [
            TextNode("Code `import path` and `import sys` in Python", TextType.TEXT),
            TextNode("import os", TextType.CODE),
        ]
        assert split_nodes_delimiter(nodes, "`", TextType.CODE) == [
            TextNode("Code ", TextType.TEXT),
            TextNode("import path", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("import sys", TextType.CODE),
            TextNode(" in Python", TextType.TEXT),
            TextNode("import os", TextType.CODE)
        ]

    def test_invalid_syntax(self):
        nodes = [
            TextNode("Code `import path` and `import sys in Python", TextType.TEXT),
        ]
        with pytest.raises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

class TestExtractMarkdownImages:
    def test_extract_images(self):
        text = "Here is an image ![alt text](https://example.com/image.png) and some text."
        assert extract_markdown_images(text) == [("alt text", "https://example.com/image.png")]


class TestExtractMarkdownLinks:
    def test_extract_links(self):
        text = "Here is a link [example](https://example.com) and some text."
        assert extract_markdown_links(text) == [("example", "https://example.com")]


class TestSplitNodesImage:
    def test_split_images(self):
        nodes = [
            TextNode("This is an image ![alt text](https://example.com/image.png) and some text.", TextType.TEXT),
        ]
        expected_nodes = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and some text.", TextType.TEXT)
        ]
        assert split_nodes_image(nodes) == expected_nodes


class TestSplitNodesLink:
    def test_split_links(self):
        nodes = [
            TextNode("This is a link [example](https://example.com) and some text.", TextType.TEXT),
        ]
        expected_nodes = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("example", TextType.LINK, "https://example.com"),
            TextNode(" and some text.", TextType.TEXT)
        ]
        assert split_nodes_link(nodes) == expected_nodes

class TestTextToTextNodes:
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        assert nodes == expected_nodes
