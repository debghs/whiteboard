import tkinter as tk
from tkinter import font

class CanvasOperations:
    def __init__(self, canvas, zoom_scale=1.0):
        self.canvas = canvas
        self.zoom_scale = zoom_scale
        self.eraser_lines = []
        self.cursor_Oval_id = None
        self.history = []
        self.current_state = -1
        self.max_history = 50

    def draw_freehand(self, prev_x, prev_y, current_x, current_y, color, line_width):
        self.canvas.create_line(prev_x, prev_y, current_x, current_y, 
                              fill=color, width=line_width, 
                              capstyle=tk.ROUND, smooth=True)

    def draw_eraser(self, prev_x, prev_y, current_x, current_y, line_width):
        line = self.canvas.create_line(prev_x, prev_y, current_x, current_y, 
                                     fill=self.canvas["bg"], width=line_width, 
                                     capstyle=tk.ROUND, smooth=True, tags="eraser")
        self.eraser_lines.append(line)
        return current_x, current_y

    def draw_shape(self, shape_type, start_x, start_y, current_x, current_y, color, line_width):
        if shape_type == "line":
            return self.canvas.create_line(start_x, start_y, current_x, current_y, 
                                         fill=color, width=line_width)
        elif shape_type == "rectangle":
            return self.canvas.create_rectangle(start_x, start_y, current_x, current_y, 
                                             outline=color, width=line_width)
        elif shape_type == "Oval":
            return self.canvas.create_oval(start_x, start_y, current_x, current_y, 
                                        outline=color, width=line_width)

    def update_shape(self, shape_id, shape_type, start_x, start_y, current_x, current_y, color, line_width):
        if shape_id:
            self.canvas.delete(shape_id)
        return self.draw_shape(shape_type, start_x, start_y, current_x, current_y, color, line_width)

    def draw_cursor(self, event, color, line_width):
        if self.cursor_Oval_id:
            self.canvas.delete(self.cursor_Oval_id)
            self.cursor_Oval_id = None

        if event is None:
            return

        if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            radius = line_width / 2
            self.cursor_Oval_id = self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline=color, width=1
            )

    def save_state(self):
        state = []
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            item_type = self.canvas.type(item)
            config = {key: self.canvas.itemcget(item, key) for key in self.canvas.itemconfig(item)}
            tags = self.canvas.gettags(item)
            state.append((item_type, coords, config, tags))
        
        # Remove future states if we're in the middle of the history
        self.history = self.history[:self.current_state + 1]
        self.history.append(state)
        
        # Keep history size manageable
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.current_state += 1

    def undo(self):
        if self.current_state > 0:
            self.current_state -= 1
            self.restore_state(self.history[self.current_state])

    def redo(self):
        if self.current_state < len(self.history) - 1:
            self.current_state += 1
            self.restore_state(self.history[self.current_state])

    def restore_state(self, state):
        self.canvas.delete("all")
        self.eraser_lines.clear()
        for item_type, coords, config, tags in state:
            item = None
            if item_type == "line":
                item = self.canvas.create_line(*coords)
            elif item_type == "rectangle":
                item = self.canvas.create_rectangle(*coords)
            elif item_type == "oval":
                item = self.canvas.create_oval(*coords)
            elif item_type == "text":
                item = self.canvas.create_text(*coords)
            
            if item:
                for key, value in config.items():
                    try:
                        if "eraser" in tags and key == "fill":
                            value = self.canvas["bg"]
                        self.canvas.itemconfig(item, **{key: value})
                    except tk.TclError:
                        pass
                if "eraser" in tags:
                    self.eraser_lines.append(item)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.eraser_lines.clear()
        self.save_state()

    def update_eraser_lines_color(self):
        for line in self.eraser_lines:
            self.canvas.itemconfig(line, fill=self.canvas["bg"])

    def zoom(self, factor):
        self.canvas.scale("all", 0, 0, factor, factor)
        self.zoom_scale *= factor
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reset_zoom(self, initial_zoom_level, initial_scroll_x, initial_scroll_y):
        self.canvas.scale("all", 0, 0, 1/initial_zoom_level, 1/initial_zoom_level)
        self.canvas.configure(scrollregion=(0, 0, 10000, 10000))
        self.canvas.xview_moveto(initial_scroll_x)
        self.canvas.yview_moveto(initial_scroll_y)
        self.zoom_scale = 1.0
