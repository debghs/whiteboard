import tkinter as tk
from tkinter import font

class TextOperations:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.text_boxes = []
        self.active_textbox = None
        self.textbox_window = None
        self.textbox = None
        self.selected_textbox = None
        self.selected_textbox_window = None
        self.moving_textbox = False
        self.offset_x = 0
        self.offset_y = 0
        self.font_size = 12
        self.text_color = "black"
        self.font_family = "Arial"
        self.zoom_scale = 1.0
        self.text_content = ""

    def start_text_drawing(self, event, drawing_color, line_width):
        self.shape_start_x = self.canvas.canvasx(event.x)
        self.shape_start_y = self.canvas.canvasy(event.y)
        self.active_textbox = self.canvas.create_rectangle(
            self.shape_start_x, self.shape_start_y,
            self.shape_start_x, self.shape_start_y,
            outline=drawing_color, width=line_width
        )

    def update_text_drawing(self, event):
        if self.active_textbox:
            current_x = self.canvas.canvasx(event.x)
            current_y = self.canvas.canvasy(event.y)
            self.canvas.coords(
                self.active_textbox,
                self.shape_start_x, self.shape_start_y,
                current_x, current_y
            )

    def stop_text_drawing(self, event):
        if self.active_textbox:
            x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)
            self.create_text_window(x1, y1, x2, y2)
            self.canvas.delete(self.active_textbox)
            self.active_textbox = None

    def create_text_window(self, x1, y1, x2, y2):
        self.textbox_window = tk.Toplevel(self.root)
        self.textbox_window.overrideredirect(True)
        self.textbox_window.attributes('-topmost', True)

        width = int(abs(x2 - x1) * self.zoom_scale)
        height = int(abs(y2 - y1) * self.zoom_scale)
        pos_x = int(min(x1, x2))
        pos_y = int(min(y1, y2))

        self.textbox_window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        text_font = font.Font(family=self.font_family, size=self.font_size)
        self.textbox = tk.Text(self.textbox_window, bg=self.canvas["bg"], fg=self.text_color, wrap="word", font=text_font)
        self.textbox.pack(fill="both", expand=True)
        self.textbox.focus_set()
        self.textbox.bind("<KeyRelease>", self.update_textbox_size)
        self.textbox_window.bind("<Escape>", self.add_text_as_image)
        self.textbox_window.protocol("WM_DELETE_WINDOW", self.on_popup_close)
        self.textbox_window.bind("<FocusOut>", self.on_popup_focusout)

    def update_textbox_size(self, event=None):
        if self.textbox:
            text_content = self.textbox.get("1.0", "end-1c").strip()
            text_font = font.Font(family=self.font_family, size=self.font_size)
            lines = text_content.split('\n')
            width = max(text_font.measure(line) for line in lines) + 10
            height = text_font.metrics("linespace") * len(lines) + 10

            self.textbox_window.geometry(f"{width}x{height}")

            if self.active_textbox:
                x1, y1, x2, y2 = self.canvas.coords(self.active_textbox)
                self.canvas.coords(self.active_textbox, x1, y1, x1 + width, y1 + height)

    def add_text_as_editable(self):
        if self.textbox_window:
            text_content = self.textbox.get("1.0", "end-1c").strip()
            if text_content:
                geometry = self.textbox_window.geometry()
                x, y = map(int, geometry.split("+")[1:])
                text_x = x / self.zoom_scale
                text_y = y / self.zoom_scale
                text_font = font.Font(family=self.font_family, size=self.font_size)

                text_widget = tk.Text(self.canvas, bg=self.canvas["bg"], fg=self.text_color, wrap="word", font=text_font, borderwidth=0, highlightthickness=0)
                text_widget.insert("1.0", text_content)
                text_widget.configure(state="normal")

                lines = text_content.split('\n')
                width = max(text_font.measure(line) for line in lines) + 10
                height = text_font.metrics("linespace") * len(lines) + 10

                text_widget_window = self.canvas.create_window(text_x, text_y, window=text_widget, anchor="nw", width=width, height=height)
                text_widget.bind("<Button-1>", lambda e, tw=text_widget, tw_id=text_widget_window: self.select_textbox(e, tw, tw_id))
                self.text_boxes.append(text_widget_window)

            if self.active_textbox:
                self.canvas.delete(self.active_textbox)
            self.textbox_window.destroy()
            self.textbox_window = None
            self.textbox = None

    def add_text_as_image(self, event=None):
        if self.textbox_window:
            text_content = self.textbox.get("1.0", "end-1c").strip()
            if text_content:
                # Get the current position and size of the text window
                geometry = self.textbox_window.geometry()
                x, y = map(int, geometry.split("+")[1:])
                text_x = x / self.zoom_scale
                text_y = y / self.zoom_scale
                text_font = font.Font(family=self.font_family, size=self.font_size)

                text_item = self.canvas.create_text(
                    text_x, text_y,
                    text=text_content, fill=self.text_color, anchor="nw", font=text_font
                )

            if self.active_textbox:
                self.canvas.delete(self.active_textbox)
            self.textbox_window.destroy()
            self.textbox_window = None
            self.textbox = None

    def select_textbox(self, event, text_widget, text_widget_window):
        if self.selected_textbox:
            self.deselect_textbox()

        self.selected_textbox = text_widget
        self.selected_textbox.configure(state="normal", bg="lightgray")
        self.selected_textbox.focus_set()

        self.selected_textbox.bind("<B1-Motion>", lambda e: self.move_textbox(e, text_widget_window))
        self.selected_textbox.bind("<ButtonRelease-1>", self.stop_moving_textbox)
        self.selected_textbox.bind("<Delete>", lambda e: self.delete_textbox(text_widget_window))

        self.offset_x = event.x
        self.offset_y = event.y

    def deselect_textbox(self):
        if self.selected_textbox:
            self.selected_textbox.configure(state="disabled", bg=self.canvas["bg"])
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

    def stop_moving_textbox(self, event=None):
        self.deselect_textbox()

    def delete_textbox(self, text_widget_window):
        self.canvas.delete(text_widget_window)
        if self.selected_textbox:
            self.deselect_textbox()

    def change_font_family(self, font_family):
        self.font_family = font_family

    def set_font_size(self, size):
        self.font_size = size

    def set_text_color(self, color):
        self.text_color = color

    def set_zoom_scale(self, scale):
        self.zoom_scale = scale

    def update_text_backgrounds(self):
        for text_window_id in self.text_boxes:
            text_widget = self.canvas.nametowidget(self.canvas.itemcget(text_window_id, "window"))
            if text_widget:
                text_widget.configure(bg=self.canvas["bg"])

    def on_popup_close(self):
        if self.textbox_window:
            self.add_text_as_image()

    def on_popup_focusout(self, event):
        if self.textbox_window:
            self.text_content = self.textbox.get("1.0", "end-1c").strip()
            if not self.text_content:
                self.textbox_window.destroy()
                self.textbox_window = None
                self.textbox = None
            else:
                self.add_text_as_editable()
