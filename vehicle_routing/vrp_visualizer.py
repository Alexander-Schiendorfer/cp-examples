import math
from PIL import Image, ImageDraw, ImageFont


locations = { "HQ": (840, 539), "Edeka": (418, 783), "Burger King" : (808, 234), "Audi Forum" : (532, 166), "Klinikum" : (327, 273)}
tour = ["HQ", "Edeka", "Burger King", "Audi Forum", "Klinikum"]
colors = [(0, 90, 155, 255), (240,130,0,255), (150,190,0,255) ]

def circle_at(draw, x, y, r, color):
    left_up_point = (x - r, y - r)
    right_down_point = (x + r, y + r)
    two_point_list = [left_up_point, right_down_point]
    draw.ellipse(two_point_list, fill=color)

def text_at(draw, x, y, text, myFont, color="white"):
    w, h = draw.textsize(text, font=myFont)
    #center_x, center_y = (draw_start_x + draw_end_x) / 2, (draw_start_y + draw_end_y) / 2
    draw.text((x - w / 2, y - h / 2), text, fill=color, font=myFont)

def draw_tour(img, draw, locations, tour, tour_length=0, color_index = 0):
    # get a font
    myFont = ImageFont.truetype("arialbd.ttf", 24, )
    color = colors[color_index]

    # draw the lines first for the sake of ordering
    for i, city in enumerate(tour):
        from_city = locations[city]
        to_city = locations[tour[(i + 1) % len(tour)]]

        draw.line((from_city[0], from_city[1], to_city[0], to_city[1]), fill=color, width=4)

    for i, city in enumerate(tour):
        x,y = locations[city]
        circle_at(draw, x, y, 20, color)
        text_at(draw, x, y, str(i + 1), myFont)

    # print the tour length
    text_at(draw, img.width//2, 30 * (color_index+1), f"Tour duration: {tour_length} minutes", myFont, color)

def draw_arrival_times(img, draw, locations, tour_arrival_times, color_index=0):

    myFont = ImageFont.truetype("arialbd.ttf", 24, )
    for city, time in tour_arrival_times:
        x, y = locations[city]
        text_at(draw, x+60, y-10, str(time), myFont, color=colors[color_index])

def draw_map():
    # creating new Image object
    with Image.open("map.png") as img, Image.open("thi_aimotion.png") as logo, Image.open("buechl.jpg") as buechl:
        img = img.convert("RGBA")
        # create rectangle image
        draw = ImageDraw.Draw(img)
        # convert to transparent
        logo = logo.convert("RGBA")
        buechl = buechl.convert("RGBA")
        logo = logo.resize((logo.width // 12, logo.height // 12), Image.ANTIALIAS)
        # place logo
        logo_x = img.width - logo.width
        logo_y = logo.height // 2
        img.paste(logo, (logo_x, logo_y), logo)

        # buechl_loc
        buechl_loc = (840, 579)
        img.paste(buechl, buechl_loc, buechl)
    return img, draw


if __name__ == "__main__":
    img, draw = draw_map()
    draw_tour(img, draw, locations, tour, color_index=1)
    img.show()



