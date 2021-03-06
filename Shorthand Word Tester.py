from tkinter import *
from random import shuffle
from db_manager import Database
import filter_settings
import help_menu


def render():
    root = Tk()
    root.title("Shorthand Word Tester")
    root.geometry('400x200')
    root.minsize(300, 200)
    root.bind("<space>", lambda event: new_word(word_lbl))

    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Edit Filters", command=open_filter_settings)
    file_menu.add_command(label="Help", command=open_help_menu)

    main_frame = Frame(root)
    instructions_lbl = Label(main_frame, text="Press spacebar to receive a random word", font=("Calibri", 10))
    word_lbl = Label(main_frame, font=("Calibri", 12, "bold"))
    btn = Button(main_frame, text="New Word", command=lambda: new_word(word_lbl))

    padding_y = 10
    instructions_lbl.grid(column=0, row=0, pady=padding_y)
    word_lbl.grid(column=0, row=3, pady=padding_y)
    btn.grid(column=0, row=1, pady=padding_y)

    main_frame.place(anchor="center", relx="0.5", rely="0.4")
    root.config(menu=menu_bar)
    root.mainloop()


def open_filter_settings():
    filter_settings.open(db)


def open_help_menu():
    help_menu.open(db)


def init_dictionary():
    global dictionary
    dictionary = db.get_dictionary()
    shuffle(dictionary)


def new_word(label):
    if len(dictionary) == 0:
        init_dictionary()
    label.config(text=dictionary.pop().capitalize())


dictionary = []
db = Database()
init_dictionary()
render()
db.close()


