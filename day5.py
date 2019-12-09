from util import *


intcode = readline("inputs/5.txt", type=int)[0]

outp_func = lambda x: print(f"Output: {x}")
inp_func = lambda: 5

run_intcode_program(intcode, inp_func=inp_func, outp_func=outp_func, log_instructions=True)

