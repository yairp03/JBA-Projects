# write your code here
NULL = ' '


def main():
    board = [[NULL] * 3, [NULL] * 3, [NULL] * 3]
    print_board(board)
    curr_player = 'X'
    while not check_win(board):
        update_board(board, curr_player)
        print_board(board)
        curr_player = 'X' if curr_player == 'O' else 'O'


def update_board(board, player='X'):
    updated = False
    while not updated:
        x, y = input('Enter the coordinates: ').split()
        try:
            x, y = int(x), int(y)
        except ValueError:
            print('You should enter numbers!')
            continue
        if not (1 <= x <= 3 and 1 <= y <= 3):
            print('Coordinates should be from 1 to 3!')
            continue
        if board[3 - y][x - 1] != NULL:
            print('This cell is occupied! Choose another one!')
            continue
        board[3 - y][x - 1] = player
        updated = True


def check_win(board: list):
    wins = {'X': False, 'O': False}
    count = {'X': 0, 'O': 0}
    for row in board :
        for item in row:
            if item != NULL:
                count[item] += 1
    # rows check
    for row in board:
        if row[0] == row[1] == row[2] != NULL:
            wins[row[0]] = True
    # columns check
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != NULL:
            wins[board[0][column]] = True
    # left diagonal
    if board[0][0] == board[1][1] == board[2][2] != NULL:
        wins[board[0][0]] = True
    # right diagonal
    if board[0][2] == board[1][1] == board[2][0] != NULL:
        wins[board[0][2]] = True
    if wins['X'] and wins['O'] or abs(count['X'] - count['O']) > 1:
        print('Impossible')
        raise Exception('Impossible')
    for p in wins:
        if wins[p]:
            print(p + ' wins')
            return True
    if sum(count.values()) == 9:
        print('Draw')
        return True
    return False


def print_board(board: list):
    print('---------')
    for row in board:
        print('| ', end='')
        for item in row:
            print(item, end=' ')
        print('|')
    print('---------')


if __name__ == '__main__':
    main()
