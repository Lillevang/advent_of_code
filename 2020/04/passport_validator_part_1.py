from typing import List
import util

def validate_passport(passport: List[str]) -> bool:
    fields = util.get_number_of_passport_fields(passport)
    return len(fields) == 8 or (len(fields) == 7 and 'cid' not in fields)
        

def validate_passports(passports: List[str]) -> int:
    return len([passport for passport in passports if validate_passport(passport)])
        

if __name__ == "__main__":
    passports = util.read_input()
    print(validate_passports(passports))
