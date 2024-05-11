import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, PhotoImage

class WhiteboardGUI:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic
        self.root.title("whiteboard")
        self.root.geometry("1100x600+135+70")
        self.root.resizable(True, True)
        icon_img = PhotoImage(file="assets\icon.png")
        self.root.iconphoto(False, icon_img) 

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side="left", fill="y")

        self.color_button = tk.Button(self.controls_frame, text="Change Color", command=self.logic.change_pen_color)
        self.clear_button = tk.Button(self.controls_frame, text="Clear Canvas", command=self.logic.clear_canvas)
        self.save_button = tk.Button(self.controls_frame, text="Save", command=self.logic.save_canvas)
        self.dark_mode_button = tk.Button(self.controls_frame, text="Dark Mode", command=self.logic.toggle_dark_mode)
        self.eraser_button = tk.Button(self.controls_frame, text="Eraser", command=self.logic.toggle_eraser)
        self.notes_button = tk.Button(self.controls_frame, text="Notes", command=self.logic.toggle_notes_section)

        self.color_button.pack(side="left", padx=5, pady=5)
        self.clear_button.pack(side="left", padx=5, pady=5)
        self.save_button.pack(side="left", padx=5, pady=5)
        self.dark_mode_button.pack(side="left", padx=5, pady=5)
        self.eraser_button.pack(side="left", padx=5, pady=5)
        self.notes_button.pack(side="left", padx=5, pady=5)

        self.line_width_label = tk.Label(self.controls_frame, text="Width:")
        self.line_width_label.pack(side="left", padx=5, pady=5)

        self.line_width_slider = tk.Scale(self.controls_frame, from_=1, to=100, orient="horizontal", command=self.logic.change_line_width)
        self.line_width_slider.set(self.logic.line_width)
        self.line_width_slider.pack(side="left", padx=5, pady=5)

        self.canvas.bind("<Button-1>", self.logic.start_drawing)
        self.canvas.bind("<B1-Motion>", self.logic.draw)
        self.canvas.bind("<ButtonRelease-1>", self.logic.stop_drawing)

        self.text_widget_label = tk.Label(self.controls_frame, text="Notes:")
        self.text_widget_label.pack(side="top", padx=5, pady=5)
        self.text_widget = tk.Text(self.controls_frame, height=6, width=120)
        self.text_widget.pack_forget()

        self.logic.set_widgets(self.root, self.canvas, self.controls_frame, self.color_button, self.clear_button, self.save_button, self.dark_mode_button, self.eraser_button, self.line_width_label, self.line_width_slider, self.text_widget, self.text_widget_label, self.notes_button)
        self.logic.update_theme()
