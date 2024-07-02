import customtkinter
from tkinter import filedialog
from Analyzing.GraphicalInterface.UIComponents import ChannelSelectionDialog
import tdt

# Example usage:
root = customtkinter.CTk()
root.geometry("644x434")

root.directory = filedialog.askdirectory(initialdir=".",
                                         title='Please select signal(s) from the list.')
print(root.directory)
data = tdt.read_block(root.directory)

onsets = data['epocs'].Tr1_.onset
offsets = data['epocs'].Tr1_.offset

checkbox_items = []
for key in data['streams'].keys():
    if len(data['streams'][key]['data'].shape) == 1:
        checkbox_items.append((key, 0))
    else:
        for i in range(data['streams'][key]['data'].shape[0]):
            checkbox_items.append((key + '_channel_' + str(i), 0))

# checkbox_items = [(key, 0) for key in data['streams'].keys()]
dialog = ChannelSelectionDialog(checkbox_items=checkbox_items, title="Custom Dialog")
print("Result:", dialog.get_input())

# button = tk.Button(root, text="Open Dialog", command=open_dialog)
# button.pack()

root.mainloop()
