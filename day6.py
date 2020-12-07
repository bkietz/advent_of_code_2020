class AnswerSet:
    def __init__(self, set_str, anyone=True):
        self.yes = None
        for line in set_str.strip().split('\n'):
            if self.yes is None:
                self.yes = set(line)
                continue

            if anyone:
                self.yes = set(line).union(self.yes)
            else:
                self.yes = set(line).intersection(self.yes)

        self.yes = ''.join(sorted(self.yes))

blocks = str(open('day6_input.txt').read()).split('\n\n')
answer_sets = [AnswerSet(s) for s in blocks]

#print([s.yes for s in answer_sets[:5]])

print('part 1:', sum(len(s.yes) for s in answer_sets))

answer_sets = [AnswerSet(s, anyone=False) for s in blocks]

#print([s.yes for s in answer_sets[:30]])
print('part 2:', sum(len(s.yes) for s in answer_sets))
