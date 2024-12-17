# TODO: Clean up code...

with open('./input', 'r') as file:
    data = [l.split(',') for l in file.readlines()]

def split_pairs(raw_pair):
    return raw_pair[0].strip().split('-'), _[1].strip().split('-')

cnt = 0
for _ in data:
    p1, p2 = split_pairs(_)
    if (int(p1[0]) <= int(p2[0]) and int(p1[1]) >= int(p2[1])) or int(p2[0]) <= int(p1[0]) and int(p2[1]) >= int(p1[1]):
        cnt += 1

print(f'Part 1: {cnt}')

cnt = 0
for _ in data:
    p1, p2 = split_pairs(_)
    s1 = set(range(int(p1[0]), int(p1[1]) + 1))
    s2 = set(range(int(p2[0]), int(p2[1]) + 1))
    if len(s1.intersection(s2)) > 0:
        cnt += 1

print(f'Part 2: {cnt}')
