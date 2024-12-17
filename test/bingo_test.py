import unittest
import sys
sys.path.insert(0, '../2021/04')
from solution import BingoBoard


class TestBingoBoard(unittest.TestCase):

    def test_bingoboard_creates(self):
        numbers = [['60', '79', '46', '9', '58'],['97', '81', '6', '94', '84'],['38', '40', '17', '61', '29'], ['11', '28', '0', '91', '15'], ['24', '77', '34', '59', '36']]
        board = BingoBoard(numbers)
        self.assertIsNotNone(board)
        self.assertIsNotNone(board.rows)
        self.assertIsNotNone(board.columns)
        self.assertEqual(len(board.rows), 5)
        self.assertEqual(len(board.columns), 5)


    def test_bingoboard_draw_numbers(self):
        input_ = [['60', '79', '46', '9', '58'],['97', '81', '6', '94', '84'],['38', '40', '17', '61', '29'], ['11', '28', '0', '91', '15'], ['24', '77', '34', '59', '36']]
        board = BingoBoard(input_)
        initial_sum_of_numbers = board.sum_of_numbers
        for n in [60, 79, 46, 9]:
            board.mark_number(n)
            self.assertFalse(board.has_bingo)
        board.mark_number(58)
        self.assertTrue(board.has_bingo)
        self.assertEqual(board.sum_of_numbers, initial_sum_of_numbers - sum([60, 79, 46, 9, 58]))


if __name__ == '__main__':
    unittest.main()
