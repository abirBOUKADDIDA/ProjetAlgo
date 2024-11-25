import tkinter as tk
from random import randint

num_tri = 0
trionimo_colors = {}

def create_board(n):
    rows = [[] for _ in range(n)]
    for i in range(n):
        rows[i] = [0] * (n)
    return rows

def add_defect(board, row, col):
    board[row-1][col-1] = -1

def locate_defect(board, r1, c1, r2, c2):
    r = 0
    c = 0
    loc_ = []
    for i in range(r1, r2 + 1):
        loc_[:] = board[i][c1:c2 + 1]
        if -1 in loc_:
            c = loc_.index(-1) + c1
            r = i
            break
    if r <= r1 + (r2 - r1) // 2:
        if c <= c1 + (c2 - c1) // 2:
            return 0, r, c
        else:
            return 1, r, c
    else:
        if c <= c1 + (c2 - c1) // 2:
            return 2, r, c
        else:
            return 3, r, c

def add_trionimo(board, defect, r1, c1, r2, c2):
    global num_tri
    dict_ = {
        0: (r1, c1),
        1: (r1, c2),
        2: (r2, c1),
        3: (r2, c2),
    }
    num_tri += 1
    trionimo_colors[num_tri] = "#{:06x}".format(randint(0, 0xFFFFFF))
    for i in range(r1, r2 + 1):
        board[i][c1:c2+1] = [num_tri]*(r2-r1 + 1)
    rd, cd = dict_[defect]
    board[rd][cd] = -1

def tile_rec(board, r1, c1, r2, c2):
    global num_tri
    dict_ = {
        0: (r1 + (r2 - r1)//2, c1 + (c2 - c1)//2),
        1: (r1 + (r2 - r1)//2, c1 + (c2 - c1)//2 + 1),
        2: (r1 + (r2 - r1)//2 + 1, c1 + (c2 - c1)//2),
        3: (r1 + (r2 - r1)//2 + 1, c1 + (c2 - c1)//2 + 1),
    }
    defect, r, c = locate_defect(board, r1, c1, r2, c2)
    if (r1 == r2 - 1) and (c1 == c2 - 1):
        add_trionimo(board, defect, r1, c1, r2, c2)
        return None
    else:
        redo = True
        for value in dict_.values():
            if board[value[0]][value[1]] == 0:
                board[value[0]][value[1]] = -1
            else:
                redo = False
        if redo:
            board[dict_[defect][0]][dict_[defect][1]] = 0
        tile_rec(board, r1, c1, r1 + (r2-r1)//2, c1 + (c2 - c1)//2)
        tile_rec(board, r1, c1 + (c2 - c1)//2 + 1, r1 + (r2-r1)//2, c2)
        tile_rec(board, r1 + (r2-r1)//2 + 1, c1, r2, c1 + (c2 - c1)//2)
        tile_rec(board, r1 + (r2-r1)//2 + 1, c1 + (c2 - c1)//2 + 1, r2, c2)
        num_tri += 1
        redo = True
        for value in dict_.values():
            if board[value[0]][value[1]] == -1:
                board[value[0]][value[1]] = num_tri
            else:
                redo = False
        if redo:
            board[dict_[defect][0]][dict_[defect][1]] = -1

def draw_chessboard_with_defect(board, root):
    canvas_size = 400
    square_size = canvas_size // len(board)
    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
    canvas.pack(side=tk.LEFT)
    for i in range(len(board)):
        for j in range(len(board[i])):
            color = "white" if board[i][j] == 0 else "black" if board[i][j] == -1 else trionimo_colors.get(board[i][j], "yellow")
            draw_square(canvas, i + 1, j + 1, square_size, color)

def draw_square(canvas, row, col, size, color):
    x1 = (col - 1) * size
    y1 = (row - 1) * size
    x2 = x1 + size
    y2 = y1 + size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)

def tile(board, n):
    tile_rec(board, 0, 0, n - 1, n - 1)
    return board

def start_tiling():
    k_value = int(k_entry.get())
    defect_row = int(row_entry.get())
    defect_col = int(col_entry.get())

    board = create_board(k_value)
    add_defect(board, defect_row, defect_col)

    draw_chessboard_with_defect(board, root)

    result_board = tile(board, k_value)
    draw_chessboard_with_defect(result_board, root)

root = tk.Tk()
root.title("Chessboard with User-defined Defect")

input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, pady=10)

tk.Label(input_frame, text="Valeur de n (taille de l'échiquier n) :").pack(anchor="w")
k_entry = tk.Entry(input_frame)
k_entry.pack()

tk.Label(input_frame, text="Coordonnée de la ligne du défaut :").pack(anchor="w")
row_entry = tk.Entry(input_frame)
row_entry.pack()

tk.Label(input_frame, text="Coordonnée de la colonne du défaut :").pack(anchor="w")
col_entry = tk.Entry(input_frame)
col_entry.pack()

tk.Button(input_frame, text="Lancer le carrelage", command=start_tiling).pack(pady=10)

root.mainloop()
