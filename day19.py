import re

class Rule:
    def __init__(self, line, rules):
        self.id, line = line.strip().split(': ')
        self._pattern = None
        self._re = None
        self._re2 = None
        if line[0] == '"':
            self._pattern = line[1]
        else:
            self.seqs = [seq.split() for seq in line.split(' | ')]
        self.rules = rules
        self.rules[self.id] = self

    @staticmethod
    def from_txt(txt):
        rules = {}
        for line in txt.splitlines():
            Rule(line, rules)
        return rules

    def check(self, msg):
        try:
            return self.re.match(msg) is not None
        except:
            return self.consume(msg) == ''

    def consume(self, msg):
        "consume a prefix of msg matching this rule"
        try:
            if match := self.re2.match(msg):
                return match.group(1)
            return msg

        except:
            if any(self.id in seq for seq in self.seqs):
                terminal, continuation = self.seqs
                i = continuation.index(self.id)
                pre, post = continuation[:i], continuation[i+1:]
                assert pre + post == terminal
                pre, post = terminal
                unconsumed = msg
                n = 0
                while True:
                    match = self.rules[pre].consume(unconsumed)
                    if match == unconsumed:
                        # rules[i] didn't consume
                        break
                    unconsumed = match
                    n += 1
                if n == 0:
                    return msg
                for _ in range(n):
                    match = self.rules[pre].consume(unconsumed)
                    if match == unconsumed:
                        # rules[i] didn't consume
                        return msg
                    unconsumed = match
                return uncomsumed


            for seq in self.seqs:
                unconsumed = msg
                for i in seq:
                    match = self.rules[i].consume(unconsumed)
                    if match == unconsumed:
                        # rules[i] didn't consume
                        break
                    unconsumed = match
                else:
                    # all of seq consumed; we're done
                    return unconsumed

            return msg

    def _seq_pattern(self, seq):
        return ''.join(self.rules[i].pattern for i in seq)

    @property
    def pattern(self):
        if self._pattern is not None:
            return self._pattern

        if any(self.id in seq for seq in self.seqs):
            terminal, continuation = self.seqs
            i = continuation.index(self.id)
            pre, post = continuation[:i], continuation[i+1:]
            assert pre + post == terminal
            if any(seq == [] for seq in [pre, post]):
                base = "".join(map(self._seq_pattern, pre + post))
                self._pattern = f'({base})+'
            else:
                pre, post = map(self._seq_pattern, [pre, post])
                patterns = []
                for i in range(1, 5):
                    patterns.append(f'({pre}){{{i}}}({post}){{{i}}}')
                self._pattern = f'({"|".join(patterns)})'
            return self._pattern

        self._pattern = "|".join(map(self._seq_pattern, self.seqs))
        if len(self.seqs) > 1:
            self._pattern = f'({self._pattern})'

        return self._pattern

    @property
    def re(self):
        if self._re is None:
            self._re = re.compile(f'^{self.pattern}$')
        return self._re

    @property
    def re2(self):
        if self._re2 is None:
            self._re2 = re.compile(f'^{self.pattern}(.*)$')
        return self._re2


rules, messages = open('day19_input.txt').read().split('\n\n')
rules = Rule.from_txt(rules)
messages = messages.splitlines()

print('part 1:', sum(rules['0'].check(m) for m in messages))

def test():
    rules = Rule.from_txt(txt := '''\
    42: 9 14 | 10 1
    9: 14 27 | 1 26
    10: 23 14 | 28 1
    1: "a"
    11: 42 31
    5: 1 14 | 15 1
    19: 14 1 | 14 14
    12: 24 14 | 19 1
    16: 15 1 | 14 14
    31: 14 17 | 1 13
    6: 14 14 | 1 14
    2: 1 24 | 14 4
    0: 8 11
    13: 14 3 | 1 12
    15: 1 | 14
    17: 14 2 | 1 7
    23: 25 1 | 22 14
    28: 16 1
    4: 1 1
    20: 14 14 | 1 15
    3: 5 14 | 16 1
    27: 1 6 | 14 18
    14: "b"
    21: 14 1 | 1 14
    25: 1 1 | 1 14
    22: 14 14
    8: 42
    26: 14 22 | 1 20
    18: 15 15
    7: 14 5 | 1 21
    24: 14 1''')

    messages = [m.strip() for m in '''\
    abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaaaabbaaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    babaaabbbaaabaababbaabababaaab
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''.splitlines()]

    assert sum(rules['0'].check(m) for m in messages) == 3

    rules = Rule.from_txt(txt)
    Rule('8: 42 | 42 8', rules)
    Rule('11: 42 31 | 42 11 31', rules)

    print(Rule.from_txt('0: 1\n1: "a"')['0'].pattern)
    print(Rule.from_txt('0: 1 | 0 1\n1: "a"')['0'].pattern)
    print(Rule.from_txt('0: 2 1 | 2 0 1\n1: "a"\n2: "b"')['0'].pattern)
    rules2 = Rule.from_txt('0: 2 1 | 2 0 1\n1: "a"\n2: "b"')
    assert rules2['0'].check('bbbaaa')
    assert not rules2['0'].check('bbbaa')

    assert sum(rules['0'].check(m) for m in messages) == 12


test()


Rule('8: 42 | 42 8', rules)
Rule('11: 42 31 | 42 11 31', rules)

print(rules['8'].re())

re0 = re.compile('^' + rules['0'].re() + '$')
print('part 2:', sum(re0.match(m) is not None for m in messages))

