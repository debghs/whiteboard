import tkinter as tk
from tkinter import font
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
        self.font_family = "Arial"  # Default font family

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.current_shape == "text":
            self.start_text_drawing(event)
        elif self.current_shape and not self.is_eraser:
            self.start_shape_drawing(event)

    def draw(self, event):
        if self.is_drawing:
            current_x, current_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            if self.is_eraser:
                self.draw_eraser(current_x, current_y)
            elif self.current_shape == "text":
                self.update_textbox(current_x, current_y)
            elif self.current_shape:
                self.update_shape(current_x, current_y)
            else:
                self.draw_freehand(current_x, current_y)

    def stop_drawing(self, event):
        self.is_drawing = False
        if self.current_shape == "text":
            self.stop_text_drawing(event)

    # ... (new functions added below)

    def start_text_drawing(self, event):
        self.shape_start_x, self.shape_start_y = event.x, event.y
        self.active_textbox = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)

    def update_textbox(self, current_x, current_y):
        self.canvas.coords(self.active_textbox, self.shape_start_x, self.shape_start_y, current_x, current_y)

    def stop_text_drawing(self, event):
        self.create_textbox(self.shape_start_x, self.shape_start_y, event.x, event.y)
        self.shape_start_x = None
        self.shape_start_y = None
        self.shape_id = None

    def start_shape_drawing(self, event):
        self.shape_start_x, self.shape_start_y = event.x, event.y
        if self.current_shape == "line":
            self.shape_id = self.canvas.create_line(event.x, event.y, event.x, event.y, fill=self.drawing_color, width=self.line_width)
        elif self.current_shape == "rectangle":
            self.shape_id = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)
        elif self.current_shape == "circle":
            self.shape_id = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)

    def update_shape(self, current_x, current_y):
        if self.shape_id:
            self.canvas.delete(self.shape_id)
        if self.current_shape == "line":
            self.shape_id = self.canvas.create_line(self.shape_start_x, self.shape_start_y, current_x, current_y, fill=self.drawing_color, width=self.line_width)
        elif self.current_shape == "rectangle":
            self.shape_id = self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, current_x, current_y, outline=self.drawing_color, width=self.line_width)
        elif self.current_shape == "circle":
            self.shape_id = self.canvas.create_oval(self.shape_start_x, self.shape_start_y, current_x, current_y, outline=self.drawing_color, width=self.line_width)

    def draw_eraser(self, current_x, current_y):
        line = self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.canvas["bg"], width=self.line_width, capstyle=tk.ROUND, smooth=True, tags="eraser")
        self.eraser_lines.append(line)
        self.prev_x, self.prev_y = current_x, current_y

    def draw_freehand(self, current_x, current_y):
        self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.drawing_color, width=self.line_width, capstyle=tk.ROUND, smooth=True)
        self.prev_x, self.prev_y = current_x, current_y

    def create_textbox(self, x1, y1, x2, y2):
        self.textbox_window = tk.Toplevel(self.root)
        self.textbox_window.overrideredirect(True)
        self.textbox_window.geometry(f"{abs(x2 - x1)}x{abs(y2 - y1)}+{min(x1, x2)}+{min(y1, y2)}")

        self.font_size = self.font_size_var.get() if self.font_size_var else 12

        # Use font.Font to set the desired font family
        text_font = font.Font(family=self.font_family, size=self.font_size)
        self.textbox = tk.Text(self.textbox_window, bg=self.canvas["bg"], fg=self.text_color, wrap="word", font=text_font)
        self.textbox.pack(fill="both", expand=True)
        self.textbox.focus_set()
        self.textbox_window.bind("<Escape>", self.add_text_to_canvas)

    def add_text_to_canvas(self, event=None):
        if self.textbox_window:
            text_content = self.textbox.get("1.0", "end-1c").strip()

            if text_content:
                x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)

                # Calculate the actual coordinates of the text box
                text_x = min(x1, x2)
                text_y = min(y1, y2)

                # Use font.Font to set the desired font family
                text_font = font.Font(family=self.font_family, size=self.font_size)

                # Create text with the selected font family
                text_item = self.canvas.create_text(
                    text_x, text_y,
                    text=text_content, fill=self.text_color, anchor="nw", font=text_font
                )

            self.canvas.delete(self.active_textbox)

        if self.textbox_window:
            self.textbox_window.destroy()
            self.textbox_window = None

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
        self.update_eraser_lines()  # Update eraser lines color when mode is toggled

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

    def _load_canvas(self, file_path):
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

        self.update_eraser_lines()  # Ensure eraser lines are updated after loading the canvas

    def save_canvas(self, file_path):
        self._save_canvas(file_path)

    def load_canvas(self, file_path):
        self._load_canvas(file_path)
        self.update_cursor()  # Ensure the cursor is updated after loading the canvas

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

    def update_eraser_lines(self):
        bg_color = self.canvas["bg"]
        for line in self.eraser_lines:
            self.canvas.itemconfig(line, fill=bg_color)

    def change_font_family(self, font_family):
        self.font_family = font_family
