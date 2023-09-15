
import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

import dotenv

from treasure import models
from . import utils


dotenv.load_dotenv()

# To run this script type
# python manage.py load_gemstones ~/PycharmProjects/image_upload_demo/treasure/fixtures/gemstones.csv

LOCAL_PATH = Path.home() / 'Pictures'
DEFAULT_ICON_PATH = LOCAL_PATH / 'gemstone.png'


class Command(BaseCommand):
    help = "Load gemstones from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    @transaction.atomic
    def handle(self, *args, **options):

        # Default User
        user, _ = utils.get_or_create_user(os.getenv('DEFAULT_USER'), os.getenv('DEFAULT_PASSWORD'))

        # Default Gemstone Icon
        _ = utils.get_or_create_icon_local(DEFAULT_ICON_PATH, 'default', user)

        # Gemstone CSV Data
        csv_file_path = options['csv_file']

        with open(csv_file_path, mode='r') as file:

            reader = csv.DictReader(file)

            for row in reader:

                clarity, _              = models.GemstoneClarity.objects.get_or_create(name=(row['clarity']).capitalize())
                icon                    = utils.get_or_create_icon_local(LOCAL_PATH / row['icon'], row['name'], user)
                gemstone, was_created   = utils.create_or_update_gemstone(row, clarity, user, icon)

                self.stdout.write(self.style.SUCCESS(f"{'Created' if was_created else 'Modified'}: {gemstone}"))

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
