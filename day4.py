import re

whitespace = re.compile('\s+')
hexdigits = set('0123456789abcdef')
eye_colors = set('amb blu brn gry grn hzl oth'.split())
digits = set('0123456789')

class Passport:
    allowed = set('byr iyr eyr hgt hcl ecl pid cid'.split())
    optional = set(['cid'])
    required = allowed - optional

    def __init__(self, passport_str):
        self.fields = {}
        for rec in whitespace.split(passport_str):
            if rec == '':
                continue

            field, val = rec.split(':')
            assert field in Passport.allowed

            self.fields[field] = val


    def is_valid(self, validate=False):
        missing_fields = Passport.required - set(self.fields.keys())
        if missing_fields != set():
            return False

        if not validate:
            return True

        for field, val in self.fields.items():
            if field == 'byr':
                if 1920 <= int(val) <= 2002:
                    continue

            elif field == 'iyr':
                if 2010 <= int(val) <= 2020:
                    continue

            elif field == 'eyr':
                if 2020 <= int(val) <= 2030:
                    continue

            elif field == 'hgt':
                hgt, unit = val[:-2], val[-2:]
                if unit == 'cm':
                    if 150 <= int(hgt) <= 193:
                        continue
                elif unit == 'in':
                    if 59 <= int(hgt) <= 76:
                        continue

            elif field == 'hcl':
                if val[0] == '#' and len(val) == 7:
                    if all(c in hexdigits for c in val[1:]):
                        continue

            elif field == 'ecl':
                if val in eye_colors:
                    continue

            elif field == 'pid':
                if len(val) == 9:
                    if all(c in digits for c in val):
                        continue

            elif field == 'cid':
                continue

            print('invalid', field + ':', val)
            return False

        return True


passports = [Passport(s)
             for s in str(open('day4_input.txt').read()).split('\n\n')]

print('part 1:', sum(p.is_valid() for p in passports))
print('part 2:', sum(p.is_valid(validate=True) for p in passports))
