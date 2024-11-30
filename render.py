import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random
import time


class ImageScreensaver:
    def __init__(self, image_urls):
        self.image_urls = image_urls
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.config(cursor="none")
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.bind("<Escape>", self.exit_fullscreen)
        self.display_image()

    def get_random_image(self):
        url = random.choice(self.image_urls)
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    def display_image(self):
        img = self.get_random_image()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        img = img.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo
        self.window.after(5000, self.display_image)

    def exit_fullscreen(self, event):
        self.window.attributes("-fullscreen", False)
        self.window.destroy()

    def run(self):
        self.window.mainloop()
