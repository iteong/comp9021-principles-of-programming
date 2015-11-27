# Draws an octagram, the inscribed octagon being coloured yellow,
# and the colour of the triangles alternating red and blue.
#
# Written by Eric Martin for COMP9021

from turtle import *

small_edge_length = 100
long_edge_length = 180
angle = 45

def draw_triangle(i, colour):
    right((i + 0.5) * angle)
    forward(long_edge_length)
    pendown()
    color(colour)    
    begin_fill()
    goto(vertices[i])
    goto(vertices[i + 1])
    end_fill()
    penup()
    home()

vertices = []
penup()
for i in range(8):
    right(i * angle)
    forward(small_edge_length)
    vertices.append(pos())
    home()
vertices.append(vertices[0])

pendown()
color('yellow')
begin_fill()
for i in range(9):
    goto(vertices[i])
end_fill()
penup()
home()

for i in range(8):
    if i % 2:
        colour = 'red'
    else:
        colour = 'blue'
    draw_triangle(i, colour)

    
    

