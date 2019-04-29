from tkinter import *
from random import shuffle


def add_to_listbox(listbox, entry):
    s = entry.get()
    if s:
        listbox.add_filter(END, s)
        entry.delete(0, len(s))


def delete_from_listbox(listbox):
    selection = listbox.curselection()
    if selection:
        listbox.delete(selection[0])


def open_filter_settings():
    settings = Toplevel()
    settings.title("Filter Settings")
    settings.minsize(300, 300)

    main_frame = Frame(settings)
    prefix_lbl = Label(main_frame, text="Prefixes")

    # Listbox with Scrollbar
    prefix_lb_frame = Frame(main_frame)
    prefix_lb_scrollbar = Scrollbar(prefix_lb_frame)
    prefix_listbox = Listbox(prefix_lb_frame, selectmode="SINGLE", yscrollcommand=prefix_lb_scrollbar.set)
    prefix_lb_scrollbar.config(command=prefix_listbox.yview)
    for x in range(20):
        prefix_listbox.insert(END, "Item {}".format(x))
    prefix_lb_scrollbar.pack(side=RIGHT, fill=Y)
    prefix_listbox.pack(side=LEFT, fill=BOTH)

    # Delete Buttons
    delete_frame = Frame(main_frame)
    prefix_del_btn = Button(delete_frame, text="Delete", command=lambda: delete_from_listbox(prefix_listbox))
    prefix_del_all_btn = Button(delete_frame, text="Delete All", command=lambda: prefix_listbox.delete(0, END))
    prefix_del_btn.grid(column=0, row=2, padx=5)
    prefix_del_all_btn.grid(column=1, row=2, padx=5)

    # Entry Field and Add Button
    new_entry_frame = Frame(main_frame)
    prefix_add_button = Button(new_entry_frame, text="Add", command=lambda: add_to_listbox(prefix_listbox, prefix_entry))
    prefix_entry = Entry(new_entry_frame, exportselection=0)
    prefix_entry.bind("<Return>", lambda x: add_to_listbox(prefix_listbox, prefix_entry))
    prefix_entry.grid(column=0, columnspan=2, row=0)
    prefix_add_button.grid(column=2, row=0, padx=10)

    padding_y = 5
    prefix_lbl.grid(column=0, row=0, pady=padding_y)
    prefix_lb_frame.grid(column=0, row=1, pady=padding_y)
    delete_frame.grid(column=0, row=2, pady=padding_y)
    new_entry_frame.grid(column=0, row=3, pady=padding_y)
    main_frame.place(anchor="center", relx="0.5", rely="0.5")


def open_dictionary():
    return


def reset_dictionary():
    global dictionary
    dictionary_file = open('dictionary_filtered_sql.txt', 'r')
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
    file_menu.add_command(label="Edit Filters", command=open_filter_settings)
    file_menu.add_command(label="Open Dictionary...", command=open_dictionary)

    menu_bar.add_cascade(label="File", menu=file_menu)

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


dictionary = []
reset_dictionary()
render()


