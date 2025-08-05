from gen_static_site.md_blocks import (markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node)


class TestMarkdownToBlocks:
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        assert blocks ==[
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

class TestBlockToBlockType:
    def test_block_to_block_type(self):
        assert block_to_block_type("This is a paragraph") == BlockType.paragraph
        assert block_to_block_type("# Heading 1") == BlockType.heading
        assert block_to_block_type("## Heading 2") == BlockType.heading
        assert block_to_block_type("```python\nprint('Hello')\n```") == BlockType.code
        assert block_to_block_type("> This is a quote") == BlockType.quote
        assert block_to_block_type("- Item 1\n- Item 2") == BlockType.unordered_list
        assert block_to_block_type("1. First item\n2. Second item") == BlockType.ordered_list


class TestMarkdownToHtmlNode:
    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        assert html == expected

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here
    
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        assert html == expected

    def test_quote(self):
        md = """
    > This is a **quote**
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a <b>quote</b></blockquote></div>"
        assert html == expected

    def test_headings(self):
        md = "## This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h2>This is a heading</h2></div>"
        assert html == expected

    def test_unordered_list(self):
        md = """\
        - Item 1
        - Item 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        assert html == expected

    def test_ordered_list(self):
        md = """\
        1. First item
        2. Second item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        assert html == expected
