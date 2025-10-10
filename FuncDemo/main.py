#!/usr/bin/env -S uv run --script


from __future__ import annotations

import random
import turtle


def unique_colour(increment: int = 25):
    red = 0
    green = 0
    blue = 0
    while True:
        colour = (red, green, blue)
        red = red + increment
        if red >= 255:
            red = 0
            green += increment
        if green >= 255:
            green = 0
            blue += increment
        if blue >= 255:
            blue = 0
            red = 0
            green = 0
        yield colour


def random_pos_len(x_extent: int = 200, y_extent: int = 200, max_length: int = 50):
    """
    Generate a random x,y position with + / - extents (origin is 0,0) and length from 1-max_length.

    Args:
        x_extent (int) : the range in +/- x
        y_extent (int) : the range in +/- y
        max_length  (int)  : the range from 1 - max_length we are generating


    Returns:
        x,y,length : tuple of the random values
    """
    x = random.randint(-x_extent, x_extent)
    y = random.randint(-y_extent, y_extent)
    length = random.randint(1, max_length)
    return x, y, length


def move_to(current_turtle: "turtle.Turtle", x_pos: int, y_pos: int) -> None:
    """
    Function to move turtle to a new position pen is up for this so we don't draw on the canvas
    Parameters :
        x_pos (int) : position in x
        y_pos (int) : eposition in y
    """
    current_turtle.penup()
    current_turtle.goto(x_pos, y_pos)
    current_turtle.pendown()


def square(current_turtle, x_pos, y_pos, length):
    move_to(current_turtle, x_pos, y_pos)

    for _ in range(4):
        current_turtle.forward(length)
        current_turtle.right(90)


def triangle(current_turtle, x_pos, y_pos, length):
    move_to(current_turtle, x_pos, y_pos)
    for _ in range(3):
        current_turtle.forward(length)
        current_turtle.right(120)


drawing_functions = [square, triangle]


tl = turtle.Turtle()
tl.speed(0)
turtle.colormode(255)
colour = unique_colour()
for _ in range(2000):
    x, y, length = random_pos_len(max_length=500)
    r, g, b = next(colour)
    tl.pencolor(r, g, b)
    tl.fillcolor(r,g,b)
    tl.begin_fill()
    random.choice(drawing_functions)(tl, x, y, length)
    tl.end_fill()

# to draw we need, shape, x,y, length

# shapes = [("square", 100, 100, 50), ("tri", -100, -100, 50), ("tri", -10, -10, 150)]

# my_turtle = turtle.Turtle()

# my_turtle.shape("turtle")

# for shape in shapes:
#     if shape[0] == "tri":
#         triangle(my_turtle, shape[1], shape[2], shape[3])
#     elif shape[0] == "square":
#         square(my_turtle, shape[1], shape[2], shape[3])


turtle.done()
