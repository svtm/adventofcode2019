
def readlines(filename, type=str):
    with open(filename) as f:
        lines = [type(line.rstrip('\n')) for line in f]
    return lines
