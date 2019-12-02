from util import *
import itertools


def get_operands(opcode_idx, code):
    first_loc = code[opcode_idx + 1]
    second_loc = code[opcode_idx + 2]
    dest_addr = code[opcode_idx + 3]
    return code[first_loc], code[second_loc], dest_addr


def init_noun_verb(noun, verb, code):
    program = list(code)
    program[1] = noun
    program[2] = verb
    return program


def run_program(memory):
    ip = 0
    while ip < len(memory):
        opcode = memory[ip]
        if opcode == 1:
            op1, op2, dest = get_operands(ip, memory)
            memory[dest] = op1 + op2
        elif opcode == 2:
            op1, op2, dest = get_operands(ip, memory)
            memory[dest] = op1 * op2
        elif opcode == 99:
            print(f"HALT")
            break
        else:
            print(f"Unexpected opcode: {opcode}, HALTING")
            break
        ip += 4

    return memory[0]


intcode = readline("inputs/2.txt", type=int)[0]

# Part 1:
part1_program = init_noun_verb(12, 2, intcode)
part1_output = run_program(part1_program)
print(f"Part 1: {part1_output}")


# Part 2
target_output = 19690720
combinations = itertools.product(range(0, 100), repeat=2)
for noun, verb in combinations:
    print(f"{noun}, {verb}")
    program = init_noun_verb(noun, verb, intcode)
    output = run_program(program)
    if output == target_output:
        print(f"Part 2: {100 * noun + verb}")
        break
