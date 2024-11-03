import os
import shutil
from PIL import Image
import glob
import uuid
from keyboard import is_pressed
import classify2
from tensorflow.keras.preprocessing import image

# Set up key mappings
color_keys = {'d': 'black', 'l': 'white', 'y': 'accept'}
piece_keys = {
    'k': 'King', 'q': 'Queen', 'r': 'Rook',
    'b': 'Bishop', 'n': 'Knight', 'p': 'Pawn', 'e': 'Empty'
}

def create_output_dirs(output_dir):
    """Create output subdirectories for each piece type and color combination."""
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
    """Wait until a valid key is pressed and return the key."""
    print(prompt)
    while True:
        for key in valid_keys:
            if is_pressed(key):
                print(f"Detected key: {key}")
                return key

categories = {
    'b': 'blackBishop',
    'k': 'blackKing',
    'n': 'blackKnight',
    'p': 'blackPawn',
    'q': 'blackQueen',
    'r': 'blackRook',
    'B': 'whiteBishop',
    'K': 'whiteKing',
    'N': 'whiteKnight',
    'P': 'whitePawn',
    'Q': 'whiteQueen',
    'R': 'whiteRook',
}

def classify_image(image_path, output_dir):
    """Classify image based on key input and save it to the appropriate directory."""
    print(f"\nClassifying image: {image_path}")
    # Display image
    img = Image.open(image_path)
    img.show()

    img_arr = image.img_to_array(img)
    classification = classify2.classify_image(img_arr)

    print(f"Classified as {classification}");

    # Wait for color input
    color_key = wait_for_key("Press 'd' for dark or 'l' for light or 'y' for accept:", color_keys.keys())

    if color_key == 'y':
        category = categories[classification]
    else:
        color = color_keys[color_key]

        # Wait for piece type input
        piece_key = wait_for_key(
            "Press 'k' for king, 'q' for queen, 'r' for rook, 'b' for bishop, 'n' for knight, 'p' for pawn, 'e' for empty:",
            piece_keys.keys()
        )
        piece = piece_keys[piece_key]

        # Determine output category
        if piece == "Empty":
            category = "Empty"
        else:
            category = f"{color}{piece}"
    
    # Generate a unique filename using UUID
    unique_filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(output_dir, category, unique_filename)
    
    # Save to the appropriate directory with the UUID-based filename
    shutil.copy(image_path, output_path)
    print(f"Saved {image_path} as {output_path}")

def main(input_dir, output_dir):
    # Create necessary output directories
    create_output_dirs(output_dir)

    # Get all PNG images in the input directory
    images = glob.glob(os.path.join(input_dir, "*.png"))

    # Process each image
    for index, image_path in enumerate(images):
        print(f"\nProcessing {image_path} ({index+1}/{len(images)})")
        classify_image(image_path, output_dir)

if __name__ == "__main__":
    input_dir = "Raw Data 1"  # Set the path to your input directory here
    output_dir = "Training Data"  # Set the path to your output directory here

    main(input_dir, output_dir)
