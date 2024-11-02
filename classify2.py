import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import sys

# Parameters
IMG_HEIGHT = 37  # Image height used during training
IMG_WIDTH = 37   # Image width used during training
MODEL_PATH = 'image_classifier_model.keras'  # Path to the saved model
CLASS_NAMES = [
    "b", None, "k", "n", "p", "q", "r", "B", None, "K", "N", "P", "Q", "R",
]

# Load the trained model
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully.")

# Function to load and preprocess image
def preprocess_image_array(img_array):
    # Resize the image array to the model's input size
    img_array = tf.image.resize(img_array, [IMG_HEIGHT, IMG_WIDTH])
    img_array = img_array / 255.0  # Normalize the image (same as during training)
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions for batch compatibility
    return img_array

# Function to classify the image
def classify_image(img):
    img = preprocess_image_array(img)
    predictions = model.predict(img)  # Get model predictions
    predicted_class_index = np.argmax(predictions[0])  # Get index of highest probability
    predicted_class = CLASS_NAMES[predicted_class_index]  # Map to class name
    confidence = predictions[0][predicted_class_index]  # Get confidence score
    print(f"Predicted Class: {predicted_class} with {confidence * 100:.2f}% confidence.")

    return predicted_class
