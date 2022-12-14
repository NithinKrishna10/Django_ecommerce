# Generated by Django 4.1.3 on 2022-12-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_orderproducts_order_day_orderproducts_order_month_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproducts',
            name='Order_day',
        ),
        migrations.RemoveField(
            model_name='orderproducts',
            name='Order_month',
        ),
        migrations.RemoveField(
            model_name='orderproducts',
            name='Order_year',
        ),
        migrations.AddField(
            model_name='orders',
            name='Order_day',
            field=models.IntegerField(default=26),
        ),
        migrations.AddField(
            model_name='orders',
            name='Order_month',
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name='orders',
            name='Order_year',
            field=models.IntegerField(default=2022),
        ),
    ]
