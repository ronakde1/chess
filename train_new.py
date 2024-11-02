import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Set parameters
IMG_HEIGHT = 37  # Height of images
IMG_WIDTH = 37   # Width of images
BATCH_SIZE = 32   # Number of images to process in a batch
EPOCHS = 100       # Number of training epochs
LEARNING_RATE = 0.001  # Learning rate for optimizer

# Load and preprocess data
train_dir = 'Training Data'  # Path to training data
val_dir = 'testing'  # Path to validation data

# ImageDataGenerator for data augmentation
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1.0/255)

# Load images from directories
train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_data = val_datagen.flow_from_directory(
    val_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(train_data.num_classes, activation='softmax')  # Output layer based on number of classes
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=val_data
)

# Evaluate the model on validation data
val_loss, val_accuracy = model.evaluate(val_data)
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")

# Generate classification report and confusion matrix
val_data.reset()  # Resetting to start from the beginning
Y_pred = model.predict(val_data)
y_pred = np.argmax(Y_pred, axis=1)
print('Classification Report')
print(classification_report(val_data.classes, y_pred, target_names=val_data.class_indices.keys()))

# Display confusion matrix
print('Confusion Matrix')
print(confusion_matrix(val_data.classes, y_pred))

# Save the model
model.save("image_classifier_model.keras")
print("Model saved as image_classifier_model.keras")

CLASS_NAMES = list(train_data.class_indices.keys())
print(CLASS_NAMES)
