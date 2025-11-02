import os
from PIL import Image
import numpy as np

output_dir = "files"
os.makedirs(output_dir, exist_ok=True)

sizes_text = [1024, 500_000, 2_441_000, 500_000_000]  # Añade 500MB
sizes_bin = sizes_text.copy()
resolutions_img = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}

for size in sizes_text:
    name = f"PlainText_{size//1024}KB.txt" if size < 1_000_000 else "PlainText_500MB.txt"
    with open(os.path.join(output_dir, name), "wb") as f:
        f.write(b"A" * size)

for size in sizes_bin:
    name = f"Binary_{size//1024}KB.dll" if size < 1_000_000 else "Binary_500MB.dll"
    with open(os.path.join(output_dir, name), "wb") as f:
        f.write(os.urandom(size))

for label, (w, h) in resolutions_img.items():
    array = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
    image = Image.fromarray(array)
    image.save(os.path.join(output_dir, f"Image_{label}.jpg"), format="JPEG", quality=85)

w, h = 10000, 16666  # ~500MB RGB
big_array = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
big_image = Image.fromarray(big_array)
big_image.save(os.path.join(output_dir, "Image_500MB.jpg"), format="JPEG", quality=95)

print("✅ Archivos generados incluyendo archivo de 500MB.")
