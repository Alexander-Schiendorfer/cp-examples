

# importing image object from PIL
import math
from PIL import Image, ImageDraw, ImageFont

# first let's get the coordinates from MiniZinc

model_file = "tsp.mzn"

import minizinc
from minizinc import Model, Status
import tsp_visualizer

if __name__ == "__main__":

    tsp_model = Model(model_file)
    tsp_model.add_file("tsp_2.dzn")
    solver = minizinc.Solver.lookup("chuffed")

    inst = minizinc.Instance(solver, tsp_model)
    #inst["n"] = n
    #inst["widths"] = widths
    #inst["heights"] = heights
    result = inst.solve()
    tour = result["tour"]
    if result.status == Status.SATISFIED or result.status == Status.OPTIMAL_SOLUTION:
        print("sounds good")
        loc_names = result["loc_names"]

        tour = result["tour"]
        tour_length = result["tour_length"]
        tour = [loc_names[t-1] for t in tour]
        locations = tsp_visualizer.locations
        tsp_visualizer.draw_map(locations, tour, tour_length)





