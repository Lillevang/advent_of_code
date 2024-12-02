from collections import Counter

with open('./input', 'r') as f:
    data = f.readlines()

left_list = []
right_list = []
distances = 0

for line in data:
    left, right = line.strip().split("   ")
    left_list.append(int(left))
    right_list.append(int(right))

left_list.sort()
right_list.sort()

# Part 1:
for i in range(len(left_list)):
    distances += abs(left_list[i] - right_list[i])

print(distances)

# Part 2:
p2_score = 0
freqs_right = Counter(right_list)
p2_score = sum(num * freqs_right[num] for num in left_list)
print(p2_score)
