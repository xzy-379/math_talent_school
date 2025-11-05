import tkinter as tk

import input_files.data_read as data_read

file = "test_data\01.json"

x = data_read.check(file)
print(x)
root = tk.Tk()
root.title = "talent_school"

# Create a label widget
label = tk.Label(root, text="Click the button")
label.pack()

# Run the main event loop
root.mainloop()
