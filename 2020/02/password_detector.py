import re

PATTERN = r'(?P<min>\d+)-(?P<max>\d+)\s(?P<letter>[a-z]):\s(?P<password>[a-z]+)'
p = re.compile(PATTERN)


def read_input(path='input'):
    with open(path, 'r') as file:
        for line in file:
            yield line.replace('\n', '')


def password_is_valid_1(_min: int, _max: int, _letter: str, _password: str) -> bool:
    _count = _password.count(_letter)
    return _count >= _min and _count <= _max


def password_is_valid_2(idx1: int, idx2: int, _letter: str, _password: str) -> bool:
    return (_password[idx1 - 1] == _letter or _password[idx2 - 1] == _letter) and not (_password[idx1 - 1] == _letter and _password[idx2 - 1] == _letter)


def parse_passwords(line):
    m = p.search(line)
    return int(m.group('min')), int(m.group('max')), m.group('letter'), m.group('password')


def test_pasword_is_valid_1():
    assert(password_is_valid_1(1, 3, 'a', 'abcde'))
    assert(password_is_valid_1(2, 9, 'c', 'ccccccccc'))
    assert(password_is_valid_1(1, 3, 'b', 'cdefg') is False)


def test_pasword_is_valid_2():
    assert(password_is_valid_2(1, 3, 'a', 'abcde'))
    assert(password_is_valid_2(2, 9, 'c', 'ccccccccc') is False)
    assert(password_is_valid_2(1, 3, 'b', 'cdefg') is False)


def test_parse_passwords():
    _1, _2, _3, _4 = parse_passwords('1-3 a: abcde')
    assert(type(_1) == int)
    assert(type(_2) == int)
    assert(type(_3) == str)
    assert(type(_4) == str)
    assert(_1 == 1)
    assert(_2 == 3)
    assert(_3 == 'a')
    assert(_4 == 'abcde')


if __name__ == "__main__":
    test_parse_passwords()
    test_pasword_is_valid_1()
    test_pasword_is_valid_2()

    part_1_cnt = 0
    part_2_cnt = 0

    for line in read_input():
        _1, _2, _letter, _password = parse_passwords(line)
        if password_is_valid_1(_1, _2, _letter, _password):
            part_1_cnt += 1

        if password_is_valid_2(_1, _2, _letter, _password):
            part_2_cnt += 1

    print(part_1_cnt)
    print(part_2_cnt)
