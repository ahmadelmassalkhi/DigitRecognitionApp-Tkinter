from tkinter import Tk, Canvas, Button, Frame, BOTH, filedialog, CENTER, Label
from PIL import Image, ImageDraw
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
        self.canvas = Canvas(self.root, width=side_length, height=side_length, bg="black")
        self.canvas.pack(side="left", fill=BOTH, expand=False)

        # Prepare for drawing
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.predict)

        # Set canvas image background to black
        self.image = Image.new("RGB", (side_length, side_length), "black")
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

        # Initialize correction buttons as None
        self.correct_button = None
        self.wrong_button = None
        self.digit_buttons = []

    def draw(self, event):
        x, y = event.x, event.y
        r = 15
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="white")
        self.draw_obj.ellipse([x - r, y - r, x + r, y + r], fill="white", outline="white")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.side_length, self.side_length), "black")
        self.draw_obj = ImageDraw.Draw(self.image)
        self.remove_correction_buttons()

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.image.save(file_path)

    def update_prediction(self, x, conf=1):
        self.prediction_label.config(text=f"Prediction: {x} with confidence: {conf * 100:.2f}%")

    def show_correction_buttons(self):
        # Create ✔ and ✘ buttons
        self.correct_button = Button(self.tab, text="✔", font=("Arial", 18), fg="green", command=self.handle_correct)
        self.correct_button.place(relx=0.3, rely=0.4, anchor=CENTER)

        self.wrong_button = Button(self.tab, text="✘", font=("Arial", 18), fg="red", command=self.handle_wrong)
        self.wrong_button.place(relx=0.7, rely=0.4, anchor=CENTER)

    def handle_correct(self):
        self.clear_canvas()

    def handle_wrong(self):
        self.remove_correction_buttons()
        self.show_digit_buttons()

    def show_digit_buttons(self):
        # Create buttons for digits 0-9 in a single column with more margin between them
        for i in range(10):
            btn = Button(self.tab, text=str(i), font=("Arial", 12, "bold"), command=lambda num=i: self.handle_digit_click(num))
            btn.place(relx=0.5, rely=0.3 + i * 0.07, anchor=CENTER)  # Increased vertical spacing to 0.07
            self.digit_buttons.append(btn)

    def handle_digit_click(self, num):
        print(f"User selected correction: {num}")
        self.clear_canvas()

    def remove_correction_buttons(self):
        if self.correct_button:
            self.correct_button.destroy()
            self.correct_button = None
        if self.wrong_button:
            self.wrong_button.destroy()
            self.wrong_button = None
        for btn in self.digit_buttons:
            btn.destroy()
        self.digit_buttons.clear()

    def run(self):
        self.root.mainloop()

    def predict(self, event):
        self.show_correction_buttons()
        pass
        # matrices = self.brain.matricize_images([self.image])
        # predictions = self.brain.predict(matrices)
        # self.update_prediction(predictions[0].argmax(), predictions[0].max())


# Initialize and run the app
app = WhiteboardApp(400)
app.run()

