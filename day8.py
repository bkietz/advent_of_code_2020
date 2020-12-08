class Boot:
    def __init__(self, instructions):
        self.acc = 0
        self.i = 0
        self.instructions = list(instructions)

    def reset(self, i=0, acc=0):
        self.acc = acc
        self.i = i

    def exec_one(self):
        op, arg = self.instructions[self.i]
        if op == 'jmp':
            self.i += arg
        else:
            self.i += 1
        if op == 'acc':
            self.acc += arg

    def exec(self):
        exec_once = set()
        while True:
            if self.i in exec_once:
                return 'looping'
            if self.i == len(self.instructions):
                return 'booted'
            exec_once.add(self.i)
            self.exec_one()

    def uncorrupt(self):
        flipped = {'jmp': 'nop', 'nop': 'jmp', 'acc': 'acc'}
        self.reset()
        while True:
            i = self.i
            acc = self.acc

            op, arg = self.instructions[i]
            self.instructions[i] = (flipped[op], arg)

            if self.exec() == 'booted':
                break

            self.instructions[i] = (op, arg)
            self.reset(i, acc)
            self.exec_one()


def parse_instruction(line):
    op, arg = line.strip().split()
    return op, int(arg)


def test_Boot():
    boot = Boot(parse_instruction(l) for l in '''\
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6'''.split('\n'))

    status = boot.exec()
    assert status == 'looping'
    assert boot.acc == 5

    boot.instructions[-2] = ('nop', -4)
    boot.reset()
    status = boot.exec()
    assert status == 'booted'
    assert boot.acc == 8

    boot.instructions[-2] = ('jmp', -4)
    boot.uncorrupt()
    assert boot.instructions[-2] == ('nop', -4)


#test_Boot()

boot = Boot(parse_instruction(l)
            for l in open('day8_input.txt').readlines()
            if l != '\n')


boot.exec()
print('part 1:', boot.acc)


boot.uncorrupt()
print('part 2:', boot.acc)
