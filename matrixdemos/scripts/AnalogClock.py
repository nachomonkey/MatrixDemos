#!/usr/bin/env python3
import sys
import time
from optparse import OptionParser
from math import radians, sin, cos

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from matrixdemos.scripts.utils import *

usage = "Usage %prog [--help] [options]"
description = """Display an analog clock on the matrix (32x32 only)"""

parser = OptionParser(usage=usage, description=description, add_help_option=False)

parser.add_option("--help", action="help", help="show this help message and exit")

parser.add_option("-c", default="red", help="the color of the clock", dest="clock")

parser.add_option("-s", default="green", help="the color of the seconds hand", dest="secs")

parser.add_option("-m", default="red", help="the color of the minutes hand", dest="mins")

parser.add_option("-h", default="blue", help="the color of the hour hand", dest="hours")

parser.add_option("-b", default="black", help="the color of the background", dest="bg")

(options, args) = parser.parse_args()

# Configuration for the matrix
_options = RGBMatrixOptions()
_options.drop_privileges = False
_options.rows = 32
_options.chain_length = 1
_options.parallel = 1
_options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options=_options)

CLOCK_COLOR = options.clock
SEC_COLOR = options.secs
MIN_COLOR = options.mins
HR_COLOR = options.hours
BG_COLOR = options.bg

def Sin(deg):
    return sin(radians(deg - 90))

def Cos(deg):
    return cos(radians(deg - 90))

SEC_RADIUS = 15
CENTER = (15, 15)

def run():
    colon = True
    image, canvas = new_canvas()
    while True:
        canvas.rectangle(((0, 0), (32, 32)), BG_COLOR)
        t = time.localtime()
        sec_deg = 360 * (t.tm_sec / 60)
        mins_deg = 360 * ((t.tm_min / 60) + (t.tm_sec / 3600))
        hrs_deg = 360 * ((t.tm_hour % 12 / 12) + (t.tm_min / 720))
        sec = (CENTER[0] + Cos(sec_deg) * 14, CENTER[1] + Sin(sec_deg) * 14)
        mins = (CENTER[0] + Cos(mins_deg) * 12, CENTER[1] + Sin(mins_deg) * 12)
        hrs = (CENTER[0] + Cos(hrs_deg) * 7, CENTER[1] + Sin(hrs_deg) * 7)

        # Ticks
        for x in range(12):
            deg = 360 * (x / 12)
            pos1 = (CENTER[0] + Cos(deg) * 13, CENTER[1] + Sin(deg) * 13)
            pos2 = (CENTER[0] + Cos(deg) * 15, CENTER[1] + Sin(deg) * 15)
            canvas.line((pos1, pos2), fill=CLOCK_COLOR)

        # Outline
        canvas.ellipse(((0, 0), (31, 31)), outline=CLOCK_COLOR)

        # Hours Hand
        canvas.line((CENTER, hrs), fill=HR_COLOR, width=2)

        # Minutes Hand
        canvas.line((CENTER, mins), fill=MIN_COLOR)

        # Seconds Hand
        canvas.line((CENTER, sec), fill=SEC_COLOR)

        # Center
        canvas.rectangle(((15, 15), (16, 16)), fill=CLOCK_COLOR)

        matrix.SetImage(image.convert("RGB"))
        time.sleep(1)

def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
