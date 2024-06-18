import pickle
import os
from tkinter.colorchooser import askcolor
from tkinter import filedialog

class WhiteboardLogic:
    def __init__(self, canvas, text_widget, line_width_slider):
        self.canvas = canvas
        self.text_widget = text_widget
        self.line_width_slider = line_width_slider
        
        self.is_drawing = False
        self.drawing_color = "black"
        self.line_width = 2
        self.is_dark_mode = False
        self.is_eraser = False
        self.last_drawing_color = "black"
        self.last_line_width = 2
        self.eraser_size = 20
        self.eraser_lines = []

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = event.x, event.y

    def draw(self, event):
        if self.is_drawing:
            current_x, current_y = event.x, event.y
            line = self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.drawing_color, width=self.line_width, capstyle="round", smooth=True)
            if self.is_eraser:
                self.eraser_lines.append(line)
            self.prev_x, self.prev_y = current_x, current_y

    def stop_drawing(self, event):
        self.is_drawing = False

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color
            if self.is_eraser:
                self.toggle_eraser()

    def change_line_width(self, value):
        self.line_width = int(float(value))

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_canvas_colors()

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
            self.drawing_color = "white" if not self.is_dark_mode else "gray10"
            self.canvas.config(cursor="circle")

    def update_canvas_colors(self):
        if self.is_dark_mode:
            bg_color = "gray10"
            eraser_color = "gray10"
        else:
            bg_color = "white"
            eraser_color = "white"

        self.canvas.config(bg=bg_color)
        
        for line in self.eraser_lines:
            self.canvas.itemconfig(line, fill=eraser_color)
        
        if self.is_eraser:
            self.drawing_color = eraser_color

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            canvas_data = {
                "lines": self.canvas.find_all(),
                "text": self.text_widget.get("1.0", "end")
            }
            with open(file_path, "wb") as f:
                pickle.dump(canvas_data, f)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                canvas_data = pickle.load(f)
                if "lines" in canvas_data:
                    for line in canvas_data["lines"]:
                        if self.canvas.coords(line):
                            self.canvas.create_line(self.canvas.coords(line), fill=self.drawing_color, width=self.line_width, capstyle="round", smooth=True)
                if "text" in canvas_data:
                    self.text_widget.insert("end", canvas_data["text"])

    def clear_canvas(self):
        self.canvas.delete("all")
        self.eraser_lines.clear()
