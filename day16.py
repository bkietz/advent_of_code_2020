import numpy as np
import io


class Range:
    def __init__(self, line):
        self.min, self.max = map(int, line.split('-'))

    def validate(self, vals):
        return (self.min <= vals) & (vals <= self.max)


class BiRange:
    def __init__(self, line):
        self.name, line = line.split(': ')
        self.lo, self.hi = map(Range, line.split(' or '))

    def validate(self, vals):
        return self.lo.validate(vals) | self.hi.validate(vals)


ranges, mine, nearby = open('day16_input.txt').read().split('\n\n')

ranges = list(map(BiRange, ranges.splitlines()))

mine = list(map(int, mine.splitlines()[1].split(',')))

_, nearby = nearby.split('\n', maxsplit=1)
nearby = np.loadtxt(io.StringIO(nearby), delimiter=',', dtype=int)


not_in_any_range = np.ones(nearby.shape, dtype=bool)
for r in ranges:
    not_in_any_range &= ~r.validate(nearby)

print('part 1:', np.where(not_in_any_range, nearby, 0).sum())


invalid_tickets = np.zeros(nearby.shape[0], dtype=bool)
for i in range(not_in_any_range.shape[1]):
    invalid_tickets |= not_in_any_range[:, i]


nearby = nearby[~invalid_tickets]
possibles = {r.name: set() for r in ranges}
for r in ranges:
    for i in range(nearby.shape[1]):
        if r.validate(nearby[:, i]).all():
            possibles[r.name].add(i)


field_names = [None] * len(ranges)
while possibles != {}:
    for name, possible in possibles.items():
        if len(possible) == 1:
            i = possible.pop()
            field_names[i] = name
            possibles.pop(name)
            for possible in possibles.values():
                possible.remove(i)
            break


meaningless = 1
for name, val in zip(field_names, mine):
    if name.startswith('departure'):
        meaningless *= val
print('part 2:', meaningless)
