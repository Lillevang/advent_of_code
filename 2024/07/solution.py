from collections import deque


def read_tokens(filename: str) -> tuple[tuple[str, ...], ...]:
    with open(filename) as f:
        lines = f.readlines()
    stripped_lines = [
        stripped_line
        for stripped_line in (line.strip() for line in lines)
        if stripped_line
    ]
    return tuple(tuple(line.split()) for line in stripped_lines)


INPUT = read_tokens("./2024/07/input")

ADD = lambda x, y: x + y
MULT = lambda x, y: x * y
CONCAT = lambda x, y: int(str(x) + str(y))


class Equation:
    def __init__(self, line, ops=(ADD, MULT)):
        self.test_value = int(line[0].rstrip(":"))
        self.numbers = [int(x) for x in line[1:]]
        self.ops = ops

    def all_operation_sequences(self, length: int):
        q = deque()
        q.append(())
        while q:
            root = q.pop()
            if len(root) == length:
                yield root
            else:
                for next_op in self.ops:
                    q.append(root + (next_op,))

    def seek_equation(self):
        for op_seq in self.all_operation_sequences(len(self.numbers) - 1):
            total = self.numbers[0]
            for op, num in zip(op_seq, self.numbers[1:]):
                total = op(total, num)
            if total == self.test_value:
                return total
        return None


def part1():
    results = [Equation(line).seek_equation() for line in INPUT]
    return sum(r for r in results if r is not None)


def part2():
    results = [
        Equation(line, ops=(ADD, MULT, CONCAT)).seek_equation() for line in INPUT
    ]
    return sum(r for r in results if r is not None)


print(part1())
print(part2())