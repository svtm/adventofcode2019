from util import *
import itertools


def output_func(val):
    global amp_output
    print(f"Output: {val}")
    amp_output = val

amp_output = 0
program = readline("inputs/7.txt", type=int)[0]

amp_inputs = [0, 1, 2, 3, 4]

biggest_thruster_input = 0
for phase_setting_sequence in itertools.permutations(amp_inputs):
    amp_output = 0
    for amp in range(5):
        memory = list(program)
        inputs = iter([phase_setting_sequence[amp], amp_output])
        inp_func = lambda inp=inputs: next(inp)
        run_intcode_program(memory, inp_func=inp_func, outp_func=output_func)
    if amp_output > biggest_thruster_input:
        biggest_thruster_input = amp_output

print(f"Part 1: {biggest_thruster_input}")




