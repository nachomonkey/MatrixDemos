#!/usr/bin/env python3
"""Display the time and date on the matrix"""
import sys
import time
from optparse import OptionParser
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from matrixdemos.scripts.utils import *

parser = OptionParser()

parser.set_description("""Display the time and date on a matrix.
By default, this will dim to 1% brightness at from 10 PM to 7 AM
and cease to display the date""")

parser.add_option("--24h", action="store_true", dest="twentyfour_hr",
default=False, help="make this a 24-hour clock instead of 12-hour")

parser.add_option("-a", "--always-on", action="store_false", dest="dimming",
default=True, help="disables the dimming at night")

parser.add_option("-s", "--remove-seconds", action="store_false", dest="secs",
default=True, help="removes the seconds bar at the top of the matrix")

parser.add_option("-d", "--remove-date", action="store_false", dest="date",
default=True, help="stops displaying the date")

parser.add_option("-n", "--no-flash", action="store_false", dest="flash",
default=True, help="makes the colon in the middle stop flashing")

(options, args) = parser.parse_args()

# True for 24 hour clock
CLK_24_HOUR = options.twentyfour_hr

ENABLE_DIMMING = options.dimming
DISPLAY_SECONDS = options.secs
DISPLAY_DATE = options.date
COLON_FLASH = options.flash

# Configuration for the matrix
_options = RGBMatrixOptions()
_options.drop_privileges = False
_options.rows = 32
_options.chain_length = 1
_options.parallel = 1
_options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options=_options)

SMALL_SIZE = 10
BIG_SIZE = 13

def run():
    colon = True
    while True:
        image, canvas = new_canvas()
        t = time.localtime()
        dim = False
        if t.tm_hour < 7 or t.tm_hour > 21 and ENABLE_DIMMING:
            matrix.brightness = 1
            dim = True
        else:
            matrix.brightness = 100
        am_pm = "AM"
        if t.tm_hour > 11:
            am_pm = "PM"
        hr = t.tm_hour
        if not CLK_24_HOUR:
            hr = hr % 12
            if hr == 0:
                hr = 12
        if COLON_FLASH:
            colon = not colon
        text = f"{hr if not CLK_24_HOUR else t.tm_hour}{':' if colon else ' '}{str(t.tm_min).zfill(2)}"
        size = BIG_SIZE
        if len(text) >= 5:
            size = SMALL_SIZE
        if DISPLAY_SECONDS:
            for x in range(0, t.tm_sec * 32 // 60):
                canvas.point((x, 0), fill=(int(x / 32 * 255) if not dim else 230, 0, 0)) 
        DrawText(canvas, (1 if len(text) >= 5 else 0, 0 if len(text) >= 5 else -3), size=size, text=text, color="red")
        if not CLK_24_HOUR:
            DrawText(canvas, (0, 10), size=8, text=am_pm, color="RED") 
        if not dim and DISPLAY_DATE:
            DrawText(canvas, (11, 7), size=12, text=time.asctime()[4:7], font="cambriab", color="GREEN") 
            DrawText(canvas, (0, 20), size=8, text=time.asctime()[:3], color="LIME") 
            DrawText(canvas, (15, 18), size=12, text=str(t.tm_mday), color="GREEN") 
        time.sleep(1)
        matrix.SetImage(image.convert("RGB"))

def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
