import os
import json
import pygame
from tkinter import *
from PIL import Image, ImageTk

# ---------------------------- Global Variables ----------------------------

# Root window setup
project = Tk()
project.geometry('977x750')
icon = PhotoImage(file=r"src/img/Icon.png")
project.iconphoto(True, icon)

canvas = Canvas(project, bg="#121212", width=977, height=750)
canvas.pack()

# Music playback control
playing_music = False

# Variables for marchers
marchers = []
selected_marcher = None

hash_x = [108]

tempo = 0
current_set = 0

properties_tab = 0

add_set_buttonimg = PhotoImage(file=r"src/img/add_set.png")

# creating the entire hash x values list
for i in range(9):

    for i in range(5):
        hash_x.append(hash_x[-1]+7.5)
    for i in range(5):
        hash_x.append(hash_x[-1]+8)

# ---------------------------- Image and Field Setup ----------------------------

# Load the field images
fields1 = Image.open("src/img/Field_dark.png")
fields2 = Image.open("src/img/Field_light.png")
fields3 = Image.open("src/img/Field_color.png")

# Load marcher images
marcher = Image.open("src/img/Marcher.png")
marcher_sel = Image.open("src/img/Marcher-Selected.png")

# Music control images
play_music = PhotoImage(file="src/img/PlayM.png")
pause_music = PhotoImage(file="src/img/PauseM.png")


# Resize factor for the images
def resize_image(image, factor):
    width, height = image.size
    new_width = width // factor
    new_height = height // factor
    return image.resize((new_width, new_height))


# Resize field images and marcher images
fields1_resized = resize_image(fields1, 9)
fields2_resized = resize_image(fields2, 9)
fields3_resized = resize_image(fields3, 9)

marcher1 = ImageTk.PhotoImage(resize_image(marcher, 80))
marcher_sel1 = ImageTk.PhotoImage(resize_image(marcher_sel, 80))

field_dark = ImageTk.PhotoImage(fields1_resized)
field_light = ImageTk.PhotoImage(fields2_resized)
field_colored = ImageTk.PhotoImage(fields3_resized)

# -------------------- Update Project JSON -----------------------

def change_tempo_of_set(set, tempo):
    with open(f"src/Projects/{proj_name}/project.json", "r") as file:
        data = json.load(file)

    try:
        data[set]["Tempo"] = tempo

    except:
        pass
    with open(f"src/Projects/{proj_name}/project.json", "w") as file2:
        json.dump(data, file2, indent=4)

def change_beats_of_set(set, beats):
    with open(f"src/Projects/{proj_name}/project.json", "r") as file:
        data = json.load(file)

    try:
        data[set]["Beats"] = beats

    except:
        pass
    with open(f"src/Projects/{proj_name}/project.json", "w") as file2:
        json.dump(data, file2, indent=4)


# --------------------- Set Marcher Values -----------------------

def set_x_marcher(event):
    current_text = x_value_marcher.get("1.0", "end-1c").strip()

    try:
        selected_marcher.set_x(float(current_text))
    except:
        pass

def set_y_marcher(event):
    current_text = y_value_marcher.get("1.0", "end-1c").strip()

    try:
        selected_marcher.set_y(float(current_text))
    except:
        pass

# ----------------------- Properties Tab -------------------------

