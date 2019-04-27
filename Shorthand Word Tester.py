from tkinter import *
from random import shuffle


def edit_filters():
    return


def open_dictionary():
    return


def reset_dictionary():
    global dictionary
    dictionary_file = open('dictionary_filtered.txt', 'r')
    dictionary = dictionary_file.read().split('\n')
    dictionary_file.close()
    shuffle(dictionary)


def new_word(label):
    if len(dictionary) == 0:
        reset_dictionary()
    label.config(text=dictionary.pop().capitalize())


def render():
    root = Tk()
    root.title("Shorthand Word Tester")
    root.geometry('400x200')
    root.minsize(300, 200)
    root.bind("<space>", lambda event: new_word(word_lbl))

    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Edit Filters", command=edit_filters)
    file_menu.add_command(label="Open Dictionary...", command=open_dictionary)

    menu_bar.add_cascade(label="File", menu=file_menu)

    frame = Frame(root)
    instructions_lbl = Label(frame, text="Press spacebar to receive a random word", font=("Calibri", 10))
    word_lbl = Label(frame, font=("Calibri", 12, "bold"))
    btn = Button(frame, text="New Word", command=lambda: new_word(word_lbl))

    instructions_lbl.grid(column=0, row=0, pady="10")
    word_lbl.grid(column=0, row=3, pady="10")
    btn.grid(column=0, row=1, pady="10")

    frame.place(anchor="center", relx="0.5", rely="0.4")
    root.config(menu=menu_bar)
    root.mainloop()


dictionary = []
reset_dictionary()
render()


