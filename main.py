from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from app_function import AppFunctions

# Global Constants
SELECT_COLOR = "#333C83"
BG = "#E4E9BE"
# "#FAFFAF"
FONT = "Bahnschrift"
SHOW = 0

# Creating an app object
app_function = AppFunctions()


# The function will allow to select a photo from the directory and upload it in the app.
def select_image():
    image = app_function.select_image()
    if image:
        specs = app_function.show_specs(image)
        specs_label.config(text=specs)


# Function will open the image in the app.

def show_on_off():
    global SHOW
    if SHOW == 0:
        show_image()
    else:
        image_label.config(image="")
        window.state("normal")
        window.minsize(550, 700)
        image_label.grid_forget()
        SHOW = 0


def show_image():
    global SHOW
    tk_image = app_function.show_image()
    if tk_image:
        window.state('zoomed')
        image_label.image = tk_image
        image_label.config(image=tk_image)
        image_label.grid(row=0, column=2, rowspan=15, columnspan=12, padx=20, pady=10)
        # Image is being showed
        SHOW = 1


def open_file():
    app_function.open_file()


def resize_image():
    w = int(width_entry.get())
    h = int(height_entry.get())
    tk_image_resize, resized_image = app_function.resize_image(w, h)
    image_label.config(image=tk_image_resize)
    image_label.image = tk_image_resize
    resized_specs = app_function.show_specs(resized_image)
    specs_label.config(text=resized_specs)
    show_image()
    width_entry.delete(0, END)
    height_entry.delete(0, END)


def change_format():
    image_format = format_entry.get().lower()
    formatted = app_function.change_format(image_format)
    changed_specs = app_function.show_specs(formatted)
    specs_label.config(text=changed_specs)
    format_entry.delete(0, END)


def confirm_text():
    text = mark_text_entry.get()
    app_function.confirm_text(text)
    if text:
        confirm_text_button.config(state="disable")
        color_choice.config(state="disabled")
        mark_text_entry.delete(0, END)
        confirm_location_button.config(state="!disabled")


def add_water_mark():
    color = text_color.get()
    location = location_choice.get()
    coverage = coverage_choice.get()
    watermarked_image = app_function.add_marker(color, location, coverage)
    if watermarked_image:
        show_image()
    color_choice.config(state="!disabled")
    confirm_text_button.config(state="!disable")


window = ThemedTk(theme="radiance")
window.config(padx=20, pady=20, bg=BG)
window.title("Image Water Marker and Resizer")
window.geometry("550x700")

# Image Label on the Right Side of Window
image_label = Label()

# Main Heading
main_heading = ttk.Label(
    text="Image Water Marker and Resizer",
    foreground=SELECT_COLOR,
    background=BG,
    font=("cambria", 25)
)
main_heading.grid(row=0, column=0, columnspan=2)

# Select Heading
select_heading = ttk.Label(
    text="Select an Image",
    foreground=SELECT_COLOR,
    background=BG,
    font=(FONT, 15, "bold")
)
select_heading.grid(row=1, column=0, pady=(20, 10), sticky="w")

# Select Image Button
select_btn = ttk.Button(text="Select Image", command=select_image, style="TButton")
select_btn.grid(row=2, column=0, sticky="w")

# Image Specs Label
specs_label = ttk.Label(
    text="",
    font=(FONT, 12),
    background=BG,
    foreground=SELECT_COLOR)
specs_label.grid(row=2, column=1, sticky="w")

# Show Image Button
show_button = ttk.Button(text="Show Image", command=show_on_off, style="TButton")
show_button.grid(row=3, column=0, sticky="w", pady=(5, 0))

# File Location Button
file_location_button = ttk.Button(
    text="File Location",
    command=open_file,
    style="TButton")
file_location_button.grid(row=3, column=1, sticky="e", pady=(5, 0))

# Resize Heading
resize_heading = ttk.Label(
    text="Resize Image",
    foreground=SELECT_COLOR,
    background=BG,
    font=(FONT, 15, "bold"))

resize_heading.grid(row=4, column=0, pady=(20, 10), sticky="w")

# Width Label
width_label = ttk.Label(
    text="Width  = ",
    foreground=SELECT_COLOR,
    background=BG,
    font=(FONT, 15),
)
width_label.grid(row=5, column=0, sticky="e")

# Width Entry
width_entry = ttk.Entry(width=30)
width_entry.focus()
width_entry.insert(0, "Width Pixels")
width_entry.grid(row=5, column=1, sticky="w")