def properties_tab(event):
    global properties_tab  # Make sure we modify the global variable

    if properties_tab != 1:
        global selected_marcher_label, x_value_marcher, y_value_marcher, properties_tab_items, tab, name_value

        properties_tab_items = []  # This list will hold our components

        # Create the tab
        tab = Canvas(
            width=250,
            height=750,
            bg="#121212"
        )
        tab.place(x=977-250, y=0)
        properties_tab_items.append(tab)

        # Add "Properties" label
        label = tab.create_text(125, 10, text="Properties", font=("Arial", 12), fill="white")
        properties_tab_items.append(label)

        try:
            selected_marcher_label = tab.create_text(125, 50, text=f"Selected Marcher: {selected_marcher.get_name()}", fill="white", font=("Arial", 10))
        except:
            selected_marcher_label = tab.create_text(125, 50, text=f"Selected Marcher: None", fill="white", font=("Arial", 10))

        properties_tab_items.append(selected_marcher_label)

        # Add the "x" label and input box
        labelx = tab.create_text(125, 70, text="x", font=("Arial", 10), fill="white")
        properties_tab_items.append(labelx)

        x_value_marcher = Text(tab, height=1, width=5)
        x_value_marcher.place(x=105, y=85)
        properties_tab_items.append(x_value_marcher)

        # Add the "y" label and input box
        labely = tab.create_text(125, 125, text="y", font=("Arial", 10), fill="white")
        properties_tab_items.append(labely)

        y_value_marcher = Text(tab, height=1, width=5)
        y_value_marcher.place(x=105, y=140)
        properties_tab_items.append(y_value_marcher)


        label_name = tab.create_text(125, 180, text="Name", font=("Arial", 10), fill="white")
        properties_tab_items.append(label_name)

        name_value = Text(tab, height=1, width=5)
        name_value.place(x=105, y=195)
        properties_tab_items.append(name_value)


        # After the tab is created, set properties_tab to 1
        properties_tab = 1

        name_value.bind("<KeyRelease>", set_marcher_name)
        x_value_marcher.bind("<KeyRelease>", set_x_marcher)
        y_value_marcher.bind("<KeyRelease>", set_y_marcher)

    else:
        # If properties_tab is already 1, reset it and delete the components
        properties_tab = 0
        for i in properties_tab_items:
            if isinstance(i, Canvas):
                i.destroy()  # Remove the entire canvas
            elif isinstance(i, Text):
                i.destroy()  # Remove Text widgets
            else:
                try:
                    i.delete()  # Remove other Canvas items (e.g., text)
                except:
                    pass  # In case an item doesn't support delete(), ignore it


def set_marcher_name(event):
    selected_marcher.set_name(name_value.get("1.0", "end-1c").strip())

# -------------------------- Set Handling ---------------------------

def set_dot_val(event):
    current_text = set_value.get("1.0", "end-1c").strip()

    if current_text:  # If the text is not empty
        try:
            # Convert current_text to an integer
            current_value = int(current_text)

            # Generate availability range based on current value
            availability = [str(i) for i in range(current_value + 1)]

            # Check if current_value is in the available range
            if current_value in range(len(availability)):
                switch_set(current_value)
        except ValueError:
            print("Invalid input, not a number")
    else:
        print("Input is empty")

def add_set(event=None):
    if len(marchers) > 0:
        global current_set
        current_set += 1


        for marcher2 in marchers:
            marcher2.add_set2()

        set_value.delete("1.0", END)
        set_value.insert("1.0", str(current_set))

def remove_set():
    pass

def switch_set(set_val):

    for marcher4 in marchers:

        marcher4.go_to_set(set_val)

# ---------------------------- Functions ----------------------------

def unselect(event):
    global selected_marcher
    selected_marcher = None

    for ia in marchers:
        ia.check_if_selected()

    try:
        tab.itemconfig(selected_marcher_label, text=f"Selected Marcher: None")

        x_value_marcher.delete("1.0", "end")  # Use "end" to refer to the end of the content in a Text widget

        y_value_marcher.delete("1.0", "end")  # Same for the Y coordinate
    except:
        pass


# Load the appropriate field based on settings
def load_field():
    global zoomfield, selected_field, Field, field_option
    with open("src/settings.json", "r") as f:
        field_option = json.load(f).get('mode')

    # Select the field based on the field_option
    if field_option == 0:
        selected_field = field_dark
        zoomfield = fields1_resized  # Use resized PIL image
    elif field_option == 1:
        selected_field = field_light
        zoomfield = fields2_resized  # Use resized PIL image
    elif field_option == 2:
        selected_field = field_colored
        zoomfield = fields3_resized  # Use resized PIL image

    # Create the field on canvas
    Field = canvas.create_image(488.388889, 271, image=selected_field)
    canvas.tag_bind(Field, "<Button-1>", unselect)

# Play or pause the music
def playM(event):
    global playing_music  # Declare playing_music as global to modify it
    if not playing_music:  # Check if music is not playing
        canvas.itemconfig(Mplayer, image=pause_music)
        pygame.mixer.init()

        # Get the path to the project folder
        project_folder = os.path.join("src", "projects", proj_name)

        # Find the first MP3 file in the project folder
        mp3_files = [f for f in os.listdir(project_folder) if f.endswith(".mp3")]

        if mp3_files:
            mp3_path = os.path.join(project_folder, mp3_files[0])  # Get the full path of the first MP3 file
            pygame.mixer.music.load(mp3_path)  # Load the MP3 file
            pygame.mixer.music.play()  # Play the music
            playing_music = True
        else:
            pass
    else:
        pygame.mixer.music.stop()  # Stop the music if it's playing
        playing_music = False
        canvas.itemconfig(Mplayer, image=play_music)


