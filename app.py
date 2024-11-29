import tkinter as tk
from PIL import Image, ImageDraw

class WhiteboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")
        
        # Canvas size
        self.width = 800
        self.height = 600
        
        # Create Canvas
        self.canvas = tk.Canvas(root, bg="white", width=self.width, height=self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Image to store the drawing
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)
        
        # Create clear button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()
        
        # Initial pen settings
        self.pen_color = "black"
        self.pen_size = 3
    
    def paint(self, event):
        x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
        x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
        
        # Draw on the canvas
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color)
        
        # Draw on the image
        self.draw.ellipse([x1, y1, x2, y2], fill=self.pen_color, outline=self.pen_color)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)
    
    def save_image(self, event):
        # Save the current image as a file
        self.image.save("whiteboard_output.png")
        self.clear_canvas()
        print("Image saved as whiteboard_output.png")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(root)
    root.mainloop()
