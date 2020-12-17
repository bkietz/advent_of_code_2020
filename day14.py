import re

mem_re = re.compile(r'mem\[(\d+)\] = (\d+)')
mask_re = re.compile(r'mask = ([01X]+)')


class Mask:
    def __init__(self, line):
        line = line.strip()
        self.set = int(line.replace('X', '0'), base=2)
        self.clear = int(line.replace('X', '1'), base=2)
        self.floating = [
            2 ** i
            for i, ch in enumerate(reversed(line))
            if ch == 'X'
        ]
        self.is_floating = sum(self.floating)

    def __call__(self, value):
        value |= self.set
        value &= self.clear
        return value

    def float(self, value):
        value |= self.set
        value &= ~self.is_floating
        for bits in range(2**len(self.floating)):
            yield value | sum(
                bit for i, bit in
                enumerate(self.floating)
                if bits & 2**i)


for mask in [Mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')]:
    assert mask(11) == 73
    assert mask(101) == 101
    assert mask(0) == 64

for mask in [Mask('000000000000000000000000000000X1001X')]:
    assert list(mask.float(42)) == [26,27,58,59]

for mask in [Mask('00000000000000000000000000000000X0XX')]:
    assert list(mask.float(26)) == [*range(16,20),*range(24,28)]


def run(init):
    mem = {}
    mask = None

    for line in map(str.strip, init):
        if match := mask_re.match(line):
            mask = Mask(match.group(1))
            continue

        if match := mem_re.match(line):
            addr, value = map(int, match.groups())
            mem[addr] = mask(value)
            continue

    return mem


def test_run():
    mem = run('''\
        mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
        mem[8] = 11
        mem[7] = 101
        mem[8] = 0
        '''.split('\n'))
    assert mem == {7: 101, 8: 64}
    assert sum(mem.values()) == 165
test_run()


init = open('day14_input.txt').readlines()

print('part 1:', sum(run(init).values()))



def run2(init):
    mem = {}
    mask = None

    for line in map(str.strip, init):
        if match := mask_re.match(line):
            mask = Mask(match.group(1))
            continue

        if match := mem_re.match(line):
            addr, value = map(int, match.groups())
            for floated in mask.float(addr):
                mem[floated] = value
            continue

    return mem


def test_run2():
    mem = run2('''\
        mask = 000000000000000000000000000000X1001X
        mem[42] = 100
        mask = 00000000000000000000000000000000X0XX
        mem[26] = 1
        '''.split('\n'))
    assert sum(mem.values()) == 208

test_run2()

print('part 2:', sum(run2(init).values()))

