import os

from executable_path import executable_path


def create_path_from_executable(*paths: str):
    return os.path.abspath(os.path.join(executable_path, *paths))
