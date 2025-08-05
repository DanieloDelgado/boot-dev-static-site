import argparse
import os
import shutil
import sys

from gen_static_site.page import generate_recursive_page

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--basepath",
        type=str,
        default="/",
        help="Base path for the static site, defaults to '/'"
    )
    return parser.parse_args(args)

def copy_files(src, dst):
    for path in os.listdir(src):
        if os.path.isfile(os.path.join(src, path)):
            shutil.copy(os.path.join(src, path), dst)
        else:
            os.makedirs(os.path.join(dst, path))
            copy_files(os.path.join(src, path), os.path.join(dst, path))


def copy_static_to_docs():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs", exist_ok=True)
    copy_files(src="static", dst="docs")


def main():
    parsed_args = parse_args(sys.argv[1:])
    copy_static_to_docs()
    generate_recursive_page('content', 'template.html', 'docs', basepath=parsed_args.basepath)

if __name__ == "__main__":
    main()