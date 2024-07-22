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
        self.cursor_circle_id = None
        self.text_boxes = []
        self.active_textbox = None
        self.textbox_window = None
        self.textbox = None  # Added to store reference to the text widget
        self.font_size = 12  # Default font size
        self.text_color = "black"  # Default text color

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = event.x, event.y

        if self.current_shape == "text":
            if self.active_textbox:
                self.canvas.delete(self.active_textbox)
            self.shape_start_x, self.shape_start_y = event.x, event.y
            self.active_textbox = self.canvas.create_rectangle(
                event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)

        elif self.current_shape and not self.is_eraser:
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
            elif self.current_shape == "text":
                self.canvas.coords(self.active_textbox, self.shape_start_x, self.shape_start_y, event.x, event.y)
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
        if self.current_shape == "text":
            self.create_textbox(self.shape_start_x, self.shape_start_y, event.x, event.y)
        self.shape_start_x = None
        self.shape_start_y = None
        self.shape_id = None

    def create_textbox(self, x1, y1, x2, y2):
        self.textbox_window = tk.Toplevel(self.root)
        self.textbox_window.overrideredirect(True)
        self.textbox_window.geometry(f"{abs(x2 - x1)}x{abs(y2 - y1)}+{min(x1, x2)}+{min(y1, y2)}")

        self.font_size = self.font_size_var.get() if self.font_size_var else 12

        self.textbox = tk.Text(self.textbox_window, bg=self.canvas["bg"], fg=self.text_color, wrap="word", font=("Arial", self.font_size))
        self.textbox.pack(fill="both", expand=True)
        self.textbox.focus_set()
        self.textbox_window.bind("<Escape>", self.add_text_to_canvas)
    def add_text_to_canvas(self, event=None):
        if self.textbox_window:
            text_content = self.textbox.get("1.0", "end-1c")
            self.textbox_window.destroy()
            self.textbox_window = None

            if text_content:
                x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)
                # Calculate the center of the rectangle
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                # Calculate the width and height of the rectangle
                width = abs(x2 - x1)
                height = abs(y2 - y1)

                # Create text with the same orientation and margin
                text_item = self.canvas.create_text(
                    center_x, center_y,
                    text=text_content, fill=self.text_color, anchor="center", font=("Arial", self.font_size),
                    width=width  # Set the width to match the textbox width
                )

                # Delete the outline of the textbox
                self.canvas.delete(self.active_textbox)

                # Adjust the text item to maintain the same margins
                bbox = self.canvas.bbox(text_item)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                if text_width > width:
                    scale_factor = width / text_width
                    self.canvas.scale(text_item, center_x, center_y, scale_factor, 1)

        self.current_shape = None
        self.active_textbox = None
        self.shape_start_x = None
        self.shape_start_y = None

    def change_line_width(self, value):
        self.line_width = int(float(value))
        self.update_cursor()

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()

    def toggle_eraser(self):
        if self.is_eraser:
            self.is_eraser = False
            self.drawing_color = self.last_drawing_color
            self.line_width_slider.set(self.last_line_width)
        else:
            self.is_eraser = True
            self.last_drawing_color = self.drawing_color
            self.last_line_width = self.line_width_slider.get()
            self.drawing_color = self.canvas["bg"]
        self.update_cursor()

    def update_cursor(self):
        if self.cursor_circle_id:
            self.canvas.delete(self.cursor_circle_id)
        self.root.bind("<Motion>", self.draw_cursor_circle)

    def draw_cursor_circle(self, event):
        if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            if self.cursor_circle_id:
                self.canvas.delete(self.cursor_circle_id)
            x, y = event.x, event.y
            radius = self.line_width / 2
            self.cursor_circle_id = self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline=self.drawing_color, width=1
            )
        else:
            if self.cursor_circle_id:
                self.canvas.delete(self.cursor_circle_id)
                self.cursor_circle_id = None

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
