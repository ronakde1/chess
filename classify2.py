import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import sys

IMG_HEIGHT = 37
IMG_WIDTH = 37
MODEL_PATH = 'image_classifier_model.keras'
CLASS_NAMES = [
    "b", "e", "k", "n", "p", "q", "r", "B", "E", "K", "N", "P", "Q", "R",
]

model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully.")

def preprocess_image_array(img_array):
    img_array = tf.image.resize(img_array, [IMG_HEIGHT, IMG_WIDTH])
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def classify_image(img):
    img = preprocess_image_array(img)
    predictions = model.predict(img, verbose=0)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_class_index]
    confidence = predictions[0][predicted_class_index]
    #print(f"Predicted Class: {predicted_class} with {confidence * 100:.2f}% confidence.")

    return predicted_class
