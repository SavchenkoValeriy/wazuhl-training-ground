import os

def set_wd(directory):
    define_getter("get_wd", directory)

def set_output(directory):
    directory = os.path.abspath(directory)
    define_getter("get_output", directory)

def get_clang():
    return os.path.join(get_wd(), "bin", "clang")

def get_clangpp():
    return os.path.join(get_wd(), "bin", "clang++")

def define_getter(name, value):
    globals()[name] = lambda : value
