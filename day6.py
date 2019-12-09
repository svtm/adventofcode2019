from util import *
from pprint import pprint


def get_depths(graph, root, discovered=[], depth=0):
    discovered += [root]
    child_depths = depth
    for child in graph[root]["children"]:
        if child not in discovered:
            discovered += child
            child_depths += get_depths(graph, child, list(discovered), depth+1)
    return child_depths


def walk_path(graph, target):
    # Walk path
    current = target
    length = 0
    while graph[current]["path_parent"] is not None:
        print(current)
        length += 1
        current = graph[current]["path_parent"]
    return length - 2

def bfs(graph, start, target):
    # Build path
    queue = [start]
    visited = [start]
    while len(queue) > 0:
        current = queue.pop()
        if current == target:
            return walk_path(graph, target)
        parent = graph[current]["parent"]
        if parent is not None:
            if parent not in visited:
                visited.append(parent)
                graph[parent]["path_parent"] = current
                queue.append(parent)
        for child in graph[current]["children"]:
            if child is not None:
                if child not in visited:
                    visited.append(child)
                    graph[child]["path_parent"] = current
                    queue.append(child)


map = readlines("inputs/6.txt")


orbit_graph = {}
for orbit in map:
    parent, child = orbit.split(")")
    if parent not in orbit_graph:
        orbit_graph[parent] = {
            "children": [child],
            "parent": None,
            "path_parent": None
        }
    else:
        orbit_graph[parent]["children"].append(child)
    if child not in orbit_graph:
        orbit_graph[child] = {
            "children": [],
            "parent": parent,
            "path_parent": None
        }
    elif orbit_graph[child]["parent"] is None:
        orbit_graph[child]["parent"] = parent


pprint(orbit_graph)

print(get_depths(orbit_graph, "COM"))
print(bfs(orbit_graph, "YOU", "SAN"))
