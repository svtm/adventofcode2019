
def readlines(filename, type=str):
    with open(filename) as f:
        lines = [type(line.rstrip('\n')) for line in f]
    return lines


def readline(filename, delim=",", type=str):
    return [[type(val) for val in line.split(delim)] for line in readlines(filename)]


def print_instruction(operation, immediate_string, operands):
    print(f"{'val_at ' + str(operands[0] if immediate_string[0] == '0' else operands[0])} {operation} {'val_at ' + str(operands[1] if immediate_string[1] == '0' else operands[1])} TO {operands[-1]}")


def get_immediate_string(opcode, n):
    return opcode[:-2].rjust(n, "0")[::-1]


def run_intcode_program(memory, inp_func=None, outp_func=None, log_instructions=False):
    ip = 0
    instructions = []
    while ip < len(memory):
        opcode = str(memory[ip])
        # Add
        if opcode[-1] == "1":
            immediate_string = get_immediate_string(opcode, 2)
            print_instruction("+", immediate_string, memory[ip+1:ip+4])
            op1 = memory[ip + 1] if immediate_string[0] == "1" else memory[memory[ip + 1]]
            op2 = memory[ip + 2] if immediate_string[1] == "1" else memory[memory[ip + 2]]
            dest = memory[ip + 3]
            memory[dest] = op1 + op2

            if log_instructions:
                instructions.append(",".join([str(memory[i]) for i in range(ip, ip+4)]))
            ip += 4
        # Multiply
        elif opcode[-1] == "2":
            immediate_string = get_immediate_string(opcode, 2)
            print_instruction("*", immediate_string, memory[ip+1:ip+4])
            op1 = memory[ip + 1] if immediate_string[0] == "1" else memory[memory[ip + 1]]
            op2 = memory[ip + 2] if immediate_string[1] == "1" else memory[memory[ip + 2]]
            dest = memory[ip + 3]
            memory[dest] = op1 * op2

            if log_instructions:
                instructions.append(",".join([str(memory[i]) for i in range(ip, ip+4)]))
            ip += 4
        # Input
        elif opcode[-1] == "3":
            dest_addr = memory[ip + 1]
            if inp_func:
                inp = int(inp_func())
                memory[dest_addr] = inp

            if log_instructions:
                instructions.append(",".join([str(memory[i]) for i in range(ip, ip+2)]))
            ip += 2
        # Output
        elif opcode[-1] == "4":
            immediate_string = get_immediate_string(opcode, 1)
            out_val = memory[ip + 1] if immediate_string[0] == "1" else memory[memory[ip + 1]]
            if outp_func:
                outp_func(out_val)

            if log_instructions:
                instructions.append(",".join([str(memory[i]) for i in range(ip, ip+2)]))
            ip += 2
        # jump-non-zero
        elif opcode[-1] == '5':
            immediate_string = get_immediate_string(opcode, 2)
            operand = memory[ip + 1] if immediate_string[0] == '1' else memory[memory[ip + 1]]
            jmp_dest = memory[ip + 2] if immediate_string[1] == '1' else memory[memory[ip + 2]]

            if operand != 0:
                ip = jmp_dest
            else:
                ip += 3
        # jump-zero
        elif opcode[-1] == '6':
            immediate_string = get_immediate_string(opcode, 2)
            operand = memory[ip + 1] if immediate_string[0] == '1' else memory[memory[ip + 1]]
            jmp_dest = memory[ip + 2] if immediate_string[1] == '1' else memory[memory[ip + 2]]

            if operand == 0:
                ip = jmp_dest
            else:
                ip += 3
        # less-than
        elif opcode[-1] == '7':
            immediate_string = get_immediate_string(opcode, 2)
            print_instruction("<", immediate_string, memory[ip+1:ip+4])
            op1 = memory[ip + 1] if immediate_string[0] == "1" else memory[memory[ip + 1]]
            op2 = memory[ip + 2] if immediate_string[1] == "1" else memory[memory[ip + 2]]
            dest = memory[ip + 3]
            memory[dest] = 1 if op1 < op2 else 0

            if log_instructions:
                instructions.append(",".join([str(memory[i]) for i in range(ip, ip+4)]))
            ip += 4
        # equals
        elif opcode[-1] == '8':
            immediate_string = get_immediate_string(opcode, 2)
            print_instruction("==", immediate_string, memory[ip+1:ip+4])
            op1 = memory[ip + 1] if immediate_string[0] == "1" else memory[memory[ip + 1]]
            op2 = memory[ip + 2] if immediate_string[1] == "1" else memory[memory[ip + 2]]
            dest = memory[ip + 3]
            memory[dest] = 1 if op1 == op2 else 0

            if log_instructions:
                instructions.append(",".join([str(memory[i]) for i in range(ip, ip+4)]))
            ip += 4
        elif opcode[-2:] == "99":
            print(f"HALT")
            break
        else:
            print(f"Unexpected opcode: {opcode}, HALTING")
            break

    return memory[0]
