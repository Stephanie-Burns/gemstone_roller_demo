
import hashlib
from PIL import Image

def calculate_file_hash(file):
    hasher = hashlib.md5()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

def shrink_image(img_path):
    img = Image.open(img_path)
    max_dimension = 512
    print("starting shrink")

    if img.height > max_dimension or img.width > max_dimension:
        print("condition hit")
        aspect_ratio = img.width / img.height

        if img.height >= img.width:
            new_height = max_dimension
            new_width = int(aspect_ratio * new_height)
        else:
            new_width = max_dimension
            new_height = int(new_width / aspect_ratio)

        output_size = (new_width, new_height)

        img.thumbnail(output_size, Image.LANCZOS)
        img.save(img_path)

    return img.height, img.width