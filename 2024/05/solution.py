from functools import cmp_to_key

def read_input(file_path="input"):
    with open(file_path, "r") as file:
        return file.read()

def parse_input(inp):
    l, r = inp.split('\n\n')
    ll = []
    for line in l.split('\n'):
        x, y = line.split('|')
        ll.append((int(x), int(y)))
    return ll, r.split('\n')

def process_line(line, ll):
    # Convert the line into a list of integers
    nums = [int(x) for x in line.split(',') if x]
    if not nums:
        return 0, 0
    
    # Create a dictionary to map numbers to their indices
    conums = {x: i for (i, x) in enumerate(nums)}
    
    # Check if all conditions are met
    if all((x not in conums) or (y not in conums) or conums[x] < conums[y] for (x, y) in ll):
        # Return the middle number if conditions are met
        return nums[len(nums) // 2], 0
    else:
        # Sort the numbers based on the custom comparison function
        nums.sort(key=cmp_to_key(lambda x, y: 2 * ((x, y) in ll) - 1))
        # Return the middle number after sorting
        return 0, nums[len(nums) // 2]

inp = read_input()
ll, r_lines = parse_input(inp)

ans = 0
ans2 = 0
for line in r_lines:
    part1, part2 = process_line(line, ll)
    ans += part1
    ans2 += part2

print(f"part 1: {ans}")
print(f"part 2: {ans2}")
