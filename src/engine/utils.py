
import math


def signum(number):
    return (number >= 0) + (number > 0) - 1

def gravitate_number(number, target, speed):
    dist = target - number

    if abs(dist) < speed:
        return target
    return number + (speed * signum(dist))

def fade_color(color, ammount):
    return (color[0] * ammount, color[1] * ammount, color[2] * ammount)