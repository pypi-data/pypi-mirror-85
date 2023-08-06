import os


def read_file(path):
    with open(path) as file:
        return file.read()


def folder_from(path):
    return os.path.dirname(path)


def path(*paths):
    return os.path.join(*paths)


def file_exists(path):
    return os.path.isfile(path)
