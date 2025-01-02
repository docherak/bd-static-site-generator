from recur_copy import recur_copy
import os
import shutil

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"


def main():
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)

    recur_copy(DIR_PATH_STATIC, DIR_PATH_PUBLIC)


if __name__ == "__main__":
    main()
