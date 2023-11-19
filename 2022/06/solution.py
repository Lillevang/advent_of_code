with open('input' , 'r') as file:
    stream = file.read().strip()

def part_one(stream):
    for i in range(len(stream)):
        _ = stream[i:i+4]
        if len(set(_)) == 4:
            print(f"Part one: {i + 4}")
            break

def part_two(stream):
    for i in range(len(stream)):
        _ = stream[i:i+14]
        if len(set(_)) == 14:
            print(f"Part two: {i + 14}")
            break

part_one(stream)
part_two(stream)
