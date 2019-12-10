from util import *

program_string = "104,1125899906842624,99"

program = list(map(int, program_string.split(",")))

outp_func = lambda x: print(x)

run_intcode_program(program, outp_func=outp_func, log_instructions=True)
