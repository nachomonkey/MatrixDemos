#!/usr/bin/env python3
"""Display swarms of text on the matrix"""
import time
import random
from optparse import OptionParser
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from matrixdemos.scripts.utils import *
from PIL import ImageDraw
from pygame.time import Clock

parser = OptionParser()

parser.set_description("""Show lots of text swarming about""")

parser.add_option("-t", "--text", dest="text",
help="the text to show", default="Text")

parser.add_option("-c", "--color", dest="color",
help="the color of the text", default="PURPLE")

parser.add_option("-r", "--rcolor", dest="rcolor",
help="the color the rear text gets blended to", default=None)

parser.add_option("-b", "--bgcolor", dest="bgcolor",
help="the color of the background", default="BLACK")

(options, args) = parser.parse_args()

# Configuration for the matrix
_options = RGBMatrixOptions()
_options.drop_privileges = False
_options.rows = 32
_options.chain_length = 1
_options.parallel = 1
_options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options=_options)

REAR_COLOR = options.rcolor
if REAR_COLOR == None:
    REAR_COLOR = options.bgcolor
BACKGROUND_COLOR = options.bgcolor
SIZE = 8
FONT = "monospace"

SPEED = 30

NUM_TEXT = 15

FPS = 35

def p(pix):
    if pix:
        return 1
    return 0

class Text:
    def __init__(self, canvas, start=False):
        self.order = random.randint(1, 255)
        self.text = options.text
        self.color = options.color
        self.size = round(SIZE + random.randint(-2, 2) + (2 * self.order / 255))
        self.orient = random.randint(0, 1)  # 0: Horz, 1: Vert
        text_size = canvas.textsize(self.text, font=get_font(FONT, self.size))
        self.image = Image.new("RGB", [max(text_size)] * 2, 0)
        self.canvas = ImageDraw.Draw(self.image)

        second_axis = random.randint(-self.size, 32 + self.size)
        self.pos = [0, 0]
        self.pos[not self.orient] = second_axis
        if start:
            self.pos[self.orient] = random.randint(-32, 32)
        else:
            self.pos[self.orient] = -text_size[0]
        self.speed = 30     # px/second
        DrawText(self.canvas, (0, 0), self.size, self.text, color_fade(self.color, REAR_COLOR, self.order), font=FONT, bold=True)
        if self.orient:
            self.image = self.image.rotate(90)
        self.mask = self.image.convert("L").point(p, "1")
        self.dead = False

    def get_order(self):
        return self.order

    def draw(self, image):
        pos = (int(self.pos[0]), int(self.pos[1]))
        image.paste(self.image, pos, self.mask)

    def update(self, time_passed):
        lag = (self.order / 200)
        if lag > 1:
            lag = 1
        self.pos[self.orient] += self.speed * time_passed * lag
        if self.pos[self.orient] > 32:
            self.dead = True

def run():
    time_passed = 0
    texts = []
    dead_text = []
    clock = Clock()
    image, canvas = new_canvas("RGB", BACKGROUND_COLOR)
    for x in range(NUM_TEXT):
        texts.append(Text(canvas, start=True))
    while True:
        canvas.rectangle(((0, 0), (32, 32)), BACKGROUND_COLOR)
        texts.sort(key=Text.get_order)
        for text in texts:
            text.draw(image)
            text.update(time_passed)
            if text.dead:
                dead_text.append(text)
        for dead in dead_text:
            texts.remove(dead)
            texts.append(Text(canvas))
        dead_text.clear()
        matrix.SetImage(image)
        time_passed = clock.tick(FPS) / 1000

def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
