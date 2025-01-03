from recur_copy import recur_copy
from page_generator import generate_pages_recursive
import os
import shutil

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)

    recur_copy(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    generate_pages_recursive(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_PUBLIC)


if __name__ == "__main__":
    main()
