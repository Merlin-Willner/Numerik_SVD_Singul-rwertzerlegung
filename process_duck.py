import numpy as np
from PIL import Image
import json
import os

def process_image(input_path, output_json, size=(10, 10)):
    # Load and crop (basic center crop logic to remove white borders)
    img = Image.open(input_path).convert("L")
    
    # Remove white borders: find bounding box of non-white pixels
    # Invert for bbox (letter/object is dark, background is 255)
    np_img = np.array(img)
    mask = np_img < 250 # Everything that isn't white
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
    
    with open(output_json, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Processed Duck Matrix saved to {output_json}")

if __name__ == "__main__":
    process_image("visual_audit/RubberDuck.png", "assets/duck_svd.json")
