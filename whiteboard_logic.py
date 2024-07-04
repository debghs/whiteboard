import tkinter as tk
import pickle

class WhiteboardLogic:
    def __init__(self, root):
        self.root = root
        self.is_drawing = False
        self.drawing_color = "black"
        self.line_width = 2
        self.is_dark_mode = False
        self.is_eraser = False
        self.last_drawing_color = "black"
        self.last_line_width = 2
        self.eraser_size = 20
        self.current_shape = None
        self.shape_start_x = None
        self.shape_start_y = None
        self.shape_id = None
        self.eraser_lines = []

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = event.x, event.y

        if self.current_shape and not self.is_eraser:
            self.shape_start_x, self.shape_start_y = event.x, event.y
            if self.current_shape == "line":
                self.shape_id = self.canvas.create_line(event.x, event.y, event.x, event.y, fill=self.drawing_color, width=self.line_width)
            elif self.current_shape == "rectangle":
                self.shape_id = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)
            elif self.current_shape == "circle":
                self.shape_id = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)

    def draw(self, event):
        if self.is_drawing:
            if self.is_eraser:
                current_x, current_y = event.x, event.y
                line = self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.canvas["bg"], width=self.line_width, capstyle=tk.ROUND, smooth=True)
                self.eraser_lines.append(line)
                self.prev_x, self.prev_y = current_x, current_y
            elif self.current_shape:
                if self.shape_id:
                    self.canvas.delete(self.shape_id)
                if self.current_shape == "line":
                    self.shape_id = self.canvas.create_line(self.shape_start_x, self.shape_start_y, event.x, event.y, fill=self.drawing_color, width=self.line_width)
                elif self.current_shape == "rectangle":
                    self.shape_id = self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, event.x, event.y, outline=self.drawing_color, width=self.line_width)
                elif self.current_shape == "circle":
                    self.shape_id = self.canvas.create_oval(self.shape_start_x, self.shape_start_y, event.x, event.y, outline=self.drawing_color, width=self.line_width)
            else:
                current_x, current_y = event.x, event.y
                self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.drawing_color, width=self.line_width, capstyle=tk.ROUND, smooth=True)
                self.prev_x, self.prev_y = current_x, current_y

    def stop_drawing(self, event):
        self.is_drawing = False
        self.shape_start_x = None
        self.shape_start_y = None
        self.shape_id = None

    def change_line_width(self, value):
        self.line_width = int(float(value))

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()

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
            self.drawing_color = self.canvas["bg"]
            self.canvas.config(cursor="circle")

    def _save_canvas(self, file_path):
        canvas_data = {
            "lines": self.canvas.find_all(),
            "text": self.text_widget.get("1.0", tk.END)
        }
        with open(file_path, "wb") as f:
            pickle.dump(canvas_data, f)

    def _load_canvas(self, file_path):
        with open(file_path, "rb") as f:
            canvas_data = pickle.load(f)
            if "lines" in canvas_data:
                for line in canvas_data["lines"]:
                    if self.canvas.coords(line):
                        self.canvas.create_line(self.canvas.coords(line), fill=self.drawing_color, width=self.line_width, capstyle=tk.ROUND, smooth=True)
            if "text" in canvas_data:
                self.text_widget.insert(tk.END, canvas_data["text"])

    def clear_canvas(self):
        self.canvas.delete("all")
        self.eraser_lines.clear()

    def select_shape(self, shape):
        self.current_shape = shape
        if self.is_eraser:
            self.toggle_eraser()

    def select_freehand(self):
        self.current_shape = None
        if self.is_eraser:
            self.toggle_eraser()
