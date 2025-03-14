# Generated by Django 4.2.4 on 2023-09-16 00:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GemstoneClarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Gemstone clarities',
            },
        ),
        migrations.CreateModel(
            name='GemstoneIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(height_field='height', max_length=128, upload_to='gemstone-icons', width_field='width')),
                ('file_hash', models.CharField(blank=True, max_length=32, unique=True)),
                ('height', models.PositiveIntegerField(blank=True)),
                ('width', models.PositiveIntegerField(blank=True)),
                ('origin', models.CharField(blank=True, default='user', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='icons', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gemstone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)])),
                ('color', models.CharField(blank=True, db_index=True, max_length=128, verbose_name='Color(s)')),
                ('description', models.TextField(max_length=1024)),
                ('dmg_row_value', models.IntegerField(blank=True, null=True)),
                ('dmg_item_number', models.IntegerField(blank=True, null=True)),
                ('unique_name', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('origin', models.CharField(blank=True, default='user', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clarity', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='gemstones', to='treasure.gemstoneclarity')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gemstones', to=settings.AUTH_USER_MODEL)),
                ('icon', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='gemstones', to='treasure.gemstoneicon')),
            ],
        ),
    ]
