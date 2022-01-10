#!/usr/bin/env python3
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import math
import time
from utils import celery_app, matrix
import time

@celery_app.task()
def pixel():
    offset_canvas = matrix.CreateFrameCanvas()
    cent_x = matrix.width / 2
    cent_y = matrix.height / 2 

    offset_canvas.SetPixel(cent_x, cent_y, 255, 255, 255)

    offset_canvas = matrix.SwapOnVSync(offset_canvas)