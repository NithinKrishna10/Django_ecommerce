# Generated by Django 4.1.3 on 2023-01-03 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_return_request_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='signup_day',
            field=models.CharField(default=3, max_length=50),
        ),
    ]
