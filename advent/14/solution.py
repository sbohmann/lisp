from find_sequence import FindSequence

raw_input = '440231'
input_a = int(raw_input)
input_b = list(map(int, raw_input))

mode = 'b'


class Solution:
    def __init__(self):
        self._board = [3, 7]
        a, b = 0, 1
        self._last_size = 0
        while True:
            score_sum = self._board[a] + self._board[b]
            if score_sum >= 10:
                self._board.append(1)
            self._board.append(score_sum % 10)
            a = (a + self._board[a] + 1) % len(self._board)
            b = (b + self._board[b] + 1) % len(self._board)
            if self._solve():
                break

    def _solve(self):
        if mode == 'a':
            return self._solve_a()
        elif mode == 'b':
            return self._solve_b()
        else:
            raise ValueError('Unknown mode [' + str(mode) + ']')

    def _solve_a(self):
        if len(self._board) >= input_a + 10:
            result = []
            for index in range(input_a, input_a + 10):
                result.append(self._board[index])
            print(''.join(map(str, result)))
            print(''.join(map(str, self._board)))
            return True

    def _solve_b(self):
        if len(self._board) % 100_000 == 0:
            result = FindSequence(self._board, input_b, self._last_size).result
            self._last_size = len(self._board)
            if result:
                print(result)
                return True
            print(len(self._board))


Solution()
