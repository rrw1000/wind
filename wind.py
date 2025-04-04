#! /usr/bin/env python3

"""
Richard's amazing crosswind calculator
"""

import math
from fpdf import FPDF
import random
import sys

# Should really use argparse, but ..
output_file = sys.argv[1]

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=6)
pastel_colors = [
        (255, 209, 220),  # Pink
        (209, 231, 255),  # Blue
        (220, 255, 209),  # Green
        (255, 236, 209),  # Orange
        (230, 209, 255),  # Purple
        (255, 253, 209),  # Yellow
    ]




ANGLE_STEP=15
rows = int(360/ANGLE_STEP)
cols = int(360/ANGLE_STEP)+1

page_width = 210
margin = 10
table_width = page_width - 2*margin
cell_width = table_width / cols
cell_height = 8

x_start = margin
y_start = 20

pdf.set_fill_color(200, 200,200)
pdf.set_x(x_start)
pdf.set_y(y_start)

QUANT =4
INVQUANT = 25

pdf.set_x(x_start)
pdf.text(x_start, y_start-1, "-> Track")
pdf.set_x(x_start+cell_width)
for j in range(cols-1):
    wind_angle = j*ANGLE_STEP
    pdf.cell(cell_width, cell_height, f"{wind_angle}", border=1, fill=True, align='C')


i = 0
for wind_angle in range(0,360,ANGLE_STEP):
    pdf.set_x(x_start)
    y_loc = y_start + (i+1)*cell_height
    pdf.set_y(y_loc)
    i += 1
    print(wind_angle)
    # x , t
    prev = (None, None)
    width = 0
    pdf.set_fill_color(200,200,200)
    pdf.cell(cell_width, cell_height, f"{wind_angle}", border=1, fill=True, align='C')
    for track in range(0,360,ANGLE_STEP):
        color = random.choice(pastel_colors)
        pdf.set_fill_color(color[0], color[1], color[2])

        wind_to_track = wind_angle - track
        crosswind = abs(math.sin(math.radians(wind_to_track)))
        if crosswind < 0.1:
            xdir = ""
        elif (wind_angle < track):
            xdir = "-"
        else:
            xdir = "+"
        headwind = math.cos(math.radians(wind_to_track))
        if headwind < 0:
            ydir = "T"
        else:
            ydir = "H"
        now = (int(crosswind*QUANT), int(abs(headwind)*QUANT))
        width += cell_width
        if now != prev or track==345:
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()
            pdf.cell(width, cell_height/2, f"{xdir}{now[0]*INVQUANT}", border=1, fill=True, align='C')
            pdf.set_y(y_pos + cell_height/2)
            pdf.set_x(x_pos)
            pdf.cell(width, cell_height/2, f"{now[1]*INVQUANT}{ydir}", border=1, fill=True, align='C')
            pdf.set_y(y_pos)
            pdf.set_x(x_pos + width)
            prev = now
            width = 0


print(f"Saving PDF to {output_file}")
pdf.output(output_file)
