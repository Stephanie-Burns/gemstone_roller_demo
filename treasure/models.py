
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db import models

from PIL import Image

from . import services

class GemstoneIcon(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='gemstone-icons', max_length=128, height_field='height', width_field='width')
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    file_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    def generate_name(self, gemstone_name, file_hash):
        self.name = slugify(f'gemstone-icon_{gemstone_name}_{file_hash}')

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        self.height, self.width = services.shrink_image(self.image.path)


class Gemstone(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ForeignKey(GemstoneIcon, related_name='gemstones', on_delete=models.SET_DEFAULT, default=1)
    description = models.CharField(max_length=512)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1_000_000)])

