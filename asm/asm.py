#!env python
# Created:20080312
# By Jeff Connelly
#
# 3-trit computer assembler

import sys, os

def main():
    if len(sys.argv) < 2:
        print """usage: %s program.t 
input file: program.t - assembly code
outputs: 
\tprogram.3 - assembled tritstream
\tprogram.sp - SPICE file suitable for use with swrom-fast
""" % (sys.argv[0])

        raise SystemExit

    asmfile = file(sys.argv[1], "rt")
    tritstream_filename = sys.argv[1].replace(".t", ".3")
    tritstream_file = file(tritstream_filename, "wt")
    spice_filename = sys.argv[1].replace(".t", ".sp")
    spice_file = file(spice_filename, "wt")

    tritstream = assemble(asmfile)
    tritstream_file.write(tritstream)

def assemble(asmfile):
    pc = -1
    labels = {}
    opcode_map = { "lwi": [0], "cmp": [-1], "be": [1] }
    register_map = { "in": [-1], "out": [0], "a": [1] }
    # TODO: balanced trinary conversion routines
    literal_map = { 
            "4": [1, 1],
            "3": [1, 0],
            "2": [1, -1],
            "1": [0, 1],
            "0": [0, 0],
            "-1": [0, -1],
            "-2": [-1, 1],
            "-3": [-1, 0],
            "-4": [-1, -1]
            }



    tritstream = []
    while True:
        line = asmfile.readline()
        # End on EOF
        if len(line) == 0:
            break

        # Skip blank lines
        line = line.strip()
        if len(line) == 0:
            continue

        label, opcode, operands = parse_line(line)
        #print [label, opcode, operands]
        machine_code = []

        if label is not None:
            labels[label] = [pc]

        machine_code.extend(opcode_map[opcode])
        for op in operands:
            x = register_map.get(op,
                    labels.get(op,
                        literal_map.get(op)))
            if x is None:
                print "Bad register, label, or literal: %s" % (op, )
                raise SystemExit
            else:
                machine_code.extend(x)
    
        #print machine_code
        tritstream.extend(machine_code)
        pc += 1

    #print labels

    # Serialize tritstream
    s = ""
    for t in tritstream:
        if t == -1:
            s += "i"
        else:
            s += str(t)

    return s

def parse_line(line):
    # Strip comments
    without_comment = line.split(";", 1)[0]

    # Separate label from instruction
    label_and_instruction = without_comment.split(":", 1)
    if len(label_and_instruction) > 1:
        label, instruction = label_and_instruction
        label = label.strip()
    else:
        instruction, = label_and_instruction
        label = None

    instruction = instruction.strip()

    # Separate opcode from operands
    tokens = instruction.split()
    opcode = tokens[0]
    operands = []
    for token in tokens[1:]:
        token = token.replace(",", "")
        operands.append(token)

    return (label, opcode, operands)

if __name__ == "__main__":
    main()
