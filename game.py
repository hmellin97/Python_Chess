import tkinter as tk
from tkinter import messagebox as messagebox
import tkinter.font as tkFont
import numpy as np
from MoveChecker import legal
from copy import deepcopy

board = [["", "", "", "", "", "", "", ""]] * 8
board[7] = ["wr", "wp", "", "", "", "", "bp", "br"]
board[6] = ["wn", "wp", "", "", "", "", "bp", "bn"]
board[5] = ["wb", "wp", "", "", "bq", "", "bp", "bb"]
board[4] = ["wk", "wp", "", "", "", "", "bp", "bk"]
board[3] = ["wq", "wp", "", "", "", "", "bp", "bq"]
board[2] = ["wb", "wp", "", "", "bb", "", "bp", "bb"]
board[1] = ["wn", "wp", "", "", "", "", "bp", "bn"]
board[0] = ["wr", "wp", "", "", "", "", "bp", "br"]
game_state = {
    "wqsc_possible": "blocked_by_pieces",
    "wksc_possible": "blocked_by_pieces",
    "bqsc_possible": "blocked_by_pieces",
    "bksc_possible": "blocked_by_pieces",
    "black_in_check": False,
    "white_in_check": False,
    "checkmate": False,
    "players_turn": "b"
}
valid_promotions = ["n", "b", "q", "r"]
list_of_legal_moves = []

toUnicode = {
    "wk": "\u2654",
    "wq": "\u2655",
    "wr": "\u2656",
    "wb": "\u2657",
    "wn": "\u2658",
    "wp": "\u2659",
    "bk": "\u265A",
    "bq": "\u265B",
    "br": "\u265C",
    "bb": "\u265D",
    "bn": "\u265E",
    "bp": "\u265F",
}

root = tk.Tk()


def check_board():
    messagebox.showinfo("Game Over!", winner + " wins!")


move = []
legals_for_selected_tile = []
all_legal_moves = {}
future_all_legal_moves = {}


def get_color_of_piece(piece):
    if piece[0] is "w":
        return "w"
    if piece[0] is "b":
        return "b"


def get_enemy_color(color):
    if color is "w":
        return "b"
    if color is "b":
        return "w"


def change_turn():
    if game_state["players_turn"] == "w":
        game_state["players_turn"] = "b"
    else:
        game_state["players_turn"] = "w"


def checkmate():
    # Checkmate #
    checkmate = True
    for all in all_legal_moves:
        if len(all_legal_moves[all]) is not 0:
            return False
    if checkmate is True:
        print("Checkmate!")
        game_state["checkmate"] = True
        if game_state["white_in_check"] is True:
            print("Black wins!")
        else:
            print("White wins")
    return checkmate


def get_all_legal_moves():
    game_state["white_in_check"] = False
    game_state["black_in_check"] = False
    boom()
    blahblah()


def boom():
    global all_legal_moves
    global game_state
    global board
    for i in range(len(board)):
        for j in range(len(board[i])):
            piece = board[i][j]
            if piece is "":
                continue
            legal_moves_from_current_tile = legal(board, i, j, piece, game_state)
            current_tile = (i, j)
            all_legal_moves[current_tile] = legal_moves_from_current_tile
    in_check_checker(all_legal_moves)


def blahblah():
    global board
    global all_legal_moves
    old_legals = deepcopy(all_legal_moves)
    new_legals = deepcopy(all_legal_moves)
    variations = [["black_in_check", "Black"], ["white_in_check", "White"]]
    for v in variations:
        if game_state[v[0]] is True:
            for all in old_legals:
                piece = board[all[0]][all[1]]
                for m in all_legal_moves[all]:
                    old_board = deepcopy(board)
                    old_legals = deepcopy(all_legal_moves)
                    board[m[0]][m[1]] = piece
                    board[all[0]][all[1]] = ""
                    boom()
                    if in_check_checker(all_legal_moves) is v[1]:
                        new_legals[all].remove(m)
                    board = old_board
                    all_legal_moves = old_legals
        all_legal_moves = new_legals


def in_check_checker(all_legal_moves):
    for all in all_legal_moves:
        piece = board[all[0]][all[1]]
        if piece is "":
            continue
        piece_color = get_color_of_piece(piece)
        enemy_color = get_enemy_color(piece_color)
        for m in all_legal_moves[all]:
            if board[m[0]][m[1]] == enemy_color + "k":
                if enemy_color == "w":
                    game_state["white_in_check"] = True
                    return "White"
                if enemy_color == "b":
                    game_state["black_in_check"] = True
                    return "Black"



def make_move_by_notation(notation):
    # input is a string of the form "a2-a4"
    notation_list = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    on_click(notation_list[notation[0]], int(notation[1]))
    on_click(notation_list[notation[2]], int(notation[3]))



def on_click(i, j,):
    if game_state["checkmate"] is True:
        return
    get_all_legal_moves()
    # print(all_legal_moves[4, 0])
    x = i
    y = abs(j - 7)
    piece = board[x][y]
    global move
    if (piece is "" and len(move) == 0) or \
            (len(move) == 0 and get_color_of_piece(piece) is not game_state["players_turn"]):
        return
    move.append(x)
    move.append(y)
    # print(move)
    if len(move) == 2:
        global legals_for_selected_tile
        legals_for_selected_tile = all_legal_moves[x, y]
        game_frame.destroy()
        render()
    if len(move) == 4:
        move_piece(move)
        game_frame.destroy()
        legals_for_selected_tile = []
        move = []
        render()


