#!/usr/bin/env python3
import sys
import os
import time
import random
import glob
from optparse import OptionParser
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
from matrixdemos.scripts.get_file import get_file
from matrixdemos.scripts.utils import apply_alpha

usage = "usage: %prog [options] PATH"
parser = OptionParser(usage=usage)

parser.set_description("""Display a slideshow of images on the matrix, works with any size of matrix.
Set the directory of your images via the PATH argument, or a defualt set of images will be used.""")

parser.add_option("-b", "--bgcolor", dest="bg", default="black",
help="the background color")

parser.add_option("-l", "--length", dest="secs", type=float,
        help="set how long each slide is displayed", default=3)

parser.add_option("-t", dest="trans", type=float,
        help="set how long each transistion takes", default=.5)

parser.add_option("-s", "--shuffle", action="store_true", dest="shuffle",
        help="shuffles the images", default=False)

(options, args) = parser.parse_args()

# Time of each slide, in seconds
SLIDE_TIME = options.secs
TRANSITION_TIME = options.trans
TRANSITION_STEPS = round(options.trans * 80)
SHUFFLE = options.shuffle
BG_COLOR = options.bg

if not TRANSITION_STEPS:
    TRANSITION_STEPS = 1

if not args:
    args = [get_file("demo_slideshow")]

if not os.path.exists(args[0]):
    print(f"ERR: File not found: {f}", file=sys.stdout)
    sys.exit(1)

PATH = args[0]

if os.path.isdir(PATH) and not PATH.endswith("/"):
    PATH += "/"

# Configuration for the matrix
options = RGBMatrixOptions()
options.drop_privileges = False
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

def run():
    print("\n\nCollecting images...  ", end="")
    surface = Image.new("RGB", (matrix.width, matrix.height), 0)

    if not os.path.isdir(PATH):
        images = [""]
    else:
        # Find images
        images = os.listdir(PATH)
    print("done")

    print("Processing images...  ", end="", flush=True)
    # Load and process images
    loaded_images = []
    for img in images:
        if os.path.isdir(PATH + img):
            continue
        try:
            image1 = Image.open(PATH + img)
        except (OSError):
            print(f"Couldn't load \"{img}\"")
            continue
        # If image is too small, center it on a black image
        image1.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        image1 = apply_alpha(image1, BG_COLOR)
        if image1.width < matrix.width or image1.height < matrix.height:
            image = Image.new("RGB", (matrix.width, matrix.height), BG_COLOR)
            image.paste(image1, (matrix.width // 2 - image1.width // 2, matrix.height // 2 - image1.height // 2))
        else:
            image = image1
        loaded_images.append(image)
    if not loaded_images:
        sys.stderr.write("No suitable images!\n")
        sys.exit(1)
    print("done")
    lastimg = ""
    while True:
        if SHUFFLE:
            # Shuffle it, but don't have the same image twice in a row
            random.shuffle(loaded_images)
            while loaded_images[0] == lastimg and len(loaded_images) > 1:
                random.shuffle(loaded_images)
        for image in loaded_images:
            lastimg = image
            for x in range(TRANSITION_STEPS):
                x += 1
                intensity = int(x / TRANSITION_STEPS * 255)
                mask = Image.new("L", (image.width, image.height), intensity)
                i = image.copy()
                old_surface = surface.copy()
                old_surface.paste(i, mask)
                matrix.SetImage(old_surface.convert("RGB"))
                time.sleep(TRANSITION_TIME / TRANSITION_STEPS)
            surface = image.copy()
            time.sleep(SLIDE_TIME)
        if len(loaded_images) == 1:
            while True:
                time.sleep(100)

def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
