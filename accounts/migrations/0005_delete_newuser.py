# Generated by Django 4.1.3 on 2022-12-06 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_newuser_delete_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewUser',
        ),
    ]
