import cv2
import numpy
import numpy as np
from joblib import load  # Import joblib for loading the model

# Load the trained SVM classifier
classifier = load('checker_classifier.joblib')

# Define the class names based on your label mapping
class_names = [
    'blackEmpty',
    'whiteEmpty',
    'blackPawn',
    'blackBishop',
    'blackKnight',
    'blackRook',
    'blackQueen',
    'blackKing',
    'whitePawn',
    'whiteBishop',
    'whiteKnight',
    'whiteRook',
    'whiteQueen',
    'whiteKing'
]


# Function to preprocess the image and make a prediction
def predict_image(image_path):
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image at {image_path}. Please check the path.")
        return None
    
    # Resize and normalize the image
    image_resized = cv2.resize(image, (64, 64)).astype('float32') / 255.0
    image_flat = image_resized.flatten().reshape(1, -1)  # Flatten the image

    # Make the prediction
    predictions = classifier.predict_proba(image_flat)[0]
    idx = numpy.argmax(predictions, axis=0)
    
    return predictions, idx, predictions[idx]  # Return the predicted class index

# Main function to run the program
def main():
    for i in [
    #'blackEmpty',
    #'whiteEmpty',
    'blackPawn',
    'blackBishop',
    'blackKnight',
    'blackRook',
    'blackQueen',
    'blackKing',
    'whitePawn',
    'whiteBishop',
    'whiteKnight',
    'whiteRook',
    'whiteQueen',
    'whiteKing'
]:
        # Input image path from the user
        image_path = f"testing/{i}.png"
        
        # Get the predicted class
        predicted_label_index, confidence = predict_image(image_path)
        
        if predicted_label_index is not None:
            # Print the corresponding class name
            if class_names[predicted_label_index] != i:
                print("\033[0;31m", end="")
            print(f"The predicted label is: {class_names[predicted_label_index]} for {i} with {confidence*100}% confidence\033[0m")

# Run the main function
if __name__ == "__main__":
    main()
