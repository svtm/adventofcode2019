from util import *

intcode = readline("inputs/9.txt", type=int)[0]

program_string = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
#program_string = "1102,34915192,34915192,7,4,7,99,0"
#intcode = map(int, program_string.split(","))

outp_func = lambda x: print(x)
inp_func = lambda: 2

program = list(intcode)

run_intcode_program(program, inp_func=inp_func, outp_func=outp_func, log_instructions=False)
