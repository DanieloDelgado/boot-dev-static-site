from gen_static_site.html_node import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: dict=None):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
