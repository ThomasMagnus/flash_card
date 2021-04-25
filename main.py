from tkinter import *
import pandas as pd
from typing import final

BACKGROUND_COLOR: final(str) = "#B1DDC6"
to_learn = {}

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)


def translate():
    global count
    canvas.itemconfig(lang, text='English', fill='white')
    canvas.itemconfig(word, text=words_csv.English[count], fill='white')
    canvas.itemconfig(card_bg, image=english_bg)


timer = window.after(3000, translate)

count = 0


def create_csv():
    df = pd.DataFrame(to_learn)
    df.to_csv('data/words_to_learn.csv', index=False)


def read_csv():
    global words_csv, to_learn
    words_csv = pd.read_csv('data/words_to_learn.csv', index_col=False)
    to_learn = words_csv.to_dict(orient='records')


try:
    read_csv()
except FileNotFoundError:
    read_csv()
    create_csv()
    words_csv = pd.read_csv('data/words_to_learn.csv')

french = words_csv.French[0]
english = words_csv.English[0]


def is_know():
    to_learn.remove(to_learn[0])
    create_csv()
    word_count()


def word_count():
    global count
    count += 1
    canvas.itemconfig(lang, text='French', fill='black')
    canvas.itemconfig(word, fill='black')
    canvas.itemconfig(card_bg, image=card_front_img)
    french = words_csv.French[count]
    canvas.itemconfig(word, text=french)
    window.after(3000, translate)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file='images/card_front.png')
english_bg = PhotoImage(file='images/card_back.png')
card_bg = canvas.create_image(400, 270, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
lang = canvas.create_text(400, 150, text='French', font=('Arial', 40, 'italic'))
word = canvas.create_text(400, 263, text=french, font=('Arial', 60, 'bold'))

wrong_img = PhotoImage(file='images/wrong.png')
btn_wrong = Button(image=wrong_img, highlightthickness=0, command=word_count)
btn_wrong.grid(row=1, column=0, pady=10)

right_img = PhotoImage(file='images/right.png')
btn_right = Button(image=right_img, highlightthickness=0, command=is_know)
btn_right.grid(row=1, column=1, pady=10)

window.mainloop()
