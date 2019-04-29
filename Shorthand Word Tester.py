from tkinter import *
from tkinter.ttk import Separator
from random import shuffle
from db_manager import Database


# Takes the value from the entry box and adds it to the database
def add_filter_from_entry(listbox, entry, filter_type):
    text = entry.get()
    text = ''.join([i for i in text.lower() if i.isalpha() or i == '-'])
    if text:
        db.add_filter(text, filter_type)
        entry.delete(0, len(entry.get()))
        render_listbox(listbox, filter_type)


# Deletes the selection from the database and refreshes the listbox
def delete_filter(listbox, filter_type):
    selection = listbox.curselection()
    if selection:
        db.delete_filter(listbox.get(selection), filter_type)
        render_listbox(listbox, filter_type)


# Deletes all filters that match the type from the database and re-renders the listbox
def delete_all_filters(listbox, filter_type):
    db.delete_all_filters(filter_type)
    render_listbox(listbox, filter_type)


# Empties and refills a listbox with the given filter type from the database
def render_listbox(listbox, filter_type):
    listbox.delete(0, END)
    for filter_name in db.get_filters(filter_type):
        listbox.insert(END, filter_name)

    
def create_filter_frame(parent_frame, filter_type):
    filter_frame = Frame(parent_frame)
    
    title_lbl = Label(filter_frame, text=filter_type.capitalize())

    # Listbox with Scrollbar
    lb_frame = Frame(filter_frame)
    lb_scrollbar = Scrollbar(lb_frame)
    listbox = Listbox(lb_frame, selectmode="SINGLE", yscrollcommand=lb_scrollbar.set)
    lb_scrollbar.config(command=listbox.yview)
    lb_scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH)
    render_listbox(listbox, filter_type)

    # Delete Buttons
    delete_frame = Frame(filter_frame)
    del_btn = Button(delete_frame, text="Delete", command=lambda: delete_filter(listbox, filter_type))
    del_all_btn = Button(delete_frame, text="Delete All", command=lambda: delete_all_filters(listbox, filter_type))
    del_btn.grid(column=0, row=2, padx=5)
    del_all_btn.grid(column=1, row=2, padx=5)

    # Entry Field and Add Button
    new_entry_frame = Frame(filter_frame)
    add_button = Button(new_entry_frame, text="Add", command=lambda: add_filter_from_entry(listbox, entry, filter_type))
    entry = Entry(new_entry_frame, exportselection=0)
    entry.bind("<Return>", lambda key: add_filter_from_entry(listbox, entry, add_filter_from_entry))
    entry.grid(column=0, row=0)
    add_button.grid(column=1, row=0, padx=10)

    padding_y = 5
    title_lbl.grid(column=0, row=0, pady=padding_y)
    lb_frame.grid(column=0, row=1, pady=padding_y)
    delete_frame.grid(column=0, row=2, pady=padding_y)
    new_entry_frame.grid(column=0, row=3, pady=padding_y)
    return filter_frame


def open_filter_settings():
    settings = Toplevel()
    settings.grab_set()
    settings.title("Filter Settings")
    settings.minsize(700, 400)

    main_frame = Frame(settings)

    title_lbl = Label(main_frame, text="Add or Remove Filters", font=("Calibri", 14))

    filter_frame = Frame(main_frame)
    prefix_frame = create_filter_frame(filter_frame, Database.PREFIX)
    phrase_frame = create_filter_frame(filter_frame, Database.PHRASE)
    suffix_frame = create_filter_frame(filter_frame, Database.SUFFIX)
    padding_x = 25
    prefix_frame.grid(column=0, row=0, padx=padding_x)
    Separator(filter_frame, orient=VERTICAL).grid(column=1, row=0, sticky='wns')
    phrase_frame.grid(column=1, row=0, padx=padding_x)
    Separator(filter_frame, orient=VERTICAL).grid(column=2, row=0, sticky='wns')
    suffix_frame.grid(column=2, row=0, padx=padding_x)

    title_lbl.grid(column=0, row=0, pady=10)
    filter_frame.grid(column=0, row=1)
    main_frame.place(anchor="center", relx="0.5", rely="0.45")


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
db = Database()
reset_dictionary()
render()
db.close()


