

# importing image object from PIL
import math, os
from PIL import Image, ImageDraw, ImageFont

# first let's get the coordinates from MiniZinc

model_file = "rect_packing.mzn"
# make sure the path is set relative to the current file
model_file = os.path.join(os.path.dirname(__file__), model_file)

import minizinc
from minizinc import Model, Status

square_packing_model = Model(model_file)
solver = minizinc.Solver.lookup("gecode")

# number of squares we want to pack

# 4 x 3 -> 3
# 3 x 4 -> 7
widths  = [5, 6, 4, 3, 2, 4, 3, 1, 2, 1, 7, 3]
heights = [1, 2, 3, 2, 1, 2, 4, 6, 5, 1, 1, 2]
n = len(widths)

inst = minizinc.Instance(solver, square_packing_model)
inst["n"] = n
inst["widths"] = widths
inst["heights"] = heights
inst.add_string("constraint sq_width >= sq_height;")
inst.add_string("constraint sq_width >= 15;")
inst.add_string("constraint sq_height >= 15;")
# 4 x 3 -> 3
# 3 x 4 -> 7
# abstand in X-Richtung mindestens 2:
inst.add_string("constraint x[7] + widths[7] + 2 <= x[3] \/ x[3] + widths[3] + 2 <= x[7] ;")
result = inst.solve()

# coordinates
pos_x = [ ]
curr_x = 0
for i in range(1, n+1):
    pos_x.append(curr_x)
    curr_x += widths[i-1]

pos_y = [i for i in range(1, n+1)]

if result.status == Status.SATISFIED or result.status == Status.OPTIMAL_SOLUTION:
    print("sounds good")
    pos_x, pos_y = result["x"], result["y"]
    area = result["area"]
    mzn_width = result["sq_width"]
    mzn_height = result["sq_height"]
    print(pos_x)
    print(pos_y)

start_x, start_y = 20, 40
pixel_unit = 50

imwidth, imheight = mzn_width * pixel_unit + 2 * start_x, start_y + start_x + mzn_height * pixel_unit

# creating new Image object
img = Image.new("RGB", (imwidth, imheight))

# create rectangle image
img1 = ImageDraw.Draw(img)

# get a font
myFont = ImageFont.truetype("arialbd.ttf", 20, )

# draw surrounding rectangle
shape = [(start_x, start_y), (start_x + mzn_width * pixel_unit, start_y + mzn_height * pixel_unit)]
img1.rectangle(shape, fill ="#000000", outline ="white")
for i in range(1,n+1):
    shape_x, shape_y = pos_x[i-1], pos_y[i-1]

    draw_start_x, draw_start_y = start_x + pixel_unit *  shape_x, start_y + pixel_unit * shape_y
    draw_end_x, draw_end_y = draw_start_x + widths[i-1] * pixel_unit, draw_start_y + heights[i-1] * pixel_unit

    # draw a rectangle of size i*i
    shape = [(draw_start_x, draw_start_y), (draw_end_x, draw_end_y)]
    img1.rectangle(shape, fill ="#005A9B", outline ="white")
    msg =  f"{widths[i-1]} x {heights[i-1]}"
    w, h = img1.textsize(msg, font=myFont)
    center_x, center_y = (draw_start_x + draw_end_x) / 2, (draw_start_y + draw_end_y) / 2
    img1.text((center_x - w / 2, center_y - h / 2), msg, fill="white", font=myFont)

# show area
center_x, center_y = imwidth / 2, start_y / 2
msg =  f"Area is {area}, width = {mzn_width}, height = {mzn_height}"
w, h = img1.textsize(msg, font=myFont)
img1.text((center_x - w / 2, center_y - h / 2), msg, fill="white", font=myFont)

img.show()
