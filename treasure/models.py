
import uuid

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from django.utils.text import slugify

from . import services


GEMSTONE_DEFAULT_ORDER = 'value'
GEMSTONE_ALLOWED_SEARCH_FIELDS = [
    'name',
    'value',
    'color',
    'clarity',
]


class GemstoneClarity(models.Model):

    class Meta:
        verbose_name_plural = 'Gemstone clarities'

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class GemstoneIcon(models.Model):

    # Front End Fields
    name             = models.CharField(max_length=128)
    image            = models.ImageField(
        upload_to='gemstone-icons',
        max_length=128,
        height_field='height',
        width_field='width'
    )

    # Back End Fields
    file_hash        = models.CharField(max_length=32, unique=True, blank=True)
    height           = models.PositiveIntegerField(blank=True)
    width            = models.PositiveIntegerField(blank=True)

    origin = models.CharField(max_length=32, default='user', blank=True)
    created_by       = models.ForeignKey(
        User,
        related_name='icons',
        on_delete=models.CASCADE
    )
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        self.height, self.width = services.shrink_image(self.image.path)

    def generate_name(self, gemstone_name, file_hash):
        self.name = slugify(f'gemstone-icon-{file_hash}-{gemstone_name}')


class GemstoneManager(models.Manager):

    def base_queryset(self, *, user: User = None):

        base_origins = ['dnd_fifth_edition']

        if user:
            query = self.filter(Q(origin__in=base_origins) | Q(created_by=user))

        else:
            query = self.filter(origin__in=base_origins)

        return query.order_by(GEMSTONE_DEFAULT_ORDER)

    def search_for(self, *, search_term: str, user: User = None):

        gem_pool = self.base_queryset(user=user)

        if not search_term:
            return gem_pool

        if search_term.isnumeric():
            return gem_pool.filter(value=int(search_term))

        return gem_pool.filter(
            Q(name__icontains=search_term)          |
            Q(clarity__name__icontains=search_term) |
            Q(color__icontains=search_term)
        )


class Gemstone(models.Model):

    # Front End Fields
    name             = models.CharField(max_length=128, db_index=True)
    value            = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1_000_000)])
    clarity          = models.ForeignKey(
        GemstoneClarity,
        related_name='gemstones',
        on_delete=models.SET_DEFAULT,
        default=1,
        db_index=True
    )
    color            = models.CharField(max_length=128, blank=True, verbose_name='Color(s)', db_index=True)
    description      = models.TextField(max_length=1024)
    icon             = models.ForeignKey(
        GemstoneIcon,
        related_name='gemstones',
        on_delete=models.SET_DEFAULT,
        default=1
    )

    # Back End Fields
    dmg_row_value   = models.IntegerField(null=True, blank=True)
    dmg_item_number = models.IntegerField(null=True, blank=True)
    unique_name     = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    origin          = models.CharField(max_length=32, default='user', blank=True)
    created_by      = models.ForeignKey(
        User,
        related_name='gemstones',
        on_delete=models.CASCADE,
        db_index=True
    )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    # Object Manager
    objects = GemstoneManager()

    def __str__(self):

        # System Objects
        if self.created_by == User.objects.get(username='System'):

            x_value = ('-' + str(self.value)).rjust(6, 'X')
            return f'#{self.id:02} [{self.dmg_row_value:02}:{x_value}] {self.name}'

        # User Objects
        else:
            return f'{self.name}_{self.unique_name}'

    @transaction.atomic
    def delete(self, *args, **kwargs):
        icon = self.icon
        super().delete(*args, **kwargs)

        if not Gemstone.objects.filter(icon=icon).exists():
            if default_storage.exists(icon.image.path):
                default_storage.delete(icon.image.path)
            icon.delete()
