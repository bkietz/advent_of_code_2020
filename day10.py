import numpy as np

numbers = sorted(map(int, open('day10_input.txt').readlines()))
numbers = np.array([0, *numbers, numbers[-1] + 3])
steps = [1, 2, 3]


diff_counts = {s: 0 for s in steps}
for diff in numbers[1:] - numbers[:-1]:
    diff_counts[diff] += 1

print('part 1:', diff_counts[1] * diff_counts[3])


counts = {0: 1}
for n in numbers[1:]:
    counts[n] = sum(counts.get(n - s, 0) for s in steps)

print('part 2:', counts[numbers[-1]])

