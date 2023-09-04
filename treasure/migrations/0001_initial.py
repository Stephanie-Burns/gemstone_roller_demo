# Generated by Django 4.2.4 on 2023-09-03 23:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GemstoneIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(height_field='height', max_length=128, upload_to='gemstone-icons', width_field='width')),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('file_hash', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gemstone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('descripton', models.CharField(max_length=512)),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)])),
                ('icon', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='gemstones', to='treasure.gemstoneicon')),
            ],
        ),
    ]
