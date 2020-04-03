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
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from subprocess import Popen

from math import sqrt
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
    sys.stderr.write("ERR: This program requires a joystick.\n")
    sys.stderr.write("X-BOX and GameCube remotes are compatible\n")
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

def run():
    HEAD = [16, 16]
    TAIL = [16, 17]
    SNAKE = [copy.copy(HEAD), copy.copy(TAIL)]
    DIRECTION = "RIGHT"
    state = "MENU"
    FOOD = spawn_food()
    score = 0
    def add_new_segment(SNAKE, OLDPOS):
        SNAKE.append(OLDPOS)

    hi_score = str(get_high_score())
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
            DrawText(canvas, (2, 0), 10, "Start?", font="cambriab", color=(255, 100, 0))
            DrawText(canvas, (0, 12), 8, f"Hi Score:", font="cambriab", color=(255, 255, 0))
            DrawText(canvas, (13, 18), 8, hi_score, color=(0, 255, 0))
            matrix.SetImage(image)
        if state == "GAME":
            joyPos = [0, 0]
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_LEFT and DIRECTION != "RIGHT":
                        DIRECTION = "LEFT"
                    elif event.key == pygame.K_RIGHT and DIRECTION != "LEFT":
                        DIRECTION = "RIGHT"
                    elif event.key == pygame.K_UP and DIRECTION != "DOWN":
                        DIRECTION = "UP"
                    elif event.key == pygame.K_DOWN and DIRECTION != "UP":
                        DIRECTION = "DOWN"
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        joyPos[0] = event.value
                    if event.axis == 1:
                        joyPos[1] = event.value
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        exit()
            if joyPos[0] > .7 and DIRECTION != "LEFT":
                DIRECTION = "RIGHT"
            elif joyPos[1] > .7 and DIRECTION != "UP":
                DIRECTION = "DOWN"
            elif joyPos[0] < -.7 and DIRECTION != "RIGHT":
                DIRECTION = "LEFT"
            elif joyPos[1] < -.7 and DIRECTION != "DOWN":
                DIRECTION = "UP"
            for p in SNAKE:
                if p == HEAD and SNAKE.index(p) != 0:
                    state = "LOST"
                    continue
                canvas.point(p, "GREEN")
            canvas.point(FOOD, "RED")
            if DIRECTION == "UP":
                HEAD[1] -= 1
            if DIRECTION == "DOWN":
                HEAD[1] += 1
            if DIRECTION == "LEFT":
                HEAD[0] -= 1
            if DIRECTION == "RIGHT":
                HEAD[0] += 1
            old = copy.copy(HEAD)
            for s in SNAKE:
                SNAKE[SNAKE.index(s)] = old
                old = s
            OLDPOS = SNAKE[-1]
            if HEAD == FOOD:
                score += 1
                FOOD = spawn_food()
                add_new_segment(SNAKE, OLDPOS)
            if HEAD[0] < 0 or HEAD[0] >= 32 or HEAD[1] < 0 or HEAD[1] >= 32:
                state = "LOST"
            matrix.SetImage(image)
            time.sleep(0.1 / (len(SNAKE) / 2.75))
        if state == "LOST":
            image, canvas = new_canvas()
            broke_record = check_high_score(score)
            if broke_record:
                print("\nNew High Score!!!")
            DrawText(canvas, (6, -4), 11, "You", font="cambriab", color=(255, 100, 0))
            DrawText(canvas, (5, 8), 11, "Lost", font="cambriab", color=(255, 100, 0))
            DrawText(canvas, (0, 17), 8, "Score:", font="cambriab", color=(255, 255, 0))
            DrawText(canvas, (26, 17), 8, str(score), font="cambriab", color=(0, 255, 0))
            matrix.SetImage(image)
            time.sleep(2)
            state = "MENU"
            HEAD = [16, 16]
            TAIL = [16, 17]
            score = 0
            SNAKE = [copy.copy(HEAD), copy.copy(TAIL)]
            hi_score = str(get_high_score())
            DIRECTION = "RIGHT"
            FOOD = spawn_food()
 
def main():
    try:
        run()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
