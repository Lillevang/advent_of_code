def read_input(file_path="input"):
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file.readlines()]

def count_occurrences(grid, word):
    def count_in_all_directions(sequence, word):
        return sequence.count(word) + sequence[::-1].count(word)

    total = 0
    rows, cols = len(grid), len(grid[0])

    # Horizontal and vertical directions
    for row in grid:
        total += count_in_all_directions(''.join(row), word)
    for col in range(cols):
        col_str = ''.join(grid[row][col] for row in range(rows))
        total += count_in_all_directions(col_str, word)

    # Diagonals
    for d in range(-rows + 1, cols):  # Main diagonals
        diag1 = ''.join(grid[i][i + d] for i in range(rows) if 0 <= i + d < cols)
        diag2 = ''.join(grid[i][cols - 1 - i - d] for i in range(rows) if 0 <= cols - 1 - i - d < cols)
        total += count_in_all_directions(diag1, word)
        total += count_in_all_directions(diag2, word)

    return total

def count_xmas_pattern(grid):
    def extract_diagonals(r, c):
        diag1 = grid[r - 1][c - 1] + grid[r][c] + grid[r + 1][c + 1]
        diag2 = grid[r + 1][c - 1] + grid[r][c] + grid[r - 1][c + 1]
        return diag1, diag2

    rows, cols = len(grid), len(grid[0])
    total = 0

    # Check 3x3 subgrids
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            diag1, diag2 = extract_diagonals(r, c)
            if diag1 in {"MAS", "SAM"} and diag2 in {"MAS", "SAM"}:
                total += 1
    return total

# Main
grid = read_input()
print(f"Part 1: {count_occurrences(grid, 'XMAS')}")
print(f"Part 2: {count_xmas_pattern(grid)}")
