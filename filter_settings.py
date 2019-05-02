from tkinter import *
from tkinter.ttk import Separator
from db_manager import Database


def open(db_manager_instance):
    global db
    db = db_manager_instance
    filter_lb_list = []

    settings = Toplevel()
    settings.grab_set()
    settings.title("Filter Settings")
    settings.minsize(750, 450)

    main_frame = Frame(settings)

    title_lbl = Label(main_frame, text="Add or Remove Filters", font=("Calibri", 14))

    # Creates a frame that contains the three filters and their components
    filter_frame = Frame(main_frame)
    prefix_frame = create_filter_frame(filter_frame, Database.PREFIX, filter_lb_list)
    phrase_frame = create_filter_frame(filter_frame, Database.PHRASE, filter_lb_list)
    suffix_frame = create_filter_frame(filter_frame, Database.SUFFIX, filter_lb_list)
    padding_x = 25
    prefix_frame.grid(column=0, row=0, padx=padding_x)
    Separator(filter_frame, orient=VERTICAL).grid(column=1, row=0, sticky='wns')
    phrase_frame.grid(column=1, row=0, padx=padding_x)
    Separator(filter_frame, orient=VERTICAL).grid(column=2, row=0, sticky='wns')
    suffix_frame.grid(column=2, row=0, padx=padding_x)

    # Creates a frame containing the save and cancel buttons
    save_cancel_frame = Frame(main_frame)
    cancel_btn = Button(save_cancel_frame, text="Cancel", width=10, command=settings.destroy)
    save_btn = Button(save_cancel_frame, text="Save", width=10, command=lambda: save_changes(filter_lb_list))
    cancel_btn.grid(column=0, row=0, padx=20)
    save_btn.grid(column=1, row=0, padx=20)

    title_lbl.grid(column=0, row=0, pady=10)
    filter_frame.grid(column=0, row=1)
    save_cancel_frame.grid(column=0, row=2, pady=30)
    main_frame.place(anchor="center", relx="0.5", rely="0.50")


# Creates a frame containing the components to edit the 3 types of filters.
def create_filter_frame(parent_frame, filter_type, filter_lb_list):
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
    filter_lb_list.append((listbox, filter_type))

    # Delete Buttons
    delete_frame = Frame(filter_frame)
    del_btn = Button(delete_frame, text="Delete", width=7, command=lambda: delete_filter(listbox))
    del_all_btn = Button(delete_frame, text="Delete All", width=7,
                         command=lambda: listbox.delete(0, END))
    del_btn.grid(column=0, row=0, padx=10)
    del_all_btn.grid(column=1, row=0, padx=10)

    # Entry Field and Add Button
    new_entry_frame = Frame(filter_frame)
    add_button = Button(new_entry_frame, text="Add", width=5,
                        command=lambda: add_filter_from_entry(listbox, entry))
    entry = Entry(new_entry_frame, exportselection=0)
    entry.bind("<Return>", lambda key: add_filter_from_entry(listbox, entry))
    entry.grid(column=0, row=0)
    add_button.grid(column=1, row=0, padx=10)

    # Adding all the main element frames into the filter frame
    padding_y = 5
    title_lbl.grid(column=0, row=0, pady=padding_y)
    lb_frame.grid(column=0, row=1, pady=padding_y)
    delete_frame.grid(column=0, row=2, pady=padding_y)
    new_entry_frame.grid(column=0, row=3, pady=padding_y)
    return filter_frame


# Rewrites the list boxes filters into the database
# TODO: Check data is formatted right
def save_changes(filter_lb_list):
    db.delete_all_filters()
    for filter_info in filter_lb_list:
        filter_list = filter_info[0].get(0, END)
        filter_type = filter_info[1]
        db.add_filters(filter_list, filter_type)
        render_listbox(filter_info[0], filter_type)


# Empties and refills a listbox with the given filter type from the database
def render_listbox(listbox, filter_type):
    listbox.delete(0, END)
    for filter_name in db.get_filters(filter_type):
        listbox.insert(END, filter_name)


# Takes the value from the entry box and adds it to the listbox
def add_filter_from_entry(listbox, entry):
    text = entry.get()
    text = ''.join([i for i in text.lower() if i.isalpha() or i == '-'])
    if text:
        entry.delete(0, END)
        listbox.insert(END, text)
        listbox.see(END)


# Deletes the selection from the listbox
def delete_filter(listbox):
    selection = listbox.curselection()
    if selection:
        listbox.delete(selection)
