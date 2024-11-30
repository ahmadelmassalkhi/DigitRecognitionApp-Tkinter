import os
import cv2
import numpy as np

def add_noise(image):
    """Add random noise to an image."""
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)  # Mean=0, StdDev=25
    noisy_image = cv2.add(image, noise)
    return noisy_image

def process_folder(base_folder):
    """Iterate through the folder structure and create noisy clones."""
    for digit_folder in range(10):  # Digits 0 to 9
        folder_path = os.path.join(base_folder, str(digit_folder))
        if not os.path.exists(folder_path):
            continue

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Ensure it's an image file
            if filename.endswith((".png", ".jpg", ".jpeg")):
                image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    continue
                
                # Create a noisy version of the image
                noisy_image = add_noise(image)
                noisy_filename = filename.split('.')[0] + "_noisy.png"
                noisy_path = os.path.join(folder_path, noisy_filename)
                cv2.imwrite(noisy_path, noisy_image)

if __name__ == "__main__":
    base_folder = "Images"  # Replace with the path to your Images folder
    process_folder(base_folder)
