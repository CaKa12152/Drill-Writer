from tkinter import *
import json
from PIL import Image, ImageTk



project = Tk()
project.geometry('977x643')
icon = PhotoImage(file=r"src/img/Icon.png")
project.iconphoto(True, icon)

canvas = Canvas(project, bg="#121212", width=977, height=643)
canvas.pack()

# Load the field images
fields1 = Image.open("src/img/Field_dark.png")
fields2 = Image.open("src/img/Field_light.png")
fields3 = Image.open("src/img/Field_color.png")

marcher = Image.open("src/img/Marcher.png")
marcher_sel = Image.open("src/img/Marcher-Selected.png")

hash_x = [100, 107.5, 115.5, 123.5, 131.5, 139, 147, 155, 163, 171, 178,
          186, 194, 202, 210, 217, 225, 233, 241, 249, 256, 264, 272,
          280, 288, 295, 303, 311, 319, 327, 334, 342, 350, 358, 366,
          373, 380.5, 388.5, 396.5, 404.5, 412, 419.5, 427.5, 435.5,
          443.5, 451, 458.5, 466.5, 474.5, 482.5, 490, 497.5, 505.5,
          513.5, 521.5, 529, 536.5, 544.5, 552.5, 560.5, 568, 576,
          584, 592, 600, 607, 615, 623, 631, 639, 646, 654, 662, 670,
          678, 685, 693, 701, 709, 716, 724, 732, 740, 748,  756, 763,
          771, 779, 787, 795, 801]

# Resize the images down to 1/9th of their original size
def resize_image(image, hm):
    width, height = image.size
    new_width = width // hm  # Reduce width by 3
    new_height = height // hm  # Reduce height by 3
    return image.resize((new_width, new_height))


# Apply the resize function to the images
fields1_resized = resize_image(fields1, 9)
fields2_resized = resize_image(fields2, 9)
fields3_resized = resize_image(fields3, 9)

marcher1 = ImageTk.PhotoImage(resize_image(marcher, 60))
marcher_sel1 = ImageTk.PhotoImage(resize_image(marcher_sel, 60))

# Convert resized images to PhotoImage objects
field_dark = ImageTk.PhotoImage(fields1_resized)
field_light = ImageTk.PhotoImage(fields2_resized)
field_colored = ImageTk.PhotoImage(fields3_resized)


def load_field():
    global zoomfield, selected_field, Field, field_option
    with open("src/settings.json", "r") as f:
        field_option = json.load(f).get('mode')

    if field_option == 0:
        selected_field = field_dark
        zoomfield = fields1_resized  # Use resized PIL image
    elif field_option == 1:
        selected_field = field_light
        zoomfield = fields2_resized  # Use resized PIL image
    elif field_option == 2:
        selected_field = field_colored
        zoomfield = fields3_resized  # Use resized PIL image

    Field = canvas.create_image(488.388889, 271, image=selected_field)




    x = canvas.create_image(hash_x[1], 150, image=marcher1)
    



# Keep the load_project function as it is
def load_project(name):
    global proj_name
    proj_name = name
    project.title(name)
    load_field()  # Load the field when project is loaded
    project.mainloop()

# Example usage of loading a project
# Uncomment the line below to load a project with a custom name.
# load_project("My Project")