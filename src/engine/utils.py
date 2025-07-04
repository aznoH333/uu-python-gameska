
import math
import random


def signum(number):
    return (number >= 0) + (number > 0) - 1

def gravitate_number(number, target, speed):
    dist = target - number

    if abs(dist) < speed:
        return target
    return number + (speed * signum(dist))

def fade_color(color, ammount):
    return (color[0] * ammount, color[1] * ammount, color[2] * ammount)


def pick_random_color():
    return (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))

def interpolate(start, end, weight):
    return ((end - start) * weight) + start

def interpolate_color(color1, color2, w):
    return (
        interpolate(color1[0], color2[0], w),
        interpolate(color1[1], color2[1], w),
        interpolate(color1[2], color2[2], w),
    )

def box_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2

def clamp_value(value, min_value, max_value):
    return min(max(value, min_value), max_value)