from typing import Self


class HTMLNode:
    def __init__(self, tag: str =None, value: str=None, children: list[Self]=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items())
