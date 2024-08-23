import tkinter as tk
from tkinter import font
import pickle
from PIL import ImageGrab
import os

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
        self.cursor_Oval_id = None
        self.text_boxes = []
        self.active_textbox = None
        self.textbox_window = None
        self.textbox = None  # Added to store reference to the text widget
        self.font_size = 12  # Default font size
        self.text_color = "black"  # Default text color
        self.font_family = "Arial"  # Default font family
        self.zoom_scale = 1.0 
        self.undo_stack = []
        self.redo_stack = []
        self.current_snapshot = None
        self.text_saving_method = None  # 'editable' or 'image'
        self.selected_textbox = None
        self.selected_textbox_window = None
        self.moving_textbox = False
        self.offset_x = 0
        self.offset_y = 0

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.current_shape == "text":
            self.start_text_drawing(event)
        elif self.current_shape and not self.is_eraser:
            self.start_shape_drawing(event)
        self.store_snapshot()

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
            self.text_saving_method = 'editable'
            self.stop_text_drawing(event)
        self.store_snapshot()

    def start_text_drawing(self, event):
        self.shape_start_x, self.shape_start_y = self.canvas.canvasx(event.x) / self.zoom_scale, self.canvas.canvasy(event.y) / self.zoom_scale
        self.active_textbox = self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, self.shape_start_x, self.shape_start_y, outline=self.drawing_color, width=self.line_width)

    def stop_text_drawing(self, event):
        self.create_textbox(self.shape_start_x, self.shape_start_y, event.x, event.y)
        self.shape_start_x = None
        self.shape_start_y = None
        self.shape_id = None

    def store_snapshot(self):
        self.undo_stack.append(self.get_canvas_snapshot())
        self.redo_stack.clear()

    def get_canvas_snapshot(self):
        items = self.canvas.find_all()
        snapshot = []
        for item in items:
            item_type = self.canvas.type(item)
            item_coords = self.canvas.coords(item)
            item_options = self.canvas.itemconfig(item)
            item_tags = self.canvas.gettags(item)
            snapshot.append((item_type, item_coords, item_options, item_tags))
        return snapshot
    
    def restore_snapshot(self, snapshot):
        for item in snapshot:
            item_type, item_coords, item_options, item_tags = item
            if item_type == "line":
                self.canvas.create_line(*item_coords, **{key: val[-1] for key, val in item_options.items()})
            elif item_type == "rectangle":
                self.canvas.create_rectangle(*item_coords, **{key: val[-1] for key, val in item_options.items()})
            elif item_type == "oval":
                self.canvas.create_oval(*item_coords, **{key: val[-1] for key, val in item_options.items()})
            elif item_type == "text":
                self.canvas.create_text(*item_coords, **{key: val[-1] for key, val in item_options.items()})
            elif item_type == "window":
                self.canvas.create_window(*item_coords, **{key: val[-1] for key, val in item_options.items()})
            else:
                print(f"Unsupported item type: {item_type}")


    def start_text_drawing(self, event):
        self.shape_start_x, self.shape_start_y = self.canvas.canvasx(event.x) / self.zoom_scale, self.canvas.canvasy(event.y) / self.zoom_scale
        self.active_textbox = self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, self.shape_start_x, self.shape_start_y, outline=self.drawing_color, width=self.line_width)


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
        elif self.current_shape == "Oval":
            self.shape_id = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=self.drawing_color, width=self.line_width)

    def update_shape(self, current_x, current_y):
        if self.shape_id:
            self.canvas.delete(self.shape_id)
        if self.current_shape == "line":
            self.shape_id = self.canvas.create_line(self.shape_start_x, self.shape_start_y, current_x, current_y, fill=self.drawing_color, width=self.line_width)
        elif self.current_shape == "rectangle":
            self.shape_id = self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, current_x, current_y, outline=self.drawing_color, width=self.line_width)
        elif self.current_shape == "Oval":
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

        # Adjust position and size by the zoom scale
        width = int(abs(x2 - x1) * self.zoom_scale)
        height = int(abs(y2 - y1) * self.zoom_scale)
        pos_x = int(min(x1, x2) * self.zoom_scale)
        pos_y = int(min(y1, y2) * self.zoom_scale)

        self.textbox_window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        # Set font and other text properties
        text_font = font.Font(family=self.font_family, size=self.font_size)
        self.textbox = tk.Text(self.textbox_window, bg=self.canvas["bg"], fg=self.text_color, wrap="word", font=text_font)
        self.textbox.pack(fill="both", expand=True)
        self.textbox.focus_set()
        self.textbox.bind("<KeyRelease>", self.update_textbox_size)
        self.textbox_window.bind("<Escape>", self.add_text_as_image)
        self.textbox_window.protocol("WM_DELETE_WINDOW", self.on_popup_close)
        self.textbox_window.bind("<FocusOut>", self.on_popup_focusout)

    # the next two functions return the None.destroy() exception, but i think issok
    def update_textbox_size(self, event=None):
        if self.textbox:
            text_content = self.textbox.get("1.0", "end-1c").strip()
            text_font = font.Font(family=self.font_family, size=self.font_size)
            lines = text_content.split('\n')
            width = max(text_font.measure(line) for line in lines) + 10  # Adding some padding
            height = text_font.metrics("linespace") * len(lines) + 10    # Adding some padding

            # Update the size of the popup
            self.textbox_window.geometry(f"{width}x{height}")

            # Update the size of the rectangle on the canvas
            x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)
            self.canvas.coords(self.active_textbox, x1, y1, x1 + width, y1 + height)

    def on_popup_close(self):
        self.text_saving_method = 'image'
        self.add_text_as_image()
        if self.textbox_window:
            self.textbox_window.destroy()
            self.textbox_window = None

    def on_popup_focusout(self, event):
        if self.textbox_window is not None:
            self.canvas.delete("active_textbox")
            self.add_text_as_editable()
            self.textbox_window.destroy()
            self.textbox_window = None

    def add_text_as_editable(self, event=None):
        if self.textbox_window:
            text_content = self.textbox.get("1.0", "end-1c").strip()
            if text_content:
                x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)
                text_x = min(x1, x2) / self.zoom_scale
                text_y = min(y1, y2) / self.zoom_scale
                text_font = font.Font(family=self.font_family, size=self.font_size)

                # Create the Text widget for the canvas
                text_widget = tk.Text(self.canvas, bg=self.canvas["bg"], fg=self.text_color, wrap="word", font=text_font, borderwidth=0)
                text_widget.insert("1.0", text_content)
                text_widget.configure(state="normal")  # Make the text editable

                # Calculate the required size for the text box
                lines = text_content.split('\n')
                width = max(text_font.measure(line) for line in lines)
                height = text_font.metrics("linespace") * len(lines)

                # Create a canvas window with the text widget, setting its size
                text_widget_window = self.canvas.create_window(text_x, text_y, window=text_widget, anchor="nw", width=width, height=height)
                text_widget.bind("<Button-1>", lambda e, tw=text_widget, tw_id=text_widget_window: self.select_textbox(e, tw, tw_id))
                self.text_boxes.append(text_widget_window)

            self.canvas.delete(self.active_textbox)

        if self.textbox_window:
            self.textbox_window.destroy()
            self.textbox_window = None

        self.current_shape = None
        self.active_textbox = None
        self.shape_start_x = None
        self.shape_start_y = None
        self.text_saving_method = None


    def add_text_as_image(self, event=None):
        if self.textbox_window:
            text_content = self.textbox.get("1.0", "end-1c").strip()
            if text_content:
                x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)
                text_x = min(x1, x2) / self.zoom_scale
                text_y = min(y1, y2) / self.zoom_scale
                text_font = font.Font(family=self.font_family, size=self.font_size)

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
        self.text_saving_method = None

    def select_textbox(self, event, text_widget, text_widget_window):
        if self.selected_textbox:
            self.deselect_textbox()

        self.selected_textbox = text_widget
        self.selected_textbox.configure(state="normal", bg="lightgray")
        self.selected_textbox.focus_set()

        # Bind events with proper arguments
        self.selected_textbox.bind("<B1-Motion>", lambda e: self.move_textbox(e, text_widget_window))
        self.selected_textbox.bind("<ButtonRelease-1>", self.stop_moving_textbox)
        self.selected_textbox.bind("<Delete>", lambda e: self.delete_textbox(text_widget_window))

        self.offset_x = event.x
        self.offset_y = event.y

    def deselect_textbox(self):
        if self.selected_textbox:
            self.selected_textbox.configure(state="disabled", bg=self.canvas["bg"])  # Disable editing
            self.selected_textbox.unbind("<B1-Motion>")
            self.selected_textbox.unbind("<ButtonRelease-1>")
            self.selected_textbox.unbind("<Delete>")
            self.selected_textbox = None

    def move_textbox(self, event, text_widget_window):
        if self.selected_textbox:
            x = self.canvas.canvasx(event.x) - self.offset_x
            y = self.canvas.canvasy(event.y) - self.offset_y
            self.canvas.move(text_widget_window, x, y)
            self.offset_x = event.x
            self.offset_y = event.y

    def stop_moving_textbox(self,event=None):
        self.deselect_textbox()

    def delete_textbox(self, text_widget_window):
        self.canvas.delete(text_widget_window)
        if self.selected_textbox:
            self.deselect_textbox()

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
        if self.cursor_Oval_id:
            self.canvas.delete(self.cursor_Oval_id)
        self.root.bind("<Motion>", self.draw_cursor_Oval)

    def draw_cursor_Oval(self, event):
        if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            if self.cursor_Oval_id:
                self.canvas.delete(self.cursor_Oval_id)
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            radius = self.line_width / 2
            self.cursor_Oval_id = self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline=self.drawing_color, width=1
            )
        else:
            if self.cursor_Oval_id:
                self.canvas.delete(self.cursor_Oval_id)
            self.cursor_Oval_id = None

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
    def _save_canvas_as_image(self, file_path):
        # Get the coordinates of the canvas relative to the screen
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

