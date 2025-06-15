
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