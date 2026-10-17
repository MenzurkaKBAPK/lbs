class VirtualMachine:

    IFETCH, ISTORE, IPUSH, IPOP, IADD, ISUB, ILT, JZ,\
        JNZ, JMP, HALT, IEQUAL, IMT, IMULT, IDIV, IPOW = range(16)

    def run(self, program):
        var = [None for i in range(26)]
        stack = []
        pc = 0
        while True:
            op = program[pc]
            if pc < len(program) - 1:
                arg = program[pc + 1]

            if op == VirtualMachine.IFETCH:
                stack.append(var[arg] if not var[arg] is None else 0)
                pc += 2
            elif op == VirtualMachine.ISTORE:
                var[arg] = stack.pop()
                pc += 2
            elif op == VirtualMachine.IPUSH:
                stack.append(arg)
                pc += 2
            elif op == VirtualMachine.IPOP:
                stack.append(var[arg])
                stack.pop()
                pc += 1
            elif op == VirtualMachine.IADD:
                stack[-2] += stack[-1]
                stack.pop()
                pc += 1
            elif op == VirtualMachine.ISUB:
                stack[-2] -= stack[-1]
                stack.pop()
                pc += 1
            elif op == VirtualMachine.IMULT:
                stack[-2] *= stack[-1]
                stack.pop()
                pc += 1
            elif op == VirtualMachine.IDIV:
                stack[-2] /= stack[-1]
                stack.pop()
                pc += 1
            elif op == VirtualMachine.IPOW:
                stack[-2] **= stack[-1]
                stack.pop()
                pc += 1
            elif op == VirtualMachine.ILT:
                if stack[-2] < stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == VirtualMachine.IEQUAL:
                if stack[-2] == stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == VirtualMachine.IMT:
                if stack[-2] > stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == VirtualMachine.JZ:
                if stack.pop() == 0:
                    pc = arg
                else:
                    pc += 2
            elif op == VirtualMachine.JNZ:
                if stack.pop() != 0:
                    pc = arg
                else:
                    pc += 2
            elif op == VirtualMachine.JMP:
                pc = arg
            elif op == VirtualMachine.HALT:
                break

        print('Execution finished.')

        variables = []
        for i in range(26):
            if var[i]:
                variables.append('%c = %d' % (chr(i + ord('a')), var[i]))
        return variables
