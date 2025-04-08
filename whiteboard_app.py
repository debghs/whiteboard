import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.font import families
from canvas_operations import CanvasOperations
from text_operations import TextOperations
from file_operations import FileOperations

class WhiteboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")
        self.root.geometry("1050x600+150+50")
        self.root.resizable(True, True)

        # Initialize state variables
        self.is_drawing = False
        self.drawing_color = "black"
        self.line_width = 2
        self.is_dark_mode = False
        self.is_eraser = False
        self.last_drawing_color = "black"
        self.last_line_width = 2
        self.current_shape = None
        self.shape_start_x = None
        self.shape_start_y = None
        self.shape_id = None
        self.initial_zoom_level = 1.0
        self.initial_scroll_x = 0
        self.initial_scroll_y = 0

        # Initialize operations modules
        self.canvas = tk.Canvas(self.root, bg="white", scrollregion=(0, 0, 10000, 10000))
        self.canvas_ops = CanvasOperations(self.canvas)
        self.text_ops = TextOperations(self.canvas, self.root)
        self.file_ops = FileOperations(self.canvas)

        self.create_widgets()
        self.setup_bindings()

    def create_widgets(self):
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side="top", fill="x")

        # Create buttons
        self.color_button = tk.Button(self.controls_frame, text="Color", relief="groove", command=self.change_pen_color)
        self.clear_button = tk.Button(self.controls_frame, text="Clear", relief="groove", command=self.clear_canvas)
        self.save_type_var = tk.StringVar(value="Pickle")
        self.save_type_menu = tk.OptionMenu(self.controls_frame, self.save_type_var, "Pickle", "Image")
        self.save_button = tk.Button(self.controls_frame, text="Save", relief="groove", command=self.save_canvas)
        self.load_button = tk.Button(self.controls_frame, text="Load", relief="groove", command=self.load_canvas)
        self.dark_mode_button = tk.Button(self.controls_frame, text="Dark Mode", relief="groove", command=self.toggle_dark_mode)
        self.eraser_button = tk.Button(self.controls_frame, text="Eraser", relief="groove", command=self.toggle_eraser)
        self.notes_button = tk.Button(self.controls_frame, text="Notes", relief="groove", command=self.toggle_notes_section)
        self.freehand_button = tk.Button(self.controls_frame, text="Freehand", relief="groove", command=self.select_freehand)
        self.line_button = tk.Button(self.controls_frame, text="Line", relief="groove", command=lambda: self.select_shape("line"))
        self.rectangle_button = tk.Button(self.controls_frame, text="Rectangle", relief="groove", command=lambda: self.select_shape("rectangle"))
        self.oval_button = tk.Button(self.controls_frame, text="Oval", relief="groove", command=lambda: self.select_shape("Oval"))
        self.text_button = tk.Button(self.controls_frame, text="Text", relief="groove", command=lambda: self.select_shape("text"))
        self.home_button = tk.Button(self.controls_frame, text="Home", relief="groove", command=self.reset_view)

        # Pack buttons
        self.undo_button = tk.Button(self.controls_frame, text="Undo", relief="groove", command=self.canvas_ops.undo)
        self.redo_button = tk.Button(self.controls_frame, text="Redo", relief="groove", command=self.canvas_ops.redo)

        buttons = [self.color_button, self.clear_button, self.save_button, self.save_type_menu,
                  self.load_button, self.dark_mode_button, self.eraser_button, self.notes_button,
                  self.freehand_button, self.line_button, self.rectangle_button, self.oval_button,
                  self.text_button, self.home_button, self.undo_button, self.redo_button]
        
        for button in buttons:
            button.pack(side="left", padx=5, pady=5)

        # Create line width controls
        self.line_width_label = tk.Label(self.controls_frame, text="Width:")
        self.line_width_label.pack(side="left", padx=5, pady=5)
        
        self.line_width_slider = tk.Scale(self.controls_frame, from_=1, to=100, orient="horizontal",
                                         command=self.change_line_width)
        self.line_width_slider.set(self.line_width)
        self.line_width_slider.pack(side="left", padx=5, pady=5, fill="x")

        # Create font controls
        self.setup_font_controls()

        # Create scrollbars
        self.scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create notes text widget
        self.text_widget = tk.Text(self.root, height=6, width=120)
        self.text_widget.pack_forget()

    def setup_font_controls(self):
        # Font size controls
        self.font_size_label = tk.Label(self.controls_frame, text="Font Size:")
        self.font_size_label.pack(side="left", padx=5, pady=5)
        
        self.font_size_var = tk.IntVar(value=12)
        self.font_size_menu = tk.OptionMenu(self.controls_frame, self.font_size_var, *range(8, 73, 2))
        self.font_size_menu.pack(side="left", padx=5, pady=5)

        # Font family controls
        self.font_family_label = tk.Label(self.controls_frame, text="Font Family:")
        self.font_family_label.pack(side="left", padx=5, pady=5)
        
        self.font_family_var = tk.StringVar(value="Arial")
        self.font_family_menu = tk.OptionMenu(self.controls_frame, self.font_family_var,
                                             *families(), command=self.change_font_family)
        self.font_family_menu.pack(side="left", padx=5, pady=5)

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.root.bind("<Control-plus>", self.zoom_in)
        self.root.bind("<Control-minus>", self.zoom_out)

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x = self.canvas.canvasx(event.x)
        self.prev_y = self.canvas.canvasy(event.y)
        
        if self.current_shape == "text":
            self.text_ops.start_text_drawing(event, self.drawing_color, self.line_width)
        elif self.current_shape and not self.is_eraser:
            self.shape_start_x = event.x
            self.shape_start_y = event.y
            self.shape_id = self.canvas_ops.draw_shape(
                self.current_shape, event.x, event.y, event.x, event.y,
                self.drawing_color, self.line_width
            )

    def draw(self, event):
        if not self.is_drawing:
            return
            
        current_x = self.canvas.canvasx(event.x)
        current_y = self.canvas.canvasy(event.y)
        
        if self.is_eraser:
            self.prev_x, self.prev_y = self.canvas_ops.draw_eraser(
                self.prev_x, self.prev_y, current_x, current_y, self.line_width
            )
        elif self.current_shape == "text":
            self.text_ops.update_text_drawing(event)
        elif self.current_shape:
            self.shape_id = self.canvas_ops.update_shape(
                self.shape_id, self.current_shape,
                self.shape_start_x, self.shape_start_y, current_x, current_y,
                self.drawing_color, self.line_width
            )
        else:
            self.canvas_ops.draw_freehand(
                self.prev_x, self.prev_y, current_x, current_y,
                self.drawing_color, self.line_width
            )
            self.prev_x, self.prev_y = current_x, current_y
            self.canvas_ops.save_state()

    def stop_drawing(self, event):
        self.is_drawing = False
        if self.current_shape == "text":
            self.text_ops.stop_text_drawing(event)
        self.canvas_ops.save_state()

    def change_line_width(self, value):
        self.line_width = int(float(value))
        self.canvas_ops.draw_cursor(None, self.drawing_color, self.line_width)

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color
            self.text_ops.set_text_color(color)
            if self.is_eraser:
                self.toggle_eraser()

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()

    def update_theme(self):
        bg_color = "gray10" if self.is_dark_mode else "white"
        fg_color = "white" if self.is_dark_mode else "black"
        ctrl_bg = "gray20" if self.is_dark_mode else "white"
        
        self.root.config(bg="black" if self.is_dark_mode else "white")
        self.canvas.config(bg=bg_color)
        self.controls_frame.config(bg=ctrl_bg)
        self.text_ops.update_text_backgrounds()
        
        # Update controls colors
        for widget in [self.line_width_label, self.font_size_label, self.font_family_label]:
            widget.config(bg=ctrl_bg, fg=fg_color)
            
        self.line_width_slider.config(bg=ctrl_bg, fg=fg_color,
                                     troughcolor="gray30" if self.is_dark_mode else "lightgray")
        self.text_widget.config(bg="gray30" if self.is_dark_mode else "white", fg=fg_color)
        
        # Update all buttons
        button_bg = "gray30" if self.is_dark_mode else "white"
        for button in [self.color_button, self.clear_button, self.save_button,
                      self.load_button, self.dark_mode_button, self.eraser_button,
                      self.notes_button, self.freehand_button, self.line_button,
                      self.rectangle_button, self.oval_button, self.text_button,
                      self.home_button, self.undo_button, self.redo_button]:
            button.config(bg=button_bg, fg=fg_color)
        for button in [self.color_button, self.clear_button, self.save_button,
                      self.load_button, self.dark_mode_button, self.eraser_button,
                      self.notes_button, self.freehand_button, self.line_button,
                      self.rectangle_button, self.oval_button, self.text_button,
                      self.home_button]:
            button.config(bg=button_bg, fg=fg_color)
            
        self.dark_mode_button.config(text="Light Mode" if self.is_dark_mode else "Dark Mode")
        self.canvas_ops.update_eraser_lines_color()

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

    def select_shape(self, shape):
        self.current_shape = shape
        if self.is_eraser:
            self.toggle_eraser()

    def select_freehand(self):
        self.current_shape = None
        if self.is_eraser:
            self.toggle_eraser()

    def clear_canvas(self):
        self.canvas_ops.clear_canvas()
        self.canvas_ops.save_state()

    def save_canvas(self):
        self.file_ops.show_save_dialog(self.save_type_var.get())

    def load_canvas(self):
        if self.file_ops.show_load_dialog():
            self.canvas_ops.draw_cursor(None, self.drawing_color, self.line_width)

    def toggle_notes_section(self):
        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        else:
            self.text_widget.pack(side="bottom", padx=5, pady=5, fill="x")

    def change_font_family(self, event=None):
        self.text_ops.change_font_family(self.font_family_var.get())

    def zoom_in(self, event=None):
        self.canvas_ops.zoom(1.1)
        self.initial_zoom_level *= 1.1
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_out(self, event=None):
        self.canvas_ops.zoom(0.9)
        self.initial_zoom_level *= 0.9
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reset_view(self):
        self.canvas_ops.reset_zoom(self.initial_zoom_level, self.initial_scroll_x, self.initial_scroll_y)
        self.initial_zoom_level = 1.0
