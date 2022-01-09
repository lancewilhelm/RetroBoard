#!/usr/bin/env python3
from base import Base
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import math
import asyncio

class RotatingBlockGenerator(Base):
    def __init__(self, *args, **kwargs):
        print('In Block init')
        super().__init__(*args, **kwargs)

    def rotate(self, x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }

    def scale_col(self, val, lo, hi):
        if val < lo:
            return 0
        if val > hi:
            return 255
        return 255 * (val - lo) / (hi - lo)

    def run(self, user_args):
        print('In run function')
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(self.matrix.width, self.matrix.height) * 0.7
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * math.pi/ 360
        rotation = 0
        offset_canvas = self.matrix.CreateFrameCanvas()

        while True:
            rotation += 1
            rotation %= 180

            for x in range(int(min_rotate), int(max_rotate)):
                for y in range(int(min_rotate), int(max_rotate)):
                    ret = self.rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
                    rot_x = ret["new_x"]
                    rot_y = ret["new_y"]

                    if x >= min_display and x < max_display and y >= min_display and y < max_display:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, self.scale_col(x, min_display, max_display), 255 - self.scale_col(y, min_display, max_display), self.scale_col(y, min_display, max_display))
                    else:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

            if rotation == 0:
                return

class RunText(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self, usr_args):
        print('running text')
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/6x10.bdf")
        font_height = font.height
        print(font_height)
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            asyncio.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

class SimplePixel(Base):
    @classmethod
    async def create(cls, *args, **kwargs):
        self = SimplePixel()
        super(SimplePixel, self).__init__(*args, **kwargs)
        for i in range(5):
            print('made class for simple pixel')
            asyncio.sleep(1)
        return self

    async def run(self, usr_args):
        offset_canvas = self.matrix.CreateFrameCanvas()
    
# For debugging purposes
if __name__ == '__main__':
    # Create the object
    run_text = RunText()
    
    print('between class init and running')

    if (run_text.process({})):
        print('run text succeeded')
    else:
        print('run text failed')