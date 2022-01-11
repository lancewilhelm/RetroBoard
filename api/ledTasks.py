#!/usr/bin/env python3
import time
from utils import api, matrix
import time
from PIL import Image, ImageDraw
import logging

def pixel():
    logging.debug('starting pixel function')
    # RGB example w/graphics prims.
    # Note, only "RGB" mode is supported currently.
    image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
    draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
    # Draw some shapes into image (no immediate effect on matrix)...
    draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0), outline=(0, 0, 255))
    draw.line((0, 0, 31, 31), fill=(255, 0, 0))
    draw.line((0, 31, 31, 0), fill=(0, 255, 0))

    # Then scroll image across matrix...
    for n in range(-32, 33):  # Start off top-left, move off bottom-right
        matrix.Clear()
        matrix.SetImage(image, n, n)
        time.sleep(0.05)

    matrix.Clear()
    
    logging.debug('pixel function complete')