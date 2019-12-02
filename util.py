
def readlines(filename, type=str):
    with open(filename) as f:
        lines = [type(line.rstrip('\n')) for line in f]
    return lines


def readline(filename, delim=",", type=str):
    return [[type(val) for val in line.split(delim)] for line in readlines(filename)]
