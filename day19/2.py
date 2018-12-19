#!/usr/bin/env python3

from primefac import primefac # You should use a python3 fork of primefac => https://github.com/elliptic-shiho/primefac-fork
from functools import reduce

def execute(instruction, registers):
    opcode = instruction[0]
    a = instruction[1]
    b = instruction[2]
    c = instruction[3]

    if opcode == "addr":
        registers[c] = registers[a]+registers[b]
    elif opcode == "addi":
        registers[c] = registers[a]+b
    elif opcode == "mulr":
        registers[c] = registers[a]*registers[b]
    elif opcode == "muli":
        registers[c] = registers[a]*b
    elif opcode == "banr":
        registers[c] = registers[a]&registers[b]
    elif opcode == "bani":
        registers[c] = registers[a]&b
    elif opcode == "borr":
        registers[c] = registers[a]|registers[b]
    elif opcode == "bori":
        registers[c] = registers[a]|b
    elif opcode == "setr":
        registers[c] = registers[a]
    elif opcode == "seti":
        registers[c] = a
    elif opcode == "gtir":
        registers[c] = 1 if a > registers[b] else 0
    elif opcode == "gtri":
        registers[c] = 1 if registers[a] > b else 0
    elif opcode == "gtrr":
        registers[c] = 1 if registers[a] > registers[b] else 0
    elif opcode == "eqir":
        registers[c] = 1 if a == registers[b] else 0
    elif opcode == "eqri":
        registers[c] = 1 if registers[a] == b else 0
    elif opcode == "eqrr":
        registers[c] = 1 if registers[a] == registers[b] else 0

registers = [0]*6
registers[0] = 1
instruction_pointer = None
program = [] # list of instructions, being 4-tuples: (opcode, a, b, c)
with open("input") as input_file:
    line = input_file.readline()
    while line:
        if line[0] == "#":
            instruction_pointer = int(line.replace("#ip ", ""))
        elif line != "\n":
            instruction = [v for v in line.replace("\n", "").split(" ")]
            instruction[1:] = [int(v) for v in instruction[1:]]
            program.append(tuple(instruction))
        line = input_file.readline()

# Input programs compute a sum of every factor of a goal number.

for _ in range(100): # We perform a few iterations just to be sure we have set our goal number
    line = program[registers[instruction_pointer]]
    execute(line, registers)
    registers[instruction_pointer]+= 1

goal_number = max(registers) # Our goal number is the highest value in registers (it's insanely big on part 2)
prime_factors = list(primefac(goal_number)) # We get the prime factors of our goal number

def compute_result(prime_factors, already_done):
    res = 0
    if not prime_factors in already_done:
        res = reduce(lambda a, b: a*b, prime_factors)
        already_done.append(prime_factors)
    if len(prime_factors) > 1:
        for i in range(len(prime_factors)):
            res+= compute_result(prime_factors[:i]+prime_factors[i+1:], already_done)
    
    return res

result = compute_result(prime_factors, [])+1 # We compute the sum of factors, and we don't forget to add +1 at the end (1 is a factor of our goal number)

print("Answer for puzzle #38: {}".format(result))
