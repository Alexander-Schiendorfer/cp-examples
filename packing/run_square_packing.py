

# importing image object from PIL
import math, os
from PIL import Image, ImageDraw, ImageFont

# first let's get the coordinates from MiniZinc

model_file = "square_packing.mzn"
# make sure the path is set relative to the current file
model_file = os.path.join(os.path.dirname(__file__), model_file)

import minizinc
from minizinc import Model, Status

square_packing_model = Model(model_file)
gecode_solver = minizinc.Solver.lookup("gecode")

# number of squares we want to pack
n = 8

inst = minizinc.Instance(gecode_solver, square_packing_model)
inst["n"] = n

result = inst.solve()

# coordinates
pos_x = [ ]
curr_x = 0
for i in range(1, n+1):
    pos_x.append(curr_x)
    curr_x += i

pos_y = [i for i in range(1, n+1)]

if result.status == Status.SATISFIED or result.status == Status.OPTIMAL_SOLUTION:
    print("sounds good")
    pos_x, pos_y = result["x"], result["y"]


w, h = 1600, 900
shape = [(40, 40), (w - 10, h - 10)]

# creating new Image object
img = Image.new("RGB", (w, h))

# create rectangle image
img1 = ImageDraw.Draw(img)

# get a font
myFont = ImageFont.truetype("arialbd.ttf", 24, )
#myFont.set_variation_by_name('Bold')

start_x, start_y = 20, 20
pixel_unit = 50
for i in range(1,n+1):
    shape_x, shape_y = pos_x[i-1], pos_y[i-1]

    draw_start_x, draw_start_y = start_x + pixel_unit *  shape_x, start_y + pixel_unit * shape_y
    draw_end_x, draw_end_y = draw_start_x + i * pixel_unit, draw_start_y + i*pixel_unit

    # draw a rectangle of size i*i
    shape = [(draw_start_x, draw_start_y), (draw_end_x, draw_end_y)]
    img1.rectangle(shape, fill ="#005A9B", outline ="white")
    msg = str(i)
    w, h = img1.textsize(msg, font=myFont)
    center_x, center_y = (draw_start_x + draw_end_x) / 2, (draw_start_y + draw_end_y) / 2
    img1.text((center_x - w / 2, center_y - h / 2), msg, fill="white", font=myFont)

img.show()
