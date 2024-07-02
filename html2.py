# from tkinter import *
import customtkinter
import tkinter as tk
from tkinter import filedialog
from Analyzing.GraphicalInterface.UIComponents import MyInputDialog


class CustomDialog(customtkinter.CTkInputDialog):
    def __init__(self, parent, title, checkbox_items):
        self.checkbox_items = checkbox_items
        self.result = []
        super().__init__(parent, title)

    def body(self, master):
        self.checkboxes = []
        for row, (text, _) in enumerate(self.checkbox_items):
            var = tk.IntVar()
            checkbox = customtkinter.CTkCheckBox(master, text=text, variable=var)
            checkbox.grid(row=row, column=0, sticky='w')
            self.checkboxes.append((var, text))
        return None

    def apply(self):
        self.result = [(text, var.get()) for var, text in self.checkboxes]


# Example usage:
root = customtkinter.CTk()


def open_dialog():
    checkbox_items = [("Option 1", 0), ("Option 2", 0), ("Option 3", 0)]  # Replace with your dynamic list
    # dialog = CTkCheckBoxDialog(checkbox_items, title="Custom Dialog")
    dialog = MyInputDialog(checkbox_items=checkbox_items, title="Custom Dialog")
    print("Result:", dialog.get_input())


root.directory = filedialog.askdirectory(initialdir=".",
                                         title='Please select a directory')
print(root.directory)

open_dialog()

# button = tk.Button(root, text="Open Dialog", command=open_dialog)
# button.pack()

root.mainloop()
