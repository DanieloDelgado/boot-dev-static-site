import pytest

from gen_static_site.page import extract_title


class TestExtractTitle:
    def test_extract_title(self):
        md = """
# This is a title
This is a paragraph.
"""
        title = extract_title(md)
        assert title == "This is a title"

    def test_title_not_found(self):
        md = """
## This is not a title
"""
        with pytest.raises(ValueError):
            print(extract_title(md))
