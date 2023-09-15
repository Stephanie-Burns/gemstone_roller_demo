
import csv
from pathlib import Path
from typing import Tuple

from django.core.files import File
from django.contrib.auth.models import User

from treasure import models
from treasure import services


def get_or_create_user(username: str, password: str) -> Tuple[User, bool]:

    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password(password)
        user.save()

    return user, created


def create_or_update_gemstone(row: dict, clarity: models.GemstoneClarity, user: User, icon: models.GemstoneIcon):

    gemstone, was_created = models.Gemstone.objects.update_or_create(
        unique_name=row['unique_name'],
        defaults={
            'name'          : row['name'],
            'value'         : row['value'],
            'clarity'       : clarity,
            'color'         : row['color'],
            'description'   : row['description'],
            'icon'          : icon,
            'dmg_row_value' : int(row.get('dmg_row_value'), 0),
            'created_by'    : user,
        }
    )
    return gemstone, was_created


def get_or_create_icon_local(icon_file_path: Path, name: str, user: User):

    if icon_file_path.exists():

        with open(icon_file_path, 'rb') as f:

            django_file = File(file=f, name=icon_file_path.name)
            icon = services.get_or_create_icon(django_file, name, user)

            return icon

    else:

        print(f"Failed to locate file path {icon_file_path}")
