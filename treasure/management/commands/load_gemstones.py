
import csv
import os
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

import dotenv

from treasure.models import Gemstone, GemstoneClarity
from treasure.services import get_or_create_icon
from . import utils


dotenv.load_dotenv()


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
                user, _ = utils.get_or_create_user(row['created_by'], os.getenv('DEFAULT_PASSWORD'))
                icon_file_path = Path.home() / 'Pictures' / row['icon']

                icon = None
                if os.path.exists(icon_file_path):

                    with open(icon_file_path, 'rb') as f:
                        django_file = File(file=f, name=icon_file_path.name)
                        icon = get_or_create_icon(django_file, row['name'])

                else:
                    print(f"Failed to locate file path {icon_file_path}")

                gemstone, was_created = utils.create_or_update_gemstone(row, clarity, user, icon)

                self.stdout.write(self.style.SUCCESS(f"{'Created' if was_created else 'Modified'}: {gemstone}"))

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
