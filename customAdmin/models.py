from django.db import models
from store.models import *
# Create your models here.


class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()    
    
    
    
class Productoffer(models.Model):
    product=models.CharField(max_length=100)
    discount=models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    
    
class Categoryoffer(models.Model):
    category=models.CharField(max_length=100)
    discount=models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)