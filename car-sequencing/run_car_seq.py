

# importing image object from PIL
import math
from PIL import Image, ImageDraw, ImageFont


model_file = "car_seq.mzn"

import minizinc
import datetime

from minizinc import Model, Status

model = Model(model_file)
solver = minizinc.Solver.lookup("gecode")

# problem specification
nOptions = 5
nCarConfigs = 6
at_most = [1, 2, 2, 2, 1]
per_slots = [2, 3, 3, 5, 5]
demand = [1,1,2,2,2,2]
nCars = sum(demand)
nSlots = nCars
requires = [
[1, 0, 1, 1, 0],
[0, 0, 0, 1, 0],
[0, 1, 0, 0, 1],
[0, 1, 0, 1, 0],
[1, 0, 1, 0, 0],
[1, 1, 0, 0, 0]]

lastT = 14
nTasks = 3;
dur = [ [5, 2, 3 ], [4, 5, 1], [ 3, 4, 2 ]]
nMachines = 3
taskToMach = [[1, 2, 3 ],[ 2, 1, 3],[ 2, 3, 1 ]]
# prettier output for slots
datetime_object = datetime.datetime.strptime('14:00', '%H:%M')
date_list = [datetime_object + datetime.timedelta(minutes=15*x) for x in range(0, nSlots)]
print_dates = [d.strftime('%H:%M') for d in date_list]

inst = minizinc.Instance(solver, model)

inst["nOptions"] = nOptions
inst["nCarConfigs"] = nCarConfigs
inst["nTasks"] = nTasks
inst["at_most"] = at_most
inst["per_slots"] = per_slots
inst["demand"] = demand
inst["requires"] = requires

# for example, first slot should be a config 1
#inst.add_string("constraint line[1] = 1;")
result = inst.solve()


if result.status == Status.SATISFIED or result.status == Status.OPTIMAL_SOLUTION:
    print("sounds good")
    line = result["line"]
    setup = result["setup"]
else:
    print("Problem is not solvable! Canceling.")
    exit(0)

vert_pad = 50
hor_pad = 50
slot_width = 80
car_conf_width = 200
demand_width = 100
opt_width = 50
line_height = 40

def writeAt(x, y, msg, draw, myFont, fillc):
    # write a label there
    text_w, text_h = draw.textsize(msg, font=myFont)
    draw.text((x - text_w / 2, y - text_h / 2), msg, fill=fillc, font=myFont)

problem_width = car_conf_width + nOptions*opt_width + demand_width
problem_height = (nCarConfigs + 2) * line_height

solution_width = slot_width + car_conf_width + nOptions * opt_width
solution_height = (nSlots + 1) * line_height

imwidth = 4*hor_pad + problem_width + solution_width
imheight = 2*vert_pad + max(problem_height, solution_height)
center_x = imwidth/2

# creating new Image object
img = Image.new("RGB", (imwidth, imheight), (255, 255,255))

# create rectangle image
draw = ImageDraw.Draw(img)

# draw line separating problem and solution
draw.line((center_x, 0, center_x, imheight), fill="black")
# get a font
myFont = ImageFont.truetype("arialbd.ttf", 20, )

# write "problem" and "solution"
problem_title_x = center_x/2
problem_title_y = vert_pad / 2
writeAt(problem_title_x, problem_title_y, "Problem", draw, myFont, "black")

sol_title_x = center_x + center_x/2
sol_title_y = vert_pad / 2
writeAt(sol_title_x, sol_title_y, "Solution", draw, myFont, "black")

# write the rectangle surrounding problem and solution
draw.rectangle((hor_pad, vert_pad, hor_pad+problem_width, vert_pad+problem_height), fill ="white", outline ="black")
draw.rectangle((center_x + hor_pad, vert_pad, center_x + hor_pad+solution_width, vert_pad+solution_height), fill ="white", outline ="black")

# color defs
header_gray = "#d9d9d9"
thi_blue = "#04599a"
config_cs = ["#04599a", "#0683e0", "#53b3fb", "#004200", "#006800", "#009900"]
font_cs = "#e4e8e4"
emph_cs ="#ffcc00"

# start with the problem header
problem_start_x, problem_start_y = hor_pad, vert_pad

def drawOptionHeader(start_x, start_y):
    for i in range(nOptions):
        start_opt_x, start_opt_y = start_x + i * opt_width, start_y
        end_opt_x, end_opt_y = start_opt_x + opt_width, start_opt_y + line_height
        draw.rectangle((start_opt_x, start_opt_y, end_opt_x, end_opt_y), fill=header_gray, outline="black")
        writeAt(start_opt_x + opt_width/2, start_opt_y + line_height/2, str(i+1), draw, myFont, "black")

