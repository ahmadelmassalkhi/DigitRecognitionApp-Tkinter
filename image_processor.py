import os
import numpy as np
from PIL import Image
from typing import List



class ImageProcessor:
    def matricize_images_to_mnist(images: list[Image.Image]):
        matricized_images = []
        for image in images:
            # Step 1: Make the image square by padding
            width, height = image.size
            if width != height:
                new_size = max(width, height)
                new_image = Image.new("RGB", (new_size, new_size), (0, 0, 0))  # Black padding
                new_image.paste(image, ((new_size - width) // 2, (new_size - height) // 2))
                image = new_image

            # Step 2: Resize to 28x28
            image = image.resize((28, 28), Image.Resampling.LANCZOS)

            # Step 3: Convert to grayscale and then to a NumPy array
            image = image.convert("L")  # Convert to grayscale
            image_matrix = np.array(image) / 255.0

            # Add to result
            matricized_images.append(image_matrix)

        # Normalize pixel values to match MNIST (0-255 range expected)
        return np.array(matricized_images)


    def get_png(first_n: int = 1, dir: str = './') -> List[str]:
        """
        Returns the first N PNG images as PIL Image objects from the specified directory.

        Args:
            first_n (int): Number of PNG images to return. Defaults to 1.
            dir (str): Directory to search for PNG images. Defaults to './'.

        Returns:
            List[Image.Image]: List of opened PNG images.
        """
        # Ensure directory exists
        if not os.path.isdir(dir):
            raise FileNotFoundError(f"Directory '{dir}' does not exist.")

        # List all files in the directory and filter for .png files
        png_files = [os.path.join(dir, f) for f in os.listdir(dir) if f.lower().endswith('.png')]

        # Sort the files (optional, depending on required order)
        png_files.sort()

        # Return the first N .png files
        return [Image.open(file) for file in png_files[:first_n]]


# processor = ImageProcessor()
# images = processor.get_png()
# matrix = processor.matricize_images_to_mnist(images)
# print(matrix.shape)  # Should print (28, 28)

