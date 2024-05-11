import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
import pickle
import os

class WhiteboardLogic:
    def __init__(self):
        self.is_drawing = False
        self.drawing_color = "black"
        self.line_width = 2
        self.is_dark_mode = False
        self.is_eraser = False
        self.last_drawing_color = "black"
        self.last_line_width = 2
        self.eraser_size = 20

    def set_widgets(self, root, canvas, controls_frame, color_button, clear_button, save_button, dark_mode_button, eraser_button, line_width_label, line_width_slider, text_widget, text_widget_label,notes_button):
        self.root = root
        self.canvas = canvas
        self.controls_frame = controls_frame
        self.color_button = color_button
        self.clear_button = clear_button
        self.save_button = save_button
        self.dark_mode_button = dark_mode_button
        self.eraser_button = eraser_button
        self.line_width_label = line_width_label
        self.line_width_slider = line_width_slider
        self.text_widget = text_widget
        self.text_widget_label = text_widget_label
        self.notes_button = notes_button
        
    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = event.x, event.y

    def draw(self, event):
        if self.is_drawing:
            current_x, current_y = event.x, event.y
            event.widget.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.drawing_color, width=self.line_width, capstyle=tk.ROUND, smooth=True)
            self.prev_x, self.prev_y = current_x, current_y

    def stop_drawing(self, event):
        self.is_drawing = False

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color

    def change_line_width(self, value):
        self.line_width = int(value)

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()

    def toggle_notes_section(self):
        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        else:
            self.text_widget.pack(side="left", padx=5, pady=5)

    def toggle_eraser(self):
        if self.is_eraser:
            self.is_eraser = False
            self.canvas.config(cursor="")
            self.drawing_color = self.last_drawing_color
            self.line_width_slider.set(self.last_line_width)
        else:
            self.is_eraser = True
            self.last_drawing_color = self.drawing_color
            self.last_line_width = self.line_width_slider.get()
            if self.is_dark_mode:
                self.drawing_color = "gray10"
            else:
                self.drawing_color = "white"
            self.canvas.config(cursor="circle", width=25)

    def update_theme(self):
        if self.is_dark_mode:
            self.root.config(bg="black")
            self.canvas.config(bg="gray10")
            self.controls_frame.config(bg="gray20")
            self.color_button.config(bg="gray30", fg="white")
            self.clear_button.config(bg="gray30", fg="white")
            self.save_button.config(bg="gray30", fg="white")
            self.eraser_button.config(bg="gray30", fg="white")
            self.line_width_label.config(bg="gray20", fg="white")
            self.line_width_slider.config(bg="gray20", fg="white", troughcolor="gray30")
            self.text_widget_label.config(bg="gray20", fg="white")
            self.text_widget.config(bg="gray30", fg="white")
            self.dark_mode_button.config(text="Light Mode", bg="gray30", fg="white")
            self.notes_button.config(text="notes", bg="gray30", fg="white")
        else:
            self.root.config(bg="white")
            self.canvas.config(bg="white")
            self.controls_frame.config(bg="white")
            self.color_button.config(bg="white", fg="black")
            self.clear_button.config(bg="white", fg="black")
            self.save_button.config(bg="white", fg="black")
            self.eraser_button.config(bg="white", fg="black")
            self.line_width_label.config(bg="white", fg="black")
            self.line_width_slider.config(bg="white", fg="black", troughcolor="lightgray")
            self.text_widget_label.config(bg="white", fg="black")
            self.text_widget.config(bg="white", fg="black")
            self.dark_mode_button.config(text="Dark Mode", bg="white", fg="black")
            self.notes_button.config(text="notes", bg="white", fg="black")

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            canvas_data = {
                "lines": self.canvas.find_all(),
                "text": self.text_widget.get("1.0", tk.END)
            }
            with open(file_path, "wb") as f:
                pickle.dump(canvas_data, f)

    def clear_canvas(self):
        self.canvas.delete("all")

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                canvas_data = pickle.load(f)
                if "lines" in canvas_data:
                    for line in canvas_data["lines"]:
                        if self.canvas.coords(line):
                            self.canvas.create_line(self.canvas.coords(line), fill=self.drawing_color, width=self.line_width, capstyle=tk.ROUND, smooth=True)
                if "text" in canvas_data:
                    self.text_widget.insert(tk.END, canvas_data["text"])
