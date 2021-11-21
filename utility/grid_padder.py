from typing import List

class GridPadder:

    def __init__(self, base_grid: List[List[str]], pad_char: str) -> None:
        self.base_grid = base_grid
        self.padded_grid = self.pad_grid(base_grid, pad_char)


    def pad_grid(self, base_grid: List[List[str]], pad_char: str) -> List[str]:
        padded_grid = []
        top_and_bot_row = [pad_char] * (len(base_grid[0]) + 2)
        padded_grid.append(top_and_bot_row)
        for row in base_grid:
            _row = row.copy()
            _row.insert(0, pad_char)
            _row.append(pad_char)
            padded_grid.append(_row)
        padded_grid.append(top_and_bot_row)
        return padded_grid