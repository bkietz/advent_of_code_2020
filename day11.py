import numpy as np
import scipy as sp
import scipy.signal

class Sightline:
    def __init__(self, start, step):
        self.start = start
        self.step = step

    def occupied_seen(self, grid):
        x, y = self.start
        dx, dy = self.step
        while True:
            x += dx
            y += dy
            if not grid.in_bounds((x,y)):
                return False
            if grid.is_seat(x, y):
                return grid.is_occupied(x, y)


class Grid:
    @staticmethod
    def parse_line(line):
        is_seat = np.array([c != '.' for c in line.strip()])
        is_occupied = np.array([c == '#' for c in line.strip()])
        return is_seat, is_occupied

    @staticmethod
    def from_lines(lines):
        lines = [Grid.parse_line(l) for l in lines if l != '']

        seat_mask = np.array([is_seat for is_seat, _ in lines],
                             dtype=np.uint8)

        occupied_mask = np.array([is_occupied for _, is_occupied in lines],
                                 dtype=np.uint8)

        return Grid(seat_mask, occupied_mask)

    def __init__(self, seat_mask, occupied_mask):
        self.seat_mask = seat_mask
        self.occupied_mask = occupied_mask

    @property
    def shape(self):
        return self.occupied_mask.shape

    def in_bounds(self, xy):
        x, y = xy
        return (0 <= y < self.shape[0]) and (0 <= x < self.shape[1])

    def is_seat(self, x, y):
        return self.seat_mask[y, x] == 1

    def is_occupied(self, x, y):
        return self.occupied_mask[y, x] == 1

    def crowding(self):
        neighborhood = np.ones((3,3), dtype=np.uint8)
        neighborhood[1, 1] = 0
        return sp.signal.convolve2d(self.occupied_mask, neighborhood)[1:-1, 1:-1]

    def iterate(self):
        crowding = self.crowding()
        return Grid(self.seat_mask, np.where(
            self.occupied_mask == 1,
            np.array(crowding < 4, dtype=np.uint8),
            np.array(self.seat_mask & (crowding == 0), dtype=np.uint8)))

    def occupied_seen(self):
        occupied_seen = np.zeros(self.occupied_mask.shape, dtype=np.uint8)
        steps = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        for x in range(self.occupied_mask.shape[1]):
            for y in range(self.occupied_mask.shape[0]):
                for step in steps:
                    occupied_seen[y, x] += Sightline((x,y), step).occupied_seen(self)
        return occupied_seen

    def iterate2(self):
        occupied_seen = self.occupied_seen()
        return Grid(self.seat_mask, np.where(
            self.occupied_mask == 1,
            np.array(occupied_seen < 5, dtype=np.uint8),
            np.array(self.seat_mask & (occupied_seen == 0), dtype=np.uint8)))

    def __eq__(self, other):
        return (self.occupied_mask == other.occupied_mask).all()

    def __repr__(self):
        def ch(x, y):
            if not self.is_seat(x, y):
                return '.'
            if self.is_occupied(x, y):
                return '#'
            return 'L'

        ymax, xmax = self.seat_mask.shape

        lines = []
        for y in range(ymax):
            lines.append(''.join(ch(x, y) for x in range(xmax)))
        return '\n'.join(lines)


def test_grid():
    grids = [Grid.from_lines(s.split()) for s in
        '''
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL

        #.##.##.##
        #######.##
        #.#.#..#..
        ####.##.##
        #.##.##.##
        #.#####.##
        ..#.#.....
        ##########
        #.######.#
        #.#####.##

        #.LL.L#.##
        #LLLLLL.L#
        L.L.L..L..
        #LLL.LL.L#
        #.LL.LL.LL
        #.LLLL#.##
        ..L.L.....
        #LLLLLLLL#
        #.LLLLLL.L
        #.#LLLL.##

        #.##.L#.##
        #L###LL.L#
        L.#.#..#..
        #L##.##.L#
        #.##.LL.LL
        #.###L#.##
        ..#.#.....
        #L######L#
        #.LL###L.L
        #.#L###.##

        #.#L.L#.##
        #LLL#LL.L#
        L.L.L..#..
        #LLL.##.L#
        #.LL.LL.LL
        #.LL#L#.##
        ..L.L.....
        #L#LLLL#L#
        #.LLLLLL.L
        #.#L#L#.##

        #.#L.L#.##
        #LLL#LL.L#
        L.#.L..#..
        #L##.##.L#
        #.#L.LL.LL
        #.#L#L#.##
        ..L.L.....
        #L#L##L#L#
        #.LLLLLL.L
        #.#L#L#.##
        '''.split('\n\n')]

    for grid, next_grid in zip(grids[:-1], grids[1:]):
        iterated = grid.iterate()
        assert iterated == next_grid

    assert grids[-1].iterate() == grids[-1]
    assert grids[-1].occupied_mask.sum() == 37

    grids = [Grid.from_lines(s.split()) for s in '''
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL

        #.##.##.##
        #######.##
        #.#.#..#..
        ####.##.##
        #.##.##.##
        #.#####.##
        ..#.#.....
        ##########
        #.######.#
        #.#####.##

        #.LL.LL.L#
        #LLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLL#
        #.LLLLLL.L
        #.LLLLL.L#

        #.L#.##.L#
        #L#####.LL
        L.#.#..#..
        ##L#.##.##
        #.##.#L.##
        #.#####.#L
        ..#.#.....
        LLL####LL#
        #.L#####.L
        #.L####.L#

        #.L#.L#.L#
        #LLLLLL.LL
        L.L.L..#..
        ##LL.LL.L#
        L.LL.LL.L#
        #.LLLLL.LL
        ..L.L.....
        LLLLLLLLL#
        #.LLLLL#.L
        #.L#LL#.L#

        #.L#.L#.L#
        #LLLLLL.LL
        L.L.L..#..
        ##L#.#L.L#
        L.L#.#L.L#
        #.L####.LL
        ..#.#.....
        LLL###LLL#
        #.LLLLL#.L
        #.L#LL#.L#

        #.L#.L#.L#
        #LLLLLL.LL
        L.L.L..#..
        ##L#.#L.L#
        L.L#.LL.L#
        #.LLLL#.LL
        ..#.L.....
        LLL###LLL#
        #.LLLLL#.L
        #.L#LL#.L#
        '''.split('\n\n')]

    for grid, next_grid in zip(grids[:-1], grids[1:]):
        iterated = grid.iterate2()
        assert iterated == next_grid

    assert grids[-1].iterate2() == grids[-1]
    assert grids[-1].occupied_mask.sum() == 26


test_grid()


grid = Grid.from_lines(open('day11_input.txt').readlines())

def part1(grid):
    while True:
        next_grid = grid.iterate()
        if grid == next_grid:
            print('part 1:', grid.occupied_mask.sum())
            break
        grid = next_grid

part1(grid)

def part2(grid):
    while True:
        next_grid = grid.iterate2()
        if grid == next_grid:
            print('part 2:', grid.occupied_mask.sum())
            break
        grid = next_grid

part2(grid)
