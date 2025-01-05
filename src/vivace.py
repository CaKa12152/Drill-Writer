import os
from tkinter import *
from PIL import Image, ImageTk
import importlib

# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Build absolute paths to the images based on the script's directory
bg_path = os.path.join(script_dir, 'img', 'x.png')
add_button_1_path = os.path.join(script_dir, 'img', 'add1.png')
add_button_2_path = os.path.join(script_dir, 'img', 'add2.png')
exit_asset_path = os.path.join(script_dir, 'img', 'exit.png')

# Initialize the main application window
app = Tk()
app.title('Drill Writer')

# Center the window on the screen
app.eval('tk::PlaceWindow . center')
window_width = 900
window_height = 500
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
app.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')


def open_project(name):
    app.destroy()
    load_project_ = importlib.import_module('src.project')
    load_project_.load_project(name, )



# Event handlers for Add button
def on_add_click(event):
    create_proj = importlib.import_module('src.Create_Project')
    ret_val = create_proj.Create_Popup()
    while ret_val[0] != 1:
        pass
    # Left off here, make the project open here
    open_project(ret_val[1])


def on_add_hover(event):
    # Change the Add button image on hover
    Add_Button.configure(image=add_button_2_tk)


def on_add_leave(event):
    # Revert the Add button image when hover ends
    Add_Button.configure(image=add_button_1_tk)


def on_escape(event):
    app.quit()  # Close the app when Escape key is pressed


# Load images using Pillow to preserve transparency
bg1 = Image.open(bg_path)
bg_tk = ImageTk.PhotoImage(bg1)

add_button_1 = Image.open(add_button_1_path)
add_button_1_tk = ImageTk.PhotoImage(add_button_1)

add_button_2 = Image.open(add_button_2_path)
add_button_2_tk = ImageTk.PhotoImage(add_button_2)

exit_asset = Image.open(exit_asset_path).convert("RGBA")  # Ensure transparency is preserved
exit_tk = ImageTk.PhotoImage(exit_asset)

# Background label with the background image
background1 = Label(app, image=bg_tk)
background1.pack(fill=BOTH, expand=True)

# Add button with the first image (normal state)
Add_Button = Label(app, image=add_button_1_tk, bd=0)
Add_Button.place(x=381.6, y=205)

# Create a canvas for the exit button
exit_canvas = Canvas(app, width=exit_tk.width(), height=exit_tk.height(), bd=0, highlightthickness=0, bg="#121212")
exit_canvas.place(x=39.5, y=0)

# Create the image on the canvas (ensure no border and proper placement)
exit_canvas.create_image(0, 0, anchor=NW, image=exit_tk)

# Bind events to the Add button
Add_Button.bind("<Button-1>", on_add_click)  # Click event
Add_Button.bind("<Enter>", on_add_hover)  # Hover event
Add_Button.bind("<Leave>", on_add_leave)  # Leave event

# Bind Escape key to close the application
app.bind('<Escape>', on_escape)
exit_canvas.bind("<Button-1>", on_escape)

# Make the window borderless and remove the title bar
app.overrideredirect(True)


# Start the Tkinter event loop
def Start():
    app.mainloop()
