import tkinter as tk
from tkinter import filedialog
import pickle
from PIL import ImageGrab
import os

class FileOperations:
    def __init__(self, canvas):
        self.canvas = canvas
        self.eraser_lines = []

    def save_as_pickle(self, file_path):
        items = self.canvas.find_all()
        canvas_data = []

        for item in items:
            item_type = self.canvas.type(item)
            item_coords = self.canvas.coords(item)
            item_options = self.canvas.itemconfig(item)
            item_tags = self.canvas.gettags(item)

            item_data = {
                "type": item_type,
                "coords": item_coords,
                "options": {key: val[-1] for key, val in item_options.items()},
                "tags": item_tags
            }
            canvas_data.append(item_data)

        with open(file_path, "wb") as f:
            pickle.dump(canvas_data, f)

    def save_as_image(self, file_path):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab(bbox=(x, y, x1, y1)).save(file_path)

    def load_pickle(self, file_path):
        self.canvas.delete("all")
        self.eraser_lines.clear()

        with open(file_path, "rb") as f:
            canvas_data = pickle.load(f)

            for item_data in canvas_data:
                item_type = item_data["type"]
                item_coords = item_data["coords"]
                item_options = item_data["options"]
                item_tags = item_data["tags"]

                if item_type == "line":
                    new_item = self.canvas.create_line(*item_coords, **item_options)
                elif item_type == "rectangle":
                    new_item = self.canvas.create_rectangle(*item_coords, **item_options)
                elif item_type == "oval":
                    new_item = self.canvas.create_oval(*item_coords, **item_options)
                elif item_type == "text":
                    new_item = self.canvas.create_text(*item_coords, **item_options)

                if "eraser" in item_tags:
                    self.eraser_lines.append(new_item)

    def show_save_dialog(self, save_type):
        if save_type == "Pickle":
            file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
            if file_path:
                self.save_as_pickle(file_path)
        elif save_type == "Image":
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.save_as_image(file_path)

    def show_load_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path and os.path.exists(file_path):
            self.load_pickle(file_path)
            return True
        return False
