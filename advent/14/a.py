input = 440231

board = [3, 7]
a, b = 0, 1

while True:
    sum = board[a] + board[b]
    if sum >= 10:
        board.append(1)
    board.append(sum % 10)
    a = (a + board[a] + 1) % len(board)
    b = (b + board[b] + 1) % len(board)
    if len(board) >= input + 10:
        result = []
        for index in range(input, input + 10):
            result.append(board[index])
        print(''.join(map(str, result)))
        print(''.join(map(str, board)))
        break
