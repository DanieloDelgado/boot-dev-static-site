import os
import re
from pathlib import Path

from gen_static_site.md_blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    title_match = re.search(r"^#\s+(.*)", markdown, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    raise ValueError("Could not extract title")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

def generate_recursive_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    for path in os.listdir(from_path):
        full_path = os.path.join(from_path, path)
        if os.path.isdir(full_path):
            os.makedirs(os.path.join(dest_path, path), exist_ok=True)
            generate_recursive_page(full_path, template_path, os.path.join(dest_path, path), basepath)
        elif path.endswith(".md"):
            dest_file = Path(path).stem + ".html"
            dest_full_path = os.path.join(dest_path, dest_file)
            generate_page(full_path, template_path, dest_full_path, basepath)
