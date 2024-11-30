from tkinter import Tk, Canvas, Button, Frame, BOTH, filedialog, CENTER, Label
from PIL import Image, ImageDraw
import numpy as np
import time


class WhiteboardApp:
    def __init__(self, side_length):
        self.side_length = side_length

        # Create the main window
        self.root = Tk()
        self.root.title("Whiteboard App")
        self.root.resizable(False, False)  # Make the window unresizable

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - (self.side_length + 100)) // 2
        y = (screen_height - self.side_length) // 2
        self.root.geometry(f"{self.side_length + 100}x{self.side_length + 50}+{x}+{y}")

        # Add a label for the prediction
        self.prediction_label = Label(self.root, text="Prediction: None", font=("Arial", 12, "bold"))
        self.prediction_label.pack(side="top")

        # Create a canvas
        self.canvas = Canvas(self.root, width=side_length, height=side_length, bg="#1F1F1F")  # Slight gray background
        self.canvas.pack(side="left", fill=BOTH, expand=False)
        self.image = Image.new("RGB", (side_length, side_length), (31, 31, 31))  # Slight gray background

        # Prepare for drawing
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.predict)
        self.draw_obj = ImageDraw.Draw(self.image)

        # Create a tab for buttons
        self.tab = Frame(self.root, width=100, height=side_length, bg="white")
        self.tab.pack(side="right", fill=BOTH, expand=False)

        # Add clear button
        self.clear_button = Button(self.tab, text="Clear", font=("Arial", 12, "bold"), command=self.clear_canvas)
        self.clear_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        # Add save button
        self.save_button = Button(self.tab, text="Save", font=("Arial", 12, "bold"), command=self.save_canvas)
        self.save_button.place(relx=0.5, rely=0.2, anchor=CENTER)


    def draw(self, event):
        x, y = event.x, event.y
        r = 9  # Update brush size to 8
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="white")  # Set pen color to white
        self.draw_obj.ellipse([x - r, y - r, x + r, y + r], fill="white", outline="white")  # Set pen color to white

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.side_length, self.side_length), (31, 31, 31))  # Slight gray background
        self.draw_obj = ImageDraw.Draw(self.image)

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.image.save(file_path)

    def update_prediction(self, x, conf=1):
        self.prediction_label.config(text=f"Prediction: {x} with confidence: {conf*100:.2f}%")

    def run(self):
        self.root.mainloop()

    def predict(self, event):
        self.image.save(f'{time.time()}.png')
        pass
        
# Initialize and run the app
app = WhiteboardApp(400)  # Set side length of the drawing area
app.run()
