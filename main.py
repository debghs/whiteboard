import tkinter as tk
from whiteboard_gui import WhiteboardGUI
from whiteboard_logic import WhiteboardLogic

if __name__ == "__main__":
    root = tk.Tk()
    logic = WhiteboardLogic()
    gui = WhiteboardGUI(root, logic)
    root.mainloop()