def check_stuff(x1, y1, x2, y2, piece):
    global game_state

    # Promotions #
    variations = [[7, "w"], [0, "b"]]
    for v in variations:
        for i in range(len(board)):
            if board[i][v[0]] == v[1] + "p":
                print("What do you want to promote to?")
                while True:
                    choice = input()
                    if choice in valid_promotions:
                        break
                    else:
                        print("invalid")
                board[i][v[0]] = v[1] + choice

    # Room for castling?
    empty_spaces_required_for_castling = [
        [3, 7, 2, 7, 1, 7, "bqsc_possible"],
        [5, 7, 6, 7, 6, 7, "bksc_possible"],  # (check twice to allow clean loop)
        [3, 0, 2, 0, 1, 0, "wqsc_possible"],
        [5, 0, 6, 0, 6, 0, "wksc_possible"]
    ]
    for e in empty_spaces_required_for_castling:
        if board[e[0]][e[1]] is "" and board[e[2]][e[3]] is "" and board[e[4]][e[5]] is "" and game_state[
            e[6]] is "blocked_by_pieces":
            game_state[e[6]] = True

    # Castling
    castle_variations = [
        ["wk", 4, 0, 6, 0, "wksc_possible", 7, 0, 5, 0, "wr"],
        ["wk", 4, 0, 2, 0, "wqsc_possible", 0, 0, 3, 0, "wr"],
        ["bk", 4, 7, 6, 7, "bksc_possible", 7, 7, 5, 7, "br"],
        ["bk", 4, 7, 2, 7, "bqsc_possible", 0, 7, 3, 7, "br"]
    ]
    for v in castle_variations:
        if piece is v[0] and x1 is v[1] and y1 is v[2] and x2 is v[3] and y2 is v[4] and game_state[v[5]] is True:
            board[v[6]][v[7]] = ""
            board[v[8]][v[9]] = v[10]
            game_state[v[5]] = False

    # Stuff that prevents castling
    moving_a_rook_for_the_first_time = [
        ["wr", 0, 0, "wqsc_possible"],
        ["wr", 7, 0, "wksc_possible"],
        ["br", 0, 7, "bqsc_possible"],
        ["br", 7, 7, "bksc_possible"],
    ]
    for m in moving_a_rook_for_the_first_time:
        if piece is m[0] and x1 is m[1] and y1 is m[2]:
            game_state[m[3]] = False
    moving_the_king_without_castling_first = [
        ["wk", 4, 0, "wksc_possible", "wqsc_possible"],
        ["bk", 4, 7, "bksc_possible", "bqsc_possible"]
    ]
    for m in moving_the_king_without_castling_first:
        if piece is m[0] and x1 is m[1] and y1 is m[2]:
            game_state[m[3]] = False
            game_state[m[4]] = False


def move_piece(m):
    piece = board[m[0]][m[1]]
    # print(legal(board, m[0], m[1], piece, game_state))
    if [m[2], m[3]] in all_legal_moves[m[0], m[1]]:
        destination = board[m[2]][m[3]]
        board[m[2]][m[3]] = piece
        board[m[0]][m[1]] = ""
        change_turn()
        get_all_legal_moves()
        # This might cause bugs
        del all_legal_moves[m[2], m[3]]
        del all_legal_moves[m[0], m[1]]
        check_stuff(m[0], m[1], m[2], m[3], piece)
        print(game_state)
        if destination is not "":
            print(piece + " at " + str(m[0]) + "," + str(m[1]) + " captured " + destination + " at " + str(
                m[2]) + "," + str(m[3]))
        else:
            print(piece + " at " + str(m[0]) + "," + str(m[1]) + " moved to " + str(m[2]) + "," + str(m[3]))
    else:
        print("Illegal move")
    checkmate()
    print(game_state["players_turn"] + " to move")


def render():
    global game_frame
    game_frame = tk.Frame(root)
    root.title("Chess")
    game_frame.pack()
    root.geometry("700x688")
    font_style = tkFont.Font(family="Arial", size=20)
    for i, row in (enumerate(board)):
        for j, column in enumerate(reversed(row)):
            mod = i % 2
            if j % 2 == mod:
                bg = 'white'
            else:
                bg = 'chocolate3'
            square = [i, abs(7 - j)]
            if legals_for_selected_tile is not None:
                if square in legals_for_selected_tile:
                    bg = 'royal blue'

            l = tk.Label(game_frame, text=toUnicode.get(column), bg=bg, font=font_style)
            # x = int('{}{}'.format(i,j ))
            # L = tk.Label(gameframe, text=x , bg=bg, font=fontStyle)
            l.config(width=2)
            l.config(height=1)
            l.config(font=("Arial", 53))
            l.grid(row=j, column=i)
            l.bind('<Button-1>', lambda e, i=i, j=j: on_click(i, j))


def start():
    render()
    print(game_state["players_turn"] + " to move")
    root.mainloop()


if __name__ == '__main__':
    start()

