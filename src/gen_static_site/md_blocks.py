import re
from enum import Enum

from gen_static_site.html_node import HTMLNode
from gen_static_site.conversions import text_node_to_html_node, text_to_textnodes
from gen_static_site.parent_node import ParentNode
from gen_static_site.leaf_node import LeafNode
from gen_static_site.text_node import TextNode, TextType


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split('\n\n') if block]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s\w", block):
        return BlockType.heading
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.code
    elif all(line.strip().startswith('> ') for line in block.splitlines()):
        return BlockType.quote
    elif all(line.strip().startswith('- ') for line in block.splitlines()):
        return BlockType.unordered_list
    elif all(line.strip().startswith(str(i) + '. ') for i, line in enumerate(block.splitlines(), start=1)):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph


def text_to_children(text: str) -> list[LeafNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_node = ParentNode(tag="div", props=None, children=[])
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        if block_type == BlockType.code:
            code_content = '\n'.join(line.strip() for line in block.splitlines()[1:-1])
            text_node = TextNode(code_content, text_type=TextType.CODE)
            code_node = text_node_to_html_node(text_node)
            pre_node = ParentNode(tag="pre", props=None, children=[code_node])
            html_node.children.append(pre_node)
        elif block_type == BlockType.quote:
            content = ' '.join(line.removeprefix('> ').strip() for line in block.splitlines())
            children_nodes = text_to_children(content)
            blockquote_node = ParentNode(tag="blockquote", props=None, children=children_nodes)
            html_node.children.append(blockquote_node)
        elif block_type == BlockType.paragraph:
            content = ' '.join(line.strip() for line in block.splitlines())
            children_nodes = text_to_children(content)
            paragraph_node = ParentNode(tag="p", props=None, children=children_nodes)
            html_node.children.append(paragraph_node)
        elif block_type == BlockType.heading:
            level = block.count('#', 0, 6)
            content = block.removeprefix('#' * level).strip()
            children_nodes = text_to_children(content)
            heading_node = ParentNode(tag=f"h{level}", props=None, children=children_nodes)
            html_node.children.append(heading_node)
        elif block_type == BlockType.unordered_list:
            items = [line.strip().removeprefix('- ') for line in block.splitlines()]
            list_items = [ParentNode(tag="li", props=None, children=text_to_children(item)) for item in items]
            unordered_list_node = ParentNode(tag="ul", props=None, children=list_items)
            html_node.children.append(unordered_list_node)
        elif block_type == BlockType.ordered_list:
            items = [line.strip().split('. ', 1)[1] for line in block.splitlines()]
            list_items = [ParentNode(tag="li", props=None, children=text_to_children(item)) for item in items]
            ordered_list_node = ParentNode(tag="ol", props=None, children=list_items)
            html_node.children.append(ordered_list_node)
    return html_node