drawOptionHeader(problem_start_x + car_conf_width, problem_start_y)
# write demand
start_demand_x, start_demand_y = problem_start_x + car_conf_width + nOptions*opt_width, problem_start_y,
end_demand_x, end_demand_y =  start_demand_x + demand_width, problem_start_y+line_height
draw.rectangle((start_demand_x, start_demand_y, end_demand_x, end_demand_y ), fill=thi_blue, outline="black")
writeAt(start_demand_x + demand_width/2, start_demand_y + line_height/2, "Demand", draw, myFont, "white")

def writtenRectangle(x, y, w, h, msg, fillc, fontc):
    draw.rectangle((x, y, x + w, y + h), fill=fillc, outline="black")
    writeAt(x + w / 2, y + h / 2, msg, draw, myFont, fontc)

def drawOptions(start_x, start_y, opts):
    for i in range(nOptions):
        start_opt_x, start_opt_y = start_x + i * opt_width, start_y
        end_opt_x, end_opt_y = start_opt_x + opt_width, start_opt_y + line_height
        fillc = emph_cs if opts[i] > 0 else "white"
        draw.rectangle((start_opt_x, start_opt_y, end_opt_x, end_opt_y), fill=fillc, outline="black")


# for all configs
for i in range(nCarConfigs):
    start_cc_x, start_cc_y = problem_start_x, problem_start_y + (i + 1) * line_height
    writtenRectangle(start_cc_x, start_cc_y,car_conf_width, line_height, f"Car config {i+1}", \
                     fillc = config_cs[i % len(config_cs)], fontc = font_cs)
    opts = requires[i]
    drawOptions(start_cc_x + car_conf_width, start_cc_y, opts)
    # draw demand
    writtenRectangle(start_cc_x + car_conf_width + nOptions * opt_width, start_cc_y, demand_width, line_height, \
                     str(demand[i]), fillc="white", fontc=config_cs[i % len(config_cs)])

# and the capacity line
def writeCapacityLine(start_cap_x, start_cap_y):
    writtenRectangle(start_cap_x, start_cap_y, car_conf_width, line_height, "Capacity", \
                     fillc=header_gray, fontc="black")
    for i in range(nOptions):
        start_opt_x, start_opt_y = start_cap_x + car_conf_width + i * opt_width, start_cap_y
        end_opt_x, end_opt_y = start_opt_x + opt_width, start_opt_y + line_height
        draw.rectangle((start_opt_x, start_opt_y, end_opt_x, end_opt_y), fill=header_gray, outline="black")
        writeAt(start_opt_x + opt_width / 2, start_opt_y + line_height / 2,\
                f"{at_most[i]}/{per_slots[i]}", draw, myFont, "black")

start_cap_x, start_cap_y = problem_start_x, problem_start_y + (nCarConfigs + 1) * line_height
writeCapacityLine(start_cap_x, start_cap_y)
# the sum of demands
writtenRectangle(start_cap_x + car_conf_width + nOptions * opt_width, start_cap_y, demand_width, line_height, \
                     str(nCars), fillc=thi_blue, fontc="white")

# now the solution header
sol_start_x, sol_start_y = center_x + hor_pad, vert_pad
writtenRectangle(sol_start_x, sol_start_y, slot_width, line_height, \
                     "Slots", fillc="white", fontc="BLACK")
writtenRectangle(sol_start_x + slot_width, sol_start_y, car_conf_width, line_height, \
                     "Car Config (line)", fillc="white", fontc="BLACK")
drawOptionHeader(sol_start_x + slot_width + car_conf_width, sol_start_y)

for i in range(nSlots):
    slot_start_x, slot_start_y = sol_start_x, sol_start_y + (i+1) * line_height
    writtenRectangle(slot_start_x, slot_start_y, slot_width, line_height, \
                     print_dates[i], fillc=thi_blue , fontc="white")

    # which config is placed in slot i?
    c_at_i = line[i]
    writtenRectangle(slot_start_x + slot_width, slot_start_y, car_conf_width, line_height, f"Car config {c_at_i}", \
                     fillc=config_cs[c_at_i % len(config_cs)], fontc=font_cs)
    opts = requires[c_at_i - 1 ]
    drawOptions(slot_start_x + slot_width + car_conf_width, slot_start_y, opts)

img.show()