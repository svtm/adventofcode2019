from util import *


def check_facts(num):
    has_adjacent = False
    for i in range(len(num) - 1):
        if num[i] == num[i+1]:
            try:
                has_adjacent = True if num[i+2] != num[i] else has_adjacent
            except:
                continue
        if not (num[i] <= num[i+1]):
            return False
    return has_adjacent


input_range = readlines("inputs/4.txt")[0]

start, end = map(int, input_range.split("-"))

matching = 0

bad = "111122"
check_facts(bad)

for i in range(start, end):
    if check_facts(str(i)):
        matching += 1

print(f"Part 1: {matching}")
