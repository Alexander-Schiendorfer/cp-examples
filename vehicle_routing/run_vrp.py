

# importing image object from PIL
import math
from PIL import Image, ImageDraw, ImageFont

# first let's get the coordinates from MiniZinc

model_file = "vehicle_routing_core.mzn"

import minizinc
from minizinc import Model, Status
import vrp_visualizer
from datetime import timedelta
import datetime

def convert_next_to_tour(next):
    # example: next = [2, 1, 3, 4, 5]
    next = [i - 1 for i in next]
    # now: next = [1, 0, 2, 3, 4]

    next_index = 0
    tour = []
    while next_index != 0 or tour == []:
        print(next_index)
        tour.append(next_index)
        next_index = next[next_index]

    return [t+1 for t in tour]

def time_plus(time, td):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + td
    return end.time()

if __name__ == "__main__":
    #print(convert_next_to_tour([2, 1, 3, 4, 5]))
    #print(convert_next_to_tour([3, 2, 4, 5, 1]))
    start_time = datetime.time(7)

    tsp_model = Model(model_file)
    tsp_model.add_file("data/1.dzn")
    # data for now fixed
    loc_names =  ["HQ", "Edeka", "Burger King", "Audi Forum", "Klinikum"]
    solver = minizinc.Solver.lookup("chuffed")

    inst = minizinc.Instance(solver, tsp_model)

    # Burger King only after 07:15
    #inst.add_string("constraint arrivalTime[2] > 15;")

    result = inst.solve()
    if result.status == Status.SATISFIED or result.status == Status.OPTIMAL_SOLUTION:
        print("sounds good")
        next_matrix = result["next"]
        for next in next_matrix:
            print(next)
        # contains a "next" vector for every vehicle

        arrival_time = result["arrivalTime"] #
        latest_arrival = result["latest_arrival"]

        locations = vrp_visualizer.locations

        img, draw = vrp_visualizer.draw_map()
        for v, next in enumerate(next_matrix): # all vehicles
            tour = convert_next_to_tour(next)
            arrival_times_tour = [arrival_time[t-1] for t in tour]

            arrival_times_tour_str = [time_plus(start_time, timedelta(minutes=t)).strftime('%H:%M') for t in arrival_times_tour]
            # convert to names for visualizers
            tour = [loc_names[t-1] for t in tour]
            vrp_visualizer.draw_tour(img, draw, locations, tour, tour_length=latest_arrival[v], color_index=v)
            vrp_visualizer.draw_arrival_times(img, draw, locations, zip(tour, arrival_times_tour_str), color_index=v)
        img.show()





