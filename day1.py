entries = set(map(int, open('day1_input.txt').readlines()))

def pair_summing_to(total):
    [a, b] = set(total - n for n in entries).intersection(entries)
    assert a + b == total
    return a, b

[a, b] = pair_summing_to(2020)
print(f'part 1: {a}*{b} == {a*b}')

for c in entries:
    try:
        [a, b] = pair_summing_to(2020 - c)
        assert a + b + c == 2020
        print(f'part 2: {a}*{b}*{c} == {a*b*c}')
        break
    except:
        continue
else:
    print('not found')
