
import hashlib
from functools import wraps
from PIL import Image
from typing import Optional

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse

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


def get_or_create_icon(upload_icon: InMemoryUploadedFile, gemstone_name: str, user: User):

    if upload_icon:

        file_hash = calculate_file_hash(upload_icon)
        existing_icon = models.GemstoneIcon.objects.filter(file_hash=file_hash).first()

        if existing_icon:

            return existing_icon

        else:

            new_icon = models.GemstoneIcon.objects.create(image=upload_icon, file_hash=file_hash, created_by=user)
            new_icon.generate_name(gemstone_name, file_hash)
            new_icon.save()

            return new_icon

    else:

        return models.GemstoneIcon.objects.get(id=1)


def validate_search_filter(request: HttpRequest) -> str:

    search_filters = ['user', 'system']
    search_filter = request.GET.get('filter', '')
    return '' if search_filter not in search_filters else search_filter


def get_user(request: HttpRequest) -> Optional[User]:

    if request.user and request.user.is_authenticated:

        return request.user


def htmx_redirect(request, view_name, *args, **kwargs):

    response = HttpResponse()
    url = reverse(view_name, args=args, kwargs=kwargs)
    response["HX-Redirect"] = request.build_absolute_uri(url)

    return response


def user_owns_gemstone(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        gemstone_id = kwargs.get('gemstone_id')
        gemstone = get_object_or_404(models.Gemstone, pk=gemstone_id)

        if gemstone.created_by != request.user:
            return HttpResponseForbidden("You do not have permission to modify this gemstone.")

        request.gemstone = gemstone
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def is_modal_view(request: HttpRequest) -> bool:

    if request.GET.get('modal', '') == 'true':
        return True
