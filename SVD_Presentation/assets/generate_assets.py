import numpy as np
from PIL import Image
import json
import os

def process_image(input_path, output_json, size=(10, 10)):
    # Absolute paths
    input_abs_path = "/mnt/c/Users/merli/OneDrive/THWS Informatik Studium/4.Numerik/visual_audit/RubberDuck.png"
    output_abs_path = "/mnt/c/Users/merli/OneDrive/THWS Informatik Studium/4.Numerik/SVD_Presentation/assets/duck_svd.json"
    
    # Load and crop
    if not os.path.exists(input_abs_path):
        print(f"Error: {input_abs_path} not found.")
        return

    img = Image.open(input_abs_path).convert("L")
    
    # Remove white borders: find bounding box of non-white pixels
    np_img = np.array(img)
    mask = np_img < 250 
    if np.any(mask):
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        img = img.crop((cmin, rmin, cmax, rmax))
    
    # Resize to 10x10
    img = img.resize(size, Image.Resampling.LANCZOS)
    X = np.array(img, dtype=float)
    
    # Compute SVD
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    
    data = {
        "U": U.tolist(),
        "S": S.tolist(),
        "Vt": Vt.tolist(),
        "n": size[0],
        "m": size[1],
        "original": X.tolist()
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)
    
    with open(output_abs_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully generated duck SVD assets at: {output_abs_path}")

if __name__ == "__main__":
    process_image("unused", "unused")
