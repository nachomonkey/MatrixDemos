#!/usr/bin/python3
import sys
import os

from optparse import OptionParser
from matrixdemos import DATA_PATH

description = """The classic snake game, now on your matrix!
This requires a USB joystick."""

HI_SCORE_FILE = f"{DATA_PATH}/snakey_hiscore"

parser = OptionParser(description=description)

parser.add_option("-c", help="clear the high score", action="store_true", dest="clear", default=False)

(options, args) = parser.parse_args()

if options.clear:
    print("Are you sure you want to clear the high score?")
    ans = input("[y/N]: ").lower()
    if ans in ("y", "yes"):
        print("Clearing high score...", end="")
        os.remove(HI_SCORE_FILE)
        print(" done")
    else:
        print("Exiting without clearing high score...")
    sys.exit()

import random
import time
import copy
import colorsys                                         # Convert hsl to rgb
import pygame                                           # Joystick support
from subprocess import Popen
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageEnhance

from math import sqrt, sin
from matrixdemos.scripts.utils import *
from matrixdemos.scripts.get_file import get_file

os.environ["DISPLAY"] = ":0"

pygame.display.init()
pygame.joystick.init()

OK_CODE = 1

print()

if not os.path.isdir(DATA_PATH):
    sys.stderr.write(f"""ERR: The destination data directory ({DATA_PATH})
for this program is occupied by a file!
Delete or move this file to continue\n""")
    sys.exit(1)

try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    name = joy.get_name().lower()
    if ("x" in name and "box" in name):
        OK_CODE = 0
except:
    sys.stderr.write("ERR: This program requires a USB joystick.\n")
    sys.stderr.write("X-BOX and Nintendo GameCube controllers are compatible\n")
    sys.exit(1)

def spawn_food():
    return [random.randint(1, 30), random.randint(1, 30)]

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
options.drop_privileges = False

matrix = RGBMatrix(options = options)

JOYSTICK_SENSITIVITY = 0.6

def get_high_score():
    if not os.path.exists(HI_SCORE_FILE):
        with open(HI_SCORE_FILE, "wb") as file:
            file.write((0).to_bytes(1, 'little'))
    with open(HI_SCORE_FILE, "rb") as file:
        return int.from_bytes(file.read(), 'little')

def check_high_score(score):
    high_score = get_high_score()
    if score > high_score:
        with open(HI_SCORE_FILE, "wb") as file:
            file.write(score.to_bytes(1, 'little'))
        return True
    return False

# Change RGB from 0-1 to 0-255
def make_rgb(rgb):
    r, g, b = rgb
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r, g, b)

def run():
    print("--Snakey--")
    print("Press A to Start")

    head = [16, 16]
    tail = [16, 17]
    snake = [copy.copy(head), copy.copy(tail)]
    direction = "RIGHT"
    state = "MENU"
    food = spawn_food()
    score = 0
    def add_new_segment(snake, oldpos):
        snake.append(oldpos)

    hi_score = str(get_high_score())

    start_image = Image.open(get_file("images/SnakeyStart.png"))
    start_image2 = Image.open(get_file("images/SnakeyStart2.png"))
    start_image3 = Image.open(get_file("images/SnakeyStart3.png"))
    start_image4 = Image.open(get_file("images/SnakeyStart4.png"))
    gameover_image = Image.open(get_file("images/SnakeyGameOver.png"))

    while True:
        image, canvas = new_canvas()
        if state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = "GAME"
                    if event.key == pygame.K_ESCAPE:
                        exit()
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == OK_CODE:
                        state = "GAME"
            enhancer = ImageEnhance.Brightness((start_image, start_image2, start_image3, start_image4)[int((time.time()) * 10) % 4])
            start_img = enhancer.enhance(abs(sin(time.time() * 1.5 )) * 0.5 + 0.75)
            canvas = ImageDraw.Draw(start_img)
            DrawText(canvas, (16, 23), 8, hi_score, make_rgb(colorsys.hsv_to_rgb(time.time() % 360, 1, 1)), center=True)
            matrix.SetImage(start_img)
        if state == "GAME":
            joyPos = [0, 0]
            old_direction = direction

# This variable is used to prevent multiple direction changes
# occuring in one frame, which can cause U-Turn
            changed_direction = False

            for event in pygame.event.get():
                if old_direction != direction:
                    changed_direction = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if not changed_direction:
                        if event.key == pygame.K_LEFT and direction != "RIGHT":
                            direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and direction != "LEFT":
                            direction = "RIGHT"
                        elif event.key == pygame.K_UP and direction != "DOWN":
                            direction = "UP"
                        elif event.key == pygame.K_DOWN and direction != "UP":
                            direction = "DOWN"
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        joyPos[0] = event.value
                    if event.axis == 1:
                        joyPos[1] = event.value
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        exit()
                if event.type == pygame.JOYHATMOTION:
                    if not changed_direction:
                        if event.value == (-1, 0) and direction != "RIGHT":
                            direction = "LEFT"
                        elif event.value == (1, 0) and direction != "LEFT":
                            direction = "RIGHT"
                        elif event.value == (0, 1) and direction != "DOWN":
                            direction = "UP"
                        elif event.value == (0, -1) and direction != "UP":
                            direction = "DOWN"
            if not changed_direction:
                if joyPos[0] > JOYSTICK_SENSITIVITY and direction != "LEFT":
                    direction = "RIGHT"
                elif joyPos[1] > JOYSTICK_SENSITIVITY and direction != "UP":
                    direction = "DOWN"
                elif joyPos[0] < -JOYSTICK_SENSITIVITY and direction != "RIGHT":
                    direction = "LEFT"
                elif joyPos[1] < -JOYSTICK_SENSITIVITY and direction != "DOWN":
                    direction = "UP"
            for index, point in enumerate(snake):
                if point == head and index:
                    state = "LOST"
                    continue
                canvas.point(point, "GREEN")
            canvas.point(food, "RED")
            if direction == "UP":
                head[1] -= 1
            if direction == "DOWN":
                head[1] += 1
            if direction == "LEFT":
                head[0] -= 1
            if direction == "RIGHT":
                head[0] += 1
            old = copy.copy(head)
            for s in snake:
                snake[snake.index(s)] = old
                old = s
            oldpos = snake[-1]
            if head == food:
                score += 1
                food = spawn_food()
                add_new_segment(snake, oldpos)
            if head[0] < 0 or head[0] >= 32 or head[1] < 0 or head[1] >= 32:
                state = "LOST"
            matrix.SetImage(image)
            time.sleep(0.1 / (len(snake) / 2.75))
        if state == "LOST":
            pygame.event.set_blocked(True)
            image = gameover_image.copy()
            canvas = ImageDraw.Draw(image)
            broke_record = check_high_score(score)
            if broke_record:
                print("\nNew High Score!!!")
            DrawText(canvas, (15, 23), 8, str(score), color=(0, 255, 0), center=True)
            matrix.SetImage(image)
            for x in range(40):
                if broke_record:
                    if x % 2:
                        matrix.SetImage(gameover_image)
                    else:
                        matrix.SetImage(image)
                time.sleep(0.1)
            state = "MENU"
            head = [16, 16]
            tail = [16, 17]
            score = 0
            snake = [copy.copy(head), copy.copy(tail)]
            hi_score = str(get_high_score())
            direction = "RIGHT"
            food = spawn_food()
            pygame.event.set_blocked(False)
 
def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