# Function to handle mouse click and add marcher
def on_mouse_click(event):
    check_marchers()
    x, y = event.x, event.y

    # Check if Shift key is held down during the click
    if event.state & 0x0001:  # 0x0001 corresponds to the Shift key being pressed
        if current_set == 0:

        # Check if the mouse click is over the field image
            if canvas.bbox(Field) is not None:
                img_bbox = canvas.bbox(Field)  # Get the bounding box of the image
                if img_bbox[0] <= x <= img_bbox[2] and img_bbox[1] <= y <= img_bbox[3]:
                    marchers.append(Marchers(x, y, len(marchers) + 1))  # Create a new Marcher object


# Function to handle mouse hover over the field
def on_mouse_hover(event):
    x, y = event.x, event.y
    img_bbox = canvas.bbox(Field)  # Get the bounding box of the image

# ---------------------------- Marcher Class ----------------------------

class Marchers():
    def __init__(self, x, y, name):
        # Create the marcher image and label
        self.marcher = canvas.create_image(x, y, image=marcher1)
        self.marcher_label = canvas.create_text(x, y - 15, text=name, font=("Arial", 6), fill="red")

        # Save position data to a JSON file
        new_data = {"0": {"x": x, "y": y}}
        self.name = name
        file_path = f"src/projects/{proj_name}/DOTS/{name}.json"

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_data = json.load(f)
                existing_data.update(new_data)
        else:
            existing_data = new_data

        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        canvas.tag_bind(self.marcher, "<Button-1>", self.select)

    def select(self, event=None):
        global selected_marcher
        selected_marcher = self
        canvas.itemconfig(self.marcher, image=marcher_sel1)

        try:
            tab.itemconfig(selected_marcher_label, text=f"Selected Marcher: {self.name}")

            x_value_marcher.delete("1.0", "end")  # Use "end" to refer to the end of the content in a Text widget
            x_value_marcher.insert("1.0", str(canvas.coords(self.marcher)[0]))  # Insert the X coordinate

            y_value_marcher.delete("1.0", "end")  # Same for the Y coordinate
            y_value_marcher.insert("1.0", str(canvas.coords(self.marcher)[1]))  # Insert the Y coordinate

            name_value.delete("1.0", "end")
            name_value.insert("1.0", str(self.get_name()))

        except:
            pass
        #except:
         #   pass

    def move(self, dx, dy):
        # Move the marcher on the canvas
        canvas.move(self.marcher, dx, dy)
        canvas.move(self.marcher_label, dx, dy)

        # Read the current data from the JSON file
        try:
            with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "r") as c3:
                existing_data3 = json.load(c3)

            #
            # Update the coordinates of the marcher
            existing_data3[str(current_set)]['x'] = canvas.coords(self.marcher)[0]
            existing_data3[str(current_set)]['y'] = canvas.coords(self.marcher)[1]



            # Overwrite the file with the updated data (replacing the content)
            with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "w") as c3:
                json.dump(existing_data3, c3, indent=4)  # This replaces the file content

        except json.JSONDecodeError as e:
            pass
            # Handle the error (log it, raise it, etc.)
        except Exception as e:
            pass

        try:
            x_value_marcher.delete("1.0", "end")  # Use "end" to refer to the end of the content in a Text widget
            x_value_marcher.insert("1.0", str(canvas.coords(self.marcher)[0]))  # Insert the X coordinate

            y_value_marcher.delete("1.0", "end")  # Same for the Y coordinate
            y_value_marcher.insert("1.0", str(canvas.coords(self.marcher)[1]))
        except:
            pass

    def set_name(self, name):
        self.name = name
        canvas.itemconfig(self.marcher_label, text=name)

    def check_if_selected(self):
        if selected_marcher != self:
            canvas.itemconfig(self.marcher, image=marcher1)  # Reset to original image if not selected

    def set_position(self, x, y):
        canvas.coords(self.marcher, x, y)
        canvas.coords(self.marcher_label, x, y - 15)

    def set_x(self, x):
        canvas.coords(self.marcher, x, canvas.coords(self.marcher)[1])
        canvas.coords(self.marcher_label, x, canvas.coords(self.marcher)[1] - 15)
        try:
            x_value_marcher.delete("1.0", "end")  # Use "end" to refer to the end of the content in a Text widget
            x_value_marcher.insert("1.0", str(canvas.coords(self.marcher)[0]))
        except:
            pass

        with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "r") as c:
            existing_data = json.load(c)

        existing_data[str(current_set)]['x'] = x

        with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "w") as c:
            json.dump(existing_data, c, indent=4)



    def set_y(self, y):
        canvas.coords(self.marcher, canvas.coords(self.marcher)[0], y)
        canvas.coords(self.marcher_label, canvas.coords(self.marcher)[0], y - 15)

        try:
            y_value_marcher.delete("1.0", "end")  # Use "end" to refer to the end of the content in a Text widget
            y_value_marcher.insert("1.0", str(canvas.coords(self.marcher)[1]))
        except:
            pass

        with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "r") as c:
            existing_data = json.load(c)

        existing_data[str(current_set)]['y'] = y

        with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "w") as c:
            json.dump(existing_data, c, indent=4)

    def return_coords(self, h):
        if h == "x":
            return canvas.coords(self.marcher)[0]
        elif h == "y":
            return canvas.coords(self.marcher)[1]
        elif h == "xy":
            return [canvas.coords(self.marcher)[0], canvas.coords(self.marcher)[1]]

    def add_set2(self):

        with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "r+") as f:
            existing_data = json.load(f)

            new_data = {f"{current_set}":
                            {
                             "x":
                                 canvas.coords(self.marcher)[0],
                             "y":
                                 canvas.coords(self.marcher)[1]
                             }
                        }

            existing_data.update(new_data)

            f.seek(0)

            json.dump(existing_data, f, indent=4)

            f.truncate()

    def go_to_set(self, set_val):

        with open(f"src/Projects/{proj_name}/DOTS/{self.name}.json", "r") as f:
            data = json.load(f)

            x_val = data[str(set_val)]["x"]
            y_val = data[str(set_val)]["y"]

            canvas.coords(self.marcher, x_val, y_val)
            canvas.coords(self.marcher_label, x_val, y_val - 15)

            f.close()


    def get_name(self):
        return self.name





