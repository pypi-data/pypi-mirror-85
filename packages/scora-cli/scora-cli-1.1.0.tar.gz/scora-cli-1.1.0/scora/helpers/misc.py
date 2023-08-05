import os


def getdir(dir=None):
    """Gets the absolute path of the current directory or the provided relative
    path

    Args:
        dir (str, optional): The optional relative path to resolve. \
          Defaults to None.

    Returns:
        absolute_path (str): the absolute resolved path
    """
    return os.path.abspath(dir or ".")


def get_files_recursively(dir=".", exclude=[]):
    """Given a directory, will scan recursively for its files optionaly \
        excluding some extensions

    Args:
        dir (str, optional): [description]. Defaults to ".".
        exclude (list, optional): The list of extensions to exclude \
            from the output \
            Defaults to []

    Returns:
        (tuple): format: (relative_path, absolute_path)
    """
    file_set = set()
    for dir_, _, files in os.walk(dir):
        for file_name in files:
            ext = file_name.split(".").pop()
            if ext in exclude:
                continue
            rel_dir = os.path.relpath(dir_, dir)
            rel_file = os.path.join(rel_dir, file_name)
            file_set.add((rel_file, os.path.join(dir_, file_name)))

    return file_set
