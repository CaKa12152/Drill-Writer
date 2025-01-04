from tkinter import *
from tkinter import filedialog
import shutil
import os
import json


popup = Tk()
popup.title("Create Project")


def select_file():
    popup.lift()
    global file_path
    # Open the file dialog to let the user select a file
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")]
    )

    Choose_Audio.config(text=file_path)
    popup.lift()


def create_project():
    try:
        global Project_name
        Project_name = Title_name.get('1.0', 'end-1c')
        os.mkdir(f"src/Projects/{str(Title_name.get('1.0', 'end-1c'))}")
        os.mkdir(f"src/Projects/{str(Title_name.get('1.0', 'end-1c'))}/DOTS")
        shutil.copy(file_path, f"src/Projects/{str(Title_name.get('1.0', 'end-1c'))}")
        shutil.copy('src/project.json', f"src/Projects/{str(Title_name.get('1.0', 'end-1c'))}")

        with open(f"src/Projects/{str(Title_name.get('1.0', 'end-1c'))}/project.json", 'r') as file:
            data = json.load(file)

        # Update the Tempo value
        data["0"]['Tempo'] = int(Tempo.get('1.0', 'end-1c'))

        # Write the updated data back to the file
        with open(f"src/Projects/{str(Title_name.get('1.0', 'end-1c'))}/project.json", 'w') as file:
            json.dump(data, file, indent=4)

        popup.quit()
        popup.destroy()
    except Exception as e:
        print(f"An error occurred: {e}")
        error = Label(background,
                      text="ERROR: This project already exists or no track was chosen or tempo isnt a valid integer",
                      fg="red", bg="#121212", font=("Helvetica", 8))
        error.pack()


# Window size and positioning
window_width = 500
window_height = 350
screen_width = popup.winfo_screenwidth()
screen_height = popup.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

popup.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

# Set background color for the window
popup.config(bg="#121212")

# Create the Canvas with the same background color
background = Canvas(popup, bg="#121212", width=500, height=350)
background.pack(fill=BOTH, expand=True)

Title = Label(background, text="Title", font=("Helvetica", 16), bg="#121212", fg="white")
Title.place(x=20, y=20)

Title_name = Text(background, font=("Helvetica", 8), height=1, width=20)
Title_name.place(x=20, y=60)

Path_To_Audio = Label(background, text="Select Track", font=("Helvetica", 16), bg='#121212', fg="white")
Path_To_Audio.place(x=20, y=100)

Choose_Audio = Button(background, text="Select", font=("Helvetica", 8), height=1, command=select_file)
Choose_Audio.place(x=20, y=140)

Tempo_text = Label(background, text="Tempo", font=("Helvetica", 16), bg='#121212', fg="white")
Tempo_text.place(x=20, y=180)

Tempo = Text(background, font=("Helvetica", 8), height=1, width=20)
Tempo.place(x=20, y=220)

Create = Button(background, font=("Helvetica", 16), bg='#121212', text="Create Project", fg="white",
                command=create_project)
Create.place(x=20, y=280)

# Remove the window title bar
popup.overrideredirect(True)


def Create_Popup():
    popup.mainloop()
    return [1, Project_name]
