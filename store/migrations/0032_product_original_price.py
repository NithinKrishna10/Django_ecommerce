# Generated by Django 4.1.3 on 2023-01-06 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_remove_brand_brand_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='original_price',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
