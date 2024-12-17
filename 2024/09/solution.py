from collections import deque

def parse_disk_map(disk_map, part2):
    FILE_QUEUE = deque()
    FREE_BLOCKS = deque()
    FINAL = []
    file_id = 0
    pos = 0

    for i, c in enumerate(disk_map):
        size = int(c)
        if i % 2 == 0:  # File block
            if part2:
                FILE_QUEUE.append((pos, size, file_id))
            for _ in range(size):
                FINAL.append(file_id)
                if not part2:
                    FILE_QUEUE.append((pos, 1, file_id))
                pos += 1
            file_id += 1
        else:  # FREE_BLOCKS block
            FREE_BLOCKS.append((pos, size))
            FINAL.extend([None] * size)
            pos += size

    return FILE_QUEUE, FREE_BLOCKS, FINAL


def move_files(FILE_QUEUE, FREE_BLOCKS, FINAL):
    for (pos, size, file_id) in reversed(FILE_QUEUE):
        for space_idx, (space_pos, space_size) in enumerate(FREE_BLOCKS):
            if space_pos < pos and size <= space_size:
                # Move the file into this FREE_BLOCKS
                for i in range(size):
                    assert FINAL[pos + i] == file_id, f'{FINAL[pos + i]=}'
                    FINAL[pos + i] = None
                    FINAL[space_pos + i] = file_id
                # Update the FREE_BLOCKS deque
                FREE_BLOCKS[space_idx] = (space_pos + size, space_size - size)
                break


def calculate_checksum(FINAL):
    return sum(i * c for i, c in enumerate(FINAL) if c is not None)


def solve_disk(disk_map, part2):
    FILE_QUEUE = FREE_BLOCKS, FINAL = parse_disk_map(disk_map, part2)
    move_files(FILE_QUEUE, FREE_BLOCKS, FINAL)
    return calculate_checksum(FINAL)


with open('input', 'r') as f:
    disk_map_input = f.readline().strip()

# Solve for part 2 (whole files moving)
final_checksum = solve_disk(disk_map_input, part2=False)
print(final_checksum)

# Solve for part 2 (whole files moving)
final_checksum = solve_disk(disk_map_input, part2=True)
print(final_checksum)
