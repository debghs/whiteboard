import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, PhotoImage
from tkinter.font import families
from whiteboard_logic import WhiteboardLogic

class WhiteboardApp(WhiteboardLogic):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Whiteboard")
        self.root.geometry("1050x600+150+50")
        self.root.resizable(True, True)
        icon_img = PhotoImage(file="assets/icon.png")
        self.root.iconphoto(False, icon_img)
        self.create_widgets()
        self.update_cursor()
        self.root.bind("<Control-+>", self.zoom_in)
        self.root.bind("<Control-*>", self.zoom_out)
        self.initial_zoom_level = 1
        self.initial_scroll_x = 0
        self.initial_scroll_y = 0

    def create_widgets(self):
        self.controls_frame = ttk.Frame(self.root)
        self.controls_frame.grid(row=0, column=0, sticky="ew")
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        # Creating buttons with grid layout
        self.color_button = ttk.Button(self.controls_frame, text="Color", command=self.change_pen_color)
        self.clear_button = ttk.Button(self.controls_frame, text="Clear", command=self.clear_canvas)
        self.save_type_var = tk.StringVar(value="Pickle")
        self.save_type_menu = ttk.Combobox(self.controls_frame, textvariable=self.save_type_var, values=["Pickle", "Image"], state="readonly")
        self.save_button = ttk.Button(self.controls_frame, text="Save", command=self.save_canvas)
        self.load_button = ttk.Button(self.controls_frame, text="Load", command=self.load_canvas)
        self.dark_mode_button = ttk.Button(self.controls_frame, text="Dark Mode", command=self.toggle_dark_mode)
        self.eraser_button = ttk.Button(self.controls_frame, text="Eraser", command=self.toggle_eraser)
        self.notes_button = ttk.Button(self.controls_frame, text="Notes", command=self.toggle_notes_section)
        self.freehand_button = ttk.Button(self.controls_frame, text="Freehand", command=self.select_freehand)
        self.line_button = ttk.Button(self.controls_frame, text="Line", command=lambda: self.select_shape("line"))
        self.rectangle_button = ttk.Button(self.controls_frame, text="Rectangle", command=lambda: self.select_shape("rectangle"))
        self.oval_button = ttk.Button(self.controls_frame, text="Oval", command=lambda: self.select_shape("Oval"))
        self.text_button = ttk.Button(self.controls_frame, text="Text", command=lambda: self.select_shape("text"))
        self.home_button = ttk.Button(self.controls_frame, text="Home", command=self.reset_view)
        self.undo_button = ttk.Button(self.controls_frame, text="Undo", command=self.undo)
        self.redo_button = ttk.Button(self.controls_frame, text="Redo", command=self.redo)

        # Adding buttons to the grid
        buttons = [
            self.color_button, self.clear_button, self.save_button, self.save_type_menu, self.load_button,
            self.dark_mode_button, self.eraser_button, self.notes_button, self.freehand_button,
            self.line_button, self.rectangle_button, self.oval_button, self.text_button,
            self.home_button, self.undo_button, self.redo_button
        ]

        for i, button in enumerate(buttons):
            button.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.controls_frame.grid_columnconfigure(i, weight=1)

        self.line_width_label = ttk.Label(self.controls_frame, text="Width:")
        self.line_width_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.line_width_slider = ttk.Scale(self.controls_frame, from_=1, to=100, orient="horizontal", command=self.change_line_width)
        self.line_width_slider.set(self.line_width)
        self.line_width_slider.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="ew")
        self.controls_frame.grid_columnconfigure(1, weight=1)

        # Font size selection widget
        self.font_size_label = ttk.Label(self.controls_frame, text="Font Size:")
        self.font_size_label.grid(row=1, column=4, padx=5, pady=5, sticky="e")

        self.font_size_var = tk.IntVar(value=12)
        self.font_size_menu = ttk.Combobox(self.controls_frame, textvariable=self.font_size_var, values=list(range(8, 73, 2)), state="readonly")
        self.font_size_menu.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
        self.controls_frame.grid_columnconfigure(5, weight=1)

        # Font family selection widget
        font_families = families()
        self.font_family_label = ttk.Label(self.controls_frame, text="Font Family:")
        self.font_family_label.grid(row=1, column=6, padx=5, pady=5, sticky="e")

        self.font_family_var = tk.StringVar(value="Arial")  # Default font family
        self.font_family_menu = ttk.Combobox(self.controls_frame, textvariable=self.font_family_var, values=font_families, state="readonly")
        self.font_family_menu.grid(row=1, column=7, padx=5, pady=5, sticky="ew")
        self.controls_frame.grid_columnconfigure(7, weight=1)

        # Canvas with modern scrollbars
        self.canvas = tk.Canvas(self.root, bg="white", scrollregion=(0, 0, 10000, 10000))
        self.scroll_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.grid(row=2, column=0, columnspan=10, sticky="ew")
        self.scroll_y.grid(row=1, column=8, sticky="ns")
        self.canvas.grid(row=1, column=0, columnspan=8, sticky="nsew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Bindings for canvas actions
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.text_widget = tk.Text(self.root, height=6, width=120)
        self.text_widget.grid(row=3, column=0, columnspan=8, sticky="ew")
        self.text_widget.grid_forget()

        self.update_theme()

    def update_theme(self):
        # Update the theme (unchanged from the previous version)
        if self.is_dark_mode:
            self.root.config(bg="black")
            self.canvas.config(bg="gray10")
            self.controls_frame.config(style="Dark.TFrame")
            self.line_width_label.config(style="Dark.TLabel")
            self.line_width_slider.config(style="Dark.Horizontal.TScale")
            self.text_widget.config(bg="gray30", fg="white")
            self.update_button_colors("gray30", "white")
            self.dark_mode_button.config(text="Light Mode")
            self.font_size_label.config(style="Dark.TLabel")
            self.font_size_menu.config(style="Dark.TCombobox")
            self.font_family_label.config(style="Dark.TLabel")
            self.font_family_menu.config(style="Dark.TCombobox")
            self.home_button.config(style="Dark.TButton")
            self.undo_button.config(style="Dark.TButton")
            self.redo_button.config(style="Dark.TButton")
            self.save_type_menu.config(style="Dark.TCombobox")
        else:
            self.root.config(bg="white")
            self.canvas.config(bg="white")
            self.controls_frame.config(style="Light.TFrame")
            self.line_width_label.config(style="Light.TLabel")
            self.line_width_slider.config(style="Light.Horizontal.TScale")
            self.text_widget.config(bg="white", fg="black")
            self.update_button_colors("white", "black")
            self.dark_mode_button.config(text="Dark Mode")
            self.font_size_label.config(style="Light.TLabel")
            self.font_size_menu.config(style="Light.TCombobox")
            self.font_family_label.config(style="Light.TLabel")
            self.font_family_menu.config(style="Light.TCombobox")
            self.home_button.config(style="Light.TButton")
            self.undo_button.config(style="Light.TButton")
            self.redo_button.config(style="Light.TButton")
            self.save_type_menu.config(style="Light.TCombobox")

        #self.update_eraser_lines_color()

    def update_button_colors(self, bg_color, fg_color):
        # Apply ttk styling instead of changing colors directly
        button_list = [
            self.color_button, self.clear_button, self.save_button,
            self.load_button, self.dark_mode_button, self.eraser_button, self.notes_button,
            self.freehand_button, self.line_button, self.rectangle_button, self.oval_button, self.text_button
        ]

        for button in button_list:
            button.style = ttk.Style()
            button.style.configure(f"{button}.TButton", background=bg_color, foreground=fg_color)
            button.configure(style=f"{button}.TButton")

        self.home_button.style = ttk.Style()
        self.home_button.style.configure("Home.TButton", background=bg_color, foreground=fg_color)
        self.home_button.configure(style="Home.TButton")

        self.undo_button.style = ttk.Style()
        self.undo_button.style.configure("Undo.TButton", background=bg_color, foreground=fg_color)
        self.undo_button.configure(style="Undo.TButton")

        self.redo_button.style = ttk.Style()
        self.redo_button.style.configure("Redo.TButton", background=bg_color, foreground=fg_color)
        self.redo_button.configure(style="Redo.TButton")

    def update_eraser_lines_color(self):
        eraser_color = "white" if self.is_dark_mode else "black"
        self.canvas.itemconfig(self.eraser_line_id, fill=eraser_color)
