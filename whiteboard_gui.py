import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, PhotoImage
from tkinter.font import Font, families
from whiteboard_logic import WhiteboardLogic
import os

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
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side="top", fill="x")

        # Existing widgets
        self.color_button = tk.Button(self.controls_frame, text="Color", relief="groove", command=self.change_pen_color)
        self.clear_button = tk.Button(self.controls_frame, text="Clear", relief="groove", command=self.clear_canvas)

        # Dropdown to select save type
        self.save_type_var = tk.StringVar(value="Pickle")
        self.save_type_menu = tk.OptionMenu(self.controls_frame, self.save_type_var, "Pickle", "Image")
        #self.save_type_menu.pack(side="left", padx=5, pady=5)         pack this down

        self.save_button = tk.Button(self.controls_frame, text="Save", relief="groove", command=self.save_canvas)
        self.load_button = tk.Button(self.controls_frame, text="Load", relief="groove", command=self.load_canvas)
        self.dark_mode_button = tk.Button(self.controls_frame, text="Dark Mode", relief="groove", command=self.toggle_dark_mode)
        self.eraser_button = tk.Button(self.controls_frame, text="Eraser", relief="groove", command=self.toggle_eraser)
        self.notes_button = tk.Button(self.controls_frame, text="Notes", relief="groove", command=self.toggle_notes_section)
        self.freehand_button = tk.Button(self.controls_frame, text="Freehand", relief="groove", command=self.select_freehand)
        self.line_button = tk.Button(self.controls_frame, text="Line", relief="groove", command=lambda: self.select_shape("line"))
        self.rectangle_button = tk.Button(self.controls_frame, text="Rectangle", relief="groove", command=lambda: self.select_shape("rectangle"))
        self.Oval_button = tk.Button(self.controls_frame, text="Oval", relief="groove", command=lambda: self.select_shape("Oval"))
        self.text_button = tk.Button(self.controls_frame, text="Text", relief="groove", command=lambda: self.select_shape("text"))

        self.color_button.pack(side="left", padx=5, pady=5)
        self.clear_button.pack(side="left", padx=5, pady=5)
        self.save_button.pack(side="left", padx=5, pady=5)
        self.save_type_menu.pack(side="left", padx=5, pady=5)
        self.load_button.pack(side="left", padx=5, pady=5)
        self.dark_mode_button.pack(side="left", padx=5, pady=5)
        self.eraser_button.pack(side="left", padx=5, pady=5)
        self.notes_button.pack(side="left", padx=5, pady=5)
        self.freehand_button.pack(side="left", padx=5, pady=5)
        self.line_button.pack(side="left", padx=5, pady=5)
        self.rectangle_button.pack(side="left", padx=5, pady=5)
        self.Oval_button.pack(side="left", padx=5, pady=5)
        self.text_button.pack(side="left", padx=5, pady=5)
        self.home_button = tk.Button(self.controls_frame, text="Home", relief="groove", command=self.reset_view)
        self.home_button.pack(side="left", padx=5, pady=5)
        self.undo_button = tk.Button(self.controls_frame, text="Undo", relief="groove", command=self.undo)
        self.undo_button.pack(side="left", padx=5, pady=5)
        self.redo_button = tk.Button(self.controls_frame, text="Redo", relief="groove", command=self.redo)
        self.redo_button.pack(side="left", padx=5, pady=5)

        self.line_width_label = tk.Label(self.controls_frame, text="Width:")
        self.line_width_label.pack(side="left", padx=5, pady=5)

        self.line_width_slider = tk.Scale(self.controls_frame, from_=1, to=100, orient="horizontal", command=self.change_line_width)
        self.line_width_slider.set(self.line_width)
        self.line_width_slider.pack(side="left", padx=5, pady=5, fill="x")

        # Add font size selection widget
        self.font_size_label = tk.Label(self.controls_frame, text="Font Size:")
        self.font_size_label.pack(side="left", padx=5, pady=5)

        self.font_size_var = tk.IntVar(value=12)
        self.font_size_menu = tk.OptionMenu(self.controls_frame, self.font_size_var, *range(8, 73, 2))
        self.font_size_menu.pack(side="left", padx=5, pady=5)

        # Add font family selection widget using tkinter.font.Font
        font_families = families()
        self.font_family_label = tk.Label(self.controls_frame, text="Font Family:")
        self.font_family_label.pack(side="left", padx=5, pady=5)

        self.font_family_var = tk.StringVar(value="Arial")  # Default font family
        self.font_family_menu = tk.OptionMenu(self.controls_frame, self.font_family_var, *font_families, command=self.change_font_family_selection)
        self.font_family_menu.pack(side="left", padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg="white", scrollregion=(0, 0, 10000, 10000))
        self.scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.text_widget = tk.Text(self.root, height=6, width=120)
        self.text_widget.pack_forget()
        
        self.update_theme()

    def update_theme(self):
        if self.is_dark_mode:
            self.root.config(bg="black")
            self.canvas.config(bg="gray10")
            self.controls_frame.config(bg="gray20")
            self.line_width_label.config(bg="gray20", fg="white")
            self.line_width_slider.config(bg="gray20", fg="white", troughcolor="gray30")
            self.text_widget.config(bg="gray30", fg="white")
            self.update_button_colors("gray30", "white")
            self.dark_mode_button.config(text="Light Mode")
            self.font_size_label.config(bg="gray30", fg="white")
            self.font_size_menu.config(bg="gray30", fg="white")
            self.font_family_label.config(bg="gray30", fg="white")
            self.font_family_menu.config(bg="gray30", fg="white")
            self.home_button.config(bg="gray30", fg="white")
            self.undo_button.config(bg="gray30", fg="white")
            self.redo_button.config(bg="gray30", fg="white")
            self.save_type_menu.config(bg="gray30", fg="white")
        else:
            self.root.config(bg="white")
            self.canvas.config(bg="white")
            self.controls_frame.config(bg="white")
            self.line_width_label.config(bg="white", fg="black")
            self.line_width_slider.config(bg="white", fg="black", troughcolor="lightgray")
            self.text_widget.config(bg="white", fg="black")
            self.update_button_colors("white", "black")
            self.dark_mode_button.config(text="Dark Mode")
            self.font_size_label.config(bg="white", fg="black")
            self.font_size_menu.config(bg="white", fg="black")
            self.font_family_label.config(bg="white", fg="black")
            self.font_family_menu.config(bg="white", fg="black")
            self.home_button.config(bg="white", fg="black")
            self.undo_button.config(bg="white", fg="black")
            self.redo_button.config(bg="white", fg="black")
            self.save_type_menu.config(bg="white", fg="black")
        #self.undo_button.config(bg="gray30" if self.is_dark_mode else "white", fg="white" if self.is_dark_mode else "black")            redundant
        #self.redo_button.config(bg="gray30" if self.is_dark_mode else "white", fg="white" if self.is_dark_mode else "black")            redundant
		



        self.update_eraser_lines_color()

    def update_button_colors(self, bg_color, fg_color):
        button_list = [
            self.color_button, self.clear_button, self.save_button,
            self.load_button, self.dark_mode_button, self.eraser_button, self.notes_button,
            self.freehand_button, self.line_button, self.rectangle_button, self.Oval_button, self.text_button
        ]

        for button in button_list:
            button.config(bg=bg_color, fg=fg_color)

    def update_eraser_lines_color(self):
        for line in self.eraser_lines:
            self.canvas.itemconfig(line, fill=self.canvas["bg"])
#testing workflow build
