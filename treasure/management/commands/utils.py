
from typing import Tuple

from django.contrib.auth.models import User

from treasure import models


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
            'dmg_row_value' : row.get('dmg_row_value', None),
            'created_by'    : user,
        }
    )
    return gemstone, was_created
