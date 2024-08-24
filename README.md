# whiteboard
whiteboard is a simple drawing application built using Tkinter in Python. It allows users to draw on a canvas, change pen colors, adjust line width, toggle dark mode, use an eraser, save and load drawings, and take notes.

## Features
- Drawing on canvas with various colors and line widths
- Drawing basic shapes by dragging them to the required size
- Changing pen colors using a color picker
- Clearing the canvas
- Toggling dark mode for better visibility
- Using an eraser to remove drawn lines
- Saving and loading drawings in pickle format as well as image format.
- Inserting text inside dynamically shaped custom textboxes as embedded type or editable type
- Taking notes alongside drawings
- Zoom In and Out while drawing
- Infinitely scrollable canvas
- Undo and Redo

## File Structure
The project is structured into three main files:
1. `main.py`: Entry point of the application, initializes the GUI and Logic components.
2. `whiteboard_gui.py`: Handles the graphical user interface using Tkinter.
3. `whiteboard_logic.py`: Contains the core logic and functionality of the Whiteboard App.

## Installation
1. Clone the repository:

   ```git clone https://github.com/your-username/whiteboard-app.git```

2. Navigate to the project directory:

   ```cd whiteboard-app```

3. Install the required dependencies:

   ```pip install -r requirements.txt```

4. Run the application:

   ```python main.py```

## Usage
- Draw on the canvas by clicking and dragging the mouse/touchpad.
- Change pen color by clicking the "Change Color" button and selecting a color from the color picker.
- Adjust line width using the slider.
- Draw straight lines using the "Line" button.
- Draw Basic geometric shapes using the specific buttons.
- Toggle to "Dark mode" / "Light Mode" for better visibility in different lighting conditions.
- Use the "Eraser" to remove drawn lines.
- Adjust the eraser width using the slider.
- Save and load drawings using the "Save" and "Load" buttons.
- Use "Text" button to draw a textbox, enter the text in the pop-up and then press ```esc``` button to save it inside the canvas.
- Use "Text" button to draw a textbox, enter the text in the pop-up and then click the cursor somewhere else and the text would be saved as into an editable transparent box.
- Double click on the editable text to select and then drag to re-position it or use arrow keys to position the cursor and edit the text or press ```delete``` to delete the text. 
- The text would have the color the ink had previously.
- To choose the font size of the text input, adjust the "Font Size:" before inserting the text.
- Take notes alongside drawings by clicking the "Notes" button.
- Place the cursor on where you would like to zoom and press ```Ctrl-Shift-+``` to Zoom In and ```Ctrl-Shift-*``` to Zoom Out.
- Use the sliders to navigate across the canvas.
- Press the "Home" button to return to the original camvas coordinates(in case you get lost).
- Press the "Undo" and "Redo" buttons to undo and redo.
- Choose the mode of file to be saved from the dropdown and press the ```Save``` button to save.

## BUGS
There are some bugs in this version:
- The saved pickle files lose all the data when reopened using the app.(FIXED)
- The text insertion probably needs some tuning.(FIXED)
- The home button is glitching.(FIXED)
- The zoom is interfering with the textbox pop-up dimensions, i believe.(FIXED)
- The already embeded texts are not enlarging/contracting while zooming in/out.
- Both Undo and Redo buttons are requiring two clicks everytime to work.(FIXED, kinda)
- The text insertion feature is having a minor glitch with Undo, cuz the textbox outline is getting counted as a snapshot.
- The editing of the editable text is functional, but a little weird.
- The texts are not redo-ing because of the window element.(FIXED)
- The editable textbox needs to be transparent. It's currently mirroring the bg.
- The moving around of the editable text is glitching when done in a zoomed-in canvas.
- The undo and redo are still buggy in zoom-in/zoom-out canvases.
- The text size is changing sometimes after doing undo-redo.
- The text-size choice isn't working anymore.
- The save as image functionality captures external stuff (backgorund) when the app isn't in fullscreen mode.
- The save as image functionality doesn't properly capture the whole canvas either.
