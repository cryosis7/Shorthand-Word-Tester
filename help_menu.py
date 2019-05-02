from tkinter import *


def open(db_manager_instance):
    global db
    db = db_manager_instance

    window = Toplevel()
    window.grab_set()
    window.title("Help")
    window.minsize(500, 500)

    msg = StringVar()
    help_txt = Message(window, textvariable=msg, width=400)

    msg.set("Welcome to the Shorthand Word Tester\n\n"
            "This application was developed with the purpose in mind to train yourself to make use of all the prefixes,"
            " suffixes and other shortcuts available to you in your chosen method of shorthand.\n\n"
            "The program will filter down a full English dictionary based on the chosen filters, then will give words"
            " to you at random.\nYou should then write these words out on paper. After writing several words down - "
            "go back and translate what you have written.\n\n\n"
            "-------- HOW TO USE --------\n\n"
            "Open the edit filters window from the menu.\n"
            "Add or remove any filters that you wish.\n"
            "A PREFIX is a letter combination that a word MUST START with.\n"
            "A PHRASE is a combination that may appear ANYWHERE in the word\n"
            "A SUFFIX is a combination that MUST appear at the END of the word.\n\n"
            "From the main window, you can press the space bar or the button to receive a new word.\n\n"
            "-------------------------------------------------\n\n"
            "Developed By Scott Curtis")

    help_txt.place(anchor="center", relx="0.5", rely="0.5")
    window.mainloop()
