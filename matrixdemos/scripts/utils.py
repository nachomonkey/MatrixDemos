import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor
from matrixdemos.scripts.get_file import get_file

def apply_alpha(image, background):
    try:
        if isinstance(image.getpixel((0, 0)), int):
            return image
        if len(image.getpixel((0, 0))) != 4:
            return image
    except:
        return image
    else:
        new_image = image.convert("RGB")
        for x in range(image.width):
            for y in range(image.height):
                px = image.getpixel((x, y))
                new_image.putpixel((x, y), color_fade(px[:3], background, px[3]))
        return new_image

def get_font(font, size):
    if os.path.exists(font):
        path = font
    else:
        path = get_file("fonts/" + font.lower() + ".ttf")
    if os.path.isdir(path):
        print(f"The font must not be a directory", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(path):
        print("The font file does not exist and is not built in", file=sys.stderr)
        sys.exit(2)
    return ImageFont.truetype(path, size)

def DrawText(canvas, pos, size=24, text="TEXT", color="BLUE", align="center", anchor="center", font="monospace", **kwargs):
    canvas.text(pos, text, fill=color, font=get_font(font, size), align=align, anchor=anchor, **kwargs)

def new_canvas(mode="RGB", color=0):
    image = Image.new(mode, (32, 32), color)
    canvas = ImageDraw.Draw(image)
    return image, canvas

def color_fade(color, back, alpha):
    if isinstance(color, str):
        color = ImageColor.getcolor(color, "RGB")
    if isinstance(back, str):
        back = ImageColor.getcolor(back, "RGB")
    if alpha < 0:
        alpha = 0
    new_color = list(back)
    new_color[0] += int((color[0] - back[0]) * (alpha / 255))
    new_color[1] += int((color[1] - back[1]) * (alpha / 255))
    new_color[2] += int((color[2] - back[2]) * (alpha / 255))
    return tuple(new_color)

