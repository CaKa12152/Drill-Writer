from tkinter import *
import importlib
import random  # Make sure to import random, as it's used in moves()

root = Tk()
window_width = 450
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

icon = PhotoImage(file=r"src/img/Icon.png")
root.iconphoto(True, icon)

root.resizable(False, False)

def open():
    root.destroy()
    file1 = importlib.import_module('src.vivace')
    file1.Start()

def moves():
    # Move the rectangle to the right by a random amount between 1 and 5 pixels
    canvas.move(c, random.randrange(1, 5), 0)

def start_movement():
    if canvas.coords(c)[0] <= -2:  # If the box has moved off the left side of the screen
        moves()
        root.after(random.randrange(1, 10), start_movement)
    else:
        root.after(2000, open)  # Delay the open() call by 2000ms (2 seconds)

# Load background with Pillow (ImageTk.PhotoImage for labels)
background = PhotoImage(file=r"src/img/BG.png")

bg = Label(root, image=background)
bg.place(x=-2, y=-2)

canvas = Canvas(root, width=460, height=12, bd=0, highlightthickness=0, bg="#121212")
canvas.place(x=0, y=288)

# Create the orange rectangle at the leftmost position
c = canvas.create_rectangle(0, 0, -460, 12, fill="orange", outline="")

root.after(1000, start_movement)

root.overrideredirect(True)

root.mainloop()