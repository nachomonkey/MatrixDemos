try:
    from matrixdemos import __version__, __author__
except ImportError:
    header = ""
else:
    header = f"--- MatrixDemos V{__version__} by {__author__} ---\n"

e = '\033[0m'
b = '\033[1m'

def main():
    print(header, end="")
    print("A collection of demos for the Adafruit 32x32 matrix.\n")
    print("This package contains:\n")
    print("---")
    print(f"{b}matrix_digitalclock{e}      A clock that shows the time and date")
    print(f"{b}matrix_analogclock{e}       A simple analog clock")
    print(f"{b}matrix_slideshow{e}         Display images from a diretory")
    print(f"{b}matrix_snakegame{e}         The classic \"Snake Game\" (Requires a joystick)")
    print(f"{b}matrix_stars{e}             A simple demo of twinkling stars")
    print(f"{b}matrix_textswarm{e}         Display text flying all about")
    print(f"{b}matrix_animations{e}        Play an animation from images, GIFs, or videos")
    print(f"{b}matrix_scrolling{e}         Scroll text or an image from left to right")
    print(f"---")

if __name__ == "__main__":
    main()
