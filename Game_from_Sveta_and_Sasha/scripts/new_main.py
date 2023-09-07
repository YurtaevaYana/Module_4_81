import tkinter as tk
from PIL import Image, ImageTk
import pygame
import random
import pyglet
from datetime import datetime
pyglet.font.add_file('../Font.ttf')
pygame.init()

clock = pygame.time.Clock()

jazz = pygame.mixer.Sound('../music/jazz.mp3')
main_game_sound = pygame.mixer.Sound('../music/main_game.mp3')

window = tk.Tk()
window.config(bg = 'orange')
window.geometry('750x592+250+50')
window.title('Найди пару')
window.resizable(False, False)

for c in range(9):
    window.columnconfigure(index=c, weight=1)
for r in range(8):
    window.rowconfigure(index=r, weight=1)

time_timer = 0
after_id = ''

clicks = 0
score = 0
now_level = None
buttons = []
new_colors = []
pictures_at_buttons = []
saved_pictures = []
pictures = []
last_moves = []
true_pictures = []
new_letters = []
pictures_index = -1
change_volume_check = False
secret_level_list = 'Спасибо за всё, Яна!'.upper()

colors = ['#f05946', '#ffa34d', '#f7f25e', '#8be362', '#aaebf0', '#7687de', '#b176de']
colors = colors * 10
levels_name_list = ['3 на 4 клеток\n на поле', '4 на 4 клеток\n на поле', '4 на 5 клеток\n на поле', 'секретный \n уровень']

background = Image.open('../sprites/background.png')
play_button = Image.open('../sprites/play.png')
volume = Image.open('../sprites/volume.png')
no_volume = Image.open('../sprites/no-volume.png')
quit_pic = Image.open('../sprites/exit.png')
menu_bg = Image.open('../sprites/menu_background.png')
home_bg = Image.open('../sprites/home.png')
locked_lvl= Image.open('../sprites/locked_lvl.png')
bronze = Image.open('../sprites/bronze.png')
silver = Image.open('../sprites/silver.png')
gold = Image.open('../sprites/gold.png')

volume_photo = ImageTk.PhotoImage(volume)
no_volume_photo = ImageTk.PhotoImage(no_volume)
play_button_photo = ImageTk.PhotoImage(play_button)
background_photo = ImageTk.PhotoImage(background)
quit_photo = ImageTk.PhotoImage(quit_pic)
menu_bg_photo = ImageTk.PhotoImage(menu_bg)
home_photo = ImageTk.PhotoImage(home_bg)
locked_lvl_photo = ImageTk.PhotoImage(locked_lvl)
bronze_photo = ImageTk.PhotoImage(bronze)
silver_photo = ImageTk.PhotoImage(silver)
gold_photo = ImageTk.PhotoImage(gold)

fr_1 = Image.open('../sprites/1_lvl.png')
fr_1_p = ImageTk.PhotoImage(fr_1)
fr_2 = Image.open('../sprites/2_lvl.png')
fr_2_p = ImageTk.PhotoImage(fr_2)
fr_3 = Image.open('../sprites/3_lvl.png')
fr_3_p = ImageTk.PhotoImage(fr_3)
fr_4 = Image.open('../sprites/secret.png')
fr_4_p = ImageTk.PhotoImage(fr_4)

panel = tk.Label(window, image = menu_bg_photo)
panel.place(x=0, y=0)

def tick():
    global  after_id, time_timer
    after_id = window.after(1000, tick)
    f_time = datetime.fromtimestamp(time_timer).strftime('%M:%S')
    time_label.configure(text=f'Время: \n{f_time}')
    time_timer += 1

def start_timer():
    tick()

def timer_clear():
    global time_timer
    time_timer = 0

def timer_zero():
    window.after_cancel(after_id)

def make_picture_list(ROW, COLUMNS):
    global pictures
    list_len = ROW * COLUMNS / 2
    while list_len != 0:
        pictures.append(f'frame{int(list_len)}.png')
        list_len -= 1
    pictures = pictures * 2
    make_buttons(ROW, COLUMNS)

def button_main(i, j, ROW, COLUMNS):
    global clicks
    if clicks == 2:
        clicks = 1
        if check_true_of_pictures():
            clicks = 1
        else:
            hide_pictures()
        last_moves.clear()
        show_picture(i, j)
        last_moves.append([i, j])
        if show_picture(i, j):
            win_screen_clear()
    else:
        if show_picture(i, j):
            clicks = 1
        else:
            show_picture(i, j)
            last_moves.append([i,j])
            clicks += 1

def button_secret(i, j):
    btn = buttons[i][j]
    btn['text'] = new_letters[i][j]
    btn['bg'] = new_colors[i][j]

