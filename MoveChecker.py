def get_enemy_color(color):
    if color is "w":
        return "b"
    if color is "b":
        return "w"


def legal(board, x1, y1, piece, game_state):
    color = piece[0]
    type = piece[1]
    try:
        if type is "r":
            return line_search(board, x1, y1, get_enemy_color(color))
        if type is "b":
            return diagonal_search(board, x1, y1, get_enemy_color(color))
        if type is "q":
            return line_search(board, x1, y1, get_enemy_color(color)) + diagonal_search(board, x1, y1,
                                                                                        get_enemy_color(color))
        if type is "n":
            return knight_search(board, x1, y1, get_enemy_color(color))
        if type is "p":
            return pawn_search(board, x1, y1, color, get_enemy_color(color))
        if type is "k":
            return king_search(board, x1, y1, color, get_enemy_color(color), game_state)
    except IndexError:
        pass


# Could be optimized by adding list of variables for each direction, but readability would be decreased
def diagonal_search(board, x1, y1, enemy_color):
    list_of_legal_moves = []
    # north-east
    for s in range(1, 8):
        if (x1 + s) > 7 or (y1 + s) > 7:
            break
        if board[x1 + s][y1 + s] is "":
            list_of_legal_moves.append([x1 + s, y1 + s])
        elif enemy_color in board[x1 + s][y1 + s][0]:
            list_of_legal_moves.append([x1 + s, y1 + s])
            break
        else:
            break

    # south-east
    for s in range(1, 8):
        # if (x1 + s) > 7 or (y1 - s) > 7:
        if (x1 + s) > 7 or (y1 - s) < 0:
            break
        if board[x1 + s][y1 - s] is "":
            list_of_legal_moves.append([x1 + s, y1 - s])
        elif enemy_color in board[x1 + s][y1 - s][0]:
            list_of_legal_moves.append([x1 + s, y1 - s])
            break
        else:
            break

    # north-west
    for s in range(1, 8):
        if (x1 + s) < 0 or (y1 + s) > 7:
            break
        if board[x1 - s][y1 + s] is "":
            list_of_legal_moves.append([x1 - s, y1 + s])
        elif enemy_color in board[x1 - s][y1 + s][0]:
            list_of_legal_moves.append([x1 - s, y1 + s])
            break
        else:
            break

    # south-west
    for s in range(1, 8):
        if (x1 - s) < 0 or (y1 - s) < 0:
            break
        if board[x1 - s][y1 - s] is "":
            list_of_legal_moves.append([x1 - s, y1 - s])
        elif enemy_color in board[x1 - s][y1 - s][0]:
            list_of_legal_moves.append([x1 - s, y1 - s])
            break
        else:
            break

    return list_of_legal_moves


# Could be optimized by adding list of variables for each direction, but readability would be decreased
def line_search(board, x1, y1, enemy_color):
    list_of_legal_moves = []
    # Right
    for x in range((x1 + 1), 8):
        if board[x][y1] is "":
            list_of_legal_moves.append([x, y1])
        elif enemy_color in board[x][y1][0]:
            list_of_legal_moves.append([x, y1])
            break
        else:
            break

    # Left
    for x in range((x1 - 1), -1, -1):
        if board[x][y1] is "":
            list_of_legal_moves.append([x, y1])
        elif enemy_color in board[x][y1][0]:
            list_of_legal_moves.append([x, y1])
            break
        else:
            break

    # Up
    for y in range((y1 + 1), 8):
        if board[x1][y] is "":
            list_of_legal_moves.append([x1, y])
        elif enemy_color in board[x1][y][0]:
            list_of_legal_moves.append([x1, y])
            break
        else:
            break

    # Down
    for y in range((y1 - 1), -1, -1):
        if board[x1][y] is "":
            list_of_legal_moves.append([x1, y])
        elif enemy_color in board[x1][y][0]:
            list_of_legal_moves.append([x1, y])
            break
        else:
            break

    return list_of_legal_moves


def knight_search(board, x1, y1, enemy_color):
    list_of_legal_moves = []
    knight_moves = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]
    for m in knight_moves:
        if (x1 + m[0]) >= 0 and (y1 + m[1] >= 0):
            try:
                if board[x1 + m[0]][y1 + m[1]] is "" or enemy_color in board[x1 + m[0]][y1 + m[1]][0]:
                    list_of_legal_moves.append([x1 + m[0], y1 + m[1]])
            except IndexError:
                pass
    return list_of_legal_moves


def pawn_search(board, x1, y1, color, enemy_color):
    list_of_legal_moves = []

    try:
        # Move one square
        if color is "w" and board[x1][y1 + 1] is "":
            list_of_legal_moves.append([x1, y1 + 1])
        if color is "b" and board[x1][y1 - 1] is "":
            list_of_legal_moves.append([x1, y1 - 1])

        # Move two squares
        if color is "w" and y1 is 1 and board[x1][y1 + 2] is "":
            list_of_legal_moves.append([x1, y1 + 2])
        if color is "b" and y1 is 6 and board[x1][y1 - 2] is "":
            list_of_legal_moves.append([x1, y1 - 2])

        # Capture diagonally
        # capture north-west
        if color is "w" and board[x1 - 1][y1 + 1] and "b" in board[x1 - 1][y1 + 1][0]:
            list_of_legal_moves.append([x1 - 1, y1 + 1])
        # capture south-west
        if color is "b" and board[x1 - 1][y1 - 1] and "w" in board[x1 - 1][y1 - 1]:
            list_of_legal_moves.append([x1 - 1, y1 - 1])
        # exception for right edge of the board
        if (x1 + 1) > 7:
            return list_of_legal_moves
        # capture north-east
        if color is "w" and board[x1 + 1][y1 + 1] and "b" in board[x1 + 1][y1 + 1][0]:
            list_of_legal_moves.append([x1 + 1, y1 + 1])
        # capture south-east
        if color is "b" and board[x1 + 1][y1 - 1] and "w" in board[x1 + 1][y1 - 1]:
            list_of_legal_moves.append([x1 + 1, y1 - 1])
    except:
        pass
    return list_of_legal_moves


def king_search(board, x1, y1, color, enemy_color, game_state):
    list_of_legal_moves = []
    # Modified with cheat moves, change later
    king_moves = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [0, 1], [1, -1], [0, -1], [-1, -1]]

    castle_moves = [
        ["w", "wqsc_possible", -2, 0],
        ["w", "wksc_possible", 2, 0],
        ["b", "bqsc_possible", -2, 0],
        ["b", "bksc_possible", 2, 0]
    ]
    for c in castle_moves:
        if color is c[0] and game_state[c[1]] is True:
            king_moves.append([c[2], c[3]])

    for m in king_moves:
        # Out of bounds
        if x1 + m[0] > 7 or y1 + m[1] > 7 or x1 + m[0] < 0 or y1 + m[1] < 0:
            continue
        # funny bug with wb registering as enemy b
        if board[x1 + m[0]][y1 + m[1]] is "" or enemy_color in board[x1 + m[0]][y1 + m[1]][0]:
            list_of_legal_moves.append([x1 + m[0], y1 + m[1]])

    return list_of_legal_moves
