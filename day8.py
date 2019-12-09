from util import *
from PIL import Image


def parse_layers(encoded, width, height):
    if len(encoded) % (width * height) != 0:
        raise ValueError("Dimensions do not match length of encoding")

    layers = [encoded[i:i+width*height] for i in range(0, len(encoded), width*height)]
    return layers


def layer_rows(layer, width):
    return [layer[i:i+width] for i in range(0, len(layer), width)]


encoded = readlines("inputs/8.txt")[0]

width = 25
height = 6

layers = parse_layers(encoded, width, height)

zero_counts = list(map(lambda l: l.count('0'), layers))
part1_layer = layers[zero_counts.index(min(zero_counts))]
print(f"Part 1: {part1_layer.count('1') * part1_layer.count('2')}")

layers = [layer_rows(layer, width) for layer in layers]
print(layers)

colors = {
    "0": (0, 0, 0),
    "1": (255, 255, 255),
    "2": (255, 0, 0)
}

img = Image.new('RGB', (width, height), "red")
pixels = img.load()
for y in range(height):
    for x in range(width):
        for layer in layers:
            if layer[y][x] != "2":
                pixels[x, y] = colors[layer[y][x]]
                break


img.show()