# ---------------------------- Movement Functions ----------------------------

# Function to move the selected marcher down
def marcher_down(event):
    if selected_marcher:
        selected_marcher.move(0, 1)


# Function to move the selected marcher up
def marcher_up(event):
    if selected_marcher:
        selected_marcher.move(0, -1)


# Function to move the selected marcher left
def marcher_left(event):
    if selected_marcher:
        if event.state & 0x0001:
            selected_marcher.move(-5, 0)
            x_val = selected_marcher.return_coords("x")
            max_values = []
            for i in range(len(hash_x)):
                max_values.append(abs(hash_x[i] - x_val))
            selected_marcher.move(min(max_values), 0)
        else:
            selected_marcher.move(-1, 0)


# Function to move the selected marcher right
def marcher_right(event):
    if selected_marcher:
        if event.state & 0x0001:
            selected_marcher.move(5, 0)
            x_val = selected_marcher.return_coords("x")
            max_values = []
            for i in range(len(hash_x)):
                max_values.append(abs(hash_x[i] - x_val))
            selected_marcher.move(min(max_values), 0)
        else:
            selected_marcher.move(1, 0)


# Function to check all marchers for selection
def check_marchers(event=None):
    for marcher in marchers:
        marcher.check_if_selected()


# ---------------------------- GUI Setup and Event Binding ----------------------------

# Initialize the GUI elements
def load_GUI():
    global playing_music, Mplayer, set_value
    Mplayer = canvas.create_image(40, 600, image=play_music)

    add_set_button = Button(canvas, image=add_set_buttonimg, command=add_set)
    add_set_button.place(x=10, y=750 - 60, anchor="w")

    set_value = Text(canvas, width=3, height=1)
    set_value.place(x=(997 - 37) // 2, y=700)
    set_value.insert("1.0", "0")

    # Bind music player click to toggle play/pause
    canvas.tag_bind(Mplayer, "<Button-1>", playM)

    # Bind mouse and keyboard events
    project.bind("<Button-1>", on_mouse_click)
    canvas.bind("<Motion>", on_mouse_hover)
    project.bind("<Left>", marcher_left)
    project.bind("<Right>", marcher_right)
    project.bind("<Up>", marcher_up)
    project.bind("<Down>", marcher_down)
    project.bind("<KeyPress-Escape>", unselect)
    set_value.bind("<KeyRelease>", set_dot_val)
    project.bind("<Control-p>", properties_tab)


# ---------------------------- Project Loading ----------------------------

# Load the project settings and field
def load_project(name):
    global proj_name
    proj_name = name
    project.title(name)
    load_field()  # Load the field when project is loaded
    load_GUI()  # Set up the GUI
    change_tempo_of_set("0", 132)
    project.mainloop()


# ---------------------------- Main ----------------------------

if __name__ == "__main__":
    load_project("SampleProject")  # Replace with the actual project name