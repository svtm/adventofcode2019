from util import *
import math


def calc_fuel(mass):
    return math.floor(mass / 3) - 2

def calc_additional_fuel(mass):
    fuel = calc_fuel(mass)
    if fuel <= 0:
        return 0
    else:
        return fuel + calc_additional_fuel(fuel)

modules = readlines("inputs/1.txt", int)

# Part 1
fuel_req = sum(map(calc_fuel, modules))
print(f"Sum fuel requirements: {fuel_req}")


# Part 2
total_fuel = sum(map(calc_additional_fuel, modules))
print(f"Part 2: {total_fuel}")