def check_true_of_pictures():
    pic1 = saved_pictures[last_moves[0][0]][last_moves[0][1]]
    pic2 = saved_pictures[last_moves[1][0]][last_moves[1][1]]
    if pic1 == pic2:
        if last_moves[0][0] == last_moves[1][0] and last_moves[0][1] == last_moves[1][1]:
            hide_pictures()
        else:
            try:
                true_pictures.remove([last_moves[0][0], last_moves[0][1]])
                true_pictures.remove([last_moves[1][0], last_moves[1][1]])
            except:
                pass
    else:
        hide_pictures()
    last_moves.clear()
    return True

def hide_pictures():
    for i in true_pictures:
        btn = buttons[i[0]][i[1]]
        btn['image'] = background_photo

def show_picture(i, j):
    if len(true_pictures) ==0:
        return True
    else:
        btn = buttons[i][j]
        btn['image'] = pictures_at_buttons[i][j]

def secret_level_scene(ROW,COLUMNS):
    global pictures_index, saved_pictures, pictures, new_letters, temp, colors
    number_of_letter = -1
    for i in range(ROW):
        temp = []
        pictures_index += 1
        new_letters.append(list())
        new_colors.append(list())
        for j in range(COLUMNS):

            number_of_letter += 1
            btn = tk.Button(window, width=4, height=3, font=('Franklin Gothic Heavy', 25), borderwidth=4, relief="solid",bg = '#f7fa52', fg = 'black', command=lambda x=i, y=j, ROW=ROW, COLUMNS=COLUMNS: button_secret(x,y))
            temp.append(btn)
            new_colors[pictures_index].append(colors[number_of_letter])
            new_letters[pictures_index].append(secret_level_list[number_of_letter])

        buttons.append(temp)

    main(ROW, COLUMNS)

def make_buttons(ROW, COLUMNS):
    global pictures_index, saved_pictures, pictures, pictures_at_buttons, temp

    for i in range(ROW):
        temp = []
        pictures_index += 1
        pictures_at_buttons.append(list())
        saved_pictures.append(list())
        for j in range(COLUMNS):
            random_picture = random.choice(pictures)
            image = Image.open(f'../sprites/{random_picture}')
            photo = ImageTk.PhotoImage(image)

            pictures.remove(random_picture)

            btn = tk.Button(window, width=150, height=150, borderwidth=4, relief="solid", image = background_photo, command=lambda x = i, y = j, ROW = ROW, COLUMNS = COLUMNS: button_main(x, y, ROW, COLUMNS))
            temp.append(btn)
            true_pictures.append([i, j])

            pictures_at_buttons[pictures_index].append(photo)
            saved_pictures[pictures_index].append(random_picture)

        buttons.append(temp)
    main(ROW, COLUMNS)

def main(ROW, COLUMNS):
    global now_level, timer_true
    try:
        jazz.stop()
    except:
        pass
    main_game_sound.play(0,0,0)
    window.config(bg='orange')
    clear_screen()
    try:
        timer_zero()
        timer_clear()
    except:
        pass
    start_timer()
    if ROW == 4 and COLUMNS == 5:
        now_level = '4_5'
        window.geometry('935x650')
        time_label.grid(row=2, column=COLUMNS + 1, pady=1, padx=4)
    elif ROW == 4 and COLUMNS == 4:
        now_level = '4_4'
        window.geometry('760x650')
        time_label.grid(row=2, column=COLUMNS + 1, pady=1, padx=4)
    elif ROW == 3 and COLUMNS == 4:
        now_level = '3_4'
        window.geometry('760x490')
        time_label.grid(row=2, column=COLUMNS + 1, pady=1, padx=4)
    elif ROW == 2 and COLUMNS == 10:
        window.geometry('1100x250')
        timer_zero()
        timer_clear()
    for i in range(ROW):
        for j in range(COLUMNS):
            btn = buttons[i][j]
            btn.grid(row=i, column=j, padx=3, pady=3)
    menu_button.grid(row=0, column=COLUMNS + 1, pady=1, padx=4)


def main_menu():
    try:
        main_game_sound.stop()
    except:
        pass
    jazz.play(0,0,0)
    window.config(bg='orange')
    panel.place(x=0, y=0)
    settings.place(x = 90,y = 235)
    play.place(x = 272.25,y = 212.5)
    quit_button.place(x = 510,y = 235)

def chose_level():
    window.config(bg='orange')
    clear_screen()
    first_level.grid(row=2, column=2, pady=1, padx=2)
    first_level_label.grid(row=3, column=2, pady=1, padx=2)
    second_level.grid(row=2, column=3, pady=1, padx=2)
    second_level_label.grid(row=3, column=3, pady=1, padx=2)
    third_level.grid(row=2, column=4, pady=1, padx=2)
    third_level_label.grid(row=3, column=4, pady=1, padx=2)
    secret_level.grid(row=2, column=5, pady=1, padx=2)
    secret_level_label.grid(row=3, column=5, pady=1)
    menu_button.grid(row=0, column=2)
    question.place(x=200, y = 80)

