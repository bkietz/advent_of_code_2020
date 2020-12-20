class Game:
    def __init__(self, *starting):
        self.recent = {
            num: i + 1
            for i, num in enumerate(starting)
        }
        self.i = len(starting)
        self.last = starting[-1]

    def next(self):
        if self.last not in self.recent:
            n = 0
        else:
            n = self.i - self.recent[self.last]

        self.recent[self.last] = self.i
        self.i += 1
        self.last = n
        return n

    def __call__(self):
        while True:
            yield self.next()

    def until(self, i):
        for n in self():
            if self.i == i:
                return n

def expect(starting, following):
    game = Game(*starting)
    for actual, expected in zip(game(), following):
        if actual != expected:
            print(actual, expected, game.i)
        assert actual == expected

expect([0,3,6], [0,3,3,1,0,4,0])
assert Game(0,3,6).until(2020) == 436
assert Game(1,3,2).until(2020) == 1
assert Game(2,1,3).until(2020) == 10
assert Game(1,2,3).until(2020) == 27
assert Game(2,3,1).until(2020) == 78
assert Game(3,2,1).until(2020) == 438
assert Game(3,1,2).until(2020) == 1836
print('part 1:', Game(15,5,1,4,7,0).until(2020))

print('part 2:', Game(15,5,1,4,7,0).until(30000000))
