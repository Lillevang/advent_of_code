from typing import List
import re

def read_input(path='input'):
    output = []
    _ = 0
    with open(path, 'r') as file:
        lines = file.readlines()
        for idx, l in enumerate(lines):
            if l == '\n':
                output.append(' '.join(x.strip() for x in lines[_:idx]).strip())
                _ = idx
    return output    


def get_number_of_passport_fields(passport: str) -> List[str]:
    return [match.group('code') for match in re.finditer(r'(?P<code>[a-z]+):(?P<value>\S+)', passport)]
    

def validate_passport(passport: List[str]) -> bool:
    fields = get_number_of_passport_fields(passport)
    return len(fields) == 8 or (len(fields) == 7 and 'cid' not in fields)
        

def validate_passports(passports: List[str]) -> int:
    return len([passport for passport in passports if validate_passport(passport)])
        

def test_validate_passport():
    l = [
        ("iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929", False),
        ("ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm", True),
        ("hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm", True),
        ("hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in", False)
    ]
    for t in l:
        try:
            assert(validate_passport(t[0]) == t[1])
        except AssertionError:
            print(t)

if __name__ == "__main__":
    test_validate_passport()
    passports = read_input()
    print(validate_passports(passports))
