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