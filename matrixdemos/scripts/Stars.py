#!/usr/bin/env python3
import sys
import time
import random

from optparse import OptionParser
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from matrixdemos.scripts.utils import *

description = "A simple demo of twinkling stars"

parser = OptionParser(description=description)

parser.add_option("-s", "--speed",
help="set the animation speed multiplier as a float", type=float,
dest="speed", default=1)

(options, args) = parser.parse_args()

_options = RGBMatrixOptions()
_options.drop_privileges = False
_options.rows = 32
_options.chain_length = 1
_options.parallel = 1
_options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=_options)

STAR_COLOR = (190, 200, 255)
BACKGROUND_COLOR = (1, 3, 5)

SPEED = options.speed
if SPEED <= 0:
    sys.stderr.write("ERR: Animation speed must exceed zero\n")
    sys.exit()
if SPEED > 20:
    sys.stderr.write("ERR: Animation speed must be below 20\n")
    sys.exit()

STAR_COUNT = 40

class Star:
    def __init__(self, start=False):
        self.pos = (random.randint(0, matrix.width - 1), (random.randint(0, matrix.height - 1)))
        self.fuzz_amount = 5        # Alpha can always be +/- this number
        self.max_alpha = random.randint(30, 200)
        self.alpha = random.randint(-100, (self.max_alpha - 5) if start else 0)
        self.grow_speed = random.uniform(.4, .8)
        self.fade_speed = random.uniform(.3, .8)
        self.tolerance = 1          # Starts going down if max_alpha-alpha>=tolerance
        self.going_up = True
        self.dead = False

    def draw(self, canvas):
        fuzz = random.uniform(-self.fuzz_amount, self.fuzz_amount)
        canvas.point(self.pos, color_fade(STAR_COLOR, BACKGROUND_COLOR, self.alpha + fuzz))

    def update(self, time_passed):
        if not time_passed:
            return
        if self.going_up:
            self.alpha += (self.max_alpha - self.alpha) * (time_passed * self.grow_speed)
        else:
            self.alpha -= (self.alpha) * (time_passed * self.fade_speed)
        if self.going_up and abs(self.max_alpha - self.alpha) <= self.tolerance:
            self.going_up = False
        if (not self.going_up) and self.alpha < 5:
            self.dead = True

class StarSimulator:
    def __init__(self):
        self.image, self.canvas = new_canvas()
        self.time_passed = 0
        self.stars = []

    def run(self):
        for x in range(STAR_COUNT):
            self.stars.append(Star(True))
        while True:
            self.draw()
            self.update()

    def draw(self):
        self.canvas.rectangle(((0, 0), (matrix.width, matrix.height)), BACKGROUND_COLOR)
        for star in self.stars:
            star.draw(self.canvas)
        matrix.SetImage(self.image)

    def update(self):
        dead_stars = []
        for star in self.stars:
            star.update(self.time_passed)
            if star.dead:
                dead_stars.append(star)
        for dead in dead_stars:
            self.stars.remove(dead)
            self.stars.append(Star())          # And remember: a star lost is a star earned!
        t1 = time.time()
        time.sleep(.1)
        self.time_passed = (time.time() - t1) * SPEED

def main():
    try:
        sim = StarSimulator()
        sim.run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
