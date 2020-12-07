class LetterCountPolicy:
    def __init__(self, policy_str):
        self.policy_str = policy_str
        policy_str, self.letter = policy_str.split()
        self.min, self.max = map(int, policy_str.split('-'))

    def check(self, password):
        count = sum(letter == self.letter for letter in password)
        return self.min <= count <= self.max

class LettersAtIndicesPolicy:
    def __init__(self, policy_str):
        self.policy_str = policy_str
        policy_str, self.letter = policy_str.split()
        self.indices = list(map(lambda i: int(i), policy_str.split('-')))

    def check(self, password, verbose=False):
        assert all(i-1 < len(password) for i in self.indices)

        if verbose:
            print('checking', password, 'against', self.policy_str)
            indices = map(lambda i: str(i)[-1], range(1, 1 + len(password)))
            print('        ', ''.join(indices))
            markers = [' '] * len(password)
            for i in self.indices:
                markers[i - 1] = self.letter
            print('        ', ''.join(markers))

        count = sum(password[i - 1] != self.letter for i in self.indices)
        return count == 1

total_count = 0
letter_count_valid_count = 0
letters_at_valid_count = 0
for line in open('day2_input.txt').readlines():
    total_count += 1
    policy_str, password = line.split(': ')
    password = password.strip()

    if LetterCountPolicy(policy_str).check(password):
        letter_count_valid_count += 1
    if LettersAtIndicesPolicy(policy_str).check(password):
        letters_at_valid_count += 1

print(f'part 1: {letter_count_valid_count}/{total_count} valid')
print(f'part 2: {letters_at_valid_count}/{total_count} valid')
