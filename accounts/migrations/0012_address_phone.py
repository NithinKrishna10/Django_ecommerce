# Generated by Django 4.1.3 on 2022-12-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_zipcode_address_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(default=0, max_length=15),
        ),
    ]
