import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path):
    print(f"Reading {input_path}...")
    # Read the image
    img = Image.open(input_path)
    
    # 1. Remove background
    print("Removing background...")
    img_no_bg = remove(img)
    
    # Convert to OpenCV format (numpy array)
    open_cv_image = np.array(img_no_bg) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 

    # Extract the alpha channel
    alpha_channel = open_cv_image[:, :, 3]
    
    # 2. Boost local contrast using CLAHE
    print("Enhancing contrast...")
    # Convert to grayscale for CLAHE
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGRA2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(gray)
    
    # 3. Composite onto pure white
    print("Compositing onto white background...")
    # Create white background
    white_background = np.ones_like(cl1) * 255
    
    # Create mask from alpha channel
    mask = alpha_channel > 0
    
    # Apply mask
    result = np.where(mask, cl1, white_background)
    
    # Save the output
    print(f"Saving to {output_path}...")
    cv2.imwrite(output_path, result)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = "source-prepped.png"
    prep_photo(input_file, output_file)
