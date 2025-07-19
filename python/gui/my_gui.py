# first GUI
from tkinter import Tk, Label, Button  # <-- You need this import

root = Tk()
root.title("My First GUI")

# create a label
label = Label(root, text="Hello, World!")
label.pack()

# create a button
def on_button_click():
    label.config(text="Button Clicked!")

button = Button(root, text="Click Me", command=on_button_click)
button.pack()

# run the application
root.mainloop()