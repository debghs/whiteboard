import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, PhotoImage
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

    def create_widgets(self):
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side="top", fill="x")

        self.color_button = tk.Button(self.controls_frame, text="Change Color", relief="groove", command=self.change_pen_color)
        self.clear_button = tk.Button(self.controls_frame, text="Clear Canvas", relief="groove", command=self.clear_canvas)
        self.save_button = tk.Button(self.controls_frame, text="Save", relief="groove", command=self.save_canvas)
        self.load_button = tk.Button(self.controls_frame, text="Load", relief="groove", command=self.load_canvas)
        self.dark_mode_button = tk.Button(self.controls_frame, text="Dark Mode", relief="groove", command=self.toggle_dark_mode)
        self.eraser_button = tk.Button(self.controls_frame, text="Eraser", relief="groove", command=self.toggle_eraser)
        self.notes_button = tk.Button(self.controls_frame, text="Notes", relief="groove", command=self.toggle_notes_section)
        self.line_button = tk.Button(self.controls_frame, text="Line", relief="groove", command=lambda: self.select_shape("line"))
        self.rectangle_button = tk.Button(self.controls_frame, text="Rectangle", relief="groove", command=lambda: self.select_shape("rectangle"))
        self.circle_button = tk.Button(self.controls_frame, text="Circle", relief="groove", command=lambda: self.select_shape("circle"))

        self.color_button.pack(side="left", padx=5, pady=5)
        self.clear_button.pack(side="left", padx=5, pady=5)
        self.save_button.pack(side="left", padx=5, pady=5)
        self.load_button.pack(side="left", padx=5, pady=5)
        self.dark_mode_button.pack(side="left", padx=5, pady=5)
        self.eraser_button.pack(side="left", padx=5, pady=5)
        self.notes_button.pack(side="left", padx=5, pady=5)
        self.line_button.pack(side="left", padx=5, pady=5)
        self.rectangle_button.pack(side="left", padx=5, pady=5)
        self.circle_button.pack(side="left", padx=5, pady=5)

        self.line_width_label = tk.Label(self.controls_frame, text="Width:")
        self.line_width_label.pack(side="left", padx=5, pady=5)

        self.line_width_slider = tk.Scale(self.controls_frame, from_=1, to=100, orient="horizontal", command=self.change_line_width)
        self.line_width_slider.set(self.line_width)
        self.line_width_slider.pack(side="left", padx=5, pady=5, fill="x")

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.text_widget = tk.Text(self.root, height=6, width=120)
        self.text_widget.pack_forget()

        self.update_theme()

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color
            if self.is_eraser:
                self.toggle_eraser()

    def toggle_notes_section(self):
        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        else:
            self.text_widget.pack(side="bottom", padx=5, pady=5, fill="x")

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            self._save_canvas(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path and os.path.exists(file_path):
            self._load_canvas(file_path)

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
        else:
            self.root.config(bg="white")
            self.canvas.config(bg="white")
            self.controls_frame.config(bg="white")
            self.line_width_label.config(bg="white", fg="black")
            self.line_width_slider.config(bg="white", fg="black", troughcolor="lightgray")
            self.text_widget.config(bg="white", fg="black")
            self.update_button_colors("white", "black")
            self.dark_mode_button.config(text="Dark Mode")

        self.update_eraser_lines_color()

    def update_button_colors(self, bg_color, fg_color):
        button_list = [
            self.color_button, self.clear_button, self.save_button,
            self.load_button, self.dark_mode_button, self.eraser_button, self.notes_button,
            self.line_button, self.rectangle_button, self.circle_button
        ]

        for button in button_list:
            button.config(bg=bg_color, fg=fg_color)

    def update_eraser_lines_color(self):
        for line in self.eraser_lines:
            self.canvas.itemconfig(line, fill=self.canvas["bg"])
