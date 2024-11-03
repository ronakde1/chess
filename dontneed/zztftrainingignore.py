import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Set the paths to your training and testing data
train_data_dir = "Training Data"
test_data_dir = "testing"

# Set the image size and batch size
image_size = (150, 150)  # Change this as needed
batch_size = 32

# Prepare the training data using an ImageDataGenerator
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2  # 20% of data will be used for validation
)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Prepare the testing data
test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False  # Keep the order for consistent evaluation
)

# Define the CNN model
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_generator.num_classes, activation='softmax')  # Output layer
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
epochs = 10  # Adjust as needed
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=epochs
)

# Save the trained model
model.save("chess_piece_classifier.h5")

# Evaluate the model on the testing data
loss, accuracy = model.evaluate(test_generator)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

# Predict on the testing data
predictions = model.predict(test_generator)
predicted_classes = np.argmax(predictions, axis=1)

# Map the class indices to class labels
class_labels = {v: k for k, v in test_generator.class_indices.items()}
predicted_labels = [class_labels[i] for i in predicted_classes]

# Print some predictions
print("Predicted labels for the first few images:")
print(predicted_labels[:10])
