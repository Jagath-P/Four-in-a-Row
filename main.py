# agent red
# human green

ROWS = 6
COLS = 7

board = []
windows = []
weights = [1, 10, 100]

for row in range(ROWS):
    board.append([])
    for col in range(COLS):
        board[row].append(0)


def create_windows():
    # horizontal: 24
    for row in range(ROWS):
        for col in range(COLS - 3):
            windows.append([(row, col + k) for k in range(4)])

    # vertical: 21
    for row in range(ROWS - 3):
        for col in range(COLS):
            windows.append([(row + k, col) for k in range(4)])

    # diagonal down-right: 12
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            windows.append([(row + k, col + k) for k in range(4)])

    # diagonal down-left: 12
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            windows.append([(row + k, col - k) for k in range(4)])


def evaluate(board):
    # not ready
    score = 0
    for w in windows:
        cells = [board[r][c] for r, c in w]
        r_count = cells.count("R")
        g_count = cells.count("G")

        if r_count > 0 and g_count > 0:
            continue

        count = max(r_count, g_count)  # at most one of them is non-zero here
        if count < 1:
            continue

        s = weights[count - 1]

        if count == 3:
            r, c = w[cells.index(0)]  # the single empty cell
            gap = drop_row(board, c) - r  # empty cells below it
            s = s // (1 + gap)

        if g_count > 0:  # sign applied once, at the end
            s = -s

        score += s

    return score


def check_valid(row, col):
    return 0 <= col < COLS and 0 <= row < ROWS and board[row][col] == 0


def drop_row(board, col):
    # row 0 is the top, so scan from the bottom up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None


def is_full(board):
    return all(board[0][c] != 0 for c in range(COLS))


"""
def print_board(board):
    for row in board:
        print(" ".join("." if x == 0 else x for x in row))
    print(" ".join(str(c + 1) for c in range(COLS)))
"""


def print_board(board):
    for row in board:
        # print(" ".join("." if x == 0 else x for x in row))
        print(
            " ".join(
                (
                    "."
                    if x == 0
                    else "\033[31mR\033[0m" if x == "R" else "\033[32mG\033[0m"
                )
                for x in row
            )
        )
    print(" ".join(str(c + 1) for c in range(COLS)))


def check_winner(board, player):
    for w in windows:
        val = board[w[0][0]][w[0][1]]
        check = val == player
        for i in range(1, 4):
            if board[w[i][0]][w[i][1]] != val:
                check = False
        if check:
            return True

    return False


def humanInput(board):
    print("Human's Turn\nEnter the column value: ")
    try:
        option = int(input()) - 1
        while not check_valid(0, option):
            print(f"Column {option+1} is full or invalid!\nEnter other column value: ")
            option = int(input()) - 1

        board[drop_row(board, option)][option] = "G"
    except:
        print("Invalid input!!\n")
        exit()


def minimax(board, max_player, depth, alpha, beta):
    if check_winner(board, "R"):
        return 1000000 + depth  # faster win scores higher
    if check_winner(board, "G"):
        return -1000000 - depth
    if is_full(board):
        return 0
    if depth == 0:
        return evaluate(board)

    if max_player:
        best_score = -float("inf")
        for i in range(COLS):
            if check_valid(0, i):
                j = drop_row(board, i)
                board[j][i] = "R"
                score = minimax(board, False, depth - 1, alpha, beta)
                board[j][i] = 0
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    return best_score

        return best_score

    else:
        best_score = float("inf")
        for i in range(COLS):
            if check_valid(0, i):
                j = drop_row(board, i)
                board[j][i] = "G"
                score = minimax(board, True, depth - 1, alpha, beta)
                board[j][i] = 0
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    return best_score

        return best_score


def best_move(board):
    best_score = -float("inf")
    move = None
    alpha = -float("inf")
    beta = float("inf")

    for i in [
        3,
        2,
        4,
        1,
        5,
        0,
        6,
    ]:  # prioritizing center cols first as they are part of many windows
        if check_valid(0, i):
            j = drop_row(board, i)
            board[j][i] = "R"
            score = minimax(board, False, 4, alpha, beta)  # searching till depth 4
            board[j][i] = 0
            if score > best_score:
                best_score = score
                move = i  # 0-based, matches main
    return move


def main():
    create_windows()
    current_player = "Human"
    print("----------Four in a Row Game----------\n")
    print("HUMAN - G (Green)\nAGENT - R (Red)\n")

    while True:
        print_board(board)

        if is_full(board):
            print("It's a Draw!")
            break

        if current_player == "Agent":
            print("\nAI is thinking ..\n")
            move = best_move(board)
            board[drop_row(board, move)][move] = "R"
            print(f"AI chooses column {move+1}\n")
            if check_winner(board, "R"):
                print_board(board)
                print("AI wins!\n")
                break
            current_player = "Human"

        else:
            humanInput(board)

            if check_winner(board, "G"):
                print_board(board)
                print("Congratulations! You win!")
                break
            current_player = "Agent"


main()
