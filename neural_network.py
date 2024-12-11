import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
from tensorflow.keras.datasets import mnist # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore
from tensorflow.keras.models import load_model # type: ignore



class NeuralNetwork:
    def __init__(self, file_path:str):
        self.load(file_path)

    def load(self, file_path:str):
        try:
            self.model = load_model(file_path)
        except:
            # Build the CNN model
            self.model = models.Sequential([
                # First convolutional block
                layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.2),
                
                # Flatten and fully connected layers
                layers.Flatten(),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.5),
                layers.Dense(10, activation='softmax')
            ])

            # Compile the model
            self.model.compile(optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
    
    def save(self):
        # Save the entire model to a file
        self.model.save('model.keras')




if __name__ == "__main__":
    
    # Load and preprocess the MNIST dataset
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
    test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    brain = NeuralNetwork(file_path='model.keras')

    # Train the model
    # history = model.fit(train_images, train_labels, epochs=10, batch_size=128, validation_split=0.1)

    # # Evaluate the model on test data
    test_loss, test_acc = NeuralNetwork.evaluate(test_images, test_labels)
    print(f"Test accuracy: {test_acc:.4f}")

