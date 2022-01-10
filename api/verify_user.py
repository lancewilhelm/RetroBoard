import os
import pwd
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.drop_privileges = False

print('User before RGBMatrix: ' + pwd.getpwuid(os.getuid()).pw_name)
matrix = RGBMatrix(options=options)
print('User after RGBMatrix: ' + pwd.getpwuid(os.getuid()).pw_name)