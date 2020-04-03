import sys
import os
import time
from matrixdemos.scripts.utils import *
from optparse import OptionParser
from rgbmatrix import RGBMatrixOptions, RGBMatrix
from PIL import Image, ImageDraw

usage = "usage: %prog [options] [path/text]"
description = """Display an image or text scrolling from left to right.
The argument can be either the path to an image or the text to display"""

parser = OptionParser(usage=usage, description=description)

parser.add_option("-c", "--color", dest="color",
help="the color of the text", default="red")

parser.add_option("-B", "--bgcolor", dest="bg",
help="the background color", default="black")

parser.add_option("-f", "--font", dest="font",
help="the path to a font file to use for text", default="cambriab")

parser.add_option("-b", "--bounce", dest="bounce",
help="the path to a font file to use for text", default=False, action="store_true")

parser.add_option("-r", "--repeat", dest="repeat",
help="repeat the demo forever", default=False, action="store_true")

parser.add_option("-p", "--padding", dest="px", type=int, default=0,
help="an integer representing the extra spacing during looping")

parser.add_option("-s", "--speed", dest="speed", type=float,
help="a float value multiplying the speed", default=1)

(options, args) = parser.parse_args()

TEXT_COLOR = options.color
TEXT_FONT = options.font
BG_COLOR = options.bg
PADDING = options.px
SPEED = options.speed
BOUNCE = options.bounce
REPEAT = options.repeat

if PADDING < 0:
    print("The padding must be positive", file=sys.stderr)
    sys.exit(1)
if SPEED <= 0:
    print("The speed must above zero", file=sys.stderr)
    sys.exit(1)

DATA = None
if args:
    DATA = args[0]
else:
    print("Enter lines of text to display (^D to finish):")
    try:
        DATA = sys.stdin.readlines()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(4)
    DATA = ("    ".join(DATA)).replace("\n", "")

if not DATA:
    print("No text to display, exiting...", file=sys.stderr)
    sys.exit(1)

_options = RGBMatrixOptions()
_options.drop_privileges = False
_options.rows = 32
_options.chain_length = 1
_options.parallel = 1
_options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=_options)

TEXT_SIZE = matrix.height
if os.getuid():
    print()

DEFAULT_FPS = 60

def run():
    image, canvas = new_canvas()
    done = 2 if BOUNCE else 1

    picture = None
    if (os.path.exists(DATA) and not os.path.isdir(DATA)):
        try:
            picture = Image.open(DATA)
        except:
            print(f"Couldn't load \"{DATA}\" as an image", file=sys.stderr)
            sys.exit(3)
        picture = apply_alpha(picture, BG_COLOR)
        if picture.height > matrix.height:
            size = matrix.height / picture.height
            picture = picture.resize((round(picture.width * size), round(picture.height * size)))
        elif picture.height < matrix.height:
            image1 = Image.new("RGB", (picture.width, matrix.height), BG_COLOR)
            image1.paste(picture, (0, matrix.height // 2 - picture.height // 2))
            picture = image1
        if BOUNCE and picture.width < matrix.width:
            image1 = Image.new("RGB", (matrix.width * 2, matrix.height), BG_COLOR)
            image1.paste(picture, (matrix.width // 2 - picture.width // 2, 0))
            picture = image1
    else:
        text_size = canvas.textsize(DATA, font=get_font(TEXT_FONT, TEXT_SIZE))
        picture = Image.new("RGB", text_size, BG_COLOR)
        cnv = ImageDraw.Draw(picture)
        DrawText(cnv, (0, -9), TEXT_SIZE, DATA, font=TEXT_FONT, color=TEXT_COLOR)

    bounce = False
    pos = [32, 0]
    extra = matrix.width
    if BOUNCE:
        extra = 0
    has_bounced = False
    while done:
        for x in range(picture.width + extra):
            if not bounce:
                pos[0] -= 1
            else:
                pos[0] += 1
            canvas.rectangle(((0, 0), (32, 32)), BG_COLOR)
            image.paste(picture, tuple(pos))
            matrix.SetImage(image)
            time.sleep(1 / (DEFAULT_FPS * SPEED))
        if BOUNCE:
            has_bounced = True
            bounce = not bounce
        if not REPEAT:
            done -= 1
        if not BOUNCE:
            pos = [32 + PADDING, 0]
        else:
            if has_bounced:
                extra = -matrix.width
            if not bounce:
                pos = [0, 0]
            else:
                pos = [-picture.width + matrix.width, 0]

def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
