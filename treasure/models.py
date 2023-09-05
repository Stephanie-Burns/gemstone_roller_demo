
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db import models, transaction

from . import services


class GemstoneClarity(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Gemsonte clarities'


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
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1_000_000)])
    clarity = models.ForeignKey(GemstoneClarity, related_name='gemstones', on_delete=models.SET_DEFAULT, default=1)
    color = models.CharField(max_length=128, blank=True, verbose_name='Color(s)')
    description = models.TextField(max_length=1024)
    icon = models.ForeignKey(GemstoneIcon, related_name='gemstones', on_delete=models.SET_DEFAULT, default=1)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        icon = self.icon
        super().delete(*args, **kwargs)

        if not Gemstone.objects.filter(icon=icon).exists():
            if default_storage.exists(icon.image.path):
                default_storage.delete(icon.image.path)
            icon.delete()
