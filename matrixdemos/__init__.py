import os
import shutil

__title__ = "MatrixDemo"
__author__ = "NachoMonkey"
__version__ = "0.2"

# Put special data in your home directory
DATA_PATH = "/home/" + os.getlogin() + "/.matrixdemos_data"

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
    shutil.chown(DATA_PATH, os.getlogin())
