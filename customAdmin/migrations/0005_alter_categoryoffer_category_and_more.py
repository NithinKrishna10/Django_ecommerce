# Generated by Django 4.1.3 on 2023-01-03 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customAdmin', '0004_alter_categoryoffer_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='product',
            field=models.CharField(max_length=100),
        ),
    ]
