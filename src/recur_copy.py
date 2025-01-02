import os
import shutil


def recur_copy(source_dir_path, destination_dir_path):
    if not os.path.exists(destination_dir_path):
        os.mkdir(destination_dir_path)

    for filename in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, filename)
        destination_path = os.path.join(destination_dir_path, filename)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            recur_copy(source_path, destination_path)
