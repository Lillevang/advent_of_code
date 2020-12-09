import util
import passport_validator_part_1 as pv1
import re
from typing import List

FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


def base_validation(passports: List[str]) -> List[str]:
    return [passport for passport in passports if pv1.validate_passport(passport)]


def validate_byr(value: str) -> bool:
    return len(value) == 4 and int(value) in range(1920, 2003)


def validate_iyr(value: str) -> bool:
    return len(value) == 4 and int(value) in range(2010, 2021)


def validate_eyr(value: str) -> bool:
    return len(value) == 4 and int(value) in range(2020, 2031)


def validate_hgt(value: str) -> bool:
    rules = {'in': range(59, 77), 'cm': range(150, 194)}
    matches = re.compile('(?P<val>\d+)(?P<unit>\D+)').search(value)
    return matches is not None and int(matches.group('val')) in rules[matches.group('unit')]


def validate_hcl(value: str) -> bool:
    return re.compile(r'#[0-9a-f]{6}').search(value) is not None


def validate_ecl(value: str) -> bool:
    return len(value) == 3 and value in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def validate_pid(value: str) -> bool:
    return re.compile(r'^\d{9}$').search(value) is not None


def validate_passport(passport: str) -> bool:
    VALIDATORS = {'byr': validate_byr, 'iyr': validate_iyr, 'eyr': validate_eyr, 'hgt': validate_hgt, 'hcl': validate_hcl, 'ecl': validate_ecl, 'pid': validate_pid}
    for field in FIELDS:
        pattern = re.compile(r'(?P<code>{0}):(?P<val>\S+)'.format(field))
        if not VALIDATORS[field](pattern.search(passport).group('val')):
            return False
    return True


def validate_passports(passports: List[str]) -> int:
    passports = base_validation(passports)
    return len([passport for passport in passports if validate_passport(passport)])


if __name__ == "__main__":
    passports = util.read_input()
    print(validate_passports(passports))