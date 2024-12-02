
with open('./input', 'r') as file:
    data = [list(map(int, line.split())) for line in file.read().strip().split('\n')]

def is_good(report):
    is_sorted = report == sorted(report) or report == sorted(report, reverse=True)
    valid_differences = all(1 <= abs(report[i] - report[i + 1]) <= 3 for i in range(len(report) - 1))
    return is_sorted and valid_differences


part_1 = 0
part_2 = 0

for report in data:
    if is_good(report):
        part_1 += 1
        
    if any(is_good(report[:i] + report[i + 1:]) for i in range(len(report))):
        part_2 += 1

print(part_1)
print(part_2)