# MatrixDemos

*A collection of demos for a Raspberry Pi and the Adafruit 32x32 matrix*

### Software Dependencies

* Python >= 3.6

* Pillow
* pygame (joystick support)

### Hardware Dependencies

* Raspberry Pi 2, 3, or 4; running Raspbian Buster or greater
* [Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)
* [Adafruit 32x32 RGB LED Matrix](https://www.adafruit.com/product/1484)
* [5V 4A power supply](https://www.adafruit.com/product/1466)
* USB joystick (optional)

## Instructions

1. [Assemble your Matrix HAT](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly)
2. [Wire up and configure the Raspberry Pi](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices)
3. Install MatrixDemos

```bash
sudo pip3 install MatrixDemos
```

Now, the MatrixDemos are installed. You can test by running this, which lists the possible demo commands:

```bash
python3 -m matrixdemos
```

## Usage

Execute any of the following console commands.

* `matrix_digitalclock`: Shows the time and date. Run with `-sdn` to only display time.
* `matrix_analogclock`: Displays a simple analog clock, use command line options to change colors
* `matrix_slideshow path/to/images/`: Display images from a directory.  Use `-l` to change the slide time in seconds, and `-b` for the background color
* `matrix_snakegame` The classic "snake game" now on your matrix! **Requires a USB joystick!**
* `matrix_stars` Displays some twinkling stars. Use `-s` to adjust speed
* `matrix_textswarm` Displays text flying about. Use `-c` to edit the text color, and `-b` for the background color.
* `matrix_animations [[PATH]/[DEMO]]` Shows an animation from images in a directory. Use `-f` to adjust framerate, and `-l` and `-n` to control looping. Use `-g` to specify an animated gif or video
* `matrix_scrolling [[TEXT]/[PATH]]` Scrolls text or an image from left to right. Use `-c` and `-f` to adjust text color and font, `-s` for speed, `-r` to repeat, and `-b` to bounce.

Visit the [Gallery](extra/gallery.md) to see a visualization of each demo.

### Setting Colors:

When setting the color on (ie. `-c` in `matrix_textswarm`) you can specify either the color's name (RED) or its hex code ("#ff000").

Example of setting the color of the analog clock:
`matrix_analogclock -c "#333" -s Red -m white -h "#aaaaaa" -b "#001"`

# License

This software is under the MIT License. See the [LICENSE](https://github.com/nachomonkey/MatrixDemos/blob/master/LICENSE) file for more details.
