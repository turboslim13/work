from tkinter import *
from random import randint


def reset(event: Event, random_choice: bool) -> None:
    global GAME_IS_RUNNING, CELL_COUNT
    if random_choice:
        choice_var.set(randint(0, 1))
    for row in buttons:
        for butt in row:
            butt['text'] = ''
    label['text'] = ' '
    GAME_IS_RUNNING = True
    CELL_COUNT = int(DIMENSION)


def check_end(event: Event) -> None:
    global CELL_COUNT, GAME_IS_RUNNING

    origin_ind = CELL_POSITIONS[event.widget]
    for i in (-1, 0):
        for j in (-1, 0, 1):
            if i == 0 and j == 0: break
            line_length = 0
            depth_levels = [1, 1]
            ray = 0
            while True:
                cell_ind = origin_ind[0] + i*depth_levels[ray],\
                           origin_ind[1] + j*depth_levels[ray]
                if (0 <= cell_ind[0] < SIDE_LENGTH and\
                        0 <= cell_ind[1] < SIDE_LENGTH) and\
                        (buttons[cell_ind[0]][cell_ind[1]]['text'] ==\
                        event.widget['text']):
                    line_length += 1
                    depth_levels[ray] += 1
                    if line_length + 1 == LINE_LENGTH:
                        GAME_IS_RUNNING = False
                        for step in range(line_length + 1):
                            buttons[cell_ind[0] + (-i*step)]\
                                [cell_ind[1] + (-j*step)]['foreground'] = \
                                '#5c5c5c' 
                        label['text'] = event.widget['text'] + ' Выиграли!'
                        return
                else:
                    depth_levels[ray] = 0
                    if depth_levels[0] == 0 and depth_levels[1] == 0:
                        break
                
                if depth_levels[not ray] != 0:
                    i, j = -i, -j
                    ray = 1 if ray == 0 else 0

    CELL_COUNT -= 1
    if CELL_COUNT == 0: 
        GAME_IS_RUNNING = False
        for i in range(SIDE_LENGTH):
            for j in range(SIDE_LENGTH):
                buttons[i][j]['foreground'] = '#5c5c5c'
        label['text'] = 'Ничья!'
        return


def click(event: Event) -> None:
    if GAME_IS_RUNNING and not event.widget['text']:
        if choice_var.get():
            event.widget['text'] = 'X' 
            event.widget['foreground']='#f29c94'
        else:
            event.widget['text'] = 'O'
            event.widget['foreground']='#a785cc'
        choice_var.set(not choice_var.get())
        check_end(event)

# -------------------------------Константы--------------------------------------
SIDE_LENGTH = 8
LINE_LENGTH = 5
DIMENSION = SIDE_LENGTH * SIDE_LENGTH
GAME_IS_RUNNING = True
CELL_COUNT = int(DIMENSION)

CELL_SIZE = 4
CELL_POSITIONS = {}
ROOT = Tk()
ROOT.geometry(f'210x440')
ROOT.title('Крестики-нолики')

# ------------------------------Радио-кнопки------------------------------------
choice_var = BooleanVar()
choice_var.set(randint(0, 1))
choice_frame = Frame(ROOT)

x_rd_butt = Radiobutton(
    choice_frame, text='X', variable=choice_var, value=1)
o_rd_butt = Radiobutton(
    choice_frame, text='O', variable=choice_var, value=0)

x_rd_butt.bind('<Button-1>', 
    lambda event, random_choice=False: reset(event, random_choice))
o_rd_butt.bind('<Button-1>',
    lambda event, random_choice=False: reset(event, random_choice))

# ----------------------------------Поле----------------------------------------
field_frame = Frame(ROOT)
buttons = []
for i in range(SIDE_LENGTH):
    row = []
    for j in range(SIDE_LENGTH):
        butt = Button(   
            field_frame, text='', width=CELL_SIZE, height= \
            CELL_SIZE // 2, background='#edf2e6', font=('Arial Black', 16), 
            foreground='grey')
        butt.bind('<Button-1>', click)
        row.append(butt)
        CELL_POSITIONS[butt] = (i, j)
    buttons.append(row)

# --------------------------Метка результата игры-------------------------------
label = Label(ROOT, font=('Arial Black', 15), foreground='#5c5c5c')

# ---------------------------Кнопка 'Новая игра'--------------------------------
butt = Button(ROOT, text='Новая игра', width=20, height=2)
butt.bind('<Button-1>',
    lambda event, random_choice=True: reset(event, random_choice))

# --------------------------Расположение по сетке-------------------------------
x_rd_butt.grid(column=0, row=0)
o_rd_butt.grid(column=1, row=0)
choice_frame.grid(column=0, row=0, pady=10)
field_frame.grid(column=0, row=1)
for i in range(SIDE_LENGTH):
    for j in range(SIDE_LENGTH):
        buttons[i][j].grid(column=j, row=i)
label.grid(column=0, row=2, pady=20)
butt.grid(column=0, row=3)

# ------------------------------Главный цикл------------------------------------
ROOT.mainloop()