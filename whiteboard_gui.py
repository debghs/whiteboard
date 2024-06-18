import tkinter as tk
from tkinter import PhotoImage
from whiteboard_logic import WhiteboardLogic

class WhiteboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")
        self.root.geometry("1050x600+150+50")
        self.root.resizable(True, True)
        icon_img = PhotoImage(file="assets\icon.png")
        self.root.iconphoto(False, icon_img)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side="top", fill="x")

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.line_width_slider = tk.Scale(self.controls_frame, from_=1, to=100, orient="horizontal")
        self.line_width_slider.set(2)

        self.text_widget = tk.Text(self.root, height=6, width=120)
        self.text_widget.pack_forget()

        self.logic = WhiteboardLogic(self.canvas, self.text_widget, self.line_width_slider)
        self.create_widgets()
        self.update_theme()

    def create_widgets(self):
        self.color_button = tk.Button(self.controls_frame, text="Change Color", relief="groove", command=self.logic.change_pen_color)
        self.clear_button = tk.Button(self.controls_frame, text="Clear Canvas", relief="groove", command=self.logic.clear_canvas)
        self.save_button = tk.Button(self.controls_frame, text="Save", relief="groove", command=self.logic.save_canvas)
        self.load_button = tk.Button(self.controls_frame, text="Load", relief="groove", command=self.logic.load_canvas)
        self.dark_mode_button = tk.Button(self.controls_frame, text="Dark Mode", relief="groove", command=self.toggle_dark_mode)
        self.eraser_button = tk.Button(self.controls_frame, text="Eraser", relief="groove", command=self.logic.toggle_eraser)
        self.notes_button = tk.Button(self.controls_frame, text="Notes", relief="groove", command=self.toggle_notes_section)

        self.color_button.pack(side="left", padx=5, pady=5)
        self.clear_button.pack(side="left", padx=5, pady=5)
        self.save_button.pack(side="left", padx=5, pady=5)
        self.load_button.pack(side="left", padx=5, pady=5)
        self.dark_mode_button.pack(side="left", padx=5, pady=5)
        self.eraser_button.pack(side="left", padx=5, pady=5)
        self.notes_button.pack(side="left", padx=5, pady=5)

        self.line_width_label = tk.Label(self.controls_frame, text="Width:")
        self.line_width_label.pack(side="left", padx=5, pady=5)

        self.line_width_slider.pack(side="left", padx=5, pady=5, fill="x")
        self.line_width_slider.config(command=self.logic.change_line_width)

        self.canvas.bind("<Button-1>", self.logic.start_drawing)
        self.canvas.bind("<B1-Motion>", self.logic.draw)
        self.canvas.bind("<ButtonRelease-1>", self.logic.stop_drawing)

    def toggle_dark_mode(self):
        self.logic.toggle_dark_mode()
        self.update_theme()

    def toggle_notes_section(self):
        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        else:
            self.text_widget.pack(side="bottom", padx=5, pady=5, fill="x")

    def update_theme(self):
        if self.logic.is_dark_mode:
            self.root.config(bg="black")
            self.controls_frame.config(bg="gray20")
            self.line_width_label.config(bg="gray20", fg="white")
            self.line_width_slider.config(bg="gray20", fg="white", troughcolor="gray30")
            self.text_widget.config(bg="gray30", fg="white")
            self.update_button_colors("gray30", "white")
            self.dark_mode_button.config(text="Light Mode")
        else:
            self.root.config(bg="white")
            self.controls_frame.config(bg="white")
            self.line_width_label.config(bg="white", fg="black")
            self.line_width_slider.config(bg="white", fg="black", troughcolor="lightgray")
            self.text_widget.config(bg="white", fg="black")
            self.update_button_colors("white", "black")
            self.dark_mode_button.config(text="Dark Mode")

        self.logic.update_canvas_colors()

    def update_button_colors(self, bg_color, fg_color):
        button_list = [
            self.color_button, self.clear_button, self.save_button,
            self.load_button, self.dark_mode_button, self.eraser_button, self.notes_button
        ]

        for button in button_list:
            button.config(bg=bg_color, fg=fg_color)
