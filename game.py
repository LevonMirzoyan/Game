import random
from copy import deepcopy
from functools import partial
from tkinter import messagebox
from tkinter import *

# знаковая переменная, определяющая ход какого игрока
sign = 0

# Создаем доску
global board
board = [[" " for x in range(3)] for y in range(3)]

# Проверьте, выиграл ли l(O/X) матч или нет
# в соответствии с правилами игры
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))

# Настройка текста на кнопке во время игры с другим игроком
def get_text(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        gb.destroy()
        box = messagebox.showinfo("Победа!", "Игрок 1 выиграл партию")
    elif winner(board, "O"):
        gb.destroy()
        box = messagebox.showinfo("Победа!", "Игрок 2 выиграл партию")
    elif (isfull()):
        gb.destroy()
        box = messagebox.showinfo("Ничья", "Ничья")

# Проверьте, может ли игрок нажать кнопку или нет

def isfree(i, j):
    return board[i][j] == " "

# Проверьте, заполнена доска или нет

def isfull():
    flag = True
    for i in board:
        if (i.count(' ') > 0):
            flag = False
    return flag

# Создайте графический интерфейс игрового поля для игры вместе с другим игроком

def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()

# Решается следующий ход системы

def pc():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner) - 1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge) - 1)
            return edge[move]

# Настройка символа на кнопке во время игры с системой

def get_text_pc(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    x = True
    if winner(board, "X"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Победа!", "Игрок выиграл партию")
    elif winner(board, "O"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Победа!", "Компьютер выиграл партию")
    elif (isfull()):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Ничья", "Ничья")
    if (x):
        if sign % 2 != 0:
            move = pc()
            button[move[0]][move[1]].config(state=DISABLED)
            get_text_pc(move[0], move[1], gb, l1, l2)

# Создайте графический интерфейс игрового поля для игры вместе с системой

def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()

# Инициализируйте игровое поле для игры с системой

def withpc(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Игра Крестики-Нолики")
    l1 = Button(game_board, text="Игрок : X", width=10)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Компьютер : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2)

# Инициализируйте игровое поле, чтобы играть с другим игроком

def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Игра Крестики-Нолики")
    l1 = Button(game_board, text="Игрок 1 : X", width=10)

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Игрок 2 : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pl(game_board, l1, l2)

# Меню игры

def play():
    menu = Tk()
    menu.geometry("350x170")
    menu.title("Игра Крестики-Нолики")
    wpc = partial(withpc, menu)
    wpl = partial(withplayer, menu)

    head = Button(menu, text="Игрок VS Игрок", command=wpl,
                  activeforeground='white',
                  activebackground="white", bg="blue",
                  fg="white", width=100, font='Helvetica', bd=10)

    B1 = Button(menu, text="Игрок VS Компьютер", command=wpc,
                activeforeground='white',
                activebackground="white", bg="blue",
                fg="white", width=100, font='Helvetica', bd=10)

    B2 = Button(menu, text="ВЫХОД", command=menu.quit,
                  activeforeground='white',
                  activebackground="white", bg="blue",
                  fg="white", width=100, font='Helvetica', bd=10)

    head.pack(side='top')
    B1.pack(side='top')
    B2.pack(side='bottom')
    menu.mainloop()

if __name__ == '__main__':
    play()
