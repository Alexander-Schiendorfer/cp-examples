

# importing image object from PIL
import math
from PIL import Image, ImageDraw, ImageFont

# first let's get the coordinates from MiniZinc

model_file = "scheduling.mzn"

import minizinc
import enum

from minizinc import Model, Status

model = Model(model_file)
solver = minizinc.Solver.lookup("gecode")

# jobs
jobs = enum.Enum("JOBS", ["A", "B", "C"])
lastT = 20
nTasks = 3;
dur = [ [5, 2, 3 ], [4, 5, 1], [ 3, 4, 2 ]]
nMachines = 3
taskToMach = [[1, 2, 3 ],[ 2, 1, 3],[ 2, 3, 1 ]]

inst = minizinc.Instance(solver, model)

inst["JOBS"] = jobs
inst["lastT"] = lastT
inst["nTasks"] = nTasks
inst["dur"] = dur
inst["taskToMach"] = taskToMach
inst["nMachines"] = nMachines
inst.add_string("constraint forall(j in JOBS where j != B) ( start[j,1] >= start[B,1] );")
inst.add_string("solve minimize makespan;")

result = inst.solve()


if result.status == Status.SATISFIED or result.status == Status.OPTIMAL_SOLUTION:
    print("sounds good")
    start_times = result["start"]
    end_times = result["end"]
    print(start_times)
    print(end_times)
    makespan = result["makespan"]

start_x, start_y = 30, 40
pixel_unit = 50
pixel_task_height = 100
vert_pad = 10

imwidth, imheight = lastT * pixel_unit + 2 * start_x, start_y + start_x + nMachines * (pixel_task_height + vert_pad)

# creating new Image object
img = Image.new("RGB", (imwidth, imheight), (255, 255,255))

# create rectangle image
img1 = ImageDraw.Draw(img)

# get a font
myFont = ImageFont.truetype("arialbd.ttf", 20, )

# draw makespan label
center_x, center_y = imwidth / 2, start_y / 2
msg =  f"Makespan: {makespan}"
w, h = img1.textsize(msg, font=myFont)
img1.text((center_x - w / 2, center_y - h / 2), msg, fill="black", font=myFont)

task_cs = ["#4bacc6", "#f79646", "#9bbb59"]
lane_cs = ["#a5d5e2", "#fbcaa2", "#cdddac"]
lane_border_cs = ["#357d91", "#b66d31", "#71893f"]

# draw three rectangles for machines
machine_upper_lefts = []
for i in range(nMachines):
    start_m_x, start_m_y = start_x, start_y + i * (pixel_task_height + vert_pad)
    end_m_x, end_m_y = start_m_x + lastT * pixel_unit, start_m_y + pixel_task_height
    machine_upper_lefts += [(start_m_x, start_m_y)]

    shape = [(start_m_x, start_m_y), (end_m_x, end_m_y)]
    img1.rectangle(shape, fill =lane_cs[i], outline =lane_border_cs[i])

# draw tasks for each job
inner_sep = 5
for i,j in enumerate(jobs):
    job_name = j.name
    for t in range(nTasks):
        on_machine = taskToMach[i][t] - 1
        start_m_x, start_m_y = machine_upper_lefts[on_machine]

        start_rect_x, start_rect_y = start_m_x + start_times[i][t] * pixel_unit, start_m_y + inner_sep
        end_rect_x, end_rect_y = start_m_x + end_times[i][t] * pixel_unit, start_m_y + pixel_task_height - inner_sep

        shape = [(start_rect_x, start_rect_y), (end_rect_x, end_rect_y)]
        img1.rectangle(shape, fill=task_cs[on_machine], outline=lane_border_cs[on_machine])

        # write a label there
        msg =  f"{job_name}{t+1}"
        text_w, text_h = img1.textsize(msg, font=myFont)
        center_x, center_y = (start_rect_x + end_rect_x) / 2, (start_rect_y + end_rect_y) / 2
        img1.text((center_x - text_w / 2, center_y - text_h / 2), msg, fill="white", font=myFont)

img.show()