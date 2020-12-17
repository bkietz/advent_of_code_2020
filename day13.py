soonest, buses = open('day13_input.txt').readlines()

soonest = int(soonest.strip())

def parse_buses(buses):
    return [
        None if bus == 'x' else int(bus)
        for bus in buses.strip().split(',')
    ]

buses = parse_buses(buses)
departures = {
    bus: bus - soonest % bus
    for bus in buses
    if bus is not None
}
best = min(departures.items(), key=lambda b: b[1])
print('part 1:', best[0] * best[1])


from functools import reduce

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)


def find(buses):
    if isinstance(buses, str):
        buses = parse_buses(buses)
    assert buses != []

    soonest = 0
    cycle = buses[0]

    for offset, bus in enumerate(buses):
        if bus is None or offset == 0:
            continue
        while (soonest + offset) % bus != 0:
            soonest += cycle
        cycle = lcm(cycle, bus)
    return soonest

assert find('7') == 0
assert find('2,3') == 2
assert find('7,13,x,x,59,x,31,19') == 1068781
assert find('17,x,13,19') == 3417
assert find('67,7,59,61') == 754018
assert find('67,x,7,59,61') == 779210
assert find('67,7,x,59,61') == 1261476
assert find('1789,37,47,1889') == 1202161486

print('part 2:', find(buses))
