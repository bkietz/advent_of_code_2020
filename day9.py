numbers = [*map(int, open('day9_input.txt').readlines())]


def pair_summing_to(total, pre):
    pre = [*sorted(pre)]
    while pre != []:
        a, b = pre[0], pre[-1]
        if a + b == total:
            return a, b
        if a + b > total:
            pre = pre[:-1]
        else:
            pre = pre[1:]
    raise Exception('nope')


def find_corrupted(numbers, preamble_length):
    for i, n in enumerate(numbers[preamble_length:]):
        pre = numbers[i:i + preamble_length]
        try:
            a, b = pair_summing_to(n, pre)
            #print(f'{n}={a}+{b}')
        except:
            return n

def find_range_summing_to(numbers, total):
    begin, end = 0, 1
    while True:
        r = numbers[begin:end]
        s = sum(r)
        if s == total:
            return r
        if s > total:
            begin += 1
        else:
            end += 1


def test():
    numbers = [int(i) for i in '''\
        35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576'''.split()]

    corrupt = find_corrupted(numbers, 5)
    rng = find_range_summing_to(numbers, corrupt)
    assert rng == numbers[2:6]
    assert min(rng) + max(rng) == 62

test()
corrupt = find_corrupted(numbers, 25)
print('part 1:', corrupt)

rng = find_range_summing_to(numbers, corrupt)
print('part 2:', min(rng) + max(rng))
