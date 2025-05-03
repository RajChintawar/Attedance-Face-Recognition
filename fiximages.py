import os
from PIL import Image

# Your input and output folder
input_folder = r"D:\Attendence_System-main\images"
output_folder = r"D:\Attendence_System-main\images_fixed"

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Supported extensions
valid_exts = ['.jpg', '.jpeg', '.png']

for filename in os.listdir(input_folder):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in valid_exts:
        continue

    try:
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')

        output_path = os.path.join(output_folder, f"{name}.jpg")
        img.save(output_path, format='JPEG', quality=95)
        print(f"[OK] Converted {filename} -> {output_path}")

    except Exception as e:
        print(f"[ERROR] Failed to process {filename}: {e}")

print("\n✅ All images processed and saved in 'images_fixed' folder.")
