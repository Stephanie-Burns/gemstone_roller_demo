
import hashlib
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

from . import models


def calculate_file_hash(file):

    hasher = hashlib.md5()
    for chunk in file.chunks():

        hasher.update(chunk)

    return hasher.hexdigest()


def shrink_image(img_path):

    img = Image.open(img_path)
    max_dimension = 512

    if img.height > max_dimension or img.width > max_dimension:

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


def get_or_create_icon(upload_icon: InMemoryUploadedFile, gemstone_name: str):

    if upload_icon:

        file_hash = calculate_file_hash(upload_icon)
        existing_icon = models.GemstoneIcon.objects.filter(file_hash=file_hash).first()

        if existing_icon:

            return existing_icon

        else:

            new_icon = models.GemstoneIcon.objects.create(image=upload_icon, file_hash=file_hash)
            new_icon.generate_name(gemstone_name, file_hash)
            new_icon.save()

            return new_icon

    else:

        return models.GemstoneIcon.objects.get(id=1)


def get_gemstone_sort_order_from_session(request):

    sort_by = request.GET.get('sort_by', None)

    if not sort_by or sort_by not in models.GEMSTONE_ALLOWED_SEARCH_FIELDS:
        sort_by = models.GEMSTONE_DEFAULT_ORDER

    last_order = request.session.get(f'{sort_by}_order', 'asc')
    new_order = 'desc' if last_order == 'asc' else 'asc'
    request.session[f'{sort_by}_order'] = new_order

    return sort_by, new_order
