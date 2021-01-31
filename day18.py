import re

paren = re.compile(r'^(.*)\(([^\(]+?)\)(.*)$')
ops = {
    '+': lambda l, r: l + r,
    '*': lambda l, r: l * r,
}

def ev(line):
    while match := paren.match(line):
        pre, inner, post = match.groups()
        line = f'{pre}{ev(inner)}{post}'

    line = line.strip().split()
    while len(line) > 1:
        l, op, r, *line = line
        line = [ops[op](int(l), int(r)), *line]

    return int(line[0])


assert ev('2 * 3 + (4 * 5)') == 26
assert ev('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert ev('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert ev('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

lines = open('day18_input.txt').readlines()
print('part 1:', sum(ev(line) for line in lines))

add = re.compile(r'^(.*)(\b\d+) \+ (\d+\b)(.*)$')
def ev2(line):
    while match := paren.match(line):
        pre, inner, post = match.groups()
        line = f'{pre}{ev2(inner)}{post}'

    print(line)
    while match := add.match(line):
        pre, l, r, post = match.groups()
        line = f'{pre}{int(l) + int(r)}{post}'

    line = line.strip().split()
    while len(line) > 1:
        l, op, r, *line = line
        assert op == '*'
        line = [ops[op](int(l), int(r)), *line]

    return int(line[0])


assert ev2('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert ev2('2 * 3 + (4 * 5)') == 46
assert ev2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert ev2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert ev2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340


print('part 2:', sum(ev2(line) for line in lines))
