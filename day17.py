import numpy as np
import io
from functools import reduce


class Sparse:
    def __init__(self):
        self.active = {}

    def __getitem__(self, x):
        return self.active.get(x, 0)

    def __setitem__(self, x, val):
        self.active[x] = val

    def cycle(self):
        near = Sparse()
        for x, val in self.active.items():
            if val == 0:
                continue
            for n in Sparse.neighbors(x):
                near[n] += 1
        out = Sparse()
        for x in self.active.keys():
            if near[x] in {2,3}:
                out[x] = 1
        for x in near.active.keys():
            if near[x] == 3:
                out[x] = 1
        return out

    @staticmethod
    def neighbors(x):
        for trits in range(3**len(x)):
            y = []
            for xi in x:
                y.append(xi + trits % 3 - 1)
                trits = trits // 3
            assert trits == 0
            y = tuple(y)
            if y == x:
                continue
            yield y

    @staticmethod
    def from_slice(s, dim):
        out = Sparse()
        for y, line in enumerate(s.splitlines()):
            for x, c in enumerate(line):
                if c == '#':
                    out[(x, y) + (0,) * (dim - 2)] = 1
        return out

    @staticmethod
    def test():
        s = Sparse()
        assert s[1,2,4] == 0
        assert len(s.active) == 0
        s[2,3,5] += 1
        assert s[2,3,5] == 1
        assert [*Sparse.neighbors((1,1,1))] == [
            (0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0),
            (2, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0), (0, 0, 1),
            (1, 0, 1), (2, 0, 1), (0, 1, 1), (2, 1, 1), (0, 2, 1),
            (1, 2, 1), (2, 2, 1), (0, 0, 2), (1, 0, 2), (2, 0, 2),
            (0, 1, 2), (1, 1, 2), (2, 1, 2), (0, 2, 2), (1, 2, 2),
            (2, 2, 2)]

        s = Sparse.from_slice('.#.\n..#\n###\n', 3)
        assert len(s.cycle().cycle().cycle()
                    .cycle().cycle().cycle().active) == 112


Sparse.test()

s = Sparse.from_slice(open('day17_input.txt').read(), 3)
print('part 1:', len(s.cycle().cycle().cycle()
                      .cycle().cycle().cycle().active))

s = Sparse.from_slice(open('day17_input.txt').read(), 4)
print('part 2:', len(s.cycle().cycle().cycle()
                      .cycle().cycle().cycle().active))
