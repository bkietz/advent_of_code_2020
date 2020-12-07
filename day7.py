class Rule:
    def __init__(self, rule_str):
        self.color, rule_str = rule_str.split(' bags contain ')
        self.must_contain = {}

        if rule_str.startswith('no other bags'):
            return

        for contained in rule_str.split(', '):
            count = contained.split(' ')[0]
            assert count != '0'

            color = contained[len(count) + 1:contained.index('bag') - 1]
            self.must_contain[color] = int(count)


def test_Rule():
    r = Rule('light red bags contain 1 bright white bag, 2 muted yellow bags.')
    assert r.color == 'light red'
    assert r.must_contain == {
        'bright white': 1,
        'muted yellow': 2,
    }

    r = Rule('light red bags contain no other bags.')
    assert r.color == 'light red'
    assert r.must_contain == {}

#test_Rule()

rules = [Rule(s) for s in open('day7_input.txt').readlines()]

color_may_be_contained_by = {}
for r in rules:
    for color in r.must_contain.keys():
        if not color in color_may_be_contained_by:
            color_may_be_contained_by[color] = set()

        color_may_be_contained_by[color].add(r.color)

assert 'shiny gold' in color_may_be_contained_by

finalized_containers = set()
containers = color_may_be_contained_by['shiny gold']

while containers != set():
    container = containers.pop()
    finalized_containers.add(container)

    if not container in color_may_be_contained_by:
        # this container may not be contained
        continue

    for maybe in color_may_be_contained_by[container]:
        if maybe in finalized_containers:
            continue
        containers.add(maybe)

print('part 1:', len(finalized_containers))


color_must_contain = {r.color: r.must_contain for r in rules}


def contained_count(color):
    total = 0
    for contained_color, count in color_must_contain[color].items():
        total += count * (contained_count(contained_color) + 1)
    return total

assert contained_count('wavy teal') == 0
print('part 2:', contained_count('shiny gold'))

