
import csv
import tempfile
from pathlib import Path
from os.path import exists

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from django.db import transaction
from django.utils._os import safe_join

from treasure.models import Gemstone, GemstoneClarity, GemstoneIcon
from treasure.services import get_or_create_icon


class Command(BaseCommand):
    help = "Load gemstones from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                clarity, _ = GemstoneClarity.objects.get_or_create(name=row['clarity'])

                icon_file_path = Path.home() / 'Pictures' / row['icon']

                if exists(icon_file_path):

                    with open(icon_file_path, 'rb') as f:
                        django_file = File(file=f, name=icon_file_path.name)
                        icon = get_or_create_icon(django_file, row['name'])

                Gemstone.objects.create(
                    name=row['name'],
                    value=row['value'],
                    clarity=clarity,
                    color=row['color'],
                    description=row['description'],
                    icon=icon
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))