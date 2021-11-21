import unittest
import sys
sys.path.insert(0, '../utility')

from grid_padder import GridPadder
from pprint import pprint

class TestUtilityTools(unittest.TestCase):

    def test_grid_padder(self):
        grid = [['.']*3]*3
        gp = GridPadder(grid, '*')
        self.assertGreater(len(gp.padded_grid), len(grid))
        self.assertEquals(gp.padded_grid[0][0], '*')
        self.assertEquals(len(gp.padded_grid[0]), len(grid[0]) + 2)
        print('GRID:')
        pprint(grid)
        print()
        print('PADDED GRID:')
        pprint(gp.padded_grid)
        


if __name__ == '__main__':
    unittest.main()
