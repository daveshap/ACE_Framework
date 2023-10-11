import os
import sys
import inspect


def get_package_root(obj):
    package_name = obj.__class__.__module__.split(".")[0]
    package_root = os.path.dirname(os.path.abspath(sys.modules[package_name].__file__))
    return package_root


def get_file_directory():
    filepath = inspect.stack()[1].filename
    return os.path.dirname(os.path.abspath(filepath))


def snake_to_class(string):
    parts = string.split("_")
    return "".join(word.title() for word in parts)
