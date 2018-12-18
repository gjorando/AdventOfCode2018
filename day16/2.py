#!/usr/bin/env python3

def execute(instruction, input_registers, instructions_set=None):
    if instructions_set is None:
        opcode = instruction[0]
    else:
        opcode = instructions_set[instruction[0]]
    a = instruction[1]
    b = instruction[2]
    c = instruction[3]

    registers = list(input_registers)

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

    return tuple(registers)

test_instructions = [] # list of lists of 3 4-tuples: [(u0, u1, u2, u3), (opcode, a, b, c), (u0', u1', u2', u3')]
program = [] # list of instructions, being 4-tuples: (opcode, a, b, c)
with open("input") as input_file:
    line = input_file.readline()
    while line:
        if line[0] == "B":
            before = tuple([int(v) for v in line.replace("\n", "").split(": ")[1].replace("[", "").replace("]", "").split(",")])
            instruction = tuple([int(v) for v in input_file.readline().replace("\n", "").split(" ")])
            after = tuple([int(v) for v in input_file.readline().replace("\n", "").split(": ")[1].replace("[", "").replace("]", "").split(",")])
            test_instructions.append([before, instruction, after])
            input_file.readline()
        elif line != "\n":
            program.append(tuple([int(v) for v in line.replace("\n", "").split(" ")]))
        line = input_file.readline()

opcodes = ("addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr")
instructions = [list(opcodes)]*len(opcodes)

while sum([len(i) for i in instructions]) != len(opcodes):
    found_opcodes = [i[0] for i in instructions if len(i) == 1]
    for input_registers, instruction, expected_output in test_instructions:
        opcode_id = instruction[0]

        if len(instructions[opcode_id]) == 1:
            continue

        possible_instructions = []
        for tested_opcode in opcodes:
            if tested_opcode in found_opcodes:
                continue
            output = execute((tested_opcode, instruction[1], instruction[2], instruction[3]), input_registers)
            if output == expected_output:
                possible_instructions.append(tested_opcode)

        instructions[opcode_id] = [opc for opc in instructions[opcode_id] if opc in possible_instructions]

instructions_set = [i[0] for i in instructions]

registers = [0]*4

for line in program:
    registers = execute(line, registers, instructions_set)

result = registers[0]

print("Answer for puzzle #32: {}".format(result))
