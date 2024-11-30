import time
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw
from lib.neural_network import NeuralNetwork
# from tensorflow.keras.datasets import mnist # type: ignore
import numpy as np


class WhiteboardApp:
    def __init__(self, root, side=350):
        self.root = root
        self.root.title("Whiteboard")
        self.side = side
        self._center_window()

        # Canvas and Image setup
        self.canvas = tk.Canvas(root, bg="black", width=side, height=side)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.image = Image.new("L", (side, side), "black")
        self.draw = ImageDraw.Draw(self.image)

        # Bottom Frame for buttons
        self.bottom_frame = tk.Frame(root, bg="black", height=50)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Pen settings
        self.pen_color = "white"
        self.pen_size = 8

        # Buttons
        self._create_buttons()

        # Mouse event bindings
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.predict)

        # Neural network
        self.nn = NeuralNetwork(model_path='model.pkl')

        # load training dataset
        self.all_images = []
        self.all_labels = []
        self._load_dataset()

    ##############################################################

    def get_all_files(self, dir_path: str = './', extension: str = 'png') -> list:
        """Returns a list of all files with the specified extension in the given directory."""
        return list(Path(dir_path).glob(f'*.{extension}'))

    def _load_dataset(self):
        for i in range(10):
            images = [Image.open(file) for file in self.get_all_files(f'./Images/{i}')]
            self.all_images.extend(images)
            self.all_labels.extend([i] * len(images))
        self.all_images = self.nn.prepare_images(self.all_images)

    def _dataset_add_image(self, correct_label:int):
        self.all_images = np.append(self.all_images, [self.nn.prepare_image(self.image)], axis=0)
        self.all_labels = np.append(self.all_labels, [correct_label])
        self.image.save(f'./Images/{correct_label}/{time.time()}.png')

    def _center_window(self):
        x_offset = (self.root.winfo_screenwidth() - self.side) // 2
        y_offset = (self.root.winfo_screenheight() - self.side - 50) // 2
        self.root.geometry(f"{self.side}x{self.side + 50}+{x_offset}+{y_offset}")
        self.root.resizable(False, False)

    def _create_buttons(self):
        tk.Button(self.bottom_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=10, pady=10)

    def _create_feedback_button(self, text, color, accurate):
        return tk.Button(
            self.bottom_frame, text=text, bg=color, fg="white",
            command=lambda: self.process_feedback(accurate)
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_digit_buttons(self):
        self.digit_buttons = []
        for i in range(10):
            btn = tk.Button(
                self.bottom_frame, text=str(i),
                command=lambda num=i: self.correct_digit_handler(num)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.digit_buttons.append(btn)

    def _destroy_feedback_buttons(self):
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        self._create_buttons()

    ##############################################################

    def paint(self, event):
        x1, y1 = event.x - self.pen_size, event.y - self.pen_size
        x2, y2 = event.x + self.pen_size, event.y + self.pen_size
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color)
        self.draw.ellipse([x1, y1, x2, y2], fill=self.pen_color)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (self.side, self.side), "black")
        self.draw = ImageDraw.Draw(self.image)
        self._destroy_feedback_buttons()

    def predict(self, event):
        # self.image.save(f'./{time.time()}.png')
        self.nn.forward([self.image])
        print(f'Prediction: {self.nn.output[0]} with {self.nn.output_confidence[0]} confidence')
        self._destroy_feedback_buttons()
        self.correct_button = self._create_feedback_button("✔", "green", True)
        self.incorrect_button = self._create_feedback_button("✘", "red", False)

    def process_feedback(self, accurate):
        self._destroy_feedback_buttons()
        if accurate:
            print('Learning...')
            self._dataset_add_image(self.nn.output[0])
            self.nn.learn(self.all_images, self.all_labels)
            print('Finished learning!')
            self.clear_canvas()
        else:
            self._create_digit_buttons()

    def correct_digit_handler(self, number: int):
        print('Learning...')
        self._dataset_add_image(number)
        self.nn.learn(self.all_images, self.all_labels)
        print('Finished learning!')
        self.clear_canvas()

    


# Run the app
if __name__ == "__main__":
    app = WhiteboardApp(tk.Tk())
    app.root.mainloop()
    app.nn.save()
