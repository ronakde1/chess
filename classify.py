import os
import shutil
from PIL import Image
import glob
import uuid
import classify2
from tensorflow.keras.preprocessing import image
import cv2

color_keys = {'d': 'black', 'l': 'white', 'y': 'accept'}
piece_keys = {
    'k': 'King', 'q': 'Queen', 'r': 'Rook',
    'b': 'Bishop', 'n': 'Knight', 'p': 'Pawn', 'e': 'Empty'
}

def create_output_dirs(output_dir):
    categories = [
        "blackKing", "whiteKing",
        "blackQueen", "whiteQueen",
        "blackRook", "whiteRook",
        "blackBishop", "whiteBishop",
        "blackKnight", "whiteKnight",
        "blackPawn", "whitePawn"
    ]
    for category in categories:
        os.makedirs(os.path.join(output_dir, category), exist_ok=True)

def wait_for_key(prompt, valid_keys):
    print(prompt)
    while True:
        key = chr(cv2.waitKey())
        print(f"Detected key: {key}")
        if key in valid_keys:
            return key

categories = {
    'b': 'blackBishop',
    'k': 'blackKing',
    'n': 'blackKnight',
    'p': 'blackPawn',
    'q': 'blackQueen',
    'r': 'blackRook',
    'e': 'blackEmpty',
    'B': 'whiteBishop',
    'K': 'whiteKing',
    'N': 'whiteKnight',
    'P': 'whitePawn',
    'Q': 'whiteQueen',
    'R': 'whiteRook',
    'E': 'whiteEmpty',
}

correct_auto = 0

def classify_image(image_path, output_dir):
    global correct_auto

    """Classify image based on key input and save it to the appropriate directory."""
    print(f"\nClassifying image: {image_path}")
    # Display image
    img = Image.open(image_path)

    img_arr = image.img_to_array(img)
    classification = classify2.classify_image(img_arr)

    cv2.imshow(f"Classified as {categories[classification]}", img_arr / 255.0)

    print(f"Classified as {categories[classification]}")

    color_key = wait_for_key("Press 'd' for dark or 'l' for light or 'y' for accept:", color_keys.keys())

    if color_key == 'y':
        category = categories[classification]
        correct_auto += 1
    else:
        color = color_keys[color_key]

        piece_key = wait_for_key(
            "Press 'k' for king, 'q' for queen, 'r' for rook, 'b' for bishop, 'n' for knight, 'p' for pawn, 'e' for empty:",
            piece_keys.keys()
        )
        piece = piece_keys[piece_key]

        category = f"{color}{piece}"

    unique_filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(output_dir, category, unique_filename)

    shutil.copy(image_path, output_path)
    print(f"Saved {image_path} as {output_path}")
    # and finally destroy/close all open windows
    cv2.destroyAllWindows()

def main(input_dir, output_dir):
    create_output_dirs(output_dir)

    images = glob.glob(os.path.join(input_dir, "*.png"))

    for index, image_path in enumerate(images):
        print(f"\nProcessing {image_path} ({index+1}/{len(images)})")
        classify_image(image_path, output_dir)
    print(f"Model accuracy: {100*correct_auto/len(images)}%")

if __name__ == "__main__":
    input_dir = "RawData"
    output_dir = "Training Data2"

    main(input_dir, output_dir)
