from util import *

def next_coords(dir, length, coords):
    start_x, start_y = coords[-1]
    if dir == 'R':
        return [(start_x + i, start_y) for i in range(1, length+1)]
    elif dir == 'D':
        return [(start_x, start_y - i) for i in range(1, length+1)]
    elif dir == 'L':
        return [(start_x - i, start_y) for i in range(1, length+1)]
    elif dir == 'U':
        return [(start_x, start_y + i) for i in range(1, length+1)]
    else:
        raise ValueError

wires = readline("inputs/3.txt")
w1, w2 = wires


w1_coords = [(0, 0)]
w2_coords = [(0, 0)]

closest_intersection_dist = float("inf")
intersect_step_sum = float("inf")

for stretch in w1:
    dir = stretch[0]
    length = int(stretch[1:])
    w1_coords += next_coords(dir, length, w1_coords)


for stretch in w2:
    dir = stretch[0]
    length = int(stretch[1:])
    n = next_coords(dir, length, w2_coords)
    for c in n:
        if c in w1_coords:
            w1_steps = w1_coords.index(c)
            w2_steps = len(w2_coords) + n.index(c)
            x, y = c
            manhattan = abs(x) + abs(y)
            print(f"Intersection at {c}, manhattan: {manhattan}, w1_steps: {w1_steps}, w2_steps: {w2_steps}")
            if manhattan < closest_intersection_dist:
                closest_intersection_dist = manhattan
            if w1_steps  + w2_steps < intersect_step_sum:
                intersect_step_sum = w1_steps + w2_steps
    w2_coords += n

print(f"Manhattan closest intersect: {closest_intersection_dist}, lowest steps intersect: {intersect_step_sum}")

