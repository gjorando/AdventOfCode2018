#!/usr/bin/env python3

def execute(instruction, input_registers, instructions_set=None):
    if instructions_set is None:
        opcode = instruction[0]
    else:
        opcode = instructions_set[instruction[0]]
    a = instruction[1]
    b = instruction[2]
    c = instruction[3]

    registers = input_registers.copy()

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

    return registers

registers = [0]*6
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

while registers[instruction_pointer] in range(0, len(program)):
    line = program[registers[instruction_pointer]]
    registers = execute(line, registers)
    registers[instruction_pointer]+= 1

result = registers[0]

print("Answer for puzzle #37: {}".format(result))