#        # Adding slight adjustment to the left and top offsets
#        if self.root.attributes("-fullscreen"):
#            adjustment_x = 0  # No adjustment needed for fullscreen
#            adjustment_y = 0
#        else:
#            adjustment_x = +70  # Adjustment needed for windowed mode
#            adjustment_y = +30

        ImageGrab.grab(bbox=(x , y , x1, y1)).save(file_path)


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
    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.get_canvas_snapshot())
            snapshot = self.undo_stack.pop()
            self.canvas.delete("all")
            self.restore_snapshot(snapshot)
            #repeated to fix the double clicking of uno error
            # i know this is bad code, but i fw it for now
            #tho this doesn't fix the err completely (if you click the cursor somewhere on the scrn, it is considered as a snapshot. gotta fix that too, somehow.)
            self.redo_stack.append(self.get_canvas_snapshot())        
            snapshot = self.undo_stack.pop()
            self.canvas.delete("all")
            self.restore_snapshot(snapshot)

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.get_canvas_snapshot())
            snapshot = self.redo_stack.pop()
            self.canvas.delete("all")
            self.restore_snapshot(snapshot)
            # same reason as in the undo function
            self.undo_stack.append(self.get_canvas_snapshot())
            snapshot = self.redo_stack.pop()
            self.canvas.delete("all")
            self.restore_snapshot(snapshot)
