from PIL import Image, ImageFont, ImageDraw, ImageTk, UnidentifiedImageError
from tkinter import filedialog
import os
from tkinter import messagebox


class AppFunctions:
    def __init__(self):
        self.main_image = None
        self.height = None
        self.width = None
        self.filename = None
        self.image_size = None
        self.path = None
        self.image_name = None
        self.text = None

    def select_image(self):
        # Opening image using PIL
        try:
            self.filename = filedialog.askopenfilename(initialdir="/",
                                                       title="Select an Image File")
            self.main_image = Image.open(self.filename)
        except UnidentifiedImageError:
            messagebox.showinfo(title="Error", message="This isn't an image file, only images are supported.")
            return False
        except AttributeError:
            pass
        else:
            return self.set_name()

    def set_name(self):
        # Split the file absolute path into image_name and path , for image Formatting and Resizing
        split_path = str(self.filename).rsplit("/", 1)
        self.path = split_path[0]
        self.image_name = split_path[1]
        return self.main_image

    def show_specs(self, image):
        # Show image specs
        self.image_size = image.size
        file_size = os.path.getsize(self.filename)
        image_format = image.format
        return "Specs = .{} - ({}x{}) - {:.3f} MB".format(image_format, self.image_size[0], self.image_size[1],
                                                          file_size / (1024 * 1024))

    def show_image(self):
        try:
            width, height = self.image_size
            if width > 800 or height > 600:
                width, height = 800, 600
                self.main_image = self.main_image.resize((width, height))
            # Making a Tkinter image object
            tk_image = ImageTk.PhotoImage(self.main_image)
            return tk_image
        except TypeError:
            messagebox.showinfo(title="Select an Image", message="Select an 'Image file'")

    def open_file(self):
        # Opens the file directory
        os.startfile(f"{self.path}")

    def resize_image(self, width, height):
        modified_path = "{}/resized_{}".format(self.path, self.image_name)
        resize_img = self.main_image.resize((width, height))
        resize_img.save(modified_path)
        resized_image = Image.open(modified_path)
        self.main_image = resized_image
        self.filename = modified_path
        self.set_name()
        tk_image_resize = ImageTk.PhotoImage(resize_img)
        messagebox.showinfo(title="Image Size Changed",
                            message="Image Size Changed Successfully!\n"
                                    "Click 'File Location' Button to see the new file.")
        return tk_image_resize, resized_image

    def change_format(self, image_format):
        # Modified Path for Formatting Image
        modified_path = "{}/modified_{}.{}".format(self.path, self.image_name.split(".")[0], image_format)
        message = "Format changed successfully!\nClick open folder to see the new file."
        try:
            if self.main_image.mode == "RGBA":
                rgb_image = self.main_image.convert('RGB')
                rgb_image.save(modified_path)
                messagebox.showinfo(title="Format Changed", message=message)
            else:
                self.main_image.save(modified_path)
                messagebox.showinfo(title="Format Changed", message=message)
            formatted_image = Image.open(modified_path)
            self.main_image = formatted_image
            self.filename = modified_path
            self.set_name()
            return formatted_image
        except ValueError:
            messagebox.showinfo(title="Enter Format",
                                message="Please provide format. Example: png")

    def confirm_text(self, text):
        if len(text) == 0:
            messagebox.showinfo(title="No Text Provided.", message="Provide the Text in the Text field.")
            return False
        else:
            self.text = text
            return True

    def get_location(self, selected_location, mark_width, mark_height):
        border = 10
        x, y = 0, 0
        if selected_location == "Center":
            x = (self.width / 2) - (mark_width / 2)
            y = (self.height / 2) - (mark_height / 2)
        elif selected_location == "Top-Left":
            x = border
            y = border
        elif selected_location == "Top-Right":
            x = self.width - mark_width - border
            y = border
        elif selected_location == "Bottom-Left":
            x = border
            y = self.height - mark_height - border
        elif selected_location == "Bottom-Right":
            x = self.width - mark_width - border
            y = self.height - mark_height - border

        return int(x), int(y)

    def add_marker(self, color, location_string, coverage):
        # Setting color based on user selection
        if color == "Black Text":
            color = (0, 0, 0, 100)
        else:
            color = (255, 255, 255, 100)

        # Setting Coverage
        if coverage == "Full":
            coverage = 1
        else:
            coverage = 0.5

        # Producing another image for watermark
        self.main_image = self.main_image.convert("RGBA")
        self.width, self.height = self.main_image.size
        overlay_image = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay_image)

        # Setting Text font
        font_size = 0
        font = ImageFont.truetype("arial.ttf", font_size)
        image_fraction = coverage
        jump_size = 100
        while True:
            if font.getsize(self.text)[0] < image_fraction * self.width:
                font_size += jump_size
            else:
                jump_size = jump_size // 2
                font_size -= jump_size
            font = ImageFont.truetype("arial.ttf", font_size)
            if jump_size < 1:
                break
        font = ImageFont.truetype("arial.ttf", font_size)
        mark_width, mark_height = draw.textsize(self.text, font)

        # Setting location based on user selection
        if location_string == "":
            location_string = "Center"
        location = self.get_location(location_string, mark_width, mark_height)
        draw.text(location, self.text, font=font, fill=color)
        watermarked_image = Image.alpha_composite(self.main_image, overlay_image)
        try:
            watermarked_image.save("{}/marked_{}".format(self.path, self.image_name))
        except OSError:
            watermarked_image = watermarked_image.convert("RGB")
            watermarked_image.save("{}/marked_{}".format(self.path, self.image_name))
        self.main_image = watermarked_image
        messagebox.showinfo(title="Watermark Added",
                            message="Water mark added Successfully!\n"
                                    "Click 'File Location' Button to see the new file.")
        return watermarked_image
