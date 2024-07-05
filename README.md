# whiteboard
whiteboard is a simple drawing application built using Tkinter in Python. It allows users to draw on a canvas, change pen colors, adjust line width, toggle dark mode, use an eraser, save and load drawings, and take notes.

## Features
- Drawing on canvas with various colors and line widths
- Drawing basic shapes by dragging them to the required size
- Changing pen colors using a color picker
- Clearing the canvas
- Toggling dark mode for better visibility
- Using an eraser to remove drawn lines
- Saving and loading drawings in pickle format
- Taking notes alongside drawings

## File Structure
The project is structured into three main files:
1. `main.py`: Entry point of the application, initializes the GUI and logic components.
2. `whiteboard_gui.py`: Handles the graphical user interface using Tkinter.
3. `whiteboard_logic.py`: Contains the core logic and functionality of the Whiteboard App.

## Installation
1. Clone the repository:

   ```git clone https://github.com/your-username/whiteboard-app.git```

2. Navigate to the project directory:

   ```cd whiteboard-app```

3. Run the application:

   ```python main.py```

## Usage
- Draw on the canvas by clicking and dragging the mouse/touchpad.
- Change pen color by clicking the "Change Color" button and selecting a color from the color picker.
- Adjust line width using the slider.
- Toggle dark mode for better visibility in different lighting conditions.
- Use the eraser to remove drawn lines.
- Adjust the eraser width using the same slider.
- Save and load drawings using the "Save" and "Load" buttons.
- Take notes alongside drawings by clicking the "Notes" button.

## Note 
There are some bugs in this version:
- The saved pickle files lose all the data when reopened using the app.
