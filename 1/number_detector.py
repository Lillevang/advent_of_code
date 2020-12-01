from itertools import combinations

TARGET = 2020
numbers = set()


def validate_result(val) -> bool:
    return sum(val) == 2020


def prod(val: tuple) -> int:
    res = 1
    for elem in val:
        res *= elem
    return res


def print_result(numbers: tuple) -> str:
    result = prod(numbers)
    output = str(numbers[0])
    for i in range(1, len(numbers)):
        output += f' * {numbers[i]}'
    output += f' = {result}'
    return output


def test_validate_result():
    assert(type(validate_result([1])) == bool)
    assert(validate_result([2020]))
    assert(validate_result([2000, 20]))


def test_prod():
    assert(type(prod((2, 2))) == int)
    assert(prod((2, 2)) == 4)
    assert(prod((3, 3)) == 9)


def test_print_result():
    _ = (123, 1)
    assert(print_result(_) == f'{_[0]} * {_[1]} = 123')


if __name__ == "__main__":

    test_validate_result()
    test_prod()
    test_print_result()

    with open('input', 'r') as file:
        for line in file:
            cur_num = int(line.replace('\n', ''))
            numbers.add(cur_num)

    part_1 = list(filter(validate_result, combinations(numbers, 2)))[0]
    part_2 = list(filter(validate_result, combinations(numbers, 3)))[0]

    print(print_result(part_1))
    print(print_result(part_2))
