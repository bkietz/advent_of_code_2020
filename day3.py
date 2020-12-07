class TreeLine:
    def __init__(self, treeline_str):
        treeline_str = treeline_str.strip()
        self.length = len(treeline_str)
        treeline_str = treeline_str.replace('.', '0')
        treeline_str = treeline_str.replace('#', '1')
        self.mask = int(''.join(reversed(treeline_str)), base=2)

    def is_tree(self, pos):
        pos %= self.length
        return self.mask & (2 ** pos)

def test_TreeLine():
    treeline = TreeLine('......#..........##......#.####')

    # first 8 positions:
    for i in range(6):
        assert not treeline.is_tree(i)
    assert treeline.is_tree(6)
    assert not treeline.is_tree(7)

    # last 6 positions:
    assert treeline.is_tree(treeline.length - 6)
    assert not treeline.is_tree(treeline.length - 5)
    for i in range(treeline.length - 4, treeline.length):
        assert treeline.is_tree(i)

    # wrapping:
    for i in range(treeline.length):
        assert treeline.is_tree(i) == treeline.is_tree(i + treeline.length)

#test_TreeLine()

treelines = [TreeLine(line) for line in open('day3_input.txt').readlines()]

tree_counts = [0] * treelines[0].length
for start_pos in range(len(tree_counts)):
    tree_counts[start_pos] = 0
    pos = start_pos
    for treeline in treelines:
        if treeline.is_tree(pos):
            tree_counts[start_pos] += 1
        pos += 3

print('tree_counts: ', sorted(enumerate(tree_counts),
                              key=lambda i_count: i_count[1]))
# didn't ask, but: start at position 8.

tree_counts = {}
for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    right, down = slope
    tree_count = 0
    pos = 0
    for i in range(0, len(treelines), down):
        if treelines[i].is_tree(pos):
            tree_count += 1
        pos += right
    tree_counts[slope] = tree_count

print()
print('tree_counts: ', sorted(tree_counts.items(),
                              key=lambda slope_count: slope_count[1]))

meaningless = 1
for count in tree_counts.values():
    meaningless *= count
print('\n meaningless product:', meaningless)
