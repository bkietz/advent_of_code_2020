import cmath

deltas = {
    'N': 1j,
    'E': 1,
    'S': -1j,
    'W': -1,
}

def manhattan(c):
    return int(abs(c.real) + abs(c.imag))

class Ship:
    def __init__(self):
        self.position = 0
        self.bearing = deltas['E']

    def turn_left(self, value):
        self.bearing *= 1j ** (value / 90)

    def exec_one(self, instruction):
        instruction = instruction.strip()
        value = int(instruction[1:])
        instruction = instruction[0]

        if instruction == 'L':
            return self.turn_left(value)
        if instruction == 'R':
            return self.turn_left(-value)

        if instruction == 'F':
            delta = self.bearing
        else:
            assert instruction in 'NESW'
            delta = deltas[instruction]

        self.position += delta * value

    def exec(self, instructions):
        for instruction in instructions:
            self.exec_one(instruction)
        return self

ship = Ship()
ship.exec(open('day12_input.txt').readlines())
print('part 1:', manhattan(ship.position))


class Ship:
    def __init__(self):
        self.position = 0
        self.waypoint = 10 + 1j

    def turn_left(self, value):
        self.waypoint *= 1j ** (value / 90)

    def exec_one(self, instruction):
        instruction = instruction.strip()
        value = int(instruction[1:])
        instruction = instruction[0]

        if instruction == 'L':
            return self.turn_left(value)
        if instruction == 'R':
            return self.turn_left(-value)

        if instruction == 'F':
            self.position += self.waypoint * value
            return

        assert instruction in 'NESW'
        delta = deltas[instruction]
        self.waypoint += delta * value

    def exec(self, instructions):
        for instruction in instructions:
            self.exec_one(instruction)
        return self

ship = Ship()
ship.exec(open('day12_input.txt').readlines())
print('part 2:', manhattan(ship.position))
