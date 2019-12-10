
def readlines(filename, type=str):
    with open(filename) as f:
        lines = [type(line.rstrip('\n')) for line in f]
    return lines


def readline(filename, delim=",", type=str):
    return [[type(val) for val in line.split(delim)] for line in readlines(filename)]


# --- Intcode Computer stuff --- #
# TODO: this could benefit from being a class, so we don't have to pass all the stuff around

def print_instruction(operation, immediate_string, operands):
    print(f"{'val_at ' + str(operands[0] if immediate_string[0] == '0' else operands[0])} {operation} {'val_at ' + str(operands[1] if immediate_string[1] == '0' else operands[1])} TO {operands[-1]}")


def write_memory(addr, val, memory):
    if addr >= len(memory):
        memory.extend([0] * (addr - len(memory) + 1))
    memory[addr] = val


def read_memory(addr, memory):
    if addr >= len(memory):
        memory.extend([0] * (addr - len(memory) + 1))
    return memory[addr]


def get_param(ip, param_num, relative_base, memory):
    mode = memory[ip] // (10 * 10 ** param_num)
    val = memory[ip + param_num]
    if mode % 10 == 0:
        return read_memory(val, memory)
    if mode % 10 == 1:
        return val
    if mode % 10 == 2:
        return read_memory(val + relative_base, memory)
    raise ValueError("Invalid mode")


def set_param(ip, param_num, relative_base, val, memory):
    mode = memory[ip] // (10 * 10 ** param_num)
    addr = memory[ip + param_num]
    if mode % 10 == 0:
        write_memory(addr, val, memory)
    elif mode % 10 == 2:
        write_memory(addr + relative_base, val, memory)
    else:
        raise ValueError("Invalid mode for memset")


def run_intcode_program(memory, inp_func=None, outp_func=None, log_instructions=False):
    ip = 0
    relative_base = 0
    while ip < len(memory):
        opcode = str(memory[ip])
        op_length = 0
        # Add
        if opcode[-1] == "1":
            op1 = get_param(ip, 1, relative_base, memory)
            op2 = get_param(ip, 2, relative_base, memory)
            set_param(ip, 3, relative_base, op1 + op2, memory)
            op_length = 4
        # Multiply
        elif opcode[-1] == "2":
            op1 = get_param(ip, 1, relative_base, memory)
            op2 = get_param(ip, 2, relative_base, memory)
            set_param(ip, 3, relative_base, op1 * op2, memory)
            op_length = 4
        # Input
        elif opcode[-1] == "3":
            if inp_func:
                inp = int(inp_func())
                set_param(ip, 1, relative_base, inp, memory)
            op_length = 2
        # Output
        elif opcode[-1] == "4":
            out_val = get_param(ip, 1, relative_base, memory)
            if outp_func:
                outp_func(out_val)
            op_length = 2
        # jump-non-zero
        elif opcode[-1] == '5':
            op = get_param(ip, 1, relative_base, memory)
            jmp_dest = get_param(ip, 2, relative_base, memory)
            if op != 0:
                ip = jmp_dest
                continue
            else:
                op_length = 3
        # jump-zero
        elif opcode[-1] == '6':
            op = get_param(ip, 1, relative_base, memory)
            jmp_dest = get_param(ip, 2, relative_base, memory)
            if op == 0:
                ip = jmp_dest
                continue
            else:
                op_length = 3
        # less-than
        elif opcode[-1] == '7':
            op1 = get_param(ip, 1, relative_base, memory)
            op2 = get_param(ip, 2, relative_base, memory)
            val = 1 if op1 < op2 else 0
            set_param(ip, 3, relative_base, val, memory)
            op_length = 4
        # equals
        elif opcode[-1] == '8':
            op1 = get_param(ip, 1, relative_base, memory)
            op2 = get_param(ip, 2, relative_base, memory)
            val = 1 if op1 == op2 else 0
            set_param(ip, 3, relative_base, val, memory)
            op_length = 4
        elif opcode[-2:] == "99":
            print(f"HALT")
            break
        # Set relative base
        elif opcode[-1] == "9":
            op = get_param(ip, 1, relative_base, memory)
            relative_base += op
            op_length = 2
        else:
            print(f"Unexpected opcode: {opcode}, HALTING")
            break

        if log_instructions:
            print(",".join([str(memory[i]) for i in range(ip, ip+op_length)]))
        ip += op_length

    return memory[0]
