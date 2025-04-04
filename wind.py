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
pdf.add_page("A5")
pdf.set_font("Times", style="B", size=6)
pastel_colours = [
    (255, 179, 186),  # Pastel Red
    (255, 223, 186),  # Pastel Orange
    (255, 255, 186),  # Pastel Yellow
    (186, 255, 201),  # Pastel Spring Green
    (186, 255, 230),  # Pastel Green
    (186, 225, 255),  # Pastel Cyan
    (186, 186, 255),  # Pastel Blue
    (216, 186, 255),  # Pastel Purple
    (255, 186, 246)   # Pastel Pink
]
darker_pastel = [ ]
for p in pastel_colours:
    (r,g,b) = p
    darker_pastel.append( (r-30,g-30,b-30) )

def set_fill_colour(tbl, val):
    """ tbl is table, val is -4 .. 4 """
    color = tbl[val+4]
    pdf.set_fill_color(color[0], color[1], color[2])

ANGLE_STEP=15
rows = int(360/ANGLE_STEP)
cols = int(360/ANGLE_STEP)+1

page_width = 210/2
margin = 2
table_width = page_width - 2*margin
cell_width = (table_width / cols) + 1
cell_height = 6

x_start = margin
y_start = 10

pdf.set_fill_color(200, 200,200)
pdf.set_x(x_start)
pdf.set_y(y_start)

QUANT =4
INVQUANT = 25

yloc = y_start
for wind_angle in range(0,360,ANGLE_STEP):
    yloc += cell_height
    pdf.set_y(yloc)

    if (wind_angle/ANGLE_STEP)%6 == 0:
        pdf.set_fill_color(200, 200,200)
        pdf.text(x_start+3, yloc+(cell_height/2), "Track >")
        pdf.text(x_start+3, yloc+(cell_height/2)+2, " v Wind")
        pdf.set_x(x_start + cell_width + 8)
        for j in range(cols-1):
            a2 = j*ANGLE_STEP
            pdf.cell(cell_width, cell_height, f"{a2}", border=1, fill=True, align='C')
        yloc += cell_height
    pdf.set_x(x_start)
    pdf.set_y(yloc)

    # print(wind_angle)
    # x , t
    prev = (None, None)
    width = 0
    pdf.set_fill_color(200,200,200)
    pdf.cell(cell_width, cell_height, f"{wind_angle}", border=1, fill=True, align='C')
    for track in range(0,360,ANGLE_STEP):

        wind_to_track = wind_angle - track
        crosswind = math.sin(math.radians(wind_to_track))
        headwind = math.cos(math.radians(wind_to_track))
        x_quant = int(crosswind*QUANT)
        y_quant = int(headwind*QUANT)
        if x_quant < 0:
            xdir = "-"
        elif x_quant > 0:
            xdir = "+"
        else:
            xdir = ""
        if y_quant < 0:
            ydir = "T"
        elif y_quant == 0:
            ydir = ""
        else:
            ydir = "H"
        now = (abs(x_quant), abs(y_quant))
        width += cell_width
        if now != prev or track==345:
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()
            set_fill_colour(pastel_colours, x_quant)
            pdf.cell(width, cell_height/2, f"{xdir}{now[0]*INVQUANT}", border="TLR", fill=True, align='C')
            pdf.set_y(y_pos + cell_height/2)
            pdf.set_x(x_pos)
            #set_fill_colour(darker_pastel, y_quant)
            pdf.cell(width, cell_height/2, f"{now[1]*INVQUANT}{ydir}", border="BLR", fill=True, align='C')
            pdf.set_y(y_pos)
            pdf.set_x(x_pos + width)
            prev = now
            width = 0


print(f"Saving PDF to {output_file}")
pdf.output(output_file)
