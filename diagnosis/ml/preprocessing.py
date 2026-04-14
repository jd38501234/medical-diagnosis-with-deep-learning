"""
Image preprocessing pipeline for medical image diagnosis.
"""
import numpy as np
from PIL import Image
import io


def preprocess_image(image_file, target_size=(224, 224)):
    """
    Preprocess an uploaded image file for model inference.
    
    Args:
        image_file: Django UploadedFile or file-like object
        target_size: Tuple of (width, height) for resizing
    
    Returns:
        numpy array of shape (1, height, width, 3) normalized to [0, 1]
    """
    # Read image
    if hasattr(image_file, 'read'):
        image_data = image_file.read()
        image_file.seek(0)  # Reset file pointer
        img = Image.open(io.BytesIO(image_data))
    else:
        img = Image.open(image_file)
    
    # Convert to RGB (handles grayscale and RGBA)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to target dimensions
    img = img.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(img, dtype=np.float32)
    
    # Normalize pixel values to [0, 1]
    img_array = img_array / 255.0
    
    # Add batch dimension: (H, W, C) -> (1, H, W, C)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array
