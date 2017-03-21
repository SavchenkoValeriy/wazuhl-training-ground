import os

def set_wd(directory):
    global get_wd
    get_wd = lambda : directory

def set_output(directory):
    global get_output
    get_output = lambda : directory

def get_clang():
    return os.path.join(get_wd(), "bin", "clang")

def get_clangpp():
    return os.path.join(get_wd(), "bin", "clang++")
