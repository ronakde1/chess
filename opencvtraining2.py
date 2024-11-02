import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump, load  # Import joblib for saving/loading models

# Step 1: Load images and labels
def load_images_and_labels(data_directory):
    images = []
    labels = []
    label_map = {
    'blackEmpty': 0,
    'whiteEmpty': 1,
    'blackPawn': 2,
    'blackBishop': 3,
    'blackKnight': 4,
    'blackRook': 5,
    'blackQueen': 6,
    'blackKing': 7,
    'whitePawn': 8,
    'whiteBishop': 9,
    'whiteKnight': 10,
    'whiteRook': 11,
    'whiteQueen': 12,
    'whiteKing': 13
    }

    for label_name, label in label_map.items():
        folder_path = os.path.join(data_directory, label_name)
        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            image = cv2.imread(img_path)
            if image is not None:
                images.append(cv2.resize(image, (64, 64)))  # Resize to 64x64
                labels.append(label)

    return np.array(images), np.array(labels)

# Step 2: Preprocess and split the data
data_directory = 'Training Data'
images, labels = load_images_and_labels(data_directory)
images = images.astype('float32') / 255.0  # Normalize pixel values
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Step 3: Feature extraction (using flattening for SVM)
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Step 4: Train the SVM classifier
classifier = SVC(kernel='linear', probability=True)
classifier.fit(X_train_flat, y_train)

# Step 5: Evaluate the model
y_pred = classifier.predict(X_test_flat)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Step 6: Save the model
dump(classifier, 'checker_classifier.joblib')  # Save the model to a file

# Step 7: Load the model (for future use)
# classifier = load('checker_classifier.joblib')  # Uncomment this line to load the model later

# Step 8: Make predictions on new images
def predict_image(image_path):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (64, 64)).astype('float32') / 255.0
    image_flat = image_resized.flatten().reshape(1, -1)
    prediction = classifier.predict(image_flat)
    return prediction

# Example usage
#predicted_label = predict_image('blue.png')
#hello = predicted_label[0]
#print([
#    'Black Empty',
#    'White Empty',
#    'Black Pawn',
#    'Black Bishop',
#    'Black Knight',
#    'Black Rook',
#    'Black Queen',
#    'Black King',
#    'White Pawn',
#    'White Bishop',
#    'White Knight',
#    'White Rook',
#    'White Queen',
#    'White King'
#    ] 
#    [hello])
