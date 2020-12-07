def parse_boarding_pass(s):
    fb, rl = s[:7], s[7:]
    row = int(fb.replace('B', '1').replace('F', '0'), base=2)
    seat = int(rl.replace('R', '1').replace('L', '0'), base=2)
    return row, seat, row * 8 + seat

def test_parse_boarding_pass():
    for s, (row, seat, i) in {'BFFFBBFRRR': (70, 7, 567),
                              'FFFBBBFRRR': (14, 7, 119),
                              'BBFFBBFRLL': (102, 4, 820)}.items():
        assert parse_boarding_pass(s) == (row, seat, i)

#test_parse_boarding_pass()

passes = [parse_boarding_pass(s) for s in open('day5_input.txt').readlines()]

max_id = max(i for row, seat, i in passes)
print('part 1:', max_id)

occupied = ['0'] * (max_id + 1)
for row, seat, i in passes:
    occupied[i] = '1'
occupied = ''.join(occupied)

i = occupied.index('101') + 1
assert occupied[i - 1] == '1'
assert occupied[i] == '0'
assert occupied[i + 1] == '1'

print('part 2:', i)