# Height Label
height_label = ttk.Label(
    text="Height = ",
    font=(FONT, 15),
    foreground=SELECT_COLOR,
    background=BG)
height_label.grid(row=6, column=0, sticky="e")

# Height Entry
height_entry = ttk.Entry(width=30)
height_entry.insert(0, "Height Pixels")
height_entry.grid(row=6, column=1, sticky="w")

# Resize Button
resize_button = ttk.Button(text="Resize", command=resize_image, style="TButton")
resize_button.grid(row=7, column=0, pady=(5, 0), sticky="w")

# Format Heading
format_heading = ttk.Label(
    text="Format Image",
    foreground=SELECT_COLOR,
    background=BG,
    font=(FONT, 15, "bold"))

format_heading.grid(row=8, column=0, pady=(20, 10), sticky="w")

# Format Entry
format_entry = ttk.Entry(width=30)
format_entry.grid(row=9, column=1, sticky="w")

# Change format Button
change_format_button = ttk.Button(text="Change Format to", command=change_format, style="TButton")
change_format_button.grid(row=9, column=0, sticky="w")

# Mark Heading
mark_heading = ttk.Label(
    text="Mark Image",
    foreground=SELECT_COLOR,
    background=BG,
    font=(FONT, 15, "bold"))
mark_heading.grid(row=10, column=0, pady=(20, 10), sticky="w")

# Text Entry
mark_text_entry = ttk.Entry(width=30)
mark_text_entry.grid(row=11, column=1, pady=(5, 0), sticky="w")

# Text Color Dropdown
text_color = StringVar()
color_choice = ttk.Combobox(window, textvariable=text_color)
color_choice.config(values=("White Text", "Black Text"), state="readonly")
color_choice.set("White text")
color_choice.grid(row=10, column=1, sticky="e")

# Confirm Text Button
confirm_text_button = ttk.Button(text="Confirm Text", command=confirm_text, style="TButton")
confirm_text_button.grid(row=11, column=0, pady=(5, 0), sticky="w")

# Location Label
height_label = ttk.Label(
    text="Text Location = ",
    font=(FONT, 15),
    foreground=SELECT_COLOR,
    background=BG)
height_label.grid(row=12, column=0, pady=(5, 0), sticky="se")

# Mark Location Radio buttons (5)
# For styling of all 5 buttons
button_style = ttk.Style()
button_style.map('TButton', background=[('active', BG)])
button_style.configure('TButton', background=BG)

button_style.configure("TRadiobutton", background=BG, foreground=SELECT_COLOR)

location_choice = StringVar()
center = ttk.Radiobutton(
    window,
    text="Center",
    variable=location_choice,
    value="Center",
    style="TRadiobutton"
)
center.grid(row=12, column=1, sticky="se")
top_left = ttk.Radiobutton(
    window,
    text="Top-Left",
    variable=location_choice,
    value="Top-Left",
    style="TRadiobutton"
)
top_left.grid(row=12, column=1, sticky="w")
top_right = ttk.Radiobutton(
    text="Top-Right",
    variable=location_choice,
    value="Top-Right",
    style="TRadiobutton"
)
top_right.grid(row=12, column=1)
bottom_left = ttk.Radiobutton(
    window,
    text="Bot-Left",
    variable=location_choice,
    value="Bottom-Left",
    style="TRadiobutton"
)
bottom_left.grid(row=13, column=1, sticky="w")
bottom_right = ttk.Radiobutton(
    window,
    text="Bot-Right",
    variable=location_choice,
    value="Bottom-Right",
    style="TRadiobutton"
)
bottom_right.grid(row=13, column=1)

# Coverage Radio Buttons
coverage_choice = StringVar()
full_coverage = ttk.Radiobutton(
    window,
    text="Full Cover",
    variable=coverage_choice,
    value="Full",
    style="TRadiobutton")
full_coverage.grid(row=14, column=1, ipadx=30)

half_coverage = ttk.Radiobutton(
    window,
    text="Half Cover",
    variable=coverage_choice,
    value="Half",
    style="TRadiobutton")
half_coverage.grid(row=14, column=1, sticky="e")

confirm_location_button = ttk.Button(text="Confirm Location and Coverage", command=add_water_mark, style="TButton")
confirm_location_button.config(state="disabled")
confirm_location_button.grid(column=0, row=14, columnspan=2, pady=(10, 0), sticky="w")

window.mainloop()
