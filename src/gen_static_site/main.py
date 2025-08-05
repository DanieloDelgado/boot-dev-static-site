import os
import shutil


def copy_files(src, dst):
    for path in os.listdir(src):
        if os.path.isfile(os.path.join(src, path)):
            shutil.copy(os.path.join(src, path), dst)
        else:
            os.makedirs(os.path.join(dst, path))
            copy_files(os.path.join(src, path), os.path.join(dst, path))


def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public", exist_ok=True)
    copy_files(src="static", dst="public")


def extract_title(markdown: str) -> str:



def main():
    copy_static_to_public()

if __name__ == "__main__":
    main()