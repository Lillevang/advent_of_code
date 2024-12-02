data = [[int(y) for y in x.split(" ")] for x in open("input", "r").read().split("\n")]

def is_good(report):
    inc = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    return set(inc) <= {1, 2, 3} or set(inc) <= {-1, -2, -3}

part_1 = sum([is_good(report) for report in data])
part_2 = sum([any([is_good(report[:i] + report[i + 1:]) for i in range(len(report))]) for report in data])

print(part_1)
print(part_2)