def change_volume():
    global change_volume_check
    if change_volume_check == False:
        try:
            jazz.set_volume(0)
            main_game_sound.set_volume(0)
        except:
            pass
        settings['image'] = no_volume_photo
        change_volume_check = True
    else:
        try:
            jazz.set_volume(1)
            main_game_sound.set_volume(1)
        except:
            pass
        settings['image'] = volume_photo
        change_volume_check = False

def forget_button_list():
    global temp, buttons, pictures_index
    try:
        pictures_index = -1
        pictures_at_buttons.clear()
        saved_pictures.clear()
        true_pictures.clear()
        buttons.clear()
        temp.clear()
    except:
        pass

def win_screen():
    global score, now_level
    timer_zero()
    time_label.grid(row=2, column=4, pady=1, padx=4)
    menu_button['width'] = 228
    menu_button['height'] = 228
    menu_button['relief'] = 'flat'
    if now_level == '3_4' and score == 0:
        score+= 1
        second_level['command'] = lambda x = 4, y = 4: make_picture_list(x, y)
        second_level['image'] = fr_2_p
        menu_button['image'] = bronze_photo
    elif now_level == '4_4' and score == 1:
        score += 1
        third_level['command'] = lambda x = 4, y = 5: make_picture_list(x, y)
        third_level['image'] = fr_3_p
        menu_button['image'] = silver_photo
    elif now_level == '4_5' and score == 2:
        score += 1
        secret_level['command'] = lambda x=2, y=10: secret_level_scene(x, y)
        secret_level['image'] = fr_4_p
        menu_button['image'] = gold_photo
    win_label.grid(row=1, column=2, columnspan=5)
    menu_button.grid(row=3, column=4, pady=2, padx=4)
    forget_button_list()

def clear_screen():
    for i in window.grid_slaves():
        i.grid_forget()
    for j in window.place_slaves():
        j.place_forget()

def win_screen_clear():
    for i in window.grid_slaves():
        i.grid_forget()
    for j in window.place_slaves():
        j.place_forget()
    win_screen()

def main_menu_clear():
    try:
        jazz.stop()
        main_game_sound.stop()
    except:
        pass
    forget_button_list()
    for i in window.grid_slaves():
        i.grid_forget()
    for j in window.place_slaves():
        j.place_forget()
    menu_button['image'] = home_photo
    menu_button['width'] = 98
    menu_button['height'] = 98
    menu_button['relief'] = 'solid'
    window.geometry('750x592')
    main_menu()

def quit():
    window.destroy()

settings = tk.Button(image = volume_photo, width=148, height=148, relief="solid", command = change_volume)
play = tk.Button(image=play_button_photo,width=198, height=198, relief="solid", command=chose_level)
quit_button = tk.Button(image = quit_photo, width=148, height=148, relief="solid", command= quit)

first_level = tk.Button(image = fr_1_p, width=148, height=148, borderwidth=4, relief="solid", command =lambda x = 3, y = 4: make_picture_list(x, y))
first_level_label = tk.Label(text = levels_name_list[0], bg = 'orange', font=('Franklin Gothic Heavy', 15) )
second_level = tk.Button(image = locked_lvl_photo, width=148, height=148, borderwidth=4, relief="solid")
second_level_label = tk.Label(text = levels_name_list[1], bg = 'orange', font=('Franklin Gothic Heavy', 15) )
third_level = tk.Button(image = locked_lvl_photo, width=148, height=148, borderwidth=4, relief="solid")
third_level_label = tk.Label(text = levels_name_list[2], bg = 'orange', font=('Franklin Gothic Heavy', 15) )
secret_level = tk.Button(image = locked_lvl_photo, width=148, height=148, borderwidth=4, relief="solid")
secret_level_label = tk.Label(text = levels_name_list[3], bg = 'orange', font=('Franklin Gothic Heavy', 15) )
menu_button = tk.Button(image = home_photo, width=98, height=98, borderwidth=4, relief="solid", font=('Franklin Gothic Heavy', 10), command= main_menu_clear)

game_name = tk.Label(window, text=f'Найди пару', bg = 'green', font=('Franklin Gothic Heavy', 45))
win_label = tk.Label(window, text = f'Вы выиграли', bg = 'orange', font = ('Franklin Gothic Heavy', 45))
question = tk.Label(window, text=f'Чтобы открыть следующий уровень\n пройдите предыдущий', bg = 'orange', font=('Franklin Gothic Heavy', 20))

time_label = tk.Label(window, bg = 'orange', font=('Franklin Gothic Heavy', 30))

main_menu()

window.mainloop()


