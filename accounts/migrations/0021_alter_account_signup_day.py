# Generated by Django 4.1.3 on 2023-01-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_account_phone_number_alter_account_signup_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='signup_day',
            field=models.CharField(default=6, max_length=50),
        ),
    ]
