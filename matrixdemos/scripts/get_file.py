from pkg_resources import resource_filename
import os

def get_file(filename):
    fname = resource_filename("matrixdemos", filename)
    if os.path.isdir(fname):
        fname += "/"
    return fname
