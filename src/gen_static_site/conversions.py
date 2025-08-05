import re

from gen_static_site.leaf_node import LeafNode
from gen_static_site.text_node import TextNode, TextType


def text_node_to_html_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})
        case _:
            raise ValueError("Unknown node type")


def split_nodes_delimiter(nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("Invalid markdown syntax: ", node.text)
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    matches = pattern.findall(text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(?<!!)\[(.*?)\]\((.*?)\)")
    matches = pattern.findall(text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.IMAGE:
            new_nodes.append(old_node)
        else:
            parts = extract_markdown_images(old_node.text)
            if not parts:
                new_nodes.append(old_node)
            else:
                remaining_text = old_node.text
                for alt_text, url in parts:
                    [previous_text, remaining_text]= remaining_text.split(f'![{alt_text}]({url})', 1)
                    if previous_text:
                        new_nodes.append(TextNode(previous_text, TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.LINK:
            new_nodes.append(old_node)
        else:
            parts = extract_markdown_links(old_node.text)
            if not parts:
                new_nodes.append(old_node)
            else:
                remaining_text = old_node.text
                for link_text, url in parts:
                    [previous_text, remaining_text] = remaining_text.split(f'[{link_text}]({url})', 1)
                    if previous_text:
                        new_nodes.append(TextNode(previous_text, TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = []
    parts = text.split('\n')
    for part in parts:
        new_nodes = split_nodes_delimiter([TextNode(part, TextType.TEXT)], '`', TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
        new_nodes = split_nodes_image(new_nodes)
        new_nodes = split_nodes_link(new_nodes)
        nodes.extend(new_nodes)
    return nodes
