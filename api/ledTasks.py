#!/usr/bin/env python3
import time
from utils import matrix
import time
from PIL import Image, ImageDraw
import logging
import threading
from rgbmatrix import graphics
import math

tasks = []

# Utility functions for the animations below
def scale_col(val, lo, hi):
    if val < lo:
        return 0
    if val > hi:
        return 255
    return 255 * (val - lo) / (hi - lo)


def rotate(x, y, sin, cos):
    return x * cos - y * sin, x * sin + y * cos

# This is a class template that is used for making threads stoppable
# We will be using it to run led tasks on screen while we do other things
# and then stop them when we request it
class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class TestAnimation(StoppableThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logging.debug('starting test animation')
        # RGB example w/graphics prims.
        # Note, only "RGB" mode is supported currently.
        image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
        draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
        # Draw some shapes into image (no immediate effect on matrix)...
        draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0), outline=(0, 0, 255))
        draw.line((0, 0, 31, 31), fill=(255, 0, 0))
        draw.line((0, 31, 31, 0), fill=(0, 255, 0))

        # Then scroll image across matrix...
        for n in range(-32, 33):
            if self.stopped():
                break
            matrix.Clear()
            matrix.SetImage(image, n, n)
            time.sleep(0.05)

# This is a test function to display a simple single white pixel in the middle of the screen using SwapOnVSync
class PixelTest(StoppableThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logging.debug('starting pixel test with vsync')
        cent_x = matrix.width / 2
        cent_y = matrix.height / 2

        offset_canvas = matrix.CreateFrameCanvas()

        offset_canvas.SetPixel(cent_x, cent_y, 255, 255, 255)

        offset_canvas = matrix.SwapOnVSync(offset_canvas)

# This is a test function for scrolling text
class ScrollingText(StoppableThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logging.debug('starting scrolling text')
        offscreen_canvas = matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width
        my_text = 'bendersux'

        while True:
            if self.stopped():
                logging.debug('stopping scrolling text')
                matrix.Clear()
                return
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

# This is a test function for scrolling text
class RotatingBlock(StoppableThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logging.debug('starting rotating block')
        cent_x = matrix.width / 2
        cent_y = matrix.height / 2

        rotate_square = min(matrix.width, matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(matrix.width, matrix.height) * 0.7
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * 3.14159265 / 360
        rotation = 0

        # Pre calculate colors
        col_table = []
        for x in range(int(min_rotate), int(max_rotate)):
            col_table.insert(x, scale_col(x, min_display, max_display))

        offset_canvas = matrix.CreateFrameCanvas()

        while True:
            if self.stopped():
                matrix.Clear()
                return
            rotation += 1
            rotation %= 360

            # calculate sin and cos once for each frame
            angle = rotation * deg_to_rad
            sin = math.sin(angle)
            cos = math.cos(angle)

            for x in range(int(min_rotate), int(max_rotate)):
                for y in range(int(min_rotate), int(max_rotate)):
                    # Our rotate center is always offset by cent_x
                    rot_x, rot_y = rotate(x - cent_x, y - cent_x, sin, cos)

                    if x >= min_display and x < max_display and y >= min_display and y < max_display:
                        x_col = col_table[x]
                        y_col = col_table[y]
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, x_col, 255 - y_col, y_col)
                    else:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

            offset_canvas = matrix.SwapOnVSync(offset_canvas)